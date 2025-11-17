/**
 * Main JavaScript for Huffman Image Compression
 * ==============================================
 * Handles drag & drop, form submissions, and UI interactions
 */

document.addEventListener('DOMContentLoaded', function() {

    // ========================================
    // THEME SWITCHER (Light/Dark Mode)
    // ========================================
    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme') || 'light';

    // Apply saved theme
    document.documentElement.setAttribute('data-theme', savedTheme);

    // Toggle theme
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = document.documentElement.getAttribute('data-theme');
            const newTheme = currentTheme === 'light' ? 'dark' : 'light';

            document.documentElement.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }

    // ========================================
    // UTILITY FUNCTIONS
    // ========================================

    // Toast notification system
    function showToast(message, type = 'info') {
        const toast = document.createElement('div');
        const icons = {
            'success': '✓',
            'error': '✕',
            'warning': '⚠',
            'info': 'ℹ'
        };

        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <span class="toast-icon">${icons[type] || icons.info}</span>
            <span class="toast-message">${message}</span>
        `;

        toast.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            min-width: 300px;
            max-width: 500px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : type === 'warning' ? '#f59e0b' : '#3b82f6'};
            color: white;
            border-radius: 0.75rem;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.4);
            z-index: 10000;
            display: flex;
            align-items: center;
            gap: 0.75rem;
            font-family: 'Inter', sans-serif;
            font-size: 0.95rem;
            font-weight: 500;
            animation: slideInRight 0.3s ease, fadeOut 0.3s ease 2.7s;
            opacity: 0;
        `;

        document.body.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.style.opacity = '1', 10);

        // Remove after 3 seconds
        setTimeout(() => {
            toast.style.opacity = '0';
            setTimeout(() => toast.remove(), 300);
        }, 3000);
    }

    // File size formatter
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / 1024 / 1024).toFixed(2) + ' MB';
    }

    // File validation
    function validateImageFile(file, maxSizeMB = 50) {
        const allowedTypes = ['image/jpeg', 'image/jpg', 'image/png', 'image/bmp'];
        const maxSize = maxSizeMB * 1024 * 1024;

        if (!allowedTypes.includes(file.type)) {
            showToast(`Format file tidak didukung: ${file.type}. Gunakan JPG, PNG, atau BMP.`, 'error');
            return false;
        }

        if (file.size > maxSize) {
            showToast(`Ukuran file terlalu besar: ${formatFileSize(file.size)}. Maksimal ${maxSizeMB}MB.`, 'error');
            return false;
        }

        if (file.size === 0) {
            showToast('File kosong atau corrupt.', 'error');
            return false;
        }

        return true;
    }

    // ========================================
    // SINGLE IMAGE UPLOAD
    // ========================================
    const singleDropZone = document.getElementById('singleDropZone');
    const singleImageInput = document.getElementById('singleImageInput');
    const singlePreview = document.getElementById('singlePreview');
    const singleSubmitBtn = document.getElementById('singleSubmitBtn');
    const singleForm = document.getElementById('singleImageForm');

    if (singleDropZone && singleImageInput) {
        // Click to upload
        singleDropZone.addEventListener('click', () => {
            singleImageInput.click();
        });

        // Keyboard accessibility
        singleDropZone.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                singleImageInput.click();
            }
        });

        // Drag and drop events
        singleDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            singleDropZone.classList.add('dragover');
        });

        singleDropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            singleDropZone.classList.remove('dragover');
        });

        singleDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            singleDropZone.classList.remove('dragover');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                singleImageInput.files = files;
                handleSingleFileSelect(files[0]);
            }
        });

        // File input change
        singleImageInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleSingleFileSelect(e.target.files[0]);
            }
        });
    }

    function handleSingleFileSelect(file) {
        // Validate file
        if (!validateImageFile(file)) {
            singleImageInput.value = '';
            singlePreview.innerHTML = '';
            singleSubmitBtn.disabled = true;
            return;
        }

        // Show preview
        const reader = new FileReader();
        reader.onload = function(e) {
            singlePreview.innerHTML = `
                <div style="text-align: center; margin-top: 1rem;">
                    <img src="${e.target.result}"
                         style="max-width: 100%; max-height: 200px; border-radius: 0.75rem; box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);"
                         alt="Preview of ${file.name}">
                    <p style="margin-top: 0.5rem; color: #cbd5e1; font-size: 0.875rem;">
                        <strong>${file.name}</strong><br>
                        ${formatFileSize(file.size)}
                    </p>
                </div>
            `;
            showToast('File berhasil dipilih!', 'success');
        };

        reader.onerror = function() {
            showToast('Gagal membaca file. Silakan coba lagi.', 'error');
            singleImageInput.value = '';
            singlePreview.innerHTML = '';
            singleSubmitBtn.disabled = true;
        };

        reader.readAsDataURL(file);

        // Enable submit button
        if (singleSubmitBtn) {
            singleSubmitBtn.disabled = false;
        }
    }

    // Form submission with loading spinner and validation
    if (singleForm) {
        singleForm.addEventListener('submit', function(e) {
            // Double-check file is selected
            if (!singleImageInput.files || singleImageInput.files.length === 0) {
                e.preventDefault();
                showToast('Silakan pilih gambar terlebih dahulu.', 'warning');
                return;
            }

            // Validate file again before submit
            const file = singleImageInput.files[0];
            if (!validateImageFile(file)) {
                e.preventDefault();
                singleImageInput.value = '';
                singlePreview.innerHTML = '';
                singleSubmitBtn.disabled = true;
                return;
            }

            if (singleSubmitBtn) {
                singleSubmitBtn.disabled = true;
                singleSubmitBtn.querySelector('.btn-text').textContent = 'Memproses...';
                singleSubmitBtn.querySelector('.spinner').style.display = 'inline-block';
                showToast('Memproses kompresi...', 'info');
            }
        });
    }

    // ========================================
    // DATASET UPLOAD (MULTIPLE FILES)
    // ========================================
    const datasetDropZone = document.getElementById('datasetDropZone');
    const datasetInput = document.getElementById('datasetInput');
    const datasetPreview = document.getElementById('datasetPreview');
    const datasetSubmitBtn = document.getElementById('datasetSubmitBtn');
    const datasetForm = document.getElementById('datasetForm');

    if (datasetDropZone && datasetInput) {
        // Click to upload
        datasetDropZone.addEventListener('click', () => {
            datasetInput.click();
        });

        // Keyboard accessibility
        datasetDropZone.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                datasetInput.click();
            }
        });

        // Drag and drop events
        datasetDropZone.addEventListener('dragover', (e) => {
            e.preventDefault();
            e.stopPropagation();
            datasetDropZone.classList.add('dragover');
        });

        datasetDropZone.addEventListener('dragleave', (e) => {
            e.preventDefault();
            e.stopPropagation();
            datasetDropZone.classList.remove('dragover');
        });

        datasetDropZone.addEventListener('drop', (e) => {
            e.preventDefault();
            e.stopPropagation();
            datasetDropZone.classList.remove('dragover');

            const files = e.dataTransfer.files;
            if (files.length > 0) {
                datasetInput.files = files;
                handleDatasetFileSelect(files);
            }
        });

        // File input change
        datasetInput.addEventListener('change', (e) => {
            if (e.target.files.length > 0) {
                handleDatasetFileSelect(e.target.files);
            }
        });
    }

    function handleDatasetFileSelect(files) {
        // Validate all files
        const fileArray = Array.from(files);
        const validFiles = [];
        const invalidFiles = [];

        fileArray.forEach(file => {
            if (validateImageFile(file, 50)) {
                validFiles.push(file);
            } else {
                invalidFiles.push(file.name);
            }
        });

        if (validFiles.length === 0) {
            showToast('Tidak ada file gambar yang valid!', 'error');
            datasetPreview.innerHTML = '';
            datasetSubmitBtn.disabled = true;
            return;
        }

        if (invalidFiles.length > 0) {
            showToast(`${invalidFiles.length} file tidak valid dan diabaikan.`, 'warning');
        }

        // Show preview info
        const totalSize = validFiles.reduce((sum, file) => sum + file.size, 0);
        datasetPreview.innerHTML = `
            <div style="text-align: center; margin-top: 1rem; padding: 1rem; background: rgba(16, 185, 129, 0.1); border-radius: 0.75rem; border: 1px solid #10b981;">
                <p style="color: #10b981; font-weight: 600; font-size: 1.125rem;">${validFiles.length} gambar valid dipilih</p>
                <p style="color: #cbd5e1; font-size: 0.875rem; margin-top: 0.25rem;">Total ukuran: ${formatFileSize(totalSize)}</p>
                <div style="margin-top: 0.75rem; display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;">
                    ${validFiles.slice(0, 5).map(file =>
                        `<span style="background: rgba(59, 130, 246, 0.2); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: #cbd5e1;">${file.name}</span>`
                    ).join('')}
                    ${validFiles.length > 5 ? `<span style="background: rgba(239, 68, 68, 0.2); padding: 0.25rem 0.75rem; border-radius: 9999px; font-size: 0.75rem; color: #cbd5e1;">+${validFiles.length - 5} lainnya</span>` : ''}
                </div>
            </div>
        `;

        showToast(`${validFiles.length} gambar siap dikompresi!`, 'success');

        // Enable submit button
        if (datasetSubmitBtn) {
            datasetSubmitBtn.disabled = false;
        }
    }

    // Form submission with loading spinner and validation
    if (datasetForm) {
        datasetForm.addEventListener('submit', function(e) {
            // Check files are selected
            if (!datasetInput.files || datasetInput.files.length === 0) {
                e.preventDefault();
                showToast('Silakan pilih gambar terlebih dahulu.', 'warning');
                return;
            }

            if (datasetSubmitBtn) {
                datasetSubmitBtn.disabled = true;
                datasetSubmitBtn.querySelector('.btn-text').textContent = 'Memproses Dataset...';
                datasetSubmitBtn.querySelector('.spinner').style.display = 'inline-block';
                showToast(`Memproses ${datasetInput.files.length} gambar...`, 'info');
            }
        });
    }

    // ========================================
    // DECOMPRESSION FORM
    // ========================================
    const decompressForm = document.getElementById('decompressForm');
    const binFile = document.getElementById('binFile');
    const codesFile = document.getElementById('codesFile');
    const sizeFile = document.getElementById('sizeFile');
    const decompressSubmitBtn = document.getElementById('decompressSubmitBtn');

    function checkDecompressFiles() {
        if (binFile && codesFile && sizeFile && decompressSubmitBtn) {
            const allFilled = binFile.files.length > 0 &&
                            codesFile.files.length > 0 &&
                            sizeFile.files.length > 0;
            decompressSubmitBtn.disabled = !allFilled;
        }
    }

    if (binFile) binFile.addEventListener('change', checkDecompressFiles);
    if (codesFile) codesFile.addEventListener('change', checkDecompressFiles);
    if (sizeFile) sizeFile.addEventListener('change', checkDecompressFiles);

    if (decompressForm) {
        decompressForm.addEventListener('submit', function(e) {
            if (decompressSubmitBtn) {
                decompressSubmitBtn.disabled = true;
                decompressSubmitBtn.querySelector('.btn-text').textContent = 'Memproses...';
                decompressSubmitBtn.querySelector('.spinner').style.display = 'inline-block';
            }
        });
    }

    // ========================================
    // SMOOTH ANIMATIONS
    // ========================================
    // Animate cards on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = '1';
                entry.target.style.transform = 'translateY(0)';
            }
        });
    }, observerOptions);

    // Observe all cards
    document.querySelectorAll('.card').forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
        observer.observe(card);
    });

    // ========================================
    // UTILITY FUNCTIONS
    // ========================================

    // Format file size
    function formatFileSize(bytes) {
        if (bytes < 1024) return bytes + ' B';
        if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
        return (bytes / 1024 / 1024).toFixed(2) + ' MB';
    }

    // Show notification
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 1rem 1.5rem;
            background: ${type === 'success' ? '#10b981' : type === 'error' ? '#ef4444' : '#3b82f6'};
            color: white;
            border-radius: 0.75rem;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
            z-index: 10000;
            animation: slideIn 0.3s ease;
        `;
        notification.textContent = message;
        document.body.appendChild(notification);

        setTimeout(() => {
            notification.style.animation = 'slideOut 0.3s ease';
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    // Add animation keyframes
    const style = document.createElement('style');
    style.textContent = `
        @keyframes slideIn {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        @keyframes slideOut {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
    `;
    document.head.appendChild(style);

});

// ========================================
// PRINT OPTIMIZATION
// ========================================
window.addEventListener('beforeprint', () => {
    document.body.style.background = 'white';
});

window.addEventListener('afterprint', () => {
    document.body.style.background = '';
});x