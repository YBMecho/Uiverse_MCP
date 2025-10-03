import asyncio
from typing import List
from playwright.async_api import async_playwright


def _one_line(text: str) -> str:
    if text is None:
        return ""
    return text.replace("\r", " ").replace("\n", " ")

DEFAULT_TIMEOUT_MS = 20000
COPIED_TIMEOUT_MS = 15000


async def _block_unneeded_requests(route, request):
    if request.resource_type in {"image", "media", "font"}:
        await route.abort()
    else:
        await route.continue_()


async def _read_clipboard_nonempty(page) -> str:
    for _ in range(10):
        try:
            txt = await page.evaluate("navigator.clipboard.readText()")
            if txt and txt.strip():
                return txt
        except Exception:
            pass
        await page.wait_for_timeout(200)
    return ""


async def _first_text_by_selectors(scope, selectors: List[str]) -> str:
    for selector in selectors:
        loc = scope.locator(selector)
        try:
            if await loc.count() > 0:
                # 优先使用 inner_text 以获得可见文本
                return await loc.first.inner_text()
        except Exception:
            pass
    return ""


async def extract_react_code(url: str) -> str:
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            permissions=["clipboard-read", "clipboard-write"],
            user_agent=(
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/120.0.0.0 Safari/537.36"
            ),
            viewport={"width": 1280, "height": 900},
        )
        await context.route("**/*", _block_unneeded_requests)
        page = await context.new_page()
        page.set_default_timeout(DEFAULT_TIMEOUT_MS)

        try:
            # 打开组件页面
            await page.goto(url, wait_until="networkidle")

            # 1) 点击选择框按钮（React）
            react_trigger = page.get_by_role("button", name="React")
            await react_trigger.wait_for(state="visible")
            await react_trigger.click()

            # 2) 在弹出的菜单中选择 React
            react_menuitem = page.get_by_role("menuitem", name="React")
            await react_menuitem.wait_for(state="visible")
            await react_menuitem.click()

            # 3) 等待 React 窗口出现
            dialog = page.get_by_role("dialog")
            await dialog.wait_for(state="visible")

            # 4) 提取窗口中的说明内容（如果没有则为空）
            extracted_content = await _first_text_by_selectors(
                dialog,
                [
                    "div.text-offwhite",
                    "[data-testid=modal] .text-offwhite",
                    "div:has(a[href*='styled-components'])",
                ],
            )

            # 5) 点击窗口右上角的 Copy 按钮并等待 ✔
            copy_btn = dialog.locator("button.copy-all").first
            await copy_btn.wait_for(state="visible")
            await copy_btn.click()
            await copy_btn.locator(".copy-all__text").filter(has_text="✔").first.wait_for(
                timeout=COPIED_TIMEOUT_MS
            )

            # 6) 从剪贴板读取 React 代码；失败则尝试从文本域读取
            react_code = await _read_clipboard_nonempty(page)
            if not react_code:
                # 备用：尝试读取对话框中的代码文本域
                ta = dialog.locator("textarea[name=code], textarea#codeArea2").first
                if await ta.count() > 0:
                    try:
                        react_code = await ta.input_value()
                    except Exception:
                        try:
                            react_code = await ta.evaluate("el => el.value")
                        except Exception:
                            react_code = ""

            # 7) 返回单行 Markdown（先内容，后 React 代码）
            content_md = f"### 内容 { _one_line(extracted_content or '') }"
            react_md = f" ### React ```tsx { _one_line(react_code) } ```"
            return content_md + react_md

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    pass
