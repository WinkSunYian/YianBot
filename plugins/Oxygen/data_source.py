from playwright.async_api import async_playwright


async def get_oxygen_card(name: str, url: str) -> str:
    async with async_playwright() as p:
        # 启动浏览器
        browser = await p.chromium.launch(
            headless=True
        )  # Playwright 会自动下载 Chromium
        page = await browser.new_page()

        # 打开网页
        await page.goto(f"https://oni-cn.com{url}")

        # 等待字段元素加载完毕，确保页面已经渲染
        await page.wait_for_selector("fieldset.layui-elem-field")

        # 获取整个 fieldset 元素，包括所有的子元素（表格、图片等）
        fieldset = page.locator("fieldset.layui-elem-field").nth(-1)

        path = f"data/oxygen_card/{name}.png"
        # 截取该 fieldset 元素的截图并保存
        await fieldset.screenshot(path=path)
        # 关闭浏览器
        await browser.close()

    return path
