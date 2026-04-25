#!/usr/bin/env python3
"""Extract all objects from an image as individual transparent PNGs using FastSAM-x."""

import argparse
import sys
from pathlib import Path

import cv2
import numpy as np
from ultralytics import FastSAM


def _background_mask(img_bgr: np.ndarray, tolerance: int = 30) -> np.ndarray:
    """Build a foreground mask by sampling background color from the four corners."""
    corners = [img_bgr[0, 0], img_bgr[0, -1], img_bgr[-1, 0], img_bgr[-1, -1]]
    bg_color = np.median(corners, axis=0).astype(np.float32)
    diff = np.sqrt(np.sum((img_bgr.astype(np.float32) - bg_color) ** 2, axis=2))
    fg = (diff >= tolerance).astype(np.uint8) * 255
    # close small holes and remove specks
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7, 7))
    fg = cv2.morphologyEx(fg, cv2.MORPH_CLOSE, kernel, iterations=2)
    fg = cv2.morphologyEx(fg, cv2.MORPH_OPEN, kernel, iterations=1)
    return fg


def extract(
    image_path: Path,
    out_dir: Path,
    conf: float,
    min_area: float,
    max_area: float,
    merge: bool = False,
    bg_tolerance: int = 30,
) -> int:
    model = FastSAM("FastSAM-x.pt")
    results = model(
        str(image_path), conf=conf, iou=0.9, retina_masks=True, verbose=False
    )
    result = results[0]

    if result.masks is None:
        return 0

    img_bgr = cv2.imread(str(image_path))
    h, w = img_bgr.shape[:2]
    img_area = h * w

    if merge:
        combined_mask = np.zeros((h, w), dtype=np.uint8)
        x1_all, y1_all, x2_all, y2_all = w, h, 0, 0

        for mask_tensor, box in zip(result.masks.data, result.boxes.xyxy):
            mask = cv2.resize(
                mask_tensor.cpu().numpy().astype(np.uint8) * 255,
                (w, h),
                interpolation=cv2.INTER_NEAREST,
            )
            area_ratio = np.count_nonzero(mask) / img_area
            if area_ratio < min_area or area_ratio > max_area:
                continue
            combined_mask = cv2.bitwise_or(combined_mask, mask)
            bx1, by1, bx2, by2 = box.cpu().numpy().astype(int)
            x1_all = min(x1_all, bx1)
            y1_all = min(y1_all, by1)
            x2_all = max(x2_all, bx2)
            y2_all = max(y2_all, by2)

        if not np.any(combined_mask):
            return 0

        # strip background pixels that leaked into the merged mask
        fg_mask = _background_mask(img_bgr, bg_tolerance)
        combined_mask = cv2.bitwise_and(combined_mask, fg_mask)

        img_bgra = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2BGRA)
        img_bgra[:, :, 3] = combined_mask
        out_path = out_dir / "object_01.png"
        cv2.imwrite(str(out_path), img_bgra[y1_all:y2_all, x1_all:x2_all])
        area_ratio = np.count_nonzero(combined_mask) / img_area
        print(f"  Saved: {out_path}  (area {area_ratio:.1%})")
        return 1

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
        description="Extract objects from an image as transparent PNGs (FastSAM-x)"
    )
    parser.add_argument("image", help="Path to input image")
    parser.add_argument(
        "-c", "--conf", type=float, default=0.25,
        help="Confidence threshold (default: 0.25)",
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
    parser.add_argument(
        "--merge", action="store_true",
        help="Merge all detected masks into one object (useful for single-product images)",
    )
    parser.add_argument(
        "--bg-tolerance", type=int, default=30, dest="bg_tolerance",
        help="Color distance from corner pixels considered background (default: 30)",
    )
    args = parser.parse_args()

    image_path = Path(args.image)
    if not image_path.exists():
        sys.exit(f"Error: {image_path} not found")

    out_dir = Path(args.output) if args.output else image_path.parent / image_path.stem
    out_dir.mkdir(parents=True, exist_ok=True)

    saved = extract(image_path, out_dir, args.conf, args.min_area, args.max_area, args.merge, args.bg_tolerance)
    print(f"\n{saved} object(s) extracted to: {out_dir}")


if __name__ == "__main__":
    main()
