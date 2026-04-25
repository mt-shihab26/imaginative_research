#!/usr/bin/env python3
"""Extract all objects from an image as individual transparent PNGs using SAM2."""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from ultralytics import SAM

# Available SAM2 model sizes (largest = best quality):
#   sam2_t.pt  ~39 MB   (tiny)
#   sam2_s.pt  ~185 MB  (small)
#   sam2_b.pt  ~312 MB  (base)
#   sam2_l.pt  ~856 MB  (large) <-- default here
DEFAULT_MODEL = "sam2_l.pt"


def extract(
    image_path: Path,
    out_dir: Path,
    model_name: str,
    min_area: float,
    max_area: float,
) -> int:
    model = SAM(model_name)
    # Calling without point/box prompts triggers "segment everything" mode
    results = model(str(image_path), verbose=False)
    result = results[0]

    if result.masks is None:
        return 0

    img_bgr = cv2.imread(str(image_path))
    h, w = img_bgr.shape[:2]
    img_area = h * w
    saved = 0

    for idx, (mask_tensor, box) in enumerate(zip(result.masks.data, result.boxes.xyxy)):
        mask = cv2.resize(
            mask_tensor.cpu().numpy().astype(np.uint8) * 255,
            (w, h),
            interpolation=cv2.INTER_NEAREST,
        )
        area_ratio = np.count_nonzero(mask) / img_area
        if area_ratio < min_area or area_ratio > max_area:
            continue

        img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
        img_bgra[:, :, 3] = mask
        x1, y1, x2, y2 = box.cpu().numpy().astype(int)
        out_path = out_dir / f"object_{idx + 1:02d}.png"
        cv2.imwrite(str(out_path), img_bgra[y1:y2, x1:x2])
        print(f"  Saved: {out_path}  (area {area_ratio:.1%})")
        saved += 1

    return saved


def main():
    parser = argparse.ArgumentParser(
        description="Extract objects from an image as transparent PNGs (SAM2)"
    )
    parser.add_argument("image", help="Path to input image")
    parser.add_argument(
        "-m", "--model", default=DEFAULT_MODEL,
        help=f"SAM2 model weights (default: {DEFAULT_MODEL}). "
             "Options: sam2_t.pt, sam2_s.pt, sam2_b.pt, sam2_l.pt",
    )
    parser.add_argument(
        "--min", type=float, default=0.01, dest="min_area",
        help="Min object area as fraction of image (default: 0.01)",
    )
    parser.add_argument(
        "--max", type=float, default=0.85, dest="max_area",
        help="Max object area as fraction of image (default: 0.85)",
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output directory (default: <image_stem>/ next to input)",
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        sys.exit(f"Error: {image_path} not found")

    out_dir = Path(args.output) if args.output else image_path.parent / image_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = extract(image_path, out_dir, args.model, args.min_area, args.max_area)
    print(f"\n{saved} object(s) extracted to: {out_dir}")


if __name__ == "__main__":
    main()
