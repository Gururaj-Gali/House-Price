from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import os

app = Flask(__name__)

# Load model
model = None

def load_model():
    global model
    if os.path.exists('house_price_model.pkl'):
        model = joblib.load('house_price_model.pkl')
    else:
        from model import train_model
        model = train_model()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get data from request
        data = request.get_json()
        
        # Extract features
        features = np.array([[
            float(data['area']),
            int(data['bedrooms']),
            int(data['bathrooms']),
            int(data['age']),
            float(data['location_score']),
            int(data['parking']),
            int(data['furnished'])
        ]])
        
        # Make prediction
        prediction = model.predict(features)[0]
        
        # Format prediction
        predicted_price = round(prediction, 2)
        
        return jsonify({
            'success': True,
            'predicted_price': predicted_price,
            'formatted_price': f"${predicted_price:,.2f}"
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    load_model()
    app.run(debug=True, host='0.0.0.0', port=5000)

