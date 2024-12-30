from playwright.async_api import async_playwright
import json
import os

with open("/data/YianBot/data/缺氧数据库.json", "r", encoding="utf-8") as f:
    data = json.load(f)


async def get_oxygen_card(name: str) -> str:
    if name not in data:
        return None
    path = f"data/oxygen_card/{name}.png"
    if os.path.exists(path):
        return path
    url = data[name]
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # 打开网页
        await page.goto("https://oni-cn.com" + url)

        # 等待字段元素加载完毕，确保页面已经渲染
        await page.wait_for_selector("div.layui-col-md4")

        # 隐藏 layui-footer 和 layui-header oni-header 元素
        await page.evaluate(
            """
            const footer = document.querySelector('.layui-footer');
            const header = document.querySelector('.layui-header.oni-header');
            if (footer) {
                footer.style.display = 'none';
            }
            if (header) {
                header.style.display = 'none';
            }
        """
        )

        # 获取容器元素的定位器
        element = page.locator("div.layui-col-md4")

        # 截图目标元素
        screenshot_path = "container_screenshot.png"
        await element.screenshot(path=screenshot_path)

        # 关闭浏览器
        await browser.close()

        return path
