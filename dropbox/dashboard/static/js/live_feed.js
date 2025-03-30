// Name of code artifact: live_feed.js
// Brief description of what the code does: Connects usb camera to front end
// Programmer’s name: Xavier Ruyle
// Date the code was created: 2/20/25
// Preconditions: Camera available
// Postconditions: Camera data shown in video tag
// Return values or types, and their meanings: N/A
// Error and exception condition values or types that can occur, and their meanings: N/A
// Side effects:
// Invariants: N/A

document.addEventListener("DOMContentLoaded", function () {
  async function startStream() {
    const videoElement = document.getElementById("video");
    const dropbox_id = parseInt(videoElement.dataset.dropboxId, 10);

    const protocol = window.location.protocol === "https:" ? "wss:" : "ws:";
    const wsUrl = `${protocol}//${window.location.host}/ws/video/${dropbox_id}`;

    const videoSocket = new WebSocket(wsUrl);

    videoSocket.onmessage = function (e) {
      const data = JSON.parse(e.data);

      if (dropbox_id === data.sender_id) {
        videoElement.src = "data:image/jpg;base64," + data.frame;
      }
    };
  }

  startStream();
});
