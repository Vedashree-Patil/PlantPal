
from pathlib import Path
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

# 1. Set project paths
PROJECT_DIR = Path(r"D:\PlantPal")
DATASET_DIR = PROJECT_DIR / "cleaned_dataset"
REPORT_DIR = PROJECT_DIR / "plantpal_research"

REPORT_DIR.mkdir(parents=True, exist_ok=True)

# Image file formats to recognize
IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

if not DATASET_DIR.exists():
    raise FileNotFoundError(
        f"Dataset folder not found: {DATASET_DIR}"
    )

# 2. Explore the dataset class by class
records = []
unreadable_images = []

for class_folder in sorted(DATASET_DIR.iterdir()):
    if not class_folder.is_dir():
        continue

    image_paths = [
        p for p in class_folder.rglob("*")
        if p.is_file() and p.suffix.lower() in IMAGE_EXTENSIONS
    ]

    readable_count = 0

    for image_path in image_paths:
        try:
            with Image.open(image_path) as img:
                img.verify()
            readable_count += 1
        except Exception:
            unreadable_images.append({
                "class": class_folder.name,
                "image_path": str(image_path)
            })

    class_name = class_folder.name
    is_healthy = class_name.lower().endswith("healthy")

    records.append({
        "class_name": class_name,
        "total_images": len(image_paths),
        "readable_images": readable_count,
        "unreadable_images": len(image_paths) - readable_count,
        "condition_type": "Healthy" if is_healthy else "Disease-condition"
    })

# 3. Create class-wise report
df = pd.DataFrame(records)

if df.empty:
    raise ValueError("No class folders were found in cleaned_dataset.")

df = df.sort_values("class_name")
class_csv = REPORT_DIR / "final_class_summary.csv"
df.to_csv(class_csv, index=False)

# 4. Calculate overall statistics
total_classes = len(df)
total_images = int(df["total_images"].sum())
total_readable = int(df["readable_images"].sum())
total_unreadable = int(df["unreadable_images"].sum())

healthy_classes = int((df["condition_type"] == "Healthy").sum())
disease_condition_classes = total_classes - healthy_classes

healthy_images = int(
    df.loc[df["condition_type"] == "Healthy", "total_images"].sum()
)
disease_condition_images = total_images - healthy_images

summary = pd.DataFrame([
    ["Total plant-condition classes", total_classes],
    ["Healthy classes", healthy_classes],
    ["Disease-condition classes", disease_condition_classes],
    ["Total images", total_images],
    ["Images in healthy classes", healthy_images],
    ["Images in disease-condition classes", disease_condition_images],
    ["Readable images", total_readable],
    ["Unreadable images", total_unreadable]
], columns=["Metric", "Value"])

summary_csv = REPORT_DIR / "dataset_summary.csv"
summary.to_csv(summary_csv, index=False)

# 5. Save unreadable-image report
unreadable_csv = REPORT_DIR / "unreadable_images_final.csv"
pd.DataFrame(
    unreadable_images,
    columns=["class", "image_path"]
).to_csv(unreadable_csv, index=False)

# 6. Visualize image counts for every class
plt.figure(figsize=(12, 12))
plt.barh(df["class_name"], df["total_images"])
plt.xlabel("Number of images")
plt.ylabel("Plant-condition class")
plt.title("PlantPal: Image Distribution Across Classes")
plt.tight_layout()

chart_path = REPORT_DIR / "final_class_distribution.png"
plt.savefig(chart_path, dpi=300, bbox_inches="tight")
plt.close()

# 7. Visualize healthy vs disease-condition image counts
category_counts = pd.DataFrame({
    "Category": ["Healthy classes", "Disease-condition classes"],
    "Images": [healthy_images, disease_condition_images]
})

plt.figure(figsize=(8, 5))
plt.bar(category_counts["Category"], category_counts["Images"])
plt.ylabel("Number of images")
plt.title("PlantPal: Healthy vs Disease-Condition Images")
plt.tight_layout()

category_chart = REPORT_DIR / "healthy_vs_disease_images.png"
plt.savefig(category_chart, dpi=300, bbox_inches="tight")
plt.close()

# 8. Print results
print("\n========== PLANTPAL DATASET REPORT ==========")
print(df.to_string(index=False))
print("\n========== OVERALL STATISTICS ==========")
print(summary.to_string(index=False))
print("\nReports saved in:", REPORT_DIR)
print("Class summary:", class_csv)
print("Dataset summary:", summary_csv)
print("Class distribution chart:", chart_path)
print("Healthy vs disease chart:", category_chart)
print("Unreadable-image report:", unreadable_csv)
