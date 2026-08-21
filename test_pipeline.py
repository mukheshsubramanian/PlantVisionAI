import sys
import os
from pathlib import Path
import numpy as np
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parent / "backend"))
from model_service import get_model_service, ModelService

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    except Exception:
        pass

svc = get_model_service()
print(f"Model loaded: {svc.model is not None}, num_classes: {svc.num_classes}")

expected_mappings = {
    "apple_scab.jpg": "Apple_Scab",
    "corn_common_rust.jpg": "Corn_Common_Rust",
    "corn_northern_blight.jpg": "Corn_Northern_Leaf_Blight",
    "grape_black_rot.jpg": "Grape_Black_Rot",
    "pepper_bacterial_spot.jpg": "Pepper_Bell_Bacterial_Spot",
    "potato_early_blight.jpg": "Potato_Early_Blight",
    "potato_late_blight.jpg": "Potato_Late_Blight",
    "tomato_early_blight.jpg": "Tomato_Early_Blight",
    "tomato_healthy.jpg": "Tomato_Healthy",
    "tomato_late_blight.jpg": "Tomato_Late_Blight",
}

samples_dir = Path(__file__).resolve().parent / "samples"
correct = 0
total = len(expected_mappings)

print("\n--- Testing Model Predictions ---")
for filename, expected_cls in expected_mappings.items():
    img_path = samples_dir / filename
    if not img_path.exists():
        print(f"Missing {filename}")
        continue
    img = Image.open(img_path)
    res = svc.predict(img)
    pred_id = res["disease_id"]
    is_match = (pred_id == expected_cls)
    if is_match:
        correct += 1
        status = "✅ PASS"
    else:
        status = f"❌ FAIL (expected {expected_cls})"
    print(f"{filename:<28} -> {res['disease']:<32} | {res['confidence_percentage']:<6} | {status}")

print(f"\nAccuracy: {correct}/{total} ({correct/total*100:.1f}%)")
