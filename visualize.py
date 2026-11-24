
import tensorflow as tf
import numpy as np
import matplotlib.pyplot as plt
import os

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

# 5. Get actual labels

actual_labels = np.concatenate([
    labels.numpy() for images, labels in test_data
])

# 6. Predict images

predictions = model.predict(test_data)

predicted_labels = np.argmax(predictions, axis=1)

confidence = np.max(predictions, axis=1) * 100

# 7. Display images (Samples from every category)

# Select up to 2 images from each class for a balanced view
selected_indices = []
for class_idx in range(len(class_names)):
    indices = np.where(actual_labels == class_idx)[0]
    if len(indices) > 0:
        selected_indices.extend(indices[:2])

cols = 4
rows = int(np.ceil(len(selected_indices) / cols))

plt.figure(figsize=(14, 3.5 * rows))

for plot_idx, i in enumerate(selected_indices):

    image_path = test_data.file_paths[i]

    img = tf.keras.utils.load_img(
        image_path,
        target_size=(IMG_SIZE, IMG_SIZE)
    )

    actual = class_names[actual_labels[i]]
    predicted = class_names[predicted_labels[i]]

    if actual == predicted:
        color = "green"
    else:
        color = "red"

    plt.subplot(rows, cols, plot_idx + 1)

    plt.imshow(img)

    plt.title(
        f"Actual: {actual}\n"
        f"Predicted: {predicted}\n"
        f"Conf: {confidence[i]:.2f}%",
        color=color,
        fontsize=9,
        pad=6
    )

    plt.axis("off")

plt.tight_layout()

# 8. Save report

os.makedirs("results", exist_ok=True)

plt.savefig("results/visual_report.png")

print("Visual report saved successfully!")

# 9. Display report

plt.show()
