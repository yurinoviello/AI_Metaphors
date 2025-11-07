import argparse
import logging
import datasets

from ai_metaphors.cli.config_arg_parser import ConfigArgumentParser
from ai_metaphors.common.core.utils import TermType
from ai_metaphors.common.core.processors.metaphor_processor import MetaphorProcessor
from ai_metaphors.common.core.utils.manim_type import ManimType
from ai_metaphors.common.video_from_academic_definition import AcademicDefinitionPromptProvider
from ai_metaphors.common.video_from_code import CodePromptProvider
from ai_metaphors.common.video_from_definition.providers import DefinitionPromptProvider
from ai_metaphors.common.core.utils.path_utils import process_bin_directory, process_temperature, process_working_dir


def parse_arguments() -> argparse.Namespace:
    parser = ConfigArgumentParser(description="Process term name, term definition, and metaphor.")
    parser.add_argument(
        "--config",
        type=str,
        help="Config file from which other arguments will be read. If not set, the arguments will be read from the command line."
    )
    parser.add_argument(
        "--use-dataset-example",
        type=int,
        default=-1,
        choices=range(14),
        help="Index of the example in the dataset to use directly (0-13)",
    )
    parser.add_argument("--term-name", help="Name of the term")
    parser.add_argument("--term-value", help="Value of the term")
    parser.add_argument("--metaphor", help="Metaphor associated with the term")
    parser.add_argument("--generate-metaphor-text", action="store_true", help="Flag to generate the metaphor")
    parser.add_argument("--term-type",
        choices=['definition', 'code', 'academic-definition'],
        default='definition',
        help="""Type of the input to explain:
            definition          - term with definition
            code                - term with code
            academic-definition - term with optional academic definition (without metaphor) """,
    )
    parser.add_argument(
        "--animation-type",
        choices=['basic', 'voice', 'avatar', 'cartoon-avatar'],
        default='basic',
        help="""Type of animation to generate:
            basic  - generates simple animation without voice or avatar
            voice  - adds voice-over to the animation
            avatar - adds animated avatar with voice-over
            cartoon-avatar - adds animated avatar with voice-over and cartoon style""",
    )
    parser.add_argument(
        "--bin-directory",
        type=process_bin_directory,
        default=".venv/bin",
        help="Path to the bin directory for ManimProvider."
        "This argument is not needed if the module is executed trough poetry",
    )
    parser.add_argument(
        "--working-dir",
        type=process_working_dir,
        default="./animations",
        help="Working directory for ManimProvider",
    )
    parser.add_argument(
        "--model",
        type=str,
        choices=[
            "openai-gpt-4o",
            "openai-gpt4.1",
            "openai-o1",
            "openai-o3",
            "openai-o4-mini",
            "anthropic-claude-3.7-sonnet",
            "anthropic-claude-4-sonnet",
            "anthropic-claude-4-opus",
        ],
        default="openai-gpt-4o",
        help="LLM to be used for processing.",
    )
    parser.add_argument(
        "--model-classes",
        type=str,
        choices=[
            "default",
            "anthropic-claude-3.7-sonnet",
            "anthropic-claude-4-sonnet",
            "anthropic-claude-4-opus",
        ],
        default="default",
        help="LLM to be used to create classes code, SVG graphics in particular",
    )
    parser.add_argument(
        "--model-manim",
        type=str,
        choices=[
            "default",
            "openai-gpt4.1",
            "openai-o1",
            "openai-o3",
            "openai-o4-mini",
            "anthropic-claude-3.7-sonnet",
            "anthropic-claude-4-sonnet",
            "anthropic-claude-4-opus",
        ],
        default="default",
        help="LLM to be used to process only the manim script",
    )
    parser.add_argument(
        "--temperature",
        type=process_temperature,
        default=0.1,
        help="Temperature value to be used for the LLM.",
    )
    parser.add_argument(
        "--vllm-fix",
        action="store_true",
        help="**Experimental** Perform an automatic vllm analysis and code correction.",
    )
    parser.add_argument(
        "--auto-play",
        action="store_true",
        help="Automatically play the animation at the end of the execution.",
    )
    parser.add_argument(
        "--high-quality",
        action="store_true",
        help="Generate an high quality animation (1080p60p). If not set, the default is 480p15.",
    )
    # Interactivity flags
    parser.add_argument("--wait-analogy", action="store_true", help="Wait for user input after analogy generation (accept/redo).")
    parser.add_argument("--wait-classes", action="store_true", help="Wait for user input after classes generation (accept/redo).")
    parser.add_argument("--wait-description", action="store_true", help="Wait for user input after description generation (accept/redo).")
    parser.add_argument("--wait-manim", action="store_true", help="Wait for user input after Manim code generation (accept/redo).")
    parser.add_argument("--wait-video", action="store_true", help="Wait for user input after video generation (accept/redo).")
    parser.add_argument(
        "--start-stage",
        type=str,
        choices=["analogy", "classes", "description", "manim", "video"],
        default="analogy",
        help="Stage to start the pipeline from (default: analogy). Use 'video' to skip generation and just run existing code.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activate debug mode",
    )
    args = parser.parse_args()
    match args.term_type:
        case "definition":
            args.term_kind = TermType.DEFINITION_METAPHOR
        case "code":
            args.term_kind = TermType.CODE_METAPHOR
        case "academic-definition":
            args.term_kind = TermType.ACADEMIC_DEFINITION
        case _:
            raise ValueError(f"Unknown term type: {args.term_type}")
    if args.use_dataset_example != -1:
        match args.term_kind:
            case TermType.DEFINITION_METAPHOR:
                ds = datasets.load_from_disk("ai_metaphors/resources/examples/definitions")
                args.term_name = ds[args.use_dataset_example]["name"]
                args.term_value = ds[args.use_dataset_example]["definition"]
                args.metaphor = ds[args.use_dataset_example]["metaphor"]
            case TermType.CODE_METAPHOR:
                ds = datasets.load_from_disk("ai_metaphors/resources/examples/codes")
                args.term_name = ds[args.use_dataset_example]["name"]
                args.term_value = ds[args.use_dataset_example]["folder"]
            case _:
                raise ValueError(f"Not supported term type: {args.term_kind} for dataset example")
    else:
        if args.term_name is None:
            raise ValueError("Term must not be empty when no example is used.")
        if args.term_kind != TermType.ACADEMIC_DEFINITION and args.term_value is None:
            raise ValueError("Definition must not be empty when no example is used.")
        if args.term_kind != TermType.ACADEMIC_DEFINITION and not args.generate_metaphor_text and args.metaphor is None:
            raise ValueError("Metaphor must not be empty if not generating it.")
    if args.vllm_fix:
        args.high_quality = False
    match args.animation_type:
        case "basic":
            args.manim_type = ManimType.DEFAULT
        case "voice":
            args.manim_type = ManimType.VOICE
        case "avatar":
            args.manim_type = ManimType.AVATAR
        case "cartoon-avatar":
            args.manim_type  = ManimType.CARTOON_AVATAR
        case _:
            raise ValueError(f"Unknown animation type: {args.animation_type}")
    return args


def main():
    args = parse_arguments()

    # Configure logging with timestamps; honor --debug
    logging.basicConfig(
        level=logging.INFO if args.debug else logging.WARNING,
        format="%(asctime)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        force=True
    )

    match args.term_kind:
        case TermType.DEFINITION_METAPHOR:
            term = {
                "name": args.term_name,
                "definition": args.term_value,
                "working_dir": "animations"
            }
            prompt_provider = DefinitionPromptProvider(term, args.manim_type)
        case TermType.CODE_METAPHOR:
            term = {
                "name": args.term_name,
                "code_folder": args.term_value,
                "working_dir": "animations"
            }
            prompt_provider = CodePromptProvider(term, args.manim_type)
        case TermType.ACADEMIC_DEFINITION:
            term = { "name": args.term_name, "working_dir": "animations" }
            prompt_provider = AcademicDefinitionPromptProvider(term, args.manim_type)
        case _:
            raise ValueError(f"Unknown term type: {args.term_kind}")

    subject_id = args.term_name.replace(' ', '_')

    processor = MetaphorProcessor(
        subject_id=subject_id,
        prompt_provider=prompt_provider,
        metaphor=args.metaphor,
        term_type=args.term_kind,
        manim_type=args.manim_type,
        bin_directory=args.bin_directory,
        working_dir=args.working_dir,
        model=args.model,
        model_classes=args.model_classes,
        model_manim=args.model_manim,
        temperature=args.temperature,
        vllm_fix=args.vllm_fix,
        auto_play=args.auto_play,
        high_quality=args.high_quality,
    )

    # Token usage logging: start
    logging.info("Token usage at start: %d", processor.get_token_usage())

    def _wait_loop(stage_name: str, enabled: bool, allow_jump_back: bool = False) -> str:
        if not enabled:
            return "accept"
        while True:
            if allow_jump_back:
                prompt = (
                    f"[{stage_name}] Type 'accept' to proceed, 'redo' to redo this stage, or 'redo <stage>' to jump back to a specific stage "
                    f"(analogy/classes/description/manim/video): "
                )
            else:
                prompt = f"[{stage_name}] Type 'accept' to proceed or 'redo' to redo this stage: "
            logging.info("Waiting for user input after '%s' stage", stage_name)
            try:
                choice = input(prompt).strip().lower()
            except EOFError:
                choice = "accept"
            if choice == "accept" or choice == "redo":
                logging.info("User input after '%s': %s", stage_name, choice)
                return choice
            if allow_jump_back and choice.startswith("redo "):
                target = choice.split(maxsplit=1)[1]
                if target in {"analogy", "classes", "description", "manim", "video"}:
                    logging.info("User requested jump back to stage: %s", target)
                    return choice
            logging.info("Unrecognized input: %s", choice)

    # Orchestrate stages with possibility to jump back from the video stage
    stage = args.start_stage
    while True:
        if stage == "analogy":
            while True:
                processor.generate_analogy()
                logging.info("Token usage so far: %d", processor.get_token_usage())
                decision = _wait_loop("analogy", args.wait_analogy)
                if decision == "accept":
                    stage = "classes"
                    break
                # 'redo' loops and reruns analogy
            continue

        if stage == "classes":
            while True:
                processor.reload_from_files()
                processor.generate_classes()
                logging.info("Token usage so far: %d", processor.get_token_usage())
                decision = _wait_loop("classes", args.wait_classes)
                if decision == "accept":
                    stage = "description"
                    break
            continue

        if stage == "description":
            while True:
                processor.reload_from_files()
                processor.generate_description()
                logging.info("Token usage so far: %d", processor.get_token_usage())
                decision = _wait_loop("description", args.wait_description)
                if decision == "accept":
                    stage = "manim"
                    break
            continue

        if stage == "manim":
            while True:
                processor.reload_from_files()
                processor.generate_manim_code()
                logging.info("Token usage so far: %d", processor.get_token_usage())
                decision = _wait_loop("manim", args.wait_manim)
                if decision == "accept":
                    stage = "video"
                    break
            continue

        if stage == "video":
            while True:
                processor.reload_from_files()
                processor.run_manim()
                decision = _wait_loop("video", args.wait_video, allow_jump_back=True)
                if decision == "accept":
                    logging.info("Token usage at end: %d", processor.get_token_usage())
                    return
                if decision == "redo":
                    # rerun video with current assets
                    continue
                if decision.startswith("redo "):
                    target = decision.split(maxsplit=1)[1]
                    stage = target
                    break
            continue


if __name__ == "__main__":
    main()
