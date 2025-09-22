import asyncio
from typing import Dict, Any
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


async def extract_svelte_code(url: str) -> str:
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
            await page.goto(url, wait_until="networkidle")

            # 打开选择框并选择 Svelte
            trigger = page.get_by_role("button", name="React")
            await trigger.wait_for(state="visible")
            await trigger.click()
            svelte_item = page.get_by_role("menuitem", name="Svelte")
            await svelte_item.wait_for(state="visible")
            await svelte_item.click()

            # 等待 Svelte 窗口并点击 Copy
            dialog = page.get_by_role("dialog")
            await dialog.wait_for(state="visible")
            copy_btn = dialog.locator("button.copy-all").first
            await copy_btn.wait_for(state="visible")
            await copy_btn.click()
            await copy_btn.locator(".copy-all__text").filter(has_text="✔").first.wait_for(
                timeout=COPIED_TIMEOUT_MS
            )

            svelte_code = await _read_clipboard_nonempty(page)
            if not svelte_code:
                ta = dialog.locator("textarea[name=code], textarea#codeArea2").first
                if await ta.count() > 0:
                    try:
                        svelte_code = await ta.input_value()
                    except Exception:
                        try:
                            svelte_code = await ta.evaluate("el => el.value")
                        except Exception:
                            svelte_code = ""

            return f"### Svelte ```svelte { _one_line(svelte_code) } ```"

        finally:
            await context.close()
            await browser.close()


if __name__ == "__main__":
    pass
