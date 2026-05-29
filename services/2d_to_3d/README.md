# 2D to 3D Generation Service

## Overview

This service converts a single 2D image into a 3D GLB model using TripoSR.

The generated GLB asset can be consumed by downstream services such as animation, AR rendering, WebAR visualization, and scene composition.

---

## Features

* Single image to 3D model generation
* Automatic mesh generation using TripoSR
* Automatic GLB export
* Dynamic input image support
* Job-based output generation
* Ready for integration into ARStoryTelling pipeline

---

## Pipeline

```text
Input Image
      ↓
generate_glb.py
      ↓
TripoSR Inference
      ↓
Mesh Generation
      ↓
OBJ / GLB Output
      ↓
Final GLB Asset
```

---

## Directory Structure

```text
2d_to_3d/
├── generate_glb.py
├── requirements.txt
├── README.md
└── TripoSR/
```

---

## Requirements

Python 3.10+

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Additional Dependency

The following dependency is required by `rembg` during runtime:

```bash
pip install onnxruntime
```

It is included in the service requirements.

---

## Usage

Generate a 3D model from an image:

```bash
python generate_glb.py \
    --input path/to/image.png \
    --name asset_name
```

Example:

```bash
python generate_glb.py \
    --input inputs/krishna.jpeg \
    --name krishna
```

---

## Output

Generated models are exported as:

```text
outputs/final/
```

Example:

```text
outputs/final/krishna_1748512345.glb
```

---

## Service Contract

### Input

```json
{
  "image_path": "path/to/image.png",
  "asset_name": "optional_name"
}
```

### Output

```json
{
  "status": "success",
  "glb_path": "outputs/final/asset.glb"
}
```

---

## Future Enhancements

* Background worker integration
* Queue-based processing
* FastAPI service wrapper
* Multi-view reconstruction support
* Zero123 integration
* Automatic mesh optimization
* Draco compression for WebAR delivery

---

## Integration with ARStoryTelling

This service acts as the 3D asset generation stage of the ARStoryTelling pipeline.

```text
Story Content
      ↓
Asset Generation
      ↓
2D Image Creation
      ↓
2D → 3D Service
      ↓
GLB Asset
      ↓
Animation Service
      ↓
AR Rendering
```
