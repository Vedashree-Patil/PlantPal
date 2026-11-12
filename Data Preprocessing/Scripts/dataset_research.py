
import os
import pandas as pd
import matplotlib.pyplot as plt
from PIL import Image

# 1. Set the folder paths
dataset_path = r"D:\raw\color"
output_path = r"D:\PlantPal\plantpal_research"

os.makedirs(output_path, exist_ok=True)

# 2. Check if the dataset folder exists
if not os.path.exists(dataset_path):
    print("Dataset folder not found! Check the path.")
    exit()

# 3. Collect image information
data = []
corrupt_images = []

for disease in os.listdir(dataset_path):
    disease_path = os.path.join(dataset_path, disease)

    if os.path.isdir(disease_path):
        count = 0

        for filename in os.listdir(disease_path):
            image_path = os.path.join(disease_path, filename)

            try:
                with Image.open(image_path) as img:
                    data.append([
                        disease,
                        filename,
                        img.width,
                        img.height,
                        img.format
                    ])
                    count += 1

            except Exception:
                corrupt_images.append(image_path)

        print(disease, ":", count, "images")

# 4. Create a table of image information
df = pd.DataFrame(
    data,
    columns=["Disease", "Filename", "Width", "Height", "Format"]
)

# 5. Display dataset summary
print("\n--- PLANTPAL DATASET SUMMARY ---")
print("Total images:", len(df))
print("Total classes:", df["Disease"].nunique())
print("Unreadable images:", len(corrupt_images))

if not df.empty:
    print("\nImage formats:")
    print(df["Format"].value_counts())

    # 6. Save the reports
    df.to_csv(
        os.path.join(output_path, "image_inventory.csv"),
        index=False
    )

    counts = df["Disease"].value_counts()
    counts.to_csv(
        os.path.join(output_path, "class_distribution.csv")
    )

    # 7. Create a graph showing images per class
    counts.sort_values().plot(kind="barh", figsize=(10, 10))
    plt.title("PlantVillage Dataset - Class Distribution")
    plt.xlabel("Number of Images")
    plt.ylabel("Disease Class")
    plt.tight_layout()

    plt.savefig(
        os.path.join(output_path, "class_distribution.png")
    )
    plt.show()

    print("\nResearch completed successfully!")
    print("Reports saved in:", output_path)

# 8. Save unreadable image names
pd.DataFrame(
    {"Image Path": corrupt_images}
).to_csv(
    os.path.join(output_path, "unreadable_images.csv"),
    index=False
)
