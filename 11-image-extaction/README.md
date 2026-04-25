# Image Object Extractor

Takes an image and cuts out every distinct object as a separate transparent PNG file using FastSAM or SAM2 (Meta's Segment Anything Model family).

## How it works

1. **Segment** — the model scans the image and produces a binary mask for each detected object
2. **Filter** — objects that are too small (noise) or too large (background) are discarded based on their area ratio
3. **Crop & mask** — each object's pixels are kept, everything else becomes transparent, then the result is cropped to the bounding box
4. **Save** — outputs `object_01.png`, `object_02.png`, etc.

---

## Scripts

| Script | Model | Size | Notes |
|--------|-------|------|-------|
| `extract.py` | FastSAM-s | ~23 MB | Fastest, decent quality |
| `extract_fastsam_x.py` | FastSAM-x | ~138 MB | Better quality, same API |
| `extract_sam2.py` | SAM2 | 39–856 MB | Best quality, slowest |

All three scripts share the same interface. Examples below use `extract_fastsam_x.py` but apply equally to the others.

---

## Usage

```bash
# extract all objects as separate PNGs
uv run python extract_fastsam_x.py photo.jpg

# custom confidence and area thresholds
uv run python extract_fastsam_x.py photo.jpg --conf 0.5 --min 0.02 --max 0.5

# custom output directory
uv run python extract_fastsam_x.py photo.jpg -o my_output/
```

### Output

Each detected object is saved as a cropped transparent PNG:

```
photo/
  object_01.png
  object_02.png
  object_03.png
  ...
```

---

## Options

### `extract.py` and `extract_fastsam_x.py`

| Flag | Default | Description |
|------|---------|-------------|
| `--conf` | `0.25` | Confidence threshold — how certain the model must be to keep a segment |
| `--min` | `0.01` | Discard objects smaller than this fraction of the image area |
| `--max` | `0.85` | Discard objects larger than this fraction of the image area |
| `-o / --output` | `<image_stem>/` | Output directory (created if it does not exist) |
| `--merge` | off | Merge all masks into one object — see below |
| `--bg-tolerance` | `30` | Only used with `--merge` — color distance from corner pixels considered background |

### `extract_sam2.py`

Same as above except `--conf` is replaced by:

| Flag | Default | Description |
|------|---------|-------------|
| `-m / --model` | `sam2_l.pt` | SAM2 weights to use: `sam2_t.pt`, `sam2_s.pt`, `sam2_b.pt`, `sam2_l.pt` |

---

## `--merge` flag (single-product images)

By default the tool outputs one PNG per detected segment. On product images the model often splits one object into multiple parts (e.g. a cap's brim, body panels, and logo become separate segments). `--merge` combines all valid masks into one:

```bash
uv run python extract_fastsam_x.py cap.webp --merge
```

### When `--merge` works

Product photos on a **plain, uniform background** (white, grey, studio backdrop). The tool samples the corner pixels to detect the background color and strips it from the final mask.

```
cap.webp  →  object_01.png  (clean transparent cutout of the cap)
```

### When `--merge` does NOT work

- **Screenshots** — corner pixels are UI chrome (dark status bar, etc.), not the background
- **Lifestyle / scene photos** — sky, textured, or gradient backgrounds that don't match the corners
- **Multiple distinct products** — all objects get merged into one blob

For those images, use the default mode (no `--merge`) and pick the segment you need from the numbered outputs.

---

## Requirements

- `ultralytics`
- `opencv-python`
- `numpy`
- Model weights in the working directory (auto-downloaded by ultralytics on first run):
  - `FastSAM-s.pt` for `extract.py`
  - `FastSAM-x.pt` for `extract_fastsam_x.py`
  - `sam2_l.pt` (or other size) for `extract_sam2.py`
