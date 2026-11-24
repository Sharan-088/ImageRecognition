import os
import json
from datetime import datetime
from flask import Flask, render_template, request, jsonify
import tensorflow as tf
import numpy as np
from werkzeug.utils import secure_filename

# Initialize Flask app
app = Flask(__name__)

# Configuration
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Create necessary directories
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs('logs', exist_ok=True)

# Load the trained model and class names at startup
print("Loading model...")
try:
    model = tf.keras.models.load_model("model.keras")
    with open("classes.txt", "r") as f:
        class_names = f.read().splitlines()
    print(f"Model loaded successfully! Classes: {class_names}")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None
    class_names = []


def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def cleanup_old_uploads(max_age_hours=1):
    """Remove uploaded files older than max_age_hours"""
    try:
        current_time = datetime.now().timestamp()
        max_age_seconds = max_age_hours * 3600

        for filename in os.listdir(UPLOAD_FOLDER):
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            if os.path.isfile(filepath):
                file_age = current_time - os.path.getmtime(filepath)
                if file_age > max_age_seconds:
                    os.remove(filepath)
                    print(f"Cleaned up old file: {filename}")
    except Exception as e:
        print(f"Error during cleanup: {e}")


def log_prediction(filename, predicted_class, confidence, all_predictions):
    """Log prediction to JSON file"""
    try:
        log_file = 'logs/predictions.json'

        # Read existing logs
        if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
            with open(log_file, 'r') as f:
                logs = json.load(f)
        else:
            logs = []

        # Create new log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'filename': filename,
            'predicted_class': predicted_class,
            'confidence': confidence,
            'all_predictions': all_predictions
        }

        # Append and keep only last 100 entries
        logs.append(log_entry)
        logs = logs[-100:]

        # Write back to file
        with open(log_file, 'w') as f:
            json.dump(logs, f, indent=2)

    except Exception as e:
        print(f"Error logging prediction: {e}")


@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')


@app.route('/health')
def health():
    """Health check endpoint"""
    if model is not None:
        return jsonify({
            'status': 'healthy',
            'model_loaded': True,
            'classes': class_names
        })
    else:
        return jsonify({
            'status': 'error',
            'model_loaded': False,
            'message': 'Model failed to load'
        }), 500


@app.route('/predict', methods=['POST'])
def predict():
    """Handle image upload and prediction"""
    try:
        # Check if model is loaded
        if model is None:
            return jsonify({
                'success': False,
                'error': 'Model not loaded'
            }), 500

        # Check if file is in request
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'error': 'No file uploaded'
            }), 400

        file = request.files['image']

        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'error': 'No file selected'
            }), 400

        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({
                'success': False,
                'error': 'Invalid file type. Only PNG, JPG, and JPEG are allowed.'
            }), 400

        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = secure_filename(file.filename)
        unique_filename = f"{timestamp}_{filename}"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)

        # Save uploaded file
        file.save(filepath)

        # Load and preprocess image
        img = tf.keras.utils.load_img(filepath, target_size=(224, 224))
        img_array = tf.keras.utils.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)

        # Make prediction
        predictions = model.predict(img_array, verbose=0)

        # Process results
        predicted_index = np.argmax(predictions[0])
        predicted_class = class_names[predicted_index]
        confidence = float(predictions[0][predicted_index] * 100)

        # Prepare all predictions
        all_predictions = []
        for i, class_name in enumerate(class_names):
            all_predictions.append({
                'class': class_name,
                'confidence': float(predictions[0][i] * 100)
            })

        # Sort by confidence
        all_predictions.sort(key=lambda x: x['confidence'], reverse=True)

        # Log prediction
        log_prediction(unique_filename, predicted_class, confidence, all_predictions)

        # Return results
        return jsonify({
            'success': True,
            'predicted_class': predicted_class,
            'confidence': round(confidence, 2),
            'all_predictions': all_predictions,
            'image_url': f"/static/uploads/{unique_filename}"
        })

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({
            'success': False,
            'error': f'Prediction failed: {str(e)}'
        }), 500


@app.route('/history')
def history():
    """View prediction history"""
    try:
        log_file = 'logs/predictions.json'
        if os.path.exists(log_file) and os.path.getsize(log_file) > 0:
            with open(log_file, 'r') as f:
                logs = json.load(f)
            return jsonify({
                'success': True,
                'history': logs
            })
        else:
            return jsonify({
                'success': True,
                'history': []
            })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500


if __name__ == '__main__':
    # Cleanup old uploads at startup
    print("Cleaning up old uploads...")
    cleanup_old_uploads()

    # Run Flask app
    print("Starting Flask server...")
    print("Access the application at: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000)
