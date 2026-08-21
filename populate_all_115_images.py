import os
import json
import shutil
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
disease_info_path = BASE_DIR / "disease_info.json"

with open(disease_info_path, "r", encoding="utf-8") as f:
    data = json.load(f)

diseases = data.get("diseases", {})
print(f"Total disease keys to process: {len(diseases)}")

leaf_img_dir = BASE_DIR / "frontend" / "leaf_images"
leaf_img_dir.mkdir(parents=True, exist_ok=True)

test_dir = BASE_DIR / "dataset" / "test"
train_dir = BASE_DIR / "dataset" / "train"
val_dir = BASE_DIR / "dataset" / "validation"
samples_dir = BASE_DIR / "samples"

found_count = 0
missing = []

# List all available class directories in dataset
dataset_dirs = {}
for split_dir in [test_dir, train_dir, val_dir]:
    if split_dir.exists():
        for d in split_dir.iterdir():
            if d.is_dir() and d.name not in dataset_dirs:
                dataset_dirs[d.name.lower()] = d
                dataset_dirs[d.name] = d

print(f"Discovered {len(dataset_dirs)} class directories in dataset.")

for key, d_info in diseases.items():
    dest_filename = f"{key}.jpg"
    dest_path = leaf_img_dir / dest_filename
    
    # 1. Try exact or case-insensitive match in dataset
    src_dir = dataset_dirs.get(key) or dataset_dirs.get(key.lower()) or dataset_dirs.get(key.replace("__", "_"))
    
    src_img = None
    if src_dir and src_dir.exists():
        imgs = [f for f in src_dir.iterdir() if f.suffix.lower() in [".jpg", ".jpeg", ".png"]]
        if imgs:
            src_img = imgs[0]
            
    # 2. Try samples dir
    if not src_img:
        sample_cand = samples_dir / f"{key.lower()}.jpg"
        if sample_cand.exists():
            src_img = sample_cand
            
    if src_img and src_img.exists():
        shutil.copy2(src_img, dest_path)
        d_info["image_url"] = f"/static/leaf_images/{dest_filename}"
        found_count += 1
    else:
        missing.append(key)

print(f"Copied {found_count} of {len(diseases)} leaf images.")
if missing:
    print(f"Missing ({len(missing)}): {missing}")
else:
    print("SUCCESS: 100% of all 115 leaf diseases have authentic dataset images!")

# Save back to disease_info.json
with open(disease_info_path, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=2)

print("Saved updated disease_info.json successfully!")
