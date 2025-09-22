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
