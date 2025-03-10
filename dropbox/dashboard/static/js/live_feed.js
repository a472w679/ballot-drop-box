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
  async function startWebcam() {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: { width: 1280, height: 720 }, // Request 720p resolution
      });
      document.getElementById("livefeed").srcObject = stream;
    } catch (error) {
      console.error("Error accessing webcam:", error);
    }
  }
  startWebcam();
});
