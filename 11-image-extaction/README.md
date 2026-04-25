# Image Object Extractor

Takes a single image and cuts out every distinct object as a separate transparent PNG file using FastSAM (a fast version of Meta's Segment Anything Model).

## How it works

1. **Segment** — FastSAM scans the image and produces a binary mask for each detected object
2. **Filter** — objects that are too small (noise) or too large (background) are discarded based on their area ratio
3. **Crop & mask** — each object's pixels are kept, everything else becomes transparent, then the result is cropped to the bounding box
4. **Save** — outputs `object_01.png`, `object_02.png`, etc.

## Usage

```bash
python extract.py <image>
```

```bash
# custom output directory and thresholds
python extract.py photo.jpg --conf 0.5 --min 0.02 --max 0.5 -o my_output/
```

## Options

| Flag | Default | Description |
|------|---------|-------------|
| `--conf` | `0.25` | Confidence threshold — how certain SAM must be to keep a segment |
| `--min` | `0.01` | Discard objects smaller than this fraction of the image area |
| `--max` | `0.85` | Discard objects larger than this fraction of the image area |
| `-o / --output` | `<image_stem>/` | Output directory (created if it does not exist) |

## Requirements

- `ultralytics` (FastSAM)
- `opencv-python`
- `numpy`
- `FastSAM-s.pt` model weights in the working directory
