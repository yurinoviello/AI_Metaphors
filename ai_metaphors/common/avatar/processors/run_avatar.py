import argparse
import logging
import os
import subprocess
import sys

import torch


def run_avatar_generation(ref_path, aud_path, res_video_path, working_dir, fraction):
    # Set CUDA environment variables
    if torch.cuda.is_available():
        torch.cuda.set_per_process_memory_fraction(fraction, 0)
        logging.info(f"Set CUDA memory fraction to {fraction}")

    os.environ["CUDA_MEMORY_FRACTION"] = str(fraction)
    os.environ["PYTORCH_CUDA_ALLOC_CONF"] = "max_split_size_mb:64,garbage_collection_threshold:0.8"

    os.chdir(working_dir)
    logging.info(f"Changed working directory to {working_dir}")

    command = [
        "python", "generate.py",
        "--ref_path", ref_path,
        "--aud_path", aud_path,
        "--seed", "15",
        "--a_cfg_scale", "2",
        "--e_cfg_scale", "2",
        "--ckpt_path", "./checkpoints/float.pth",
        "--emo", "neutral",
        "--res_video_path", res_video_path
    ]

    logging.info(f"Running generation command: {' '.join(command)}")
    try:
        subprocess.run(command, check=True)
        logging.info("Avatar generation completed successfully")
    except subprocess.CalledProcessError as exc:
        logging.error(f"Avatar generation failed: {exc}")
        sys.exit(exc.returncode)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    parser = argparse.ArgumentParser(description="Run avatar generation in an isolated process.")
    parser.add_argument("--ref_path", required=True)
    parser.add_argument("--aud_path", required=True)
    parser.add_argument("--res_video_path", required=True)
    parser.add_argument("--working_dir", required=True)
    parser.add_argument("--fraction", type=float, required=True)

    args = parser.parse_args()

    run_avatar_generation(
        ref_path=args.ref_path,
        aud_path=args.aud_path,
        res_video_path=args.res_video_path,
        working_dir=args.working_dir,
        fraction=args.fraction
    )
