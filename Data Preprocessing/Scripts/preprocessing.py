
import os
from PIL import Image
import numpy as np

# Dataset paths
dataset_path = r"D:\raw\color"
output_path = r"D:\PlantPal\preprocessed_data"

# Image size
image_size = (224, 224)

os.makedirs(output_path, exist_ok=True)

total_images = 0

for disease in os.listdir(dataset_path):
    disease_path = os.path.join(dataset_path, disease)

    if not os.path.isdir(disease_path):
        continue

    save_path = os.path.join(output_path, disease)
    os.makedirs(save_path, exist_ok=True)

    count = 0

    for filename in os.listdir(disease_path):
        image_path = os.path.join(disease_path, filename)

        try:
            with Image.open(image_path) as img:
                # Convert image to RGB
                img = img.convert("RGB")

                # Resize image
                img = img.resize(image_size)

                # Save processed image
                img.save(os.path.join(save_path, filename))

                count += 1
                total_images += 1

        except Exception:
            print("Skipped:", image_path)

    print(disease, ":", count, "images processed")

print("\nPreprocessing completed!")
print("Total images processed:", total_images)
print("Processed images saved in:", output_path)
