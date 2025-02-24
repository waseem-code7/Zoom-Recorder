let mediaRecorder;
let recordedChunks = [];

function saveRecording() {
  const blob = new Blob(recordedChunks, { type: "video/webm" });
  const url = URL.createObjectURL(blob);

  const a = document.createElement("a");
  a.href = url;
  a.download = "screen-recording.webm";
  document.body.appendChild(a);
  a.click();

  URL.revokeObjectURL(url);
  console.log("Recording saved");
}


function startCapture() {
  chrome.desktopCapture.chooseDesktopMedia(["screen", "window", "tab"], streamId => {
    if (!streamId) {
      console.log("User canceled screen sharing");
      return;
    }

    navigator.mediaDevices.getUserMedia({
      video: {
        mandatory: {
          chromeMediaSource: "desktop",
          chromeMediaSourceId: streamId
        }
      }
    }).then(stream => {
      mediaRecorder = new MediaRecorder(stream);

      // Store recorded data
      mediaRecorder.ondataavailable = event => {
        if (event.data.size > 0) {
          recordedChunks.push(event.data);
        }
        console.log("Capturing ::: "+ recordedChunks.length)
      };

      mediaRecorder.onstop = () => saveRecording();

      mediaRecorder.start();
      console.log("Recording started");
    }).catch(error => console.error("Error accessing screen:", error));
  });
}

chrome.runtime.onConnect.addListener(port => {
    console.log("Connected to content script:", port);

    // Listen for messages from content script
    port.onMessage.addListener((msg) => {
        console.log("Message from content script:", msg);

        // Example: Send a response back to content script
        if (msg.action === "RECORDING_START") {
            startCapture()
        }
    });
})