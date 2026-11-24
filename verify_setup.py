#!/usr/bin/env python
"""
Verification Script for Image Recognition Web App
Checks if all required files and dependencies are in place
"""

import os
import sys

def print_header(text):
    """Print formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_file(filepath, description):
    """Check if a file exists"""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {filepath}")
    return exists

def check_directory(dirpath, description):
    """Check if a directory exists"""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"{status} {description}: {dirpath}")
    return exists

def check_import(module_name, package_name=None):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✓ {package_name or module_name} is installed")
        return True
    except ImportError:
        print(f"✗ {package_name or module_name} is NOT installed")
        return False

def main():
    """Run all verification checks"""
    print_header("Image Recognition Web App - Setup Verification")

    all_checks_passed = True

    # Check core files
    print_header("Checking Core Files")
    all_checks_passed &= check_file("app.py", "Flask Application")
    all_checks_passed &= check_file("model.keras", "Trained Model")
    all_checks_passed &= check_file("classes.txt", "Class Names")
    all_checks_passed &= check_file("requirements.txt", "Dependencies File")

    # Check template files
    print_header("Checking Template Files")
    all_checks_passed &= check_file("templates/index.html", "HTML Template")

    # Check static files
    print_header("Checking Static Files")
    all_checks_passed &= check_file("static/css/style.css", "CSS Stylesheet")
    all_checks_passed &= check_file("static/js/script.js", "JavaScript File")

    # Check directories
    print_header("Checking Directories")
    all_checks_passed &= check_directory("static/uploads", "Upload Directory")
    all_checks_passed &= check_directory("logs", "Logs Directory")
    all_checks_passed &= check_directory("dataset", "Dataset Directory")

    # Check log file
    print_header("Checking Log Files")
    all_checks_passed &= check_file("logs/predictions.json", "Predictions Log")

    # Check documentation
    print_header("Checking Documentation")
    check_file("README.md", "README")
    check_file("QUICK_START.md", "Quick Start Guide")
    check_file("WEB_DEPLOYMENT_GUIDE.md", "Deployment Guide")

    # Check Python dependencies
    print_header("Checking Python Dependencies")
    flask_ok = check_import("flask", "Flask")
    tf_ok = check_import("tensorflow", "TensorFlow")
    pil_ok = check_import("PIL", "Pillow")
    numpy_ok = check_import("numpy", "NumPy")
    werkzeug_ok = check_import("werkzeug", "Werkzeug")

    all_checks_passed &= flask_ok and tf_ok and pil_ok and numpy_ok and werkzeug_ok

    # Check model details
    print_header("Checking Model Configuration")
    try:
        with open("classes.txt", "r") as f:
            classes = f.read().splitlines()
        print(f"✓ Found {len(classes)} classes: {', '.join(classes)}")

        # Try to load model
        import tensorflow as tf
        model = tf.keras.models.load_model("model.keras")
        print(f"✓ Model loaded successfully")
        print(f"  Input shape: {model.input_shape}")
        print(f"  Output classes: {model.output_shape[1]}")

        if model.output_shape[1] != len(classes):
            print(f"⚠ Warning: Model outputs {model.output_shape[1]} classes but classes.txt has {len(classes)}")
            all_checks_passed = False
    except Exception as e:
        print(f"✗ Error loading model: {e}")
        all_checks_passed = False

    # Final summary
    print_header("Verification Summary")
    if all_checks_passed:
        print("✓ All checks PASSED! Your setup is ready.")
        print("\nYou can now start the Flask server:")
        print("  python app.py")
        print("\nThen open your browser to: http://localhost:5000")
        return 0
    else:
        print("✗ Some checks FAILED. Please fix the issues above.")
        print("\nCommon fixes:")
        print("1. Install missing dependencies:")
        print("   pip install -r requirements.txt")
        print("\n2. Create missing directories:")
        print("   mkdir static\\uploads")
        print("   mkdir logs")
        print("\n3. Train model if missing:")
        print("   python train.py")
        return 1

if __name__ == "__main__":
    sys.exit(main())
