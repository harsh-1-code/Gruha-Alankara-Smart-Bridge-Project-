// Analyze page JavaScript

document.addEventListener('DOMContentLoaded', () => {
    initImageUpload();
});

function initImageUpload() {
    const uploadArea = document.getElementById('upload-area');
    const fileInput = document.getElementById('room-image');
    const preview = document.getElementById('image-preview');

    if (!uploadArea || !fileInput) return;

    // Drag and drop support
    uploadArea.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadArea.classList.add('drag-over');
    });

    uploadArea.addEventListener('dragleave', () => {
        uploadArea.classList.remove('drag-over');
    });

    uploadArea.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadArea.classList.remove('drag-over');
        const file = e.dataTransfer.files[0];
        if (file && file.type.startsWith('image/')) {
            fileInput.files = e.dataTransfer.files;
            showPreview(file);
        }
    });

    fileInput.addEventListener('change', () => {
        if (fileInput.files[0]) {
            showPreview(fileInput.files[0]);
        }
    });
}

function showPreview(file) {
    const preview = document.getElementById('image-preview');
    const reader = new FileReader();
    reader.onload = (e) => {
        preview.innerHTML = `<img src="${e.target.result}" alt="Room preview">`;
        preview.classList.remove('hidden');
    };
    reader.readAsDataURL(file);
}
