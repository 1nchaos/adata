import asyncio
from pyppeteer import launch


async def main():
    browser = await launch()
    page = await browser.newPage()

    await page.goto('https://gushitong.baidu.com/stock/ab-002926')
    content = await page.content()

    print(content)

    await browser.close()


asyncio.get_event_loop().run_until_complete(main())