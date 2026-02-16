import argparse
import logging
import subprocess
import sys


def extract_frames(video_path, output_pattern, fps):
    logging.info(f"Extracting frames from {video_path} with {fps} FPS to {output_pattern}")

    command = [
        "ffmpeg",
        "-i", video_path,
        "-vf", f"fps={fps}",
        output_pattern
    ]

    try:
        subprocess.run(command, check=True, capture_output=True, text=True)
        logging.info("Frame extraction completed successfully")
    except subprocess.CalledProcessError as e:
        logging.error(f"ffmpeg failed with error:\n{e.stderr}")
        sys.exit(e.returncode)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Extract frames from video using ffmpeg in an isolated process.")
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--output_pattern", required=True)
    parser.add_argument("--fps", type=int, required=True)

    args = parser.parse_args()

    extract_frames(
        video_path=args.video_path,
        output_pattern=args.output_pattern,
        fps=args.fps
    )
