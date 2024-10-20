document.addEventListener('DOMContentLoaded', () => {
    const video = document.getElementById('video');
    const startBtn = document.getElementById('startBtn');
    const stopBtn = document.getElementById('stopBtn');
    const message1 = document.getElementById('message');

    startBtn.addEventListener('click', () => {
        video.src = "/mask_detection/video_feed/";  // Set the img source to the video feed
        video.classList.remove('hidden');  // Show the img element
        message1.innerText = 'Video is going to start in 15 seconds...';
        setTimeout(() => {
            message1.innerText = ''
        }, 2000);
    });

    stopBtn.addEventListener('click', () => {
        video.src = "";  // Clear the source to stop the stream
        video.classList.add('hidden');  // Hide the img element
        message1.innerText = 'Video has been stopped';
        setTimeout(() => {
            message1.innerText = ''
        }, 2000);
    });
});
