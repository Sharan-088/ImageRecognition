
import tensorflow as tf
import numpy as np
from tensorflow.keras import layers, models
from sklearn.utils.class_weight import compute_class_weight

# -------------------------------
# 1. BASIC SETTINGS
# -------------------------------

IMG_SIZE = 224
BATCH_SIZE = 16
EPOCHS = 20

# -------------------------------
# 2. LOAD TRAINING DATA
# -------------------------------

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

print("\nCategories:", class_names)
print("Number of categories:", len(class_names))

# Save category names
with open("classes.txt", "w") as f:
    f.write("\n".join(class_names))

# -------------------------------
# 3. CALCULATE CLASS WEIGHTS
# -------------------------------

labels = np.concatenate([
    y.numpy() for x, y in train_data
])

weights = compute_class_weight(
    class_weight="balanced",
    classes=np.unique(labels),
    y=labels
)

class_weights = dict(enumerate(weights))

print("\nClass Weights:")
print(class_weights)

# -------------------------------
# 4. DATA AUGMENTATION
# -------------------------------

augmentation = tf.keras.Sequential([
    layers.RandomFlip("horizontal"),
    layers.RandomRotation(0.1),
    layers.RandomZoom(0.1)
])

# -------------------------------
# 5. LOAD MOBILENETV2
# -------------------------------

base_model = tf.keras.applications.MobileNetV2(
    input_shape=(IMG_SIZE, IMG_SIZE, 3),
    include_top=False,
    weights="imagenet"
)

# Freeze pretrained layers
base_model.trainable = False

# -------------------------------
# 6. BUILD THE MODEL
# -------------------------------

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

# -------------------------------
# 7. COMPILE MODEL
# -------------------------------

model.compile(
    optimizer="adam",
    loss="sparse_categorical_crossentropy",
    metrics=["accuracy"]
)

print("\n----- MODEL ARCHITECTURE -----")
model.summary()

# -------------------------------
# 8. CALLBACKS
# -------------------------------

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

# -------------------------------
# 9. TRAIN MODEL
# -------------------------------

AUTOTUNE = tf.data.AUTOTUNE

train_data = train_data.prefetch(AUTOTUNE)
val_data = val_data.prefetch(AUTOTUNE)

history = model.fit(
    train_data,
    validation_data=val_data,
    epochs=EPOCHS,
    class_weight=class_weights,
    callbacks=[early_stop, reduce_lr, checkpoint]
)

# -------------------------------
# 10. SAVE FINAL MODEL
# -------------------------------

model.save("model.keras")

print("\nTraining Completed Successfully!")
print("Model saved as model.keras")
print("Categories saved in classes.txt")
