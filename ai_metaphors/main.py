import argparse
import logging
import os
import json
from pathlib import Path
import datasets
from dotenv import load_dotenv
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient

from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.providers.manim_provider import ManimProvider
from ai_metaphors.utils.path_utils import process_bin_directory, process_working_dir
from ai_metaphors.utils.text_utils import extract_content, extract_json


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process term name, term definition, and metaphor.")
    parser.add_argument(
        "--use-dataset-example",
        type=int,
        choices=range(14),
        help="Index of the example in the dataset to use directly (0-13)",
    )
    parser.add_argument("--term-name", help="Name of the term")
    parser.add_argument("--term-definition", help="Definition of the term")
    parser.add_argument("--metaphor", help="Metaphor associated with the term")
    parser.add_argument("--generate-metaphor-text", action="store_true", help="Flag to generate the metaphor")
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
        "--debug",
        action="store_true",
        help="Activate debug mode",
    )
    args = parser.parse_args()
    if args.use_dataset_example is not None:
        ds = datasets.load_from_disk("ai_metaphors/resources/subset")
        args.term_name = ds[args.use_dataset_example]["value"]
        args.term_definition = ds[args.use_dataset_example]["definition"]
        args.metaphor = ds[args.use_dataset_example]["metaphor"]
    else:
        if args.term_name is None:
            raise ValueError("Term must not be empty when no example is used.")
        if args.term_definition is None:
            raise ValueError("Definition must not be empty when no example is used.")
        if not args.generate_metaphor_text and args.metaphor is None:
            raise ValueError("Metaphor must not be empty if not generating it.")
    return args


def animate_term(
    manim_provider: ManimProvider,
    term: dict,
    metaphor: str,
    one_line_metaphor: str,
):
    grazie_provider = manim_provider.grazie_provider
    # Creating classes
    classes = grazie_provider.get_classes(term, metaphor, manim_provider.svg)
    logging.info("Classes created")
    classes_dict = extract_json(classes)
    with manim_provider.classes_file.open(mode='w', encoding='utf-8') as json_file:
        json.dump(classes_dict, json_file, indent=4)
    logging.info("Classes extracted")

    # Creating description
    desc = grazie_provider.get_description(term, metaphor, one_line_metaphor, str(classes_dict))
    with manim_provider.description_file.open(mode='w', encoding='utf-8') as text_file:
        text_file.write(desc)
    logging.info("Description created")

    # Creating code
    manim_code = grazie_provider.get_manim(term, metaphor, one_line_metaphor, str(classes_dict), manim_provider.svg, desc)
    logging.info("Manim code created")

    # Execution
    logging.info("Execution...")
    manim_provider.write_and_run_python(manim_code)


def metaphor_generation(
    term_name: str,
    term_definition: str,
    metaphor: str,
    generate_metaphor_text: bool,
    bin_directory: Path,
    working_dir: Path,
):
    load_dotenv()
    client = GrazieApiGatewayClient(
        grazie_agent=GrazieAgent(name="grazie-api-gateway-client-readme", version="dev"),
        url=GrazieApiGatewayUrls.STAGING,
        grazie_jwt_token=os.getenv("GRAZIE_JWT_TOKEN"),
        auth_type=AuthType.USER,
    )

    grazie_provider = GrazieProvider(client, model="openai-gpt-4o")

    logging.info("Term Name: %s", term_name)
    logging.info("Term Definition: %s", term_definition)
    term = {"value": term_name, "definition": term_definition}

    if generate_metaphor_text:
        metaphor = extract_content(grazie_provider.get_metaphor(term))
    logging.info("Metaphor: %s", metaphor)

    one_line_metaphor = extract_content(grazie_provider.get_one_line_metaphor(term, metaphor))
    logging.info("One-line Metaphor: %s", one_line_metaphor)

    manim_provider = ManimProvider(grazie_provider, term, bin_directory, working_dir)
    animate_term(manim_provider, term, metaphor, one_line_metaphor)

    if manim_provider.validate_video() == 1:
        video_analysis = manim_provider.evaluate_video()
        logging.info("Evaluation complete")
        logging.info("Video Evaluation: %s", video_analysis)

        video_refined_code = grazie_provider.request_video_refinement(instructions=manim_provider.description_file.read_text(), code=manim_provider.script_path.read_text(), errors_explanation=video_analysis, svg=manim_provider.svg)

        logging.info("Execution...")
        manim_provider.write_and_run_python(video_refined_code)

def main():
    args = parse_arguments()
    if args.debug:
        logging.basicConfig(level=logging.INFO)
    metaphor_generation(
        term_name=args.term_name,
        term_definition=args.term_definition,
        metaphor=args.metaphor,
        generate_metaphor_text=args.generate_metaphor_text,
        bin_directory=args.bin_directory,
        working_dir=args.working_dir,
    )


if __name__ == "__main__":
    main()
