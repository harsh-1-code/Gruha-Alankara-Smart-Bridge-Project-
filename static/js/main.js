// ============================================
// Gruha Alankara - Main JavaScript
// ============================================

// --- Global State ---
let cameraStream = null; // Holds the active MediaStream reference

// --- Initialization ---
document.addEventListener('DOMContentLoaded', () => {
    initNavbar();
    initAlerts();
    initCameraControls();
});

// ============================================
// 1. Navigation - Active Link Highlighting
// ============================================
function initNavbar() {
    const currentPath = window.location.pathname;
    const navLinks = document.querySelectorAll('.nav-links a');
    navLinks.forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
}

// ============================================
// 2. Flash/Alert Auto-Dismiss
// ============================================
function initAlerts() {
    const alerts = document.querySelectorAll('.alert, .flash');
    alerts.forEach(alert => {
        setTimeout(() => {
            alert.style.opacity = '0';
            alert.style.transition = 'opacity 0.5s ease';
            setTimeout(() => alert.remove(), 500);
        }, 4000);
    });
}

// ============================================
// 3. Camera Controls Initialization
// ============================================

/**
 * Binds camera button event listeners if the camera elements
 * exist on the current page. This keeps the code safe for pages
 * that don't have camera UI.
 */
function initCameraControls() {
    const startBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-photo');
    const stopBtn = document.getElementById('stop-camera');

    if (startBtn) {
        startBtn.addEventListener('click', startCamera);
    }
    if (captureBtn) {
        captureBtn.addEventListener('click', captureImage);
    }
    if (stopBtn) {
        stopBtn.addEventListener('click', stopCamera);
    }
}

// ============================================
// 4. Start Camera - Request Permission & Stream
// ============================================

/**
 * Requests camera access using the MediaDevices API.
 * Prefers the environment-facing camera at 1280×720.
 * On success, streams video to the <video> element.
 */
async function startCamera() {
    const videoEl = document.getElementById('camera-feed') || document.getElementById('cameraFeed');
    const errorEl = document.getElementById('cameraError');
    const startBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-photo');
    const stopBtn = document.getElementById('stop-camera');
    const flipBtn = document.getElementById('flip-camera');

    // Clear any previous error
    if (errorEl) errorEl.textContent = '';

    // Check browser support
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
        showCameraError('Your browser does not support camera access. Please use a modern browser.');
        return;
    }

    // Camera constraints: 720p, prefer rear camera on mobile
    const constraints = {
        video: {
            width: { ideal: 1280 },
            height: { ideal: 720 },
            facingMode: { ideal: 'environment' }
        },
        audio: false
    };

    try {
        // Request camera permission and get the stream
        const stream = await navigator.mediaDevices.getUserMedia(constraints);
        cameraStream = stream;

        // Attach stream to the video element
        if (videoEl) {
            videoEl.srcObject = stream;
            videoEl.play();
        }

        // Update button states
        if (startBtn) startBtn.disabled = true;
        if (captureBtn) captureBtn.disabled = false;
        if (stopBtn) stopBtn.disabled = false;
        if (flipBtn) flipBtn.disabled = false;

        console.log('Camera started successfully.');
    } catch (error) {
        handleCameraError(error);
    }
}

// ============================================
// 5. Capture Image - Snapshot from Video Feed
// ============================================

/**
 * Draws the current video frame onto a hidden canvas,
 * converts it to a Blob, and uploads it to the Flask backend.
 */
async function captureImage() {
    const videoEl = document.getElementById('camera-feed') || document.getElementById('cameraFeed');
    const canvas = document.getElementById('ar-overlay') || document.getElementById('captureCanvas');

    if (!videoEl || !canvas) {
        showCameraError('Required video or canvas element not found.');
        return;
    }

    if (!cameraStream) {
        showCameraError('Camera is not active. Please start the camera first.');
        return;
    }

    // Set canvas dimensions to match the video feed
    canvas.width = videoEl.videoWidth;
    canvas.height = videoEl.videoHeight;

    // Draw the current video frame onto the canvas
    const ctx = canvas.getContext('2d');
    ctx.drawImage(videoEl, 0, 0, canvas.width, canvas.height);

    // Convert canvas content to a Blob for upload
    canvas.toBlob(async (blob) => {
        if (!blob) {
            showCameraError('Failed to capture image from camera.');
            return;
        }

        // Upload the captured image to the backend
        await uploadImage(blob);
    }, 'image/jpeg', 0.9);
}

// ============================================
// 6. Upload Image to Flask Backend
// ============================================

/**
 * Sends the captured image Blob to the /upload-image endpoint
 * using the Fetch API with FormData.
 */
async function uploadImage(blob) {
    const formData = new FormData();
    formData.append('image', blob, 'capture.jpg');

    try {
        showLoading(document.getElementById('capture-photo'), '');

        const response = await fetch('/upload-image', {
            method: 'POST',
            body: formData
        });

        const data = await response.json();

        if (response.ok) {
            console.log('Image uploaded successfully:', data);
            // Optionally show a success message or process the response
        } else {
            console.error('Upload failed:', data);
            showCameraError(data.message || 'Image upload failed.');
        }
    } catch (error) {
        console.error('Upload error:', error);
        showCameraError('Network error: Could not upload image.');
    } finally {
        hideLoading(document.getElementById('capture-photo'), 'Capture');
    }
}

// ============================================
// 7. Stop Camera - Release Resources
// ============================================

/**
 * Stops all tracks on the active media stream and
 * releases the camera so other apps can use it.
 */
function stopCamera() {
    const videoEl = document.getElementById('camera-feed') || document.getElementById('cameraFeed');
    const startBtn = document.getElementById('start-camera');
    const captureBtn = document.getElementById('capture-photo');
    const stopBtn = document.getElementById('stop-camera');
    const flipBtn = document.getElementById('flip-camera');

    // Stop every track in the stream
    if (cameraStream) {
        cameraStream.getTracks().forEach(track => track.stop());
        cameraStream = null;
    }

    // Clear the video element source
    if (videoEl) {
        videoEl.srcObject = null;
    }

    // Reset button states
    if (startBtn) startBtn.disabled = false;
    if (captureBtn) captureBtn.disabled = true;
    if (stopBtn) stopBtn.disabled = true;
    if (flipBtn) flipBtn.disabled = true;

    console.log('Camera stopped.');
}

// ============================================
// 8. Auto-Stop Camera on Page Exit
// ============================================

/**
 * Ensures the camera is released when the user navigates
 * away from or refreshes the page.
 */
window.addEventListener('beforeunload', stopCamera);

// ============================================
// 9. Error Handling Helpers
// ============================================

/**
 * Maps MediaDevices API errors to user-friendly messages
 * and displays them in the error container.
 */
function handleCameraError(error) {
    let message;

    switch (error.name) {
        case 'NotAllowedError':
        case 'PermissionDeniedError':
            message = 'Camera permission denied. Please allow camera access in your browser settings and try again.';
            break;
        case 'NotFoundError':
        case 'DevicesNotFoundError':
            message = 'No camera found on this device. Please connect a camera and try again.';
            break;
        case 'NotReadableError':
        case 'TrackStartError':
            message = 'Camera is already in use by another application. Please close it and try again.';
            break;
        case 'OverconstrainedError':
            message = 'Camera does not support the requested resolution. Trying with default settings...';
            break;
        case 'SecurityError':
            message = 'Camera access is blocked. Please ensure this page is served over HTTPS.';
            break;
        default:
            message = `Camera error: ${error.message || 'An unknown error occurred.'}`;
    }

    console.error('Camera error:', error);
    showCameraError(message);
}

/**
 * Displays an error message inside the #cameraError element.
 */
function showCameraError(message) {
    const errorEl = document.getElementById('cameraError');
    if (errorEl) {
        errorEl.textContent = message;
        errorEl.style.display = 'block';
    } else {
        // Fallback: alert if no error container exists
        alert(message);
    }
}

// ============================================
// 10. Utility Functions
// ============================================

/**
 * Formats a number as USD currency.
 */
function formatCurrency(amount) {
    return new Intl.NumberFormat('en-US', {
        style: 'currency',
        currency: 'USD'
    }).format(amount);
}

/**
 * Replaces element content with a loading spinner
 * and disables the element.
 */
function showLoading(element) {
    if (!element) return;
    element.dataset.originalText = element.innerHTML;
    element.innerHTML = '<div class="loading-spinner"></div>';
    element.disabled = true;
}

/**
 * Restores element content from loading state.
 */
function hideLoading(element, text) {
    if (!element) return;
    element.innerHTML = text || element.dataset.originalText || '';
    element.disabled = false;
}
