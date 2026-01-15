import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler
import joblib
import os

def create_sample_data():
    """Create sample house price data for training"""
    np.random.seed(42)
    n_samples = 1000
    
    data = {
        'area': np.random.randint(500, 5000, n_samples),
        'bedrooms': np.random.randint(1, 6, n_samples),
        'bathrooms': np.random.randint(1, 5, n_samples),
        'age': np.random.randint(0, 50, n_samples),
        'location_score': np.random.uniform(1, 10, n_samples),
        'parking': np.random.choice([0, 1], n_samples),
        'furnished': np.random.choice([0, 1], n_samples)
    }
    
    # Create price based on features with some randomness
    price = (
        data['area'] * 50 +
        data['bedrooms'] * 50000 +
        data['bathrooms'] * 30000 -
        data['age'] * 2000 +
        data['location_score'] * 20000 +
        data['parking'] * 30000 +
        data['furnished'] * 40000 +
        np.random.normal(0, 50000, n_samples)
    )
    
    data['price'] = np.maximum(price, 100000)  # Minimum price
    
    return pd.DataFrame(data)

def train_model():
    """Train the house price prediction model"""
    # Create or load data
    if os.path.exists('house_data.csv'):
        df = pd.read_csv('house_data.csv')
    else:
        df = create_sample_data()
        df.to_csv('house_data.csv', index=False)
    
    # Prepare features and target
    X = df.drop('price', axis=1)
    y = df['price']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestRegressor(n_estimators=100, random_state=42, max_depth=10)
    model.fit(X_train, y_train)
    
    # Save model
    joblib.dump(model, 'house_price_model.pkl')
    
    # Calculate and print accuracy
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"Model trained successfully!")
    print(f"Training R² Score: {train_score:.4f}")
    print(f"Test R² Score: {test_score:.4f}")
    
    return model

def load_model():
    """Load the trained model"""
    if os.path.exists('house_price_model.pkl'):
        return joblib.load('house_price_model.pkl')
    else:
        return train_model()

if __name__ == '__main__':
    train_model()

