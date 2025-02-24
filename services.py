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
            f"--load-extension={path_to_extensions}",
            "--auto-open-devtools-for-tabs",
        ]
}


async def check_participants(page):
    while True:
        num_participants = await page.evaluate(
            'document.querySelector("#participant > button > div > span > span").innerText')
        print(num_participants)

        if num_participants != '1':
            print("Participant count changed, exiting loop.")
            return  # Stop checking when the condition is met

        await asyncio.sleep(5) # Wait 5 seconds before checking again

async def end_meeting(page):
    while True:
        num_participants = await page.evaluate(
            'document.querySelector("#participant > button > div > span > span").innerText')
        print(num_participants)

        if num_participants == '1':
            print("All participants left the meeting, hence leaving zoom")
            page.click("#foot-bar > div.footer__leave-btn-container > button > div")
            return

        await asyncio.sleep(5) # Wait 5 seconds before checking again

async def main():
    try:
        browser = await launch(options)

        page = await browser.newPage()
        await page.setBypassCSP(True)
        #https://us05web.zoom.us/j/83446887496?pwd=GM5fFiMVGoidp34FSygKBJFt0pmwvM.1
        await page.goto('https://app.zoom.us/wc/83446887496/join', {"waitUntil": "networkidle2"})

        await page.waitForSelector(selector="#input-for-pwd")

        await page.click(selector="#input-for-pwd")
        await page.keyboard.type("GM5fFiMVGoidp34FSygKBJFt0pmwvM.1", options={"delay":10})

        await page.click(selector="#input-for-name")
        await page.keyboard.type("Recorder", options={"delay": 10})

        await page.click("#root > div > div.preview-new-flow > div > div.preview-meeting-info > button")

        #wait until joined
        await page.waitForSelector("#participant > button", options={"timeout": 60000})

        await page.evaluate('window.postMessage({ action: "RECORDING_START" }, "*");')

        await check_participants(page)

        await end_meeting(page)

        await page.evaluate('window.postMessage({ action: "RECORDING_END" }, "*");')

        await asyncio.sleep(10)

        # await browser.close()
    except Exception as e:
        print(e)

asyncio.get_event_loop().run_until_complete(main())
