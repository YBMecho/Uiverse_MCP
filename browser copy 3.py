import asyncio
from playwright.async_api import async_playwright

async def load_website():
    async with async_playwright() as p:
        # 启动无头浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()
        
        # 访问目标网页
        await page.goto('https://uiverse.io/')
        
        # 等待页面加载完成
        await page.wait_for_selector('body')
        
        # 获取页面标题
        title = await page.title()
        print(f"网页标题: {title}")
        
        # 获取页面内容
        content = await page.content()
        print(f"网页内容长度: {len(content)} 字符")
        print("动态网页加载完成！")
        
        # 关闭浏览器
        await browser.close()

if __name__ == "__main__":
    print("开始加载动态网页...")
    asyncio.run(load_website())
