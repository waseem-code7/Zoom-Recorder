console.log("i am starting")
chrome.runtime.onMessage.addListener(async (message) => {
    console.log("Testing 123....")
    console.log(message)
});