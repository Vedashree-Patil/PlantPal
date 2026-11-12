
import os
from PIL import Image

dataset_path = r"D:\PlantPal\cleaned_dataset"

total_images = 0
total_classes = 0
invalid_images = 0

for disease in os.listdir(dataset_path):
    folder = os.path.join(dataset_path, disease)

    if not os.path.isdir(folder):
        continue

    total_classes += 1
    count = 0

    for filename in os.listdir(folder):
        path = os.path.join(folder, filename)

        try:
            with Image.open(path) as img:
                img.verify()
            count += 1
            total_images += 1
        except Exception:
            invalid_images += 1

    print(disease, ":", count, "valid images")

print("\n--- VERIFICATION SUMMARY ---")
print("Total classes:", total_classes)
print("Total valid images:", total_images)
print("Invalid images:", invalid_images)
