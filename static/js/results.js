document.addEventListener('DOMContentLoaded', function() {
    // Download JSON results
    const downloadJsonBtn = document.getElementById('download-json-btn');
    
    if (downloadJsonBtn) {
        downloadJsonBtn.addEventListener('click', function() {
            const fileId = this.getAttribute('data-file-id');
            
            // Fetch the JSON data
            fetch(`/api/results/${fileId}`)
                .then(response => {
                    if (!response.ok) {
                        throw new Error('Network response was not ok');
                    }
                    return response.json();
                })
                .then(data => {
                    // Convert data to a formatted JSON string
                    const jsonData = JSON.stringify(data, null, 2);
                    
                    // Create a Blob from the JSON string
                    const blob = new Blob([jsonData], { type: 'application/json' });
                    
                    // Create a URL for the Blob
                    const url = URL.createObjectURL(blob);
                    
                    // Create a download link
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = `termsheet_validation_${fileId}.json`;
                    
                    // Append the link to the body
                    document.body.appendChild(a);
                    
                    // Programmatically click the link to trigger the download
                    a.click();
                    
                    // Clean up
                    document.body.removeChild(a);
                    URL.revokeObjectURL(url);
                })
                .catch(error => {
                    console.error('Error downloading results:', error);
                    alert('Error downloading results. Please try again.');
                });
        });
    }
});