from pyppeteer import launch
import asyncio

path_to_extensions = "./extensions"

options = {
    "headless": False,
    "args": [
            "--use-fake-ui-for-media-stream",  # Automatically allow mic/camera
            "--use-fake-device-for-media-stream",  # Simulate a media device
            "--enable-blink-features=WebRTC-H264WithOpenH264FFmpeg",  # Ensures WebRTC works
            f"-disable-extensions-except={path_to_extensions}",
            f"--load-extension={path_to_extensions}"
        ]
}

async def main():
    try:
        browser = await launch(options)
        page = await browser.newPage()
        await page.setBypassCSP(True)

        await page.goto('https://app.zoom.us/wc/88371882594/join', {"waitUntil": "networkidle2"})

        await page.evaluate('window.postMessage(JSON.stringify({ action: "REC_TEST", value: "Some value" }), "*");')

        await page.waitForSelector(selector="#input-for-pwd")

        await page.click(selector="#input-for-pwd")
        await page.keyboard.type("MAqJnaGlGPaD2j3fcDje6FbICVmGLZ.1", options={"delay":10})

        await page.click(selector="#input-for-name")
        await page.keyboard.type("Recorder", options={"delay": 10})

        await page.click("#root > div > div.preview-new-flow > div > div.preview-meeting-info > button")

        await asyncio.sleep(10)

        # await browser.close()
    except Exception as e:
        print(e)

asyncio.get_event_loop().run_until_complete(main())
