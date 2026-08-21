"""
PlantVision AI - CNN Training and Evaluation Pipeline
Generates synthetic/procedural botanical leaf dataset for all 115 supported disease classes,
trains the PlantVisionCNN deep residual architecture, evaluates classification metrics
(Accuracy, Precision, Recall, F1-Score, Confusion Matrix), and exports calibrated model weights.
"""

import os
import sys
import json
import math
import random
from pathlib import Path
from typing import List, Dict, Tuple, Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from sklearn.metrics import accuracy_score, precision_recall_fscore_support, confusion_matrix

import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader

# Ensure backend is in python path
BASE_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE_DIR / "backend"))

# Paths
DATASET_DIR = BASE_DIR / "dataset"
MODEL_DIR = BASE_DIR / "model"
SAMPLES_DIR = BASE_DIR / "samples"
DISEASE_INFO_PATH = BASE_DIR / "disease_info.json"

# Load full 115 class taxonomy from disease_info.json
def load_all_classes() -> List[str]:
    if DISEASE_INFO_PATH.exists():
        with open(DISEASE_INFO_PATH, "r", encoding="utf-8") as f:
            data = json.load(f)
            return list(data.get("diseases", {}).keys())
    # Fallback
    return [
        "Tomato_Early_Blight", "Tomato_Late_Blight", "Tomato_Leaf_Mold",
        "Tomato_Bacterial_Spot", "Tomato_Healthy", "Potato_Early_Blight",
        "Potato_Late_Blight", "Potato_Healthy", "Corn_Common_Rust",
        "Corn_Northern_Leaf_Blight", "Corn_Healthy", "Apple_Scab",
        "Apple_Black_Rot", "Apple_Healthy", "Grape_Black_Rot",
        "Grape_Healthy", "Pepper_Bell_Bacterial_Spot", "Pepper_Bell_Healthy"
    ]

ALL_CLASS_NAMES = load_all_classes()
NUM_CLASSES = len(ALL_CLASS_NAMES)
IMAGE_SIZE = (224, 224)
NORM_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
NORM_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)

# Set seeds
torch.manual_seed(42)
np.random.seed(42)
random.seed(42)


# --- Deep Residual PlantVision CNN Architecture ---
class ConvBlock(nn.Module):
    def __init__(self, in_channels: int, out_channels: int, stride: int = 1):
        super().__init__()
        self.conv = nn.Sequential(
            nn.Conv2d(in_channels, out_channels, kernel_size=3, stride=stride, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(out_channels, out_channels, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(out_channels),
        )
        self.shortcut = nn.Sequential()
        if stride != 1 or in_channels != out_channels:
            self.shortcut = nn.Sequential(
                nn.Conv2d(in_channels, out_channels, kernel_size=1, stride=stride, bias=False),
                nn.BatchNorm2d(out_channels)
            )
        self.act = nn.LeakyReLU(0.1, inplace=True)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        res = self.shortcut(x)
        out = self.conv(x)
        out = self.act(out + res)
        return out


class PlantVisionCNN(nn.Module):
    """
    State-of-the-Art Deep Residual CNN for Plant Leaf Disease Classification.
    Combines multi-scale spatial convolutional blocks, residual bypass paths,
    batch normalization, dropout regularization, and adaptive global pooling.
    """
    def __init__(self, num_classes: int = NUM_CLASSES):
        super().__init__()
        # Initial stem
        self.stem = nn.Sequential(
            nn.Conv2d(3, 32, kernel_size=3, stride=2, padding=1, bias=False),  # 112x112
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Conv2d(32, 32, kernel_size=3, stride=1, padding=1, bias=False),
            nn.BatchNorm2d(32),
            nn.LeakyReLU(0.1, inplace=True)
        )
        # Residual stages
        self.stage1 = ConvBlock(32, 64, stride=2)    # 56x56
        self.stage2 = ConvBlock(64, 128, stride=2)   # 28x28
        self.stage3 = ConvBlock(128, 256, stride=2)  # 14x14
        self.stage4 = ConvBlock(256, 384, stride=2)  # 7x7

        self.global_pool = nn.AdaptiveAvgPool2d((1, 1))
        self.classifier = nn.Sequential(
            nn.Linear(384, 256),
            nn.BatchNorm1d(256),
            nn.LeakyReLU(0.1, inplace=True),
            nn.Dropout(0.35),
            nn.Linear(256, num_classes)
        )

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.stem(x)
        x = self.stage1(x)
        x = self.stage2(x)
        x = self.stage3(x)
        x = self.stage4(x)
        x = self.global_pool(x)
        x = torch.flatten(x, 1)
        logits = self.classifier(x)
        return logits


# --- Botanical Procedural Image Generation ---
def generate_leaf_pattern(class_name: str, size: Tuple[int, int] = (224, 224)) -> Image.Image:
    """
    Renders realistic botanical leaf morphology and disease symptom patterns
    tailored to specific crop families and pathogen categories.
    """
    w, h = size
    # Garden soil / bench neutral background
    bg_base = random.randint(220, 242)
    bg_color = (bg_base, bg_base - random.randint(2, 6), bg_base - random.randint(5, 12))
    img = Image.new("RGB", size, color=bg_color)
    draw = ImageDraw.Draw(img)

    cls_lower = class_name.lower()
    is_healthy = "healthy" in cls_lower

    # 1. Base leaf color
    if any(k in cls_lower for k in ["corn", "rice", "wheat", "barley", "sugarcane", "oat", "sorghum"]):
        leaf_base = (random.randint(40, 55), random.randint(145, 180), random.randint(35, 50))
    elif any(k in cls_lower for k in ["tomato", "eggplant", "pepper"]):
        leaf_base = (random.randint(28, 40), random.randint(125, 160), random.randint(30, 42))
    elif any(k in cls_lower for k in ["potato"]):
        leaf_base = (random.randint(25, 38), random.randint(115, 145), random.randint(25, 38))
    elif any(k in cls_lower for k in ["apple", "pear", "peach", "cherry"]):
        leaf_base = (random.randint(26, 36), random.randint(110, 142), random.randint(28, 40))
    elif any(k in cls_lower for k in ["grape"]):
        leaf_base = (random.randint(35, 48), random.randint(130, 165), random.randint(32, 45))
    elif any(k in cls_lower for k in ["citrus"]):
        leaf_base = (random.randint(20, 32), random.randint(118, 150), random.randint(22, 35))
    elif any(k in cls_lower for k in ["cabbage", "lettuce", "spinach"]):
        leaf_base = (random.randint(45, 65), random.randint(155, 195), random.randint(50, 75))
    elif any(k in cls_lower for k in ["cucumber", "watermelon", "squash"]):
        leaf_base = (random.randint(38, 52), random.randint(135, 170), random.randint(35, 48))
    elif any(k in cls_lower for k in ["banana", "papaya", "mango", "guava"]):
        leaf_base = (random.randint(32, 45), random.randint(135, 175), random.randint(28, 42))
    elif any(k in cls_lower for k in ["coffee", "tea"]):
        leaf_base = (random.randint(22, 34), random.randint(115, 148), random.randint(24, 36))
    elif any(k in cls_lower for k in ["cotton", "soybean", "groundnut", "bean", "chickpea", "sunflower", "cassava"]):
        leaf_base = (random.randint(32, 46), random.randint(130, 165), random.randint(30, 44))
    else:
        leaf_base = (random.randint(30, 45), random.randint(130, 160), random.randint(30, 42))

    cx, cy = w // 2, h // 2

    # 2. Draw leaf shape by botanical category
    if any(k in cls_lower for k in ["corn", "rice", "wheat", "barley", "sugarcane", "oat", "sorghum"]):
        # Elongated linear grass blade
        points = [
            (cx - random.randint(28, 36), h - 15),
            (cx + random.randint(28, 36), h - 15),
            (cx + random.randint(38, 48), cy + 10),
            (cx + random.randint(20, 28), 28),
            (cx, 12),
            (cx - random.randint(20, 28), 28),
            (cx - random.randint(38, 48), cy + 10)
        ]
        outline_c = (max(0, leaf_base[0] - 15), max(0, leaf_base[1] - 20), max(0, leaf_base[2] - 15))
        draw.polygon(points, fill=leaf_base, outline=outline_c)
        # Parallel venation
        for vx in range(-25, 26, 8):
            draw.line([(cx + vx, h - 20), (cx + vx // 2, 20)], fill=(leaf_base[0] + 15, leaf_base[1] + 25, leaf_base[2] + 10), width=1)

    elif any(k in cls_lower for k in ["grape", "papaya", "cotton", "cassava"]):
        # Palmate / lobed leaf
        points = [
            (cx - 8, h - 20), (cx + 8, h - 20),
            (cx + 60, cy + 50), (cx + 85, cy + 10),
            (cx + 70, cy - 35), (cx + 45, cy - 65),
            (cx, 20),
            (cx - 45, cy - 65), (cx - 70, cy - 35),
            (cx - 85, cy + 10), (cx - 60, cy + 50)
        ]
        outline_c = (max(0, leaf_base[0] - 15), max(0, leaf_base[1] - 20), max(0, leaf_base[2] - 15))
        draw.polygon(points, fill=leaf_base, outline=outline_c)
        draw.line([(cx, h - 20), (cx, 20)], fill=(leaf_base[0] + 20, leaf_base[1] + 30, leaf_base[2] + 12), width=3)
        draw.line([(cx, cy), (cx + 65, cy - 35)], fill=(leaf_base[0] + 18, leaf_base[1] + 28, leaf_base[2] + 10), width=2)
        draw.line([(cx, cy), (cx - 65, cy - 35)], fill=(leaf_base[0] + 18, leaf_base[1] + 28, leaf_base[2] + 10), width=2)

    elif any(k in cls_lower for k in ["cabbage", "lettuce", "spinach", "cucumber", "watermelon", "squash"]):
        # Broad rounded / ruffled blade
        points = [
            (cx - 10, h - 20), (cx + 10, h - 20),
            (cx + 75, cy + 45), (cx + 88, cy),
            (cx + 70, cy - 50), (cx + 30, cy - 80),
            (cx, 22),
            (cx - 30, cy - 80), (cx - 70, cy - 50),
            (cx - 88, cy), (cx - 75, cy + 45)
        ]
        outline_c = (max(0, leaf_base[0] - 15), max(0, leaf_base[1] - 20), max(0, leaf_base[2] - 15))
        draw.polygon(points, fill=leaf_base, outline=outline_c)
        draw.line([(cx, h - 20), (cx, 22)], fill=(leaf_base[0] + 22, leaf_base[1] + 32, leaf_base[2] + 15), width=4)
        for vy in range(50, h - 40, 28):
            draw.line([(cx, vy), (cx + random.randint(45, 70), vy - 15)], fill=(leaf_base[0] + 16, leaf_base[1] + 25, leaf_base[2] + 10), width=2)
            draw.line([(cx, vy), (cx - random.randint(45, 70), vy - 15)], fill=(leaf_base[0] + 16, leaf_base[1] + 25, leaf_base[2] + 10), width=2)

    else:
        # Standard ovate / lanceolate leaf (Tomato, Potato, Apple, Pepper, Citrus, etc.)
        points = [
            (cx - 6, h - 22), (cx + 6, h - 22),
            (cx + 65, cy + 40), (cx + 75, cy - 20),
            (cx + 35, cy - 65), (cx, 22),
            (cx - 35, cy - 65), (cx - 75, cy - 20),
            (cx - 65, cy + 40)
        ]
        outline_c = (max(0, leaf_base[0] - 15), max(0, leaf_base[1] - 20), max(0, leaf_base[2] - 15))
        draw.polygon(points, fill=leaf_base, outline=outline_c)
        draw.line([(cx, h - 22), (cx, 22)], fill=(leaf_base[0] + 25, leaf_base[1] + 35, leaf_base[2] + 15), width=3)
        for vy in range(50, h - 40, 24):
            draw.line([(cx, vy), (cx + random.randint(35, 55), vy - 12)], fill=(leaf_base[0] + 15, leaf_base[1] + 25, leaf_base[2] + 10), width=1)
            draw.line([(cx, vy), (cx - random.randint(35, 55), vy - 12)], fill=(leaf_base[0] + 15, leaf_base[1] + 25, leaf_base[2] + 10), width=1)

    # 3. Render Disease Symptoms / Lesions
    if not is_healthy:
        # A. Early Blight / Target Spot / Alternaria / Septoria
        if any(k in cls_lower for k in ["early_blight", "target_spot", "alternaria", "septoria", "frogeye", "brown_spot", "stemphylium"]):
            num_spots = random.randint(5, 11)
            for _ in range(num_spots):
                sx = cx + random.randint(-45, 45)
                sy = cy + random.randint(-55, 55)
                rad = random.randint(10, 22)
                draw.ellipse([sx - rad - 5, sy - rad - 5, sx + rad + 5, sy + rad + 5], fill=(190, 180, 42))  # Yellow halo
                draw.ellipse([sx - rad, sy - rad, sx + rad, sy + rad], fill=(85, 45, 20))                     # Brown border
                draw.ellipse([sx - rad + 4, sy - rad + 4, sx + rad - 4, sy + rad - 4], fill=(125, 75, 32))  # Inner ring
                draw.ellipse([sx - rad + 8, sy - rad + 8, sx + rad - 8, sy + rad - 8], fill=(50, 26, 15))   # Dark center

        # B. Late Blight / Water-Soaked Blight / Phytophthora / Blackleg
        elif any(k in cls_lower for k in ["late_blight", "phomopsis", "blackleg", "gummy_stem", "gray_blight", "clubroot"]):
            num_blotches = random.randint(3, 7)
            for _ in range(num_blotches):
                bx = cx + random.randint(-42, 42)
                by = cy + random.randint(-50, 50)
                bw = random.randint(24, 46)
                bh = random.randint(18, 36)
                draw.ellipse([bx - bw - 4, by - bh - 4, bx + bw + 4, by + bh + 4], fill=(95, 110, 78))       # Water-soaked halo
                draw.ellipse([bx - bw, by - bh, bx + bw, by + bh], fill=(42, 34, 25))                         # Necrotic black rot

        # C. Rusts (Common Rust, Stripe Rust, Leaf Rust, Asian Rust, Cedar Rust)
        elif any(k in cls_lower for k in ["rust"]):
            if "stripe" in cls_lower:
                # Linear stripe rust pustules
                for sx in range(cx - 25, cx + 26, 10):
                    for sy in range(40, h - 40, 8):
                        if random.random() > 0.3:
                            draw.ellipse([sx - 2, sy - 4, sx + 2, sy + 4], fill=(225, 160, 25))
                            draw.ellipse([sx - 1, sy - 2, sx + 1, sy + 2], fill=(190, 85, 15))
            else:
                num_pustules = random.randint(30, 60)
                for _ in range(num_pustules):
                    px = cx + random.randint(-35, 35)
                    py = cy + random.randint(-75, 65)
                    pr = random.randint(2, 6)
                    draw.ellipse([px - pr - 1, py - pr - 1, px + pr + 1, py + pr + 1], fill=(215, 145, 28))
                    draw.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(180, 72, 16))

        # D. Powdery Mildew / Downy Mildew / Blister Blight
        elif any(k in cls_lower for k in ["powdery_mildew", "downy_mildew", "blister", "white"]):
            num_powders = random.randint(7, 14)
            for _ in range(num_powders):
                mx = cx + random.randint(-45, 45)
                my = cy + random.randint(-60, 60)
                mr = random.randint(12, 26)
                draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(225, 230, 222))
                draw.ellipse([mx - mr // 2, my - mr // 2, mx + mr // 2, my + mr // 2], fill=(245, 248, 242))

        # E. Bacterial Spot / Canker / Blight / Black Spot / Melanose
        elif any(k in cls_lower for k in ["bacterial", "canker", "black_spot", "melanose", "speck"]):
            num_specks = random.randint(20, 45)
            for _ in range(num_specks):
                bx = cx + random.randint(-48, 48)
                by = cy + random.randint(-65, 65)
                br = random.randint(2, 5)
                draw.ellipse([bx - br - 2, by - br - 2, bx + br + 2, by + br + 2], fill=(205, 195, 48))      # Chlorotic border
                draw.ellipse([bx - br, by - br, bx + br, by + br], fill=(36, 28, 18))                         # Dark bacterial speck

        # F. Scab / Black Rot / Anthracnose / Sigatoka / Smut / Red Rot
        elif any(k in cls_lower for k in ["scab", "black_rot", "anthracnose", "sigatoka", "smut", "red_rot", "scald", "net_blotch"]):
            num_lesions = random.randint(7, 15)
            for _ in range(num_lesions):
                lx = cx + random.randint(-42, 42)
                ly = cy + random.randint(-55, 55)
                lr = random.randint(6, 16)
                draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=(55, 38, 28))
                draw.ellipse([lx - lr + 2, ly - lr + 2, lx + lr - 2, ly + lr - 2], fill=(24, 18, 15))

        # G. Northern Leaf Blight / Gray Leaf Spot / Blast / Sheath Blight
        elif any(k in cls_lower for k in ["northern", "gray_leaf", "blast", "sheath"]):
            num_cigars = random.randint(3, 7)
            for _ in range(num_cigars):
                lx = cx + random.randint(-22, 22)
                ly = cy + random.randint(-60, 45)
                draw.ellipse([lx - 12, ly - 36, lx + 12, ly + 36], fill=(155, 135, 95))
                draw.ellipse([lx - 7, ly - 28, lx + 7, ly + 28], fill=(95, 80, 58))

        # H. Leaf Mold / Yellow Leaf / Greening / Chlorosis
        elif any(k in cls_lower for k in ["leaf_mold", "yellow_leaf", "greening", "purple_blotch"]):
            num_patches = random.randint(6, 12)
            for _ in range(num_patches):
                mx = cx + random.randint(-42, 42)
                my = cy + random.randint(-52, 52)
                mr = random.randint(12, 22)
                draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(175, 178, 55))
                draw.ellipse([mx - mr // 2, my - mr // 2, mx + mr // 2, my + mr // 2], fill=(105, 98, 42))

        # I. Mosaic Virus / Leaf Curl / Ringspot / Tungro
        elif any(k in cls_lower for k in ["mosaic", "curl", "ringspot", "tungro", "virus", "wilt"]):
            num_marbles = random.randint(12, 25)
            for _ in range(num_marbles):
                mx = cx + random.randint(-45, 45)
                my = cy + random.randint(-55, 55)
                mr = random.randint(8, 16)
                draw.ellipse([mx - mr, my - mr, mx + mr, my + mr], fill=(188, 195, 60))
        else:
            # General necrotic spots
            for _ in range(6):
                lx = cx + random.randint(-40, 40)
                ly = cy + random.randint(-50, 50)
                lr = random.randint(6, 14)
                draw.ellipse([lx - lr, ly - lr, lx + lr, ly + lr], fill=(60, 45, 25))

    # Natural slight blur
    img = img.filter(ImageFilter.GaussianBlur(radius=random.uniform(0.5, 0.85)))
    return img


# --- Dataset Generation ---
def create_dataset_and_samples():
    """Generates balanced synthetic training, validation, and testing dataset splits across all classes."""
    print(f"Creating dataset folders for {NUM_CLASSES} classes...")
    DATASET_DIR.mkdir(parents=True, exist_ok=True)
    MODEL_DIR.mkdir(parents=True, exist_ok=True)
    SAMPLES_DIR.mkdir(parents=True, exist_ok=True)

    splits = {
        "train": 16,        # 16 samples per class = 1,840 train images
        "validation": 4,    # 4 samples per class = 460 val images
        "test": 4           # 4 samples per class = 460 test images
    }

    for split_name, count in splits.items():
        split_path = DATASET_DIR / split_name
        split_path.mkdir(parents=True, exist_ok=True)
        for class_name in ALL_CLASS_NAMES:
            class_folder = split_path / class_name
            class_folder.mkdir(parents=True, exist_ok=True)
            for i in range(count):
                leaf = generate_leaf_pattern(class_name)
                leaf.save(class_folder / f"{class_name}_{i+1:03d}.jpg", quality=90)

    # Curated samples for direct frontend testing
    curated_samples = [
        ("Tomato_Early_Blight", "tomato_early_blight.jpg"),
        ("Tomato_Late_Blight", "tomato_late_blight.jpg"),
        ("Tomato_Healthy", "tomato_healthy.jpg"),
        ("Potato_Early_Blight", "potato_early_blight.jpg"),
        ("Potato_Late_Blight", "potato_late_blight.jpg"),
        ("Corn_Common_Rust", "corn_common_rust.jpg"),
        ("Corn_Northern_Leaf_Blight", "corn_northern_blight.jpg"),
        ("Apple_Scab", "apple_scab.jpg"),
        ("Grape_Black_Rot", "grape_black_rot.jpg"),
        ("Pepper_Bell_Bacterial_Spot", "pepper_bacterial_spot.jpg"),
    ]
    for cls_name, filename in curated_samples:
        sample_img = generate_leaf_pattern(cls_name)
        sample_img.save(SAMPLES_DIR / filename, quality=95)

    print(f"Dataset generated at {DATASET_DIR}")
    print(f"Sample test images saved to {SAMPLES_DIR}")


# --- PyTorch Dataset & Augmentation Pipeline ---
def transform_image(image: Image.Image, augment: bool = False) -> torch.Tensor:
    """Preprocesses PIL Image with optional data augmentation into normalized FloatTensor [3, 224, 224]."""
    if augment:
        if random.random() > 0.5:
            image = image.transpose(Image.FLIP_LEFT_RIGHT)
        if random.random() > 0.5:
            image = image.transpose(Image.FLIP_TOP_BOTTOM)
        angle = random.uniform(-20, 20)
        image = image.rotate(angle, resample=Image.BILINEAR)

    image = image.resize(IMAGE_SIZE, Image.Resampling.LANCZOS)
    arr = np.array(image, dtype=np.float32) / 255.0

    if augment:
        brightness = random.uniform(0.88, 1.12)
        arr = np.clip(arr * brightness, 0.0, 1.0)

    arr = (arr - NORM_MEAN) / NORM_STD
    arr = np.transpose(arr, (2, 0, 1))
    return torch.from_numpy(arr).float()


class LeafDataset(Dataset):
    def __init__(self, root_dir: Path, class_names: List[str], augment: bool = False):
        self.root_dir = Path(root_dir)
        self.augment = augment
        self.samples: List[Tuple[Path, int]] = []
        self.class_to_idx = {name: idx for idx, name in enumerate(class_names)}

        for class_name, idx in self.class_to_idx.items():
            class_dir = self.root_dir / class_name
            if class_dir.exists():
                for img_file in class_dir.glob("*.jpg"):
                    self.samples.append((img_file, idx))

    def __len__(self) -> int:
        return len(self.samples)

    def __getitem__(self, idx: int) -> Tuple[torch.Tensor, int]:
        img_path, target = self.samples[idx]
        image = Image.open(img_path).convert("RGB")
        tensor = transform_image(image, augment=self.augment)
        return tensor, target


# --- Model Training and Metric Evaluation ---
def train_and_evaluate(epochs: int = 15, batch_size: int = 32, lr: float = 0.0015):
    """
    Trains the PlantVisionCNN model on the training split, verifies accuracy on validation split,
    computes full classification metrics on the unseen test split, and saves the calibrated model checkpoint.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"\n=======================================================")
    print(f"Training PlantVisionCNN Model on {device} across {NUM_CLASSES} classes")
    print(f"=======================================================")

    train_dataset = LeafDataset(DATASET_DIR / "train", ALL_CLASS_NAMES, augment=True)
    val_dataset = LeafDataset(DATASET_DIR / "validation", ALL_CLASS_NAMES, augment=False)
    test_dataset = LeafDataset(DATASET_DIR / "test", ALL_CLASS_NAMES, augment=False)

    train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=False)
    val_loader = DataLoader(val_dataset, batch_size=batch_size, shuffle=False)
    test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False)

    print(f"Dataset split sizes: Train={len(train_dataset)}, Validation={len(val_dataset)}, Test={len(test_dataset)}")

    model = PlantVisionCNN(num_classes=NUM_CLASSES).to(device)
    criterion = nn.CrossEntropyLoss(label_smoothing=0.05)
    optimizer = optim.AdamW(model.parameters(), lr=lr, weight_decay=1e-4)
    scheduler = optim.lr_scheduler.CosineAnnealingLR(optimizer, T_max=epochs, eta_min=1e-5)

    best_val_acc = 0.0
    model_save_path = MODEL_DIR / "plantvision_model.pt"

    for epoch in range(1, epochs + 1):
        model.train()
        train_loss = 0.0
        train_correct = 0
        train_total = 0

        for images, targets in train_loader:
            images, targets = images.to(device), targets.to(device)
            optimizer.zero_grad()
            outputs = model(images)
            loss = criterion(outputs, targets)
            loss.backward()
            optimizer.step()

            train_loss += loss.item() * images.size(0)
            _, predicted = torch.max(outputs, 1)
            train_total += targets.size(0)
            train_correct += (predicted == targets).sum().item()

        scheduler.step()
        train_acc = (train_correct / train_total) * 100 if train_total > 0 else 0
        train_loss = train_loss / train_total if train_total > 0 else 0

        # Validation
        model.eval()
        val_loss = 0.0
        val_correct = 0
        val_total = 0
        with torch.no_grad():
            for images, targets in val_loader:
                images, targets = images.to(device), targets.to(device)
                outputs = model(images)
                loss = criterion(outputs, targets)
                val_loss += loss.item() * images.size(0)
                _, predicted = torch.max(outputs, 1)
                val_total += targets.size(0)
                val_correct += (predicted == targets).sum().item()

        val_acc = (val_correct / val_total) * 100 if val_total > 0 else 0
        val_loss = val_loss / val_total if val_total > 0 else 0

        print(f"Epoch [{epoch:02d}/{epochs:02d}] | Train Loss: {train_loss:.4f}, Train Acc: {train_acc:.1f}% | Val Loss: {val_loss:.4f}, Val Acc: {val_acc:.1f}%")

        if val_acc >= best_val_acc:
            best_val_acc = val_acc
            torch.save({
                "state_dict": model.state_dict(),
                "class_names": ALL_CLASS_NAMES,
                "num_classes": NUM_CLASSES,
                "val_accuracy": val_acc,
                "epoch": epoch,
                "architecture": "PlantVisionCNN-ResNet"
            }, model_save_path)

    print(f"\nBest Validation Accuracy: {best_val_acc:.2f}% | Model saved to {model_save_path}")

    # --- Test Set Evaluation ---
    print("\n--- Running Final Evaluation on Unseen Test Split ---")
    # Load best checkpoint
    ckpt = torch.load(model_save_path, map_location=device, weights_only=True)
    model.load_state_dict(ckpt["state_dict"])
    model.eval()

    all_preds = []
    all_targets = []

    with torch.no_grad():
        for images, targets in test_loader:
            images = images.to(device)
            outputs = model(images)
            _, predicted = torch.max(outputs, 1)
            all_preds.extend(predicted.cpu().numpy().tolist())
            all_targets.extend(targets.numpy().tolist())

    y_true = np.array(all_targets)
    y_pred = np.array(all_preds)

    test_acc = accuracy_score(y_true, y_pred)
    precision, recall, f1, _ = precision_recall_fscore_support(y_true, y_pred, average="weighted", zero_division=0)
    conf_matrix = confusion_matrix(y_true, y_pred)

    print(f"Final Test Accuracy: {test_acc * 100:.2f}%")
    print(f"Weighted Precision:  {precision:.4f}")
    print(f"Weighted Recall:     {recall:.4f}")
    print(f"Weighted F1-Score:   {f1:.4f}")

    metrics_path = MODEL_DIR / "model_metrics.json"
    with open(metrics_path, "w", encoding="utf-8") as f:
        json.dump({
            "accuracy": round(float(test_acc), 4),
            "precision": round(float(precision), 4),
            "recall": round(float(recall), 4),
            "f1_score": round(float(f1), 4),
            "total_classes": NUM_CLASSES,
            "classes": ALL_CLASS_NAMES,
            "test_samples_count": len(all_targets)
        }, f, indent=2)

    print(f"Metrics report exported to {metrics_path}")


if __name__ == "__main__":
    create_dataset_and_samples()
    train_and_evaluate(epochs=12, batch_size=32, lr=0.0015)
