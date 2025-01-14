import argparse
import logging
import os
from pathlib import Path

import datasets
from dotenv import load_dotenv
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient

from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.providers.manim_provider import ManimProvider
from ai_metaphors.utils.path_utils import process_executable_path, process_working_dir
from ai_metaphors.utils.text_utils import extract_content, extract_json


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process term name, term definition, and metaphor.")
    parser.add_argument(
        "--use_dataset_example",
        type=int,
        choices=range(14),
        help="Index of the example in the dataset to use directly (0-13)",
    )
    parser.add_argument("--term_name", help="Name of the term")
    parser.add_argument("--term_definition", help="Definition of the term")
    parser.add_argument("--metaphor", help="Metaphor associated with the term")
    parser.add_argument("--generate_metaphor_text", action="store_true", help="Flag to generate the metaphor")
    parser.add_argument(
        "--executable_path",
        type=process_executable_path,
        default=".venv/bin",
        help="Path to the executable for ManimProvider."
        "This argument is not needed if the module is executed trough poetry",
    )
    parser.add_argument(
        "--working_dir",
        type=process_working_dir,
        default="./animations",
        help="Working directory for ManimProvider",
    )
    parser.add_argument(
        "--max_retries",
        type=int,
        choices=range(1, 10),
        default=3,
        help="Number of attempts to retry executing the Manim script in case of failure (1-9)",
    )
    return parser.parse_args()


def animate_term(
    provider: GrazieProvider,
    term: dict,
    metaphor: str,
    one_line_metaphor: str,
    executable_path: Path,
    working_dir: Path,
    max_retries: int,
):
    # Creating classes
    classes = provider.get_classes(term, metaphor)
    logging.info("Classes created")
    classes_dict = extract_json(classes)
    logging.info("Classes extracted")

    # Creating description
    desc = provider.get_description(term, metaphor, one_line_metaphor, str(classes_dict))
    logging.info("Description created")

    # Creating code
    manim_code = provider.get_manim(term, metaphor, one_line_metaphor, str(classes_dict), desc)
    logging.info("Manim code created")

    # Execution
    manim_provider = ManimProvider(provider, term, executable_path, working_dir)
    manim_provider.write_python(manim_code)
    logging.info("Execution...")
    error = manim_provider.execute_manim_script()
    if error == "success":
        return

    for _ in range(max_retries):
        logging.info("Execution...")
        error = manim_provider.fix_code(error)
        if error == "success":
            return

    raise RuntimeError("Cannot execute Manim script")


def metaphor_generation(
    term_name: str,
    term_definition: str,
    metaphor: str,
    generate_metaphor_text: bool,
    executable_path: Path,
    working_dir: Path,
    max_retries: int,
):
    load_dotenv()
    client = GrazieApiGatewayClient(
        grazie_agent=GrazieAgent(name="grazie-api-gateway-client-readme", version="dev"),
        url=GrazieApiGatewayUrls.STAGING,
        grazie_jwt_token=os.getenv("GRAZIE_JWT_TOKEN"),
        auth_type=AuthType.USER,
    )

    provider = GrazieProvider(client, model="openai-gpt-4o")

    logging.info("Term Name: %s", term_name)
    logging.info("Term Definition: %s", term_definition)
    term = {"value": term_name, "definition": term_definition}

    if generate_metaphor_text:
        metaphor = extract_content(provider.get_metaphor(term))
    logging.info("Metaphor: %s", metaphor)

    one_line_metaphor = extract_content(provider.get_one_line_metaphor(term, metaphor))
    logging.info("One-line Metaphor: %s", one_line_metaphor)
    animate_term(provider, term, metaphor, one_line_metaphor, executable_path, working_dir, max_retries)


def main():
    args = parse_arguments()

    if args.use_dataset_example is not None:
        ds = datasets.load_from_disk("ai_metaphors/resources/subset")
        metaphor_generation(
            term_name=ds[args.use_dataset_example]["value"],
            term_definition=ds[args.use_dataset_example]["definition"],
            metaphor=ds[args.use_dataset_example]["metaphor"],
            generate_metaphor_text=args.generate_metaphor_text,
            executable_path=args.executable_path,
            working_dir=args.working_dir,
            max_retries=args.max_retries,
        )
    else:
        if args.term_name is None:
            raise ValueError("Term must not be empty when no example is used.")
        if args.term_definition is None:
            raise ValueError("Definition must not be empty when no example is used.")
        if not args.generate_metaphor_text and args.metaphor is None:
            raise ValueError("Metaphor must not be empty if not generating it.")
        metaphor_generation(
            term_name=args.term_name,
            term_definition=args.term_definition,
            metaphor=args.metaphor,
            generate_metaphor_text=args.generate_metaphor_text,
            executable_path=args.executable_path,
            working_dir=args.working_dir,
            max_retries=args.max_retries,
        )


if __name__ == "__main__":
    main()
