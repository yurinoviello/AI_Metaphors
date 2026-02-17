import argparse
import logging
import subprocess
import sys


def split_video(start_time, duration, movie_file, target):
    ffmpeg_cmd = [
        "ffmpeg",
        "-y",                                   # overwrite if exists
        "-ss", f"{start_time:.3f}",             # seek to start time
        "-i", str(movie_file),
        "-t", f"{duration:.3f}",                # exact length
        "-c", "copy",                           # stream copy
        str(target),
    ]

    logging.info(f"Running ffmpeg command: {' '.join(ffmpeg_cmd)}")
    try:
        subprocess.run(
            ffmpeg_cmd,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True
        )
        logging.info(f"Successfully wrote {target}")
    except subprocess.CalledProcessError as exc:
        logging.error(f"FFmpeg failed: {exc.stderr}")
        sys.exit(exc.returncode)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

    parser = argparse.ArgumentParser(description="Split video section using ffmpeg in an isolated process.")
    parser.add_argument("--start_time", type=float, required=True)
    parser.add_argument("--duration", type=float, required=True)
    parser.add_argument("--movie_file", required=True)
    parser.add_argument("--target", required=True)

    args = parser.parse_args()

    split_video(
        start_time=args.start_time,
        duration=args.duration,
        movie_file=args.movie_file,
        target=args.target
    )
