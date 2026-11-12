
import os
import hashlib
import shutil

source_path = r"D:\raw\color"
clean_path = r"D:\PlantPal\cleaned_dataset"

os.makedirs(clean_path, exist_ok=True)

for disease in os.listdir(source_path):
    disease_path = os.path.join(source_path, disease)

    if not os.path.isdir(disease_path):
        continue

    output_folder = os.path.join(clean_path, disease)
    os.makedirs(output_folder, exist_ok=True)

    seen = set()
    kept = 0
    removed = 0

    for filename in os.listdir(disease_path):
        image_path = os.path.join(disease_path, filename)

        try:
            with open(image_path, "rb") as file:
                image_hash = hashlib.md5(file.read()).hexdigest()

            if image_hash in seen:
                removed += 1
                continue

            seen.add(image_hash)
            shutil.copy2(
                image_path,
                os.path.join(output_folder, filename)
            )
            kept += 1

        except Exception:
            print("Skipped unreadable file:", image_path)

    print(disease, "| Kept:", kept, "| Duplicates skipped:", removed)

print("\nDuplicate removal completed!")
print("Clean dataset saved at:", clean_path)
