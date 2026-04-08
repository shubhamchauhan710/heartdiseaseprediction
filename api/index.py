"""
Vercel Serverless Function for Heart Disease Prediction API
"""
import numpy as np
import pickle
import json
from http.server import BaseHTTPRequestHandler
import os

# Load the model
model_path = os.path.join(os.path.dirname(__file__), '..', 'trained_model.sav')
try:
    loaded_model = pickle.load(open(model_path, "rb"))
except Exception as e:
    loaded_model = None
    print(f"Error loading model: {e}")


def heart_disease_prediction(input_data):
    """
    Predict heart disease based on input features
    
    Args:
        input_data: List of 13 features for prediction
        
    Returns:
        Prediction result (0 or 1)
    """
    if loaded_model is None:
        return None
        
    input_data_as_numpy_array = np.asarray(input_data)
    input_data_reshaped = input_data_as_numpy_array.reshape(1, -1)
    prediction = loaded_model.predict(input_data_reshaped)
    
    return int(prediction[0])


class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        """Handle POST requests"""
        try:
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(body)
            
            # Validate input data
            if 'features' not in data or len(data['features']) != 13:
                self.send_response(400)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({
                    'error': 'Invalid input. Please provide exactly 13 features.',
                    'features_required': [
                        'age', 'sex', 'cp', 'trestbps', 'chol', 'fbs', 'restecg',
                        'thalach', 'exang', 'oldpeak', 'slope', 'ca', 'thal'
                    ]
                })
                self.wfile.write(response.encode('utf-8'))
                return
            
            # Make prediction
            prediction = heart_disease_prediction(data['features'])
            
            if prediction is None:
                self.send_response(500)
                self.send_header('Content-Type', 'application/json')
                self.end_headers()
                response = json.dumps({'error': 'Model not loaded'})
                self.wfile.write(response.encode('utf-8'))
                return
            
            # Send response
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            result_text = 'The Person has Heart Disease' if prediction == 1 else 'The Person does not have a Heart Disease'
            response = json.dumps({
                'prediction': prediction,
                'result': result_text,
                'probability': float(prediction)
            })
            self.wfile.write(response.encode('utf-8'))
            
        except json.JSONDecodeError:
            self.send_response(400)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'Invalid JSON'})
            self.wfile.write(response.encode('utf-8'))
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': str(e)})
            self.wfile.write(response.encode('utf-8'))

    def do_GET(self):
        """Handle GET requests"""
        if self.path == '/' or self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({
                'status': 'ok',
                'message': 'Heart Disease Prediction API',
                'endpoint': '/api',
                'method': 'POST'
            })
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_response(404)
            self.send_header('Content-Type', 'application/json')
            self.end_headers()
            response = json.dumps({'error': 'Not found'})
            self.wfile.write(response.encode('utf-8'))

    def end_headers(self):
        """Add CORS headers"""
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
