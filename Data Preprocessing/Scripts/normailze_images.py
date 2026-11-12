
import os
import numpy as np
from PIL import Image

source_path = r"D:\PlantPal\cleaned_dataset"
output_path = r"D:\PlantPal\normalized_dataset"

os.makedirs(output_path, exist_ok=True)

count = 0
errors = 0

print("Starting image preprocessing...", flush=True)

for class_name in os.listdir(source_path):
    class_path = os.path.join(source_path, class_name)

    if not os.path.isdir(class_path):
        continue

    output_class = os.path.join(output_path, class_name)
    os.makedirs(output_class, exist_ok=True)

    print(f"\nProcessing class: {class_name}", flush=True)

    for filename in os.listdir(class_path):
        image_path = os.path.join(class_path, filename)

        try:
            with Image.open(image_path) as img:
                img = img.convert("RGB")
                img = img.resize((224, 224))
                image_array = np.array(img, dtype=np.float32) / 255.0

                # Save as a PNG image
                saved_image = Image.fromarray(
                    (image_array * 255).astype(np.uint8)
                )

                output_file = os.path.join(
                    output_class,
                    os.path.splitext(filename)[0] + ".png"
                )

                saved_image.save(output_file)
                count += 1

                if count % 100 == 0:
                    print(f"Images processed: {count}", flush=True)

        except Exception as e:
            errors += 1
            print(f"Skipped {image_path}: {e}", flush=True)

print("\nPreprocessing completed!", flush=True)
print("Images processed:", count, flush=True)
print("Images skipped:", errors, flush=True)
print("Saved in:", output_path, flush=True)
