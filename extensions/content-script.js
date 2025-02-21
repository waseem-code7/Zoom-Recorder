// content-script.js
window.addEventListener('message', function(event) {
    console.log("received...")
    console.log(event.data)
    // Only forward messages coming from the page (filtering based on the event origin)
    if (event.source === window && event.data) {
        // Send the message to the background script
        chrome.runtime.sendMessage({ action: event.data }, (response) => {
            console.log("Message sent to background:", response);
        });
    }
}, false);
