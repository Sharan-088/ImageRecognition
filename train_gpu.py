"""
GPU-Optimized Training Script for Image Recognition
Uses GPU acceleration for faster training
"""

import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
from sklearn.utils.class_weight import compute_class_weight
import os

# ========================================
# GPU Configuration
# ========================================

# Check GPU availability
gpus = tf.config.list_physical_devices('GPU')
print("\n" + "=" * 70)
print("GPU Configuration")
print("=" * 70)

if gpus:
    print(f"✓ GPU Detected: {len(gpus)} GPU(s)")
    for gpu in gpus:
        print(f"  • {gpu}")

    # Enable memory growth to prevent OOM errors
    for gpu in gpus:
        try:
            tf.config.experimental.set_memory_growth(gpu, True)
            print(f"✓ Memory growth enabled for {gpu}")
        except RuntimeError as e:
            print(f"⚠ Could not set memory growth: {e}")

    print("\n✓ Using GPU for training!")
else:
    print("❌ No GPU detected!")
    print("⚠ Training will use CPU (slow)")
    print("\nTo enable GPU:")
    print("  1. Install NVIDIA drivers")
    print("  2. Install CUDA 12.4")
    print("  3. Download cuDNN")
    print("  4. pip install tensorflow[and-cuda]")
    print("  5. Restart computer")

print("=" * 70 + "\n")

# ========================================
# 1. BASIC SETTINGS
# ========================================

IMG_SIZE = 224
BATCH_SIZE = 32  # Increased for GPU (use 16 if memory issues)
EPOCHS = 20

print(f"Training Configuration:")
print(f"  Image size: {IMG_SIZE}x{IMG_SIZE}")
print(f"  Batch size: {BATCH_SIZE}")
print(f"  Epochs: {EPOCHS}")
print()

# ========================================
# 2. LOAD TRAINING DATA
# ========================================

print("Loading training data...")

train_data = tf.keras.utils.image_dataset_from_directory(
    "dataset",
    validation_split=0.2,
    subset="training",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE
)

val_data = tf.keras.utils.image_dataset_from_directory(
    "dataset",
    validation_split=0.2,
    subset="validation",
    seed=123,
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

class_names = train_data.class_names

print(f"\n✓ Data loaded successfully")
print(f"  Categories: {class_names}")
print(f"  Number of categories: {len(class_names)}")

# Save category names
with open("classes.txt", "w") as f:
    f.write("\n".join(class_names))

# ========================================
# 3. CALCULATE CLASS WEIGHTS
# ========================================

print("\nCalculating class weights...")

labels = np.concatenate([
    y.numpy() for x, y in train_data
])

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(weights))

print(f"✓ Class Weights:")
for class_name, weight in zip(class_names, weights):
    print(f"    {class_name}: {weight:.3f}")

# ========================================
# 4. DATA AUGMENTATION
# ========================================

print("\nSetting up data augmentation...")

augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

print("✓ Data augmentation configured")

# ========================================
# 5. LOAD MOBILENETV2
# ========================================

print("\nLoading MobileNetV2 base model...")

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

print("✓ MobileNetV2 loaded (pretrained layers frozen)")

# ========================================
# 6. BUILD THE MODEL
# ========================================

print("\nBuilding model...")

inputs = layers.Input(shape=(IMG_SIZE, IMG_SIZE, 3))

x = augmentation(inputs)

# MobileNetV2 preprocessing
x = layers.Rescaling(1.0 / 127.5, offset=-1)(x)

x = base_model(x, training=False)

x = layers.GlobalAveragePooling2D()(x)

x = layers.Dense(128, activation="relu")(x)

x = layers.Dropout(0.4)(x)

outputs = layers.Dense(
    len(class_names),
    activation="softmax"
)(x)

model = models.Model(inputs, outputs)

print("✓ Model architecture created")

# ========================================
# 7. COMPILE MODEL
# ========================================

print("\nCompiling model...")

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("✓ Model compiled")

print("\n----- MODEL ARCHITECTURE -----")
model.summary()

# ========================================
# 8. CALLBACKS
# ========================================

print("\nSetting up callbacks...")

early_stop = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=5,
    restore_best_weights=True
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=2
)

checkpoint = tf.keras.callbacks.ModelCheckpoint(
    "model.keras",
    monitor="val_loss",
    save_best_only=True
)

print("✓ Callbacks configured")

# ========================================
# 9. OPTIMIZE DATA PIPELINE FOR GPU
# ========================================

print("\nOptimizing data pipeline for GPU...")

AUTOTUNE = tf.data.AUTOTUNE

# Prefetch for better GPU utilization
train_data = train_data.prefetch(AUTOTUNE)
val_data = val_data.prefetch(AUTOTUNE)

print("✓ Data pipeline optimized")
print(f"  - Prefetching: {AUTOTUNE} batches")

# ========================================
# 10. TRAIN MODEL (GPU ACCELERATED!)
# ========================================

print("\n" + "=" * 70)
print("STARTING GPU-ACCELERATED TRAINING")
print("=" * 70)

import time
train_start = time.time()

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr, checkpoint],
    verbose=1  # Show progress bar
)

train_time = time.time() - train_start

print("\n" + "=" * 70)
print(f"✓ TRAINING COMPLETED")
print(f"  Total time: {train_time/60:.1f} minutes ({train_time:.0f} seconds)")
print(f"  Average per epoch: {train_time/len(history.epoch):.1f} seconds")
print("=" * 70)

# ========================================
# 11. SAVE FINAL MODEL
# ========================================

print("\nSaving model...")

model.save("model.keras")

print("✓ Model saved as model.keras")
print("✓ Categories saved in classes.txt")

# ========================================
# 12. TRAINING SUMMARY
# ========================================

print("\n" + "=" * 70)
print("TRAINING SUMMARY")
print("=" * 70)

final_accuracy = history.history['accuracy'][-1]
final_val_accuracy = history.history['val_accuracy'][-1]
final_loss = history.history['loss'][-1]
final_val_loss = history.history['val_loss'][-1]

print(f"\nFinal Metrics:")
print(f"  Training Accuracy: {final_accuracy*100:.2f}%")
print(f"  Validation Accuracy: {final_val_accuracy*100:.2f}%")
print(f"  Training Loss: {final_loss:.4f}")
print(f"  Validation Loss: {final_val_loss:.4f}")

print(f"\nTraining Statistics:")
print(f"  Total epochs trained: {len(history.epoch)}")
print(f"  Stopped at epoch: {history.epoch[-1] + 1}")
print(f"  Total training time: {train_time/60:.1f} minutes")
print(f"  Time per epoch: {train_time/len(history.epoch):.1f} seconds")

if gpus:
    print(f"\n✓ Trained with GPU acceleration")
    print(f"  GPU: NVIDIA GeForce RTX 3050 Ti")
else:
    print(f"\n⚠ Trained on CPU (slower than GPU)")

print("\n" + "=" * 70)
print("✓ MODEL TRAINING COMPLETE!")
print("=" * 70)
print("\nNext steps:")
print("  1. Test predictions: python predict.py")
print("  2. Evaluate model: python evaluate.py")
print("  3. Run web interface: python app.py")
print("=" * 70)
