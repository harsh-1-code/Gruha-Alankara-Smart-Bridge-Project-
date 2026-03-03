// Live AR Camera JavaScript

let stream = null;
let facingMode = 'environment';

document.addEventListener('DOMContentLoaded', () => {
    initLiveAR();
});

function initLiveAR() {
    document.getElementById('start-camera')?.addEventListener('click', startCamera);
    document.getElementById('flip-camera')?.addEventListener('click', flipCamera);
    document.getElementById('capture-photo')?.addEventListener('click', capturePhoto);
    document.getElementById('stop-camera')?.addEventListener('click', stopCamera);
}

async function startCamera() {
    try {
        stream = await navigator.mediaDevices.getUserMedia({
            video: { facingMode, width: { ideal: 1280 }, height: { ideal: 720 } },
            audio: false
        });
        const video = document.getElementById('camera-feed');
        video.srcObject = stream;

        document.getElementById('flip-camera').disabled = false;
        document.getElementById('capture-photo').disabled = false;
        document.getElementById('stop-camera').disabled = false;
        document.getElementById('start-camera').disabled = true;

        setupAROverlay();
    } catch (err) {
        console.error('Camera error:', err);
        alert('Could not access camera. Please allow camera permissions.');
    }
}

function flipCamera() {
    facingMode = facingMode === 'environment' ? 'user' : 'environment';
    stopCamera();
    startCamera();
}

function capturePhoto() {
    const video = document.getElementById('camera-feed');
    const canvas = document.getElementById('ar-overlay');
    const ctx = canvas.getContext('2d');

    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    ctx.drawImage(video, 0, 0);

    const link = document.createElement('a');
    link.download = `gruha-alankara-ar-${Date.now()}.png`;
    link.href = canvas.toDataURL();
    link.click();
}

function stopCamera() {
    if (stream) {
        stream.getTracks().forEach(track => track.stop());
        stream = null;
    }
    const video = document.getElementById('camera-feed');
    video.srcObject = null;

    document.getElementById('flip-camera').disabled = true;
    document.getElementById('capture-photo').disabled = true;
    document.getElementById('stop-camera').disabled = true;
    document.getElementById('start-camera').disabled = false;
}

function setupAROverlay() {
    const video = document.getElementById('camera-feed');
    const canvas = document.getElementById('ar-overlay');
    canvas.width = video.videoWidth || 1280;
    canvas.height = video.videoHeight || 720;
}

function placeFurnitureAR(itemId) {
    console.log('Placing furniture in live AR:', itemId);
}
