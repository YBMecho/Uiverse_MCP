import asyncio
from typing import List
from playwright.async_api import async_playwright


def _one_line(text: str) -> str:
    if text is None:
        return ""
    return text.replace("\r", " ").replace("\n", " ")

DEFAULT_TIMEOUT_MS = 20000
COPIED_TIMEOUT_MS = 15000
RETRIES = 3


async def _block_unneeded_requests(route, request):
    if request.resource_type in {"image", "media", "font"}:
        await route.abort()
    else:
        await route.continue_()


async def _click_and_wait_copied(page, button_selector: str, copied_text_selector: str) -> bool:
    for attempt in range(RETRIES):
        try:
            button = page.locator(button_selector).first
            await button.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
            await button.click()
            await page.locator(copied_text_selector).filter(has_text="Copied").first.wait_for(
                timeout=COPIED_TIMEOUT_MS
            )
            return True
        except Exception:
            await page.wait_for_timeout(500 * (attempt + 1))
    return False


async def _read_clipboard_nonempty(page) -> str:
    for _ in range(6):
        try:
            txt = await page.evaluate("navigator.clipboard.readText()")
            if txt and txt.strip():
                return txt
        except Exception:
            pass
        await page.wait_for_timeout(250)
    return ""


async def _first_text_by_selectors(page, selectors: List[str]) -> str:
    for selector in selectors:
        loc = page.locator(selector)
        try:
            if await loc.count() > 0:
                return await loc.first.inner_text()
        except Exception:
            pass
    return ""


async def _detect_special_content(page) -> bool:
    """检测页面是否包含特殊.html中的内容（HTML + TailwindCSS标签）"""
    try:
        # 检查是否同时包含HTML和TailwindCSS文字
        html_present = await page.locator("text=HTML").count() > 0
        tailwind_present = await page.locator("text=TailwindCSS").count() > 0
        
        # 检查特定的SVG路径（HTML图标的路径）
        html_svg_path = "M12 18.178l4.62-1.256.623-6.778H9.026L8.822 7.89h8.626l.227-2.211H6.325l.636 6.678h7.82l-.261 2.866-2.52.667-2.52-.667-.158-1.844h-2.27l.329 3.544L12 18.178zM3 2h18l-1.623 18L12 22l-7.377-2L3 2z"
        svg_present = await page.locator(f'path[d="{html_svg_path}"]').count() > 0
        
        return html_present and tailwind_present and svg_present
    except Exception:
        return False


async def _click_copy_button_direct(page) -> bool:
    """直接点击copy按钮并等待复制完成"""
    try:
        # 尝试多种可能的copy按钮选择器
        copy_selectors = [
            "button:has-text('copy')",
            "button:has-text('Copy')",
            "[role='button']:has-text('copy')",
            "[role='button']:has-text('Copy')",
            ".copy-btn",
            ".copy-button"
        ]
        
        for selector in copy_selectors:
            try:
                button = page.locator(selector).first
                if await button.count() > 0:
                    await button.wait_for(state="visible", timeout=5000)
                    await button.click()
                    
                    # 等待一小段时间让复制操作完成
                    await page.wait_for_timeout(1000)
                    return True
            except Exception:
                continue
        
        return False
    except Exception:
        return False


async def extract_html_css(url: str) -> str:
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

            # 检查是否为特殊内容（HTML + TailwindCSS）
            is_special_content = await _detect_special_content(page)
            
            if is_special_content:
                # 如果检测到特殊内容，直接点击copy按钮
                copy_ok = await _click_copy_button_direct(page)
                if copy_ok:
                    combined_code = await _read_clipboard_nonempty(page)
                    if combined_code:
                        # 特殊内容通常是HTML和CSS的组合，直接返回
                        return f"### HTML+CSS（特殊内容）\n```html\n{_one_line(combined_code)}\n```"
                
                # 如果直接复制失败，继续使用原来的逻辑
            
            css_ok = await _click_and_wait_copied(
                page,
                "button.copy-all.CSS",
                "button.copy-all.CSS .copy-all__text",
            )
            css_code = await _read_clipboard_nonempty(page) if css_ok else ""

            html_tab = page.get_by_role("tab", name="HTML")
            await html_tab.wait_for(state="visible", timeout=DEFAULT_TIMEOUT_MS)
            await html_tab.click()

            html_ok = await _click_and_wait_copied(
                page,
                "button.copy-all.HTML",
                "button.copy-all.HTML .copy-all__text",
            )
            html_code = await _read_clipboard_nonempty(page) if html_ok else ""

            if not css_code:
                css_code = await _first_text_by_selectors(
                    page,
                    [
                        '[data-language="css"]',
                        "pre:has-text('{')",
                        "code:has-text('{')",
                    ],
                )

            if not html_code:
                html_code = await _first_text_by_selectors(
                    page,
                    [
                        '[data-language="html"]',
                        "pre:has-text('<')",
                        "code:has-text('<')",
                        "textarea",
                    ],
                )

            html_md = f"### HTML ```html { _one_line(html_code) } ```"
            css_md = f" ### CSS ```css { _one_line(css_code) } ```"
            return html_md + css_md

        finally:
            await context.close()
            await browser.close()
