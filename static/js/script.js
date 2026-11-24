// Wait for DOM to be fully loaded
document.addEventListener('DOMContentLoaded', function() {
    // Get DOM elements
    const imageInput = document.getElementById('imageInput');
    const previewSection = document.getElementById('previewSection');
    const imagePreview = document.getElementById('imagePreview');
    const predictButton = document.getElementById('predictButton');
    const resultSection = document.getElementById('resultSection');
    const predictionText = document.getElementById('prediction');
    const confidenceText = document.getElementById('confidence');

    // Handle image file selection
    imageInput.addEventListener('change', function(e) {
        const file = e.target.files[0];

        if (file) {
            // Check file type
            if (!file.type.match('image.*')) {
                alert('Please select an image file (PNG, JPG, or JPEG)');
                return;
            }

            // Check file size (10MB max)
            if (file.size > 10 * 1024 * 1024) {
                alert('File size too large. Please select an image under 10MB.');
                return;
            }

            // Read and display image preview
            const reader = new FileReader();

            reader.onload = function(e) {
                imagePreview.src = e.target.result;
                previewSection.classList.add('active');
                resultSection.classList.remove('active');
                predictButton.disabled = false;
            };

            reader.onerror = function() {
                alert('Error reading file. Please try again.');
            };

            reader.readAsDataURL(file);
        }
    });

    // Handle prediction button click
    predictButton.addEventListener('click', async function() {
        const file = imageInput.files[0];

        if (!file) {
            alert('Please select an image first');
            return;
        }

        // Disable button and show loading state
        predictButton.disabled = true;
        predictButton.textContent = 'Analyzing...';

        // Create loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'loading active';
        loadingDiv.innerHTML = `
            <div class="spinner"></div>
            <p>Analyzing your image...</p>
        `;
        previewSection.appendChild(loadingDiv);

        // Prepare form data
        const formData = new FormData();
        formData.append('image', file);

        try {
            // Send prediction request
            const response = await fetch('/predict', {
                method: 'POST',
                body: formData
            });

            const data = await response.json();

            // Remove loading indicator
            loadingDiv.remove();

            if (data.success) {
                // Display prediction results
                displayResults(data);
            } else {
                // Show error message
                alert(`Prediction failed: ${data.error}`);
                predictButton.disabled = false;
                predictButton.textContent = 'Predict Image';
            }

        } catch (error) {
            // Remove loading indicator
            loadingDiv.remove();

            console.error('Error:', error);
            alert('Failed to connect to server. Please try again.');
            predictButton.disabled = false;
            predictButton.textContent = 'Predict Image';
        }
    });

    // Display prediction results
    function displayResults(data) {
        // Update prediction text
        predictionText.textContent = data.predicted_class.toUpperCase();
        confidenceText.textContent = `${data.confidence}%`;

        // Create confidence bars for all predictions
        createConfidenceBars(data.all_predictions);

        // Show result section with animation
        resultSection.classList.add('active');

        // Scroll to results
        resultSection.scrollIntoView({ behavior: 'smooth', block: 'nearest' });

        // Reset predict button
        predictButton.disabled = false;
        predictButton.textContent = 'Predict Again';
    }

    // Create confidence bars visualization
    function createConfidenceBars(predictions) {
        // Check if confidence bars container already exists
        let confidenceBarsContainer = resultSection.querySelector('.confidence-bars');

        if (!confidenceBarsContainer) {
            confidenceBarsContainer = document.createElement('div');
            confidenceBarsContainer.className = 'confidence-bars';
            resultSection.appendChild(confidenceBarsContainer);
        } else {
            // Clear existing bars
            confidenceBarsContainer.innerHTML = '';
        }

        // Create a bar for each prediction
        predictions.forEach((pred, index) => {
            const confidence = pred.confidence;

            // Determine color class based on confidence
            let colorClass = 'low';
            if (confidence > 70) {
                colorClass = 'high';
            } else if (confidence > 40) {
                colorClass = 'medium';
            }

            // Create confidence item
            const itemDiv = document.createElement('div');
            itemDiv.className = 'confidence-item';

            itemDiv.innerHTML = `
                <div class="confidence-label">
                    <span>${pred.class}</span>
                    <span>${confidence.toFixed(2)}%</span>
                </div>
                <div class="confidence-bar">
                    <div class="confidence-fill ${colorClass}" style="width: 0%"></div>
                </div>
            `;

            confidenceBarsContainer.appendChild(itemDiv);

            // Animate bar width after a short delay
            setTimeout(() => {
                const fillElement = itemDiv.querySelector('.confidence-fill');
                fillElement.style.width = `${confidence}%`;
            }, 100 * (index + 1));
        });
    }

    // Reset functionality when new image is selected
    imageInput.addEventListener('change', function() {
        predictButton.textContent = 'Predict Image';
    });
});
