// AR Viewer JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initARViewer();
});

function initARViewer() {
    const startBtn = document.getElementById('start-ar');
    const captureBtn = document.getElementById('capture-ar');
    const stopBtn = document.getElementById('stop-ar');

    if (startBtn) {
        startBtn.addEventListener('click', startAR);
    }
    if (captureBtn) {
        captureBtn.addEventListener('click', captureAR);
    }
    if (stopBtn) {
        stopBtn.addEventListener('click', stopAR);
    }

    loadFurnitureList();
}

function startAR() {
    const scene = document.getElementById('ar-scene');
    scene.innerHTML = '<p style="color:white;">AR session starting...</p>';
    document.getElementById('capture-ar').disabled = false;
    document.getElementById('stop-ar').disabled = false;
    document.getElementById('start-ar').disabled = true;
    console.log('AR session started');
}

function captureAR() {
    console.log('Capturing AR screenshot...');
}

function stopAR() {
    const scene = document.getElementById('ar-scene');
    scene.innerHTML = '<p class="ar-placeholder">AR scene will load here.<br>Allow camera access when prompted.</p>';
    document.getElementById('capture-ar').disabled = true;
    document.getElementById('stop-ar').disabled = true;
    document.getElementById('start-ar').disabled = false;
}

function loadFurnitureList() {
    const list = document.getElementById('furniture-list');
    if (!list) return;
    // Fetch furniture items from API
    fetch('/api/furniture')
        .then(res => res.json())
        .then(data => {
            if (data.items) {
                list.innerHTML = data.items.map(item => `
                    <div class="furniture-thumb" onclick="placeFurniture(${item.id})">
                        <img src="/static/images/${item.image_path}" alt="${item.name}">
                        <span>${item.name}</span>
                    </div>
                `).join('');
            }
        })
        .catch(() => {
            list.innerHTML = '<p>No furniture available.</p>';
        });
}

function placeFurniture(itemId) {
    console.log('Placing furniture item:', itemId);
}
