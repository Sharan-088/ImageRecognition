
import tensorflow as tf
import numpy as np

# Load trained model
model = tf.keras.models.load_model("model.keras")

# Display model architecture
print("\n----- MODEL ARCHITECTURE -----")
model.summary()

# Load category names
with open("classes.txt", "r") as f:
    class_names = f.read().splitlines()

# Get image path
image_path = input("Enter image path: ")

# Load and resize image
img = tf.keras.utils.load_img(
    image_path,
    target_size=(224, 224)
)

# Convert image into array
img_array = tf.keras.utils.img_to_array(img)
img_array = np.expand_dims(img_array, axis=0)

# Predict image
prediction = model.predict(img_array)

print("\n----- IMAGE RECOGNITION RESULT -----")

for i in range(len(class_names)):
    confidence = prediction[0][i] * 100
    print(class_names[i], ":", round(confidence, 2), "%")

index = np.argmax(prediction[0])

print("\nFinal Prediction:", class_names[index])
