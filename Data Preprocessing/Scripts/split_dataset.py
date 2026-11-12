
import os
import csv
import random

source_path = r"D:\PlantPal\cleaned_dataset"
output_path = r"D:\PlantPal\dataset_splits"

random.seed(42)

valid_extensions = (".jpg", ".jpeg", ".png", ".bmp")

splits = {
    "train": [],
    "validation": [],
    "test": []
}

for class_name in sorted(os.listdir(source_path)):
    class_path = os.path.join(source_path, class_name)

    if not os.path.isdir(class_path):
        continue

    images = [
        f for f in os.listdir(class_path)
        if f.lower().endswith(valid_extensions)
        and os.path.isfile(os.path.join(class_path, f))
    ]

    random.shuffle(images)

    total = len(images)

    if total < 3:
        print(f"Skipping class with fewer than 3 images: {class_name}")
        continue

    train_end = int(total * 0.70)
    val_end = train_end + int(total * 0.15)

    # Ensure all three splits receive images
    train_images = images[:train_end]
    val_images = images[train_end:val_end]
    test_images = images[val_end:]

    if not train_images or not val_images or not test_images:
        print(f"Skipping class with insufficient images: {class_name}")
        continue

    for filename in train_images:
        splits["train"].append(
            [os.path.join(class_name, filename), class_name, "train"]
        )

    for filename in val_images:
        splits["validation"].append(
            [os.path.join(class_name, filename), class_name, "validation"]
        )

    for filename in test_images:
        splits["test"].append(
            [os.path.join(class_name, filename), class_name, "test"]
        )

os.makedirs(output_path, exist_ok=True)

manifest_path = os.path.join(output_path, "split_manifest.csv")

with open(manifest_path, "w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    writer.writerow(["relative_path", "class_name", "split"])

    for split_name, rows in splits.items():
        writer.writerows(rows)

print("\nDataset split completed!")

for split_name, rows in splits.items():
    print(f"{split_name}: {len(rows)} images")

print("Manifest saved to:", manifest_path)
print("Original images have not been copied or changed.")
