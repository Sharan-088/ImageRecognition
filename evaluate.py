
import tensorflow as tf
import numpy as np

from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

# 1. Basic settings

IMG_SIZE = 224
BATCH_SIZE = 16

# 2. Load trained model

model = tf.keras.models.load_model("model.keras")

# 3. Load category names

with open("classes.txt", "r") as f:
    class_names = f.read().splitlines()

# 4. Load testing images

test_data = tf.keras.utils.image_dataset_from_directory(
    "testing images",
    image_size=(IMG_SIZE, IMG_SIZE),
    batch_size=BATCH_SIZE,
    shuffle=False
)

# 5. Check category order

print("Model Categories:", class_names)
print("Testing Categories:", test_data.class_names)

if test_data.class_names != class_names:
    raise ValueError("Category order does not match!")

# 6. Predict testing images

predictions = model.predict(test_data)

predicted_labels = np.argmax(predictions, axis=1)

actual_labels = np.concatenate([
    labels.numpy() for images, labels in test_data
])

# 7. Calculate accuracy

accuracy = np.mean(predicted_labels == actual_labels)

print("\n----- TEST RESULTS -----")
print("Total Images:", len(actual_labels))
print("Correct Predictions:", np.sum(predicted_labels == actual_labels))
print("Wrong Predictions:", np.sum(predicted_labels != actual_labels))
print("Testing Accuracy:", round(accuracy * 100, 2), "%")

# 8. Classification report

print("\n----- CLASSIFICATION REPORT -----")

print(classification_report(
    actual_labels,
    predicted_labels,
    labels=list(range(len(class_names))),
    target_names=class_names,
    zero_division=0
))

# 9. Confusion matrix

print("\n----- CONFUSION MATRIX -----")

print(confusion_matrix(
    actual_labels,
    predicted_labels,
    labels=list(range(len(class_names)))
))
