document.getElementById('predictionForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const submitBtn = document.querySelector('.predict-btn');
    const originalText = submitBtn.innerHTML;
    
    // Disable button and show loading
    submitBtn.disabled = true;
    submitBtn.innerHTML = '<span>Predicting...</span><span class="loading"></span>';
    
    // Get form data
    const formData = {
        area: document.getElementById('area').value,
        bedrooms: document.getElementById('bedrooms').value,
        bathrooms: document.getElementById('bathrooms').value,
        age: document.getElementById('age').value,
        location_score: document.getElementById('location_score').value,
        parking: document.getElementById('parking').checked ? 1 : 0,
        furnished: document.getElementById('furnished').checked ? 1 : 0
    };
    
    try {
        const response = await fetch('/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        const data = await response.json();
        
        if (data.success) {
            // Display result
            document.getElementById('priceDisplay').textContent = data.formatted_price;
            document.getElementById('resultContainer').style.display = 'flex';
            
            // Scroll to result
            document.getElementById('resultContainer').scrollIntoView({ 
                behavior: 'smooth', 
                block: 'nearest' 
            });
        } else {
            showError(data.error || 'An error occurred while predicting the price.');
        }
    } catch (error) {
        showError('Failed to connect to the server. Please try again.');
        console.error('Error:', error);
    } finally {
        // Re-enable button
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalText;
    }
});

function showError(message) {
    const resultContainer = document.getElementById('resultContainer');
    resultContainer.innerHTML = `
        <div class="error-message">
            <strong>Error:</strong> ${message}
        </div>
    `;
    resultContainer.style.display = 'flex';
}

function resetForm() {
    document.getElementById('predictionForm').reset();
    document.getElementById('resultContainer').style.display = 'none';
    document.getElementById('resultContainer').innerHTML = `
        <div class="result-card">
            <h2>Predicted House Price</h2>
            <div class="price-display" id="priceDisplay">
                $0.00
            </div>
            <button class="reset-btn" onclick="resetForm()">Predict Another</button>
        </div>
    `;
}

