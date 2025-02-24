// content-script.js
const port = chrome.runtime.connect({ name: "content-script" });


const relayMessageToBackground = function(data) {
    port.postMessage(data);
}

port.onMessage.addListener(msg => {
    console.log("Message from background script:", msg);
});

window.addEventListener('message', function(event) {
    console.log("received...")
    console.log(event.data)
    // Only forward messages coming from the page (filtering based on the event origin)
    if (event.source === window && event.data.action) {
        relayMessageToBackground(event.data)
    }
}, false);
