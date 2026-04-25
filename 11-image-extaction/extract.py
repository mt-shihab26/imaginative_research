#!/usr/bin/env python3
"""Extract non-living objects from an image as individual transparent PNGs."""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from ultralytics import YOLO

# COCO class IDs for living things (person + animals) — everything else is non-living
LIVING_CLASS_IDS = {0, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23}

COCO_NAMES = {
    0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane",
    5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic_light",
    10: "fire_hydrant", 11: "stop_sign", 12: "parking_meter", 13: "bench",
    14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep",
    19: "cow", 20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe",
    24: "backpack", 25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase",
    29: "frisbee", 30: "skis", 31: "snowboard", 32: "sports_ball", 33: "kite",
    34: "baseball_bat", 35: "baseball_glove", 36: "skateboard", 37: "surfboard",
    38: "tennis_racket", 39: "bottle", 40: "wine_glass", 41: "cup",
    42: "fork", 43: "knife", 44: "spoon", 45: "bowl", 46: "banana",
    47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli", 51: "carrot",
    52: "hot_dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair",
    57: "couch", 58: "potted_plant", 59: "bed", 60: "dining_table",
    61: "toilet", 62: "tv", 63: "laptop", 64: "mouse", 65: "remote",
    66: "keyboard", 67: "cell_phone", 68: "microwave", 69: "oven",
    70: "toaster", 71: "sink", 72: "refrigerator", 73: "book", 74: "clock",
    75: "vase", 76: "scissors", 77: "teddy_bear", 78: "hair_drier",
    79: "toothbrush",
}


def extract_objects(image_path: str, model_size: str = "m", conf: float = 0.25, output_dir: str | None = None) -> Path:
    image_path = Path(image_path)
    if not image_path.exists():
        sys.exit(f"Error: {image_path} not found")

    out_dir = Path(output_dir) if output_dir else image_path.parent / image_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    model = YOLO(f"yolov8{model_size}-seg.pt")
    results = model(str(image_path), conf=conf, verbose=False)
    result = results[0]

    if result.masks is None:
        print("No segmentation masks detected.")
        return out_dir

    img_bgr = cv2.imread(str(image_path))
    counts: dict[str, int] = {}
    saved = 0

    for idx, (cls_tensor, box, polygon) in enumerate(
        zip(result.boxes.cls, result.boxes.xyxy, result.masks.xy)
    ):
        cls_id = int(cls_tensor.item())
        if cls_id in LIVING_CLASS_IDS:
            continue

        label = COCO_NAMES.get(cls_id, f"class{cls_id}")
        counts[label] = counts.get(label, 0) + 1
        filename = f"{label}_{counts[label]:02d}.png"

        # Build BGRA image with transparency
        img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)

        # Create binary mask from segmentation polygon
        mask = np.zeros(img_bgr.shape[:2], dtype=np.uint8)
        poly_pts = polygon.astype(np.int32)
        cv2.fillPoly(mask, [poly_pts], 255)

        # Zero out alpha channel outside the mask
        img_bgra[:, :, 3] = mask

        # Crop to bounding box
        x1, y1, x2, y2 = box.cpu().numpy().astype(int)
        cropped = img_bgra[y1:y2, x1:x2]

        out_path = out_dir / filename
        cv2.imwrite(str(out_path), cropped)
        print(f"  Saved: {out_path}")
        saved += 1

    print(f"\n{saved} non-living object(s) extracted to: {out_dir}")
    return out_dir


def main():
    parser = argparse.ArgumentParser(description="Extract non-living objects as transparent PNGs using YOLOv8-seg")
    parser.add_argument("image", help="Path to input image")
    parser.add_argument("-m", "--model", default="m", choices=["n", "s", "m", "l", "x"],
                        help="YOLOv8 model size: n=nano, s=small, m=medium, l=large, x=huge (default: m)")
    parser.add_argument("-c", "--conf", type=float, default=0.25,
                        help="Confidence threshold (default: 0.25)")
    parser.add_argument("-o", "--output", default=None,
                        help="Output directory (default: <image_stem>/ next to input)")
    args = parser.parse_args()

    extract_objects(args.image, model_size=args.model, conf=args.conf, output_dir=args.output)


if __name__ == "__main__":
    main()
