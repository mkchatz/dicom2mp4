import numpy as np
import pydicom
import glob
import imageio
from pathlib import Path

def dicom_to_mp4(dicom_folder, output_path, fps=24):
    """
    Convert DICOM files (3D volumes) into an MP4 video.
    Each slice in the volume becomes a frame.
    """
    dicom_files = sorted(glob.glob(f"{dicom_folder}/*.dcm"))

    if not dicom_files:
        raise ValueError(f"No DICOM files found in {dicom_folder}")

    print(f"Found {len(dicom_files)} DICOM files")

    frames = []

    # Process each DICOM file
    for i, dicom_file in enumerate(dicom_files):
        try:
            ds = pydicom.dcmread(dicom_file)
            volume = ds.pixel_array

            print(f"File {i+1}: shape={volume.shape}, dtype={volume.dtype}")

            # Handle 3D volumes (each slice becomes a frame)
            if len(volume.shape) == 3:
                for slice_idx in range(volume.shape[0]):
                    frame = volume[slice_idx, :, :]
                    frames.append(frame)
            else:
                frames.append(volume)

        except Exception as e:
            print(f"Error processing {dicom_file}: {e}")
            continue

    if not frames:
        raise ValueError("No valid frames extracted")

    print(f"Total frames: {len(frames)}")

    # Convert all frames to uint8 and stack into RGB
    rgb_frames = []
    for frame in frames:
        # Normalize to 0-255
        frame = frame.astype(np.float32)
        frame_min, frame_max = frame.min(), frame.max()
        if frame_max > frame_min:
            frame = (frame - frame_min) / (frame_max - frame_min) * 255
        frame = frame.astype(np.uint8)

        # Convert grayscale to RGB
        rgb_frame = np.stack([frame, frame, frame], axis=2)
        rgb_frames.append(rgb_frame)

    # Write video
    writer = imageio.get_writer(output_path, fps=fps)
    for frame in rgb_frames:
        writer.append_data(frame)
    writer.close()

    print(f"✓ Video saved: {output_path}")

if __name__ == "__main__":
    dicom_folder = "update this path to your DICOM folder"
    output_mp4 = "update this path to your desired output MP4 file"

    dicom_to_mp4(dicom_folder, output_mp4, fps=24)
