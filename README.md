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

### Predict an image
```bash
python predict.py
```
Enter the path to any image when prompted.

## Technologies Used

- Python
- TensorFlow / Keras
- MobileNetV2 (Transfer Learning)
