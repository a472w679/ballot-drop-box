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
