# Image Recognition - Birds, Cat & Dog Classifier

An image classification model built with TensorFlow and MobileNetV2 transfer learning that can identify birds, cats, and dogs.

## How It Works

- Uses **MobileNetV2** (pretrained on ImageNet) as a feature extractor
- Custom classification head trained on a small dataset (~100 images per class)
- Achieves **95-100% accuracy** on test images

## Setup

```bash
# Create virtual environment
python -m venv venv
venv\Scripts\activate      # Windows
source venv/bin/activate   # Mac/Linux

# Install dependencies
pip install tensorflow matplotlib numpy
```

## Dataset Structure

Place your training images in the `dataset/` folder:

```
dataset/
├── birds/    (images of birds)
├── cat/      (images of cats)
└── dog/      (images of dogs)
```

## Usage

### Train the model
```bash
python train.py
```

### Predict an image (Command Line)
```bash
python predict.py
```
Enter the path to any image when prompted.

### Web Interface (Recommended)

The project now includes a modern web interface for easy image classification!

**Step 1: Install Flask dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Start the Flask server**
```bash
python app.py
```

**Step 3: Open your browser**
Navigate to: **http://localhost:5000**

**Features:**
- 📤 Drag-and-drop or browse to upload images
- 🖼️ Live image preview before prediction
- 📊 Visual confidence bars for all classes
- 📝 Automatic prediction history logging
- 📱 Mobile-responsive design
- 🧹 Automatic cleanup of old uploads

## Project Structure

```
ImageRecognition/
├── app.py                  # Flask web application
├── train.py               # Model training script
├── predict.py             # Command-line prediction
├── evaluate.py            # Model evaluation
├── visualize.py           # Results visualization
├── model.keras            # Trained model
├── classes.txt            # Class names
├── requirements.txt       # Python dependencies
├── templates/
│   └── index.html        # Web interface HTML
├── static/
│   ├── css/
│   │   └── style.css     # Styling
│   ├── js/
│   │   └── script.js     # Client-side logic
│   └── uploads/          # Temporary image storage
├── logs/
│   └── predictions.json  # Prediction history
└── dataset/              # Training data
```

## Technologies Used

- **Backend:** Python, Flask, TensorFlow/Keras
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **ML Model:** MobileNetV2 (Transfer Learning)
- **Image Processing:** Pillow, NumPy
