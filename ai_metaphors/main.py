import argparse
import logging
import datasets

from ai_metaphors.config_arg_parser import ConfigArgumentParser
from ai_metaphors.core.processors.metaphor_processor import MetaphorProcessor
from ai_metaphors.core.utils.manim_type import ManimType
from ai_metaphors.video_from_code import CodePromptProvider
from ai_metaphors.video_from_definition.providers.definition_prompt_provider import DefinitionPromptProvider
from ai_metaphors.core.utils.path_utils import process_bin_directory, process_temperature, process_working_dir


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
        choices=['definition', 'code'],
        default='definition',
        help="""Type of the input to explain:
            definition - term with definition
            code       - term with code""",
    )
    parser.add_argument(
        "--animation-type",
        choices=['basic', 'voice', 'avatar'],
        default='basic',
        help="""Type of animation to generate:
            basic  - generates simple animation without voice or avatar
            voice  - adds voice-over to the animation
            avatar - adds animated avatar with voice-over""",
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
            "openai-gpt4.5",
            "openai-o1",
            "anthropic-claude-3.5-sonnet",
            "anthropic-claude-3.7-sonnet",
        ],
        default="openai-gpt-4o",
        help="LLM to be used for processing.",
    )
    parser.add_argument(
        "--model-manim",
        type=str,
        choices=[
            "default",
            "openai-gpt-4o",
            "openai-gpt4.5",
            "openai-o1",
            "anthropic-claude-3.5-sonnet",
            "anthropic-claude-3.7-sonnet",
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
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Activate debug mode",
    )
    args = parser.parse_args()
    if args.use_dataset_example != -1:
        match args.term_type:
            case "definition":
                ds = datasets.load_from_disk("ai_metaphors/resources/examples/definitions")
                args.term_name = ds[args.use_dataset_example]["name"]
                args.term_value = ds[args.use_dataset_example]["definition"]
                args.metaphor = ds[args.use_dataset_example]["metaphor"]
            case "code":
                ds = datasets.load_from_disk("ai_metaphors/resources/examples/codes")
                args.term_name = ds[args.use_dataset_example]["name"]
                args.term_value = ds[args.use_dataset_example]["folder"]
    else:
        if args.term_name is None:
            raise ValueError("Term must not be empty when no example is used.")
        if args.term_value is None:
            raise ValueError("Definition must not be empty when no example is used.")
        if not args.generate_metaphor_text and args.metaphor is None:
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
    return args


def main() -> None:
    args = parse_arguments()
    if args.debug:
        logging.basicConfig(level=logging.INFO)
    match args.term_type:
        case "definition":
            term = {
                "name": args.term_name,
                "definition": args.term_value
            }
            prompt_provider = DefinitionPromptProvider(term, args.manim_type)
        case "code":
            term = {
                "name": args.term_name,
                "code_folder": args.term_value
            }
            prompt_provider = CodePromptProvider(term, args.manim_type)
    subject_id = args.term_name.replace(' ', '_')

    MetaphorProcessor(
        subject_id=subject_id,
        prompt_provider=prompt_provider,
        metaphor=args.metaphor,
        manim_type=args.manim_type,
        bin_directory=args.bin_directory,
        working_dir=args.working_dir,
        model=args.model,
        model_manim=args.model_manim,
        temperature=args.temperature,
        vllm_fix=args.vllm_fix,
        auto_play=args.auto_play,
        high_quality=args.high_quality,
    ).generate_video()


if __name__ == "__main__":
    main()
