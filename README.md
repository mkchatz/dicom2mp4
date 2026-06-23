# dicom2mp4
A simple python script for converting dicom files into an mp4 video. dicom files are widely used in Radiology for imaging and primarily used in Angiogram which requires a special software called DICOM viewer. This python script converts the .dcm images into an mp4 for easily viewing the same Angiogram video on mobile or laptop using VLC player
##########
# DICOM to MP4 Converter

Convert DICOM medical imaging files to MP4 video format.

## Overview

This script processes 3D volumetric DICOM files and converts each slice into video frames, creating a playable MP4 video. This is useful for visualizing medical imaging sequences (CT, MRI, angiography, etc.) as an animated video.

## Features

- Handles 3D volumetric DICOM files (each slice becomes a frame)
- Automatic pixel value normalization (0-255)
- Converts grayscale to RGB for compatibility
- Uses ffmpeg codec for high-quality MP4 output
- Progress tracking during conversion
- Error handling for corrupted files

## Installation

### Prerequisites

- Python 3.8+
- ffmpeg (for video codec support)

### Install Dependencies

```bash
# Install Python packages
pip3 install pydicom numpy imageio imageio-ffmpeg scipy

# Install ffmpeg (macOS)
brew install ffmpeg
```

## Usage

### Basic Usage

```python
from dicom_to_mp4 import dicom_to_mp4

dicom_to_mp4(
    dicom_folder="/path/to/dicom/files",
    output_path="/path/to/output.mp4",
    fps=24
)
```

### Command Line

```bash
python3 dicom_to_mp4.py
```

Edit the script's `__main__` section to set your input/output paths:

```python
if __name__ == "__main__":
    dicom_folder = "/Users/mkchatz/Desktop/DICOM/Images/"
    output_mp4 = "/Users/mkchatz/Desktop/DICOM/output.mp4"
    dicom_to_mp4(dicom_folder, output_mp4, fps=24)
```

## Parameters

### `dicom_folder` (required)
Path to directory containing `.dcm` DICOM files.

**Example:** `"/path/to/dicom/images/"`

### `output_path` (required)
Path where the MP4 file will be saved.

**Example:** `"/path/to/output.mp4"`

### `fps` (optional)
Frames per second for video playback. Default: `24`

- Lower values (12-18) = slower animation
- Higher values (30-60) = faster animation

## Example

```bash
python3 dicom_to_mp4.py
```

**Output:**
```
Found 9 DICOM files
File 1: shape=(49, 512, 512), dtype=uint8
File 2: shape=(399, 512, 512), dtype=uint8
...
Total frames: 745
✓ Video saved: /Users/mkchatz/Desktop/DICOM/output.mp4
```

## Output Specifications

- **Format:** MP4 (H.264)
- **Resolution:** 512×512 (or native DICOM resolution)
- **Frame Rate:** Configurable (default 24 fps)
- **Color Space:** RGB (grayscale converted)
- **Pixel Format:** 8-bit unsigned integer (0-255)

## Notes

### DICOM Volume Structure

Each DICOM file can contain multiple 2D slices stacked together (3D volume):

- File shape: `(num_slices, height, width)`
- Each slice becomes one video frame
- Example: 9 files with average 83 slices each = 745-frame video

### Pixel Value Normalization

- Original pixel values are automatically scaled to 0-255 range
- Min value → 0 (black)
- Max value → 255 (white)
- Preserves image contrast

### Supported DICOM Formats

- CT scans
- MRI scans
- X-ray fluoroscopy
- Ultrasound
- Angiography
- Any DICOM with pixel_array attribute

## Troubleshooting

### "No DICOM files found"
- Verify `.dcm` files exist in the specified directory
- Check file extension is lowercase `.dcm`

### "No video codec available"
- Install ffmpeg: `brew install ffmpeg`
- Reinstall imageio-ffmpeg: `pip3 install --upgrade imageio-ffmpeg`

### Blank or corrupted video
- Check DICOM files are not corrupted
- Verify pixel values normalize correctly with test frame:
  ```bash
  python3 << 'EOF'
  import pydicom
  ds = pydicom.dcmread("your_file.dcm")
  print(f"Min: {ds.pixel_array.min()}, Max: {ds.pixel_array.max()}")
  EOF
  ```

### Video shows mostly black/white
- Try adjusting window/level values in DICOM viewer to confirm original data
- This is expected for medical imaging with specific HU ranges

## Performance

- **Input:** 9 DICOM files (745 total frames)
- **Output:** 20 MB MP4 at 512×512
- **Processing Time:** ~10-30 seconds (depends on system and file count)

## Playback

Open the generated MP4 with any standard video player:

```bash
# macOS
open output.mp4

# macOS with VLC
vlc output.mp4

# Linux
ffplay output.mp4
```

## License

This script uses open-source libraries: pydicom, imageio, numpy, scipy.
