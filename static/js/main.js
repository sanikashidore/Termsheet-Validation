document.addEventListener('DOMContentLoaded', function() {
    const uploadForm = document.getElementById('upload-form');
    const termSheetInput = document.getElementById('termsheet');
    const referenceInput = document.getElementById('reference');
    const validateBtn = document.getElementById('validate-btn');
    const validateText = document.getElementById('validate-text');
    const validateSpinner = document.getElementById('validate-spinner');
    const errorMessage = document.getElementById('error-message');
    const termSheetDropzone = document.getElementById('term-sheet-dropzone');
    const referenceDropzone = document.getElementById('reference-dropzone');

    // File selection event for term sheet
    termSheetInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const fileName = this.files[0].name;
            document.getElementById('selected-file-name').textContent = fileName;
            
            // Show the preview content and hide the dropzone content
            const dropzoneContent = termSheetDropzone.querySelector('.dropzone-content');
            const previewContent = termSheetDropzone.querySelector('.preview-content');
            
            dropzoneContent.classList.add('d-none');
            previewContent.classList.remove('d-none');
        }
    });

    // Change button for term sheet
    document.getElementById('change-file-btn').addEventListener('click', function(e) {
        e.preventDefault();
        termSheetInput.value = '';
        
        const dropzoneContent = termSheetDropzone.querySelector('.dropzone-content');
        const previewContent = termSheetDropzone.querySelector('.preview-content');
        
        previewContent.classList.add('d-none');
        dropzoneContent.classList.remove('d-none');
    });

    // File selection event for reference template
    referenceInput.addEventListener('change', function() {
        if (this.files && this.files[0]) {
            const fileName = this.files[0].name;
            document.getElementById('selected-template-name').textContent = fileName;
            
            // Show the preview content and hide the dropzone content
            const dropzoneContent = referenceDropzone.querySelector('.dropzone-content');
            const previewContent = referenceDropzone.querySelector('.preview-content');
            
            dropzoneContent.classList.add('d-none');
            previewContent.classList.remove('d-none');
        }
    });

    // Change button for reference template
    document.getElementById('change-template-btn').addEventListener('click', function(e) {
        e.preventDefault();
        referenceInput.value = '';
        
        const dropzoneContent = referenceDropzone.querySelector('.dropzone-content');
        const previewContent = referenceDropzone.querySelector('.preview-content');
        
        previewContent.classList.add('d-none');
        dropzoneContent.classList.remove('d-none');
    });

    // Drag and drop for term sheet
    ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
        termSheetDropzone.addEventListener(eventName, preventDefaults, false);
    });

    function preventDefaults(e) {
        e.preventDefault();
        e.stopPropagation();
    }

    ['dragenter', 'dragover'].forEach(eventName => {
        termSheetDropzone.addEventListener(eventName, highlight, false);
    });

    ['dragleave', 'drop'].forEach(eventName => {
        termSheetDropzone.addEventListener(eventName, unhighlight, false);
    });

    function highlight() {
        termSheetDropzone.classList.add('drag-over');
    }

    function unhighlight() {
        termSheetDropzone.classList.remove('drag-over');
    }

    termSheetDropzone.addEventListener('drop', handleDrop, false);

    function handleDrop(e) {
        const dt = e.dataTransfer;
        const files = dt.files;
        
        if (files && files.length > 0) {
            termSheetInput.files = files;
            const changeEvent = new Event('change');
            termSheetInput.dispatchEvent(changeEvent);
        }
    }

    // Click on dropzone opens file dialog
    termSheetDropzone.addEventListener('click', function() {
        if (termSheetDropzone.querySelector('.dropzone-content').classList.contains('d-none')) {
            return;
        }
        termSheetInput.click();
    });

    referenceDropzone.addEventListener('click', function() {
        if (referenceDropzone.querySelector('.dropzone-content').classList.contains('d-none')) {
            return;
        }
        referenceInput.click();
    });

    // Form submission
    uploadForm.addEventListener('submit', function(e) {
        e.preventDefault();
        
        // Validate form
        if (!termSheetInput.files || termSheetInput.files.length === 0) {
            showError('Please select a term sheet file');
            return;
        }
        
        // Prepare form data
        const formData = new FormData();
        formData.append('termsheet', termSheetInput.files[0]);
        
        if (referenceInput.files && referenceInput.files.length > 0) {
            formData.append('reference', referenceInput.files[0]);
        }
        
        // Add OCR option
        const useOCR = document.getElementById('use-ocr').checked;
        formData.append('use_ocr', useOCR);
        
        // Show loading state
        setLoading(true);
        hideError();
        
        // Send request
        fetch('/upload', {
            method: 'POST',
            body: formData
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || 'Error processing file');
                });
            }
            return response.json();
        })
        .then(data => {
            if (data.redirect) {
                window.location.href = data.redirect;
            } else {
                setLoading(false);
                showError('Unexpected response from server');
            }
        })
        .catch(error => {
            setLoading(false);
            showError(error.message);
        });
    });

    function setLoading(isLoading) {
        if (isLoading) {
            validateText.classList.add('d-none');
            validateSpinner.classList.remove('d-none');
            validateBtn.disabled = true;
        } else {
            validateText.classList.remove('d-none');
            validateSpinner.classList.add('d-none');
            validateBtn.disabled = false;
        }
    }

    function showError(message) {
        errorMessage.textContent = message;
        errorMessage.classList.remove('d-none');
    }

    function hideError() {
        errorMessage.classList.add('d-none');
    }
});