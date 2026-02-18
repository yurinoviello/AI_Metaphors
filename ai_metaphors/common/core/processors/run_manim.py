import argparse
import logging
import os
import subprocess
import sys


def run_manim(manim_path, script_path, media_dir, log_dir, high_quality, auto_play):
    env = os.environ.copy()
    env["SETUPTOOLS_USE_DISTUTILS"] = "stdlib"

    manim_command = [
        manim_path,
        "-p" if auto_play else None,
        "-qh" if high_quality else "-ql",
        script_path,
        "--save_sections",
        "--media_dir",
        media_dir,
        "--log_dir",
        log_dir,
        "--progress_bar",
        "none",
        "--verbosity",
        "WARNING"
    ]

    # Filter out None values
    command = [c for c in manim_command if c]

    logging.info(f"Running manim command: {' '.join(command)}")
    try:
        process = subprocess.run(command, capture_output=True, text=True, check=False, env=env)
        
        # Write stdout and stderr to logs if needed or just print them
        if process.stdout:
            print(process.stdout)
        if process.stderr:
            print(process.stderr, file=sys.stderr)
            
        sys.exit(process.returncode)
    except FileNotFoundError as exc:
        logging.error(f"Manim executable not found: {exc}")
        sys.exit(1)
    except Exception as exc:
        logging.error(f"Manim execution failed: {exc}")
        sys.exit(1)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")
    
    parser = argparse.ArgumentParser(description="Run manim in an isolated process.")
    parser.add_argument("--manim_path", required=True)
    parser.add_argument("--script_path", required=True)
    parser.add_argument("--media_dir", required=True)
    parser.add_argument("--log_dir", required=True)
    parser.add_argument("--high_quality", action="store_true")
    parser.add_argument("--auto_play", action="store_true")

    args = parser.parse_args()

    run_manim(
        manim_path=args.manim_path,
        script_path=args.script_path,
        media_dir=args.media_dir,
        log_dir=args.log_dir,
        high_quality=args.high_quality,
        auto_play=args.auto_play,
    )
