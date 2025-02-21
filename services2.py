import asyncio
from pyppeteer import launch

async def main():
    browser = await launch(headless=True)
    page = await browser.newPage()

    # Create a DevTools session
    client = await page.target.createCDPSession()

    # Enable network tracking
    await client.send('Network.enable')

    # Intercept requests (example: log request URLs)
    client.on('Network.requestWillBeSent', lambda req: print(req['request']['url']))

    await page.goto('https://www.google.com')
    await browser.close()

asyncio.run(main())