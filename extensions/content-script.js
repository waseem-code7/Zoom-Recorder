// content-script.js

const relayMessageToBackground = function(data) {
    chrome.runtime.sendMessage({ action: data }, (response) => {
        console.log("Message sent to background:", response);
    });
}

window.addEventListener('message', function(event) {
    console.log("received...")
    console.log(event.data)
    // Only forward messages coming from the page (filtering based on the event origin)
    if (event.source === window && event.data) {
        relayMessageToBackground(event.data)
    }
}, false);
