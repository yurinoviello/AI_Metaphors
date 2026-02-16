import argparse
import logging
import os

import torch


def run_generation(audio_path, transcript, video_path, output_path, fps, working_dir, fraction):
    # Setup logging to see what's happening
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    
    # Lazy imports inside the function to avoid issues during startup
    from moviepy.video.io.VideoFileClip import VideoFileClip
    from pytoon.animator import animate

    if torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(fraction, 0)
        logging.info(f"Set CUDA memory fraction to {fraction}")

    os.chdir(working_dir)
    logging.info(f"Changed working directory to {working_dir}")

    logging.info("Starting pytoon animation...")
    animation = animate(audio_file=audio_path, transcript=transcript)
    
    logging.info(f"Loading background clip from {video_path}")
    background_clip = VideoFileClip(video_path).with_fps(fps).with_duration(animation.duration)
    
    logging.info(f"Exporting animation to {output_path}")
    animation.export(path=output_path, background=background_clip, scale=0.4)
    logging.info("Export completed successfully")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run cartoon avatar generation in an isolated process.")
    parser.add_argument("--audio_path", required=True)
    parser.add_argument("--transcript", required=True)
    parser.add_argument("--video_path", required=True)
    parser.add_argument("--output_path", required=True)
    parser.add_argument("--fps", type=int, required=True)
    parser.add_argument("--working_dir", required=True)
    parser.add_argument("--fraction", type=float, required=True)

    args = parser.parse_args()

    run_generation(
        audio_path=args.audio_path,
        transcript=args.transcript,
        video_path=args.video_path,
        output_path=args.output_path,
        fps=args.fps,
        working_dir=args.working_dir,
        fraction=args.fraction
    )
