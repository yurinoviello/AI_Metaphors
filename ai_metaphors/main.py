import argparse
import sys
from pathlib import Path

import datasets
from grazie.api.client.endpoints import GrazieApiGatewayUrls
from grazie.api.client.gateway import AuthType, GrazieAgent, GrazieApiGatewayClient

from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.providers.manim_provider import ManimProvider
from ai_metaphors.utils.text_utils import extract_content, extract_json


def main(term_name: str, term_definition: str, metaphor: str, generate_metaphor: bool, executable_path: str, working_dir: str) -> int:
    token_path = Path("token.secret")
    with token_path.open() as t:
        token = t.read()

    client = GrazieApiGatewayClient(
        grazie_agent=GrazieAgent(name="grazie-api-gateway-client-readme", version="dev"),
        url=GrazieApiGatewayUrls.STAGING,
        grazie_jwt_token=token,
        auth_type=AuthType.USER,
    )

    provider = GrazieProvider(client, model="openai-gpt-4o")

    print(f"Term Name: {term_name}")
    print(f"Term Definition: {term_definition}")
    term = {"value": term_name, "definition": term_definition}

    if generate_metaphor:
        metaphor = extract_content(provider.get_metaphor(term))
    print(f"Metaphor: {metaphor}")
    return animate_term(provider, term, metaphor, executable_path, working_dir)


def animate_term(provider: GrazieProvider, term: dict, metaphor: str, executable_path: str, working_dir: str) -> int:
    # Creating classes
    classes = provider.get_classes(term, metaphor)
    print("Classes created")
    classes_dict = extract_json(classes)
    print("Classes extracted")

    # Creating description
    desc = provider.get_description(term, metaphor, str(classes_dict))
    print("Description created")

    # Creating code
    manim_code = provider.get_manim(term, metaphor, str(classes_dict), desc)
    print("Manim code created")

    # Execution
    manim_provider = ManimProvider(provider, term, executable=executable_path, working_dir=working_dir)
    manim_provider.write_python(manim_code, font_path="ai_metaphors/resources/JetBrainsSans-Regular.ttf")
    print("Execution...")
    error = manim_provider.execute_manim_script()
    if error == "success":
        return 0

    for _ in range(3):
        print(error)
        print("Execution...")
        error = manim_provider.fix_code(error)
        if error == "success":
            return 0

    raise RuntimeError("Cannot execute Manim script")


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Process term name, term definition, and metaphor.")
    parser.add_argument("--use_dataset_example", type=int, choices=range(-1, 14), default=-1, help="Index of the example in the dataset to use directly")
    parser.add_argument("--term_name", type=str, default="", help="Name of the term")
    parser.add_argument("--term_definition", type=str, default="", help="Definition of the term")
    parser.add_argument("--metaphor", type=str, default="", help="Metaphor associated with the term")
    parser.add_argument("--generate_metaphor", action="store_true", default=False, help="Flag to generate the metaphor")
    parser.add_argument(
        "--executable_path",
        type=str,
        default="",
        help="Path to the executable for ManimProvider.This argument is not needed if the module is executed trough poetry",
    )
    parser.add_argument("--working_dir", type=str, default="./animations", help="Working directory for ManimProvider")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # Check if the executable path exists
    if args.executable_path != "" and not Path(args.executable_path).is_dir():
        print(f"Error: The executable path '{args.executable_path}' does not exist.")
        sys.exit(1)

    # Check if the working directory exists

    if not Path(args.working_dir).is_dir():
        print(f"Error: The working directory '{args.working_dir}' does not exist.")
        sys.exit(1)

    if args.use_dataset_example != -1:
        ds = datasets.load_from_disk("ai_metaphors/resources/subset")
        main(
            term_name=ds[args.use_dataset_example]["value"],
            term_definition=ds[args.use_dataset_example]["definition"],
            metaphor=ds[args.use_dataset_example]["metaphor"],
            generate_metaphor=args.generate_metaphor,
            executable_path=args.executable_path,
            working_dir=args.working_dir,
        )
    else:
        if not args.term_name.strip():
            print("Error: Term must not be empty.")
            sys.exit(1)  # Exit the program with an error code
        if not args.term_definition.strip():
            print("Error: Definition must not be empty.")
            sys.exit(1)  # Exit the program with an error code
        if not args.generate_metaphor and not args.metaphor.strip():
            print("Error: Metaphor must not be empty if not generating it.")
            sys.exit(1)  # Exit the program with an error code
        main(
            term_name=args.term_name,
            term_definition=args.term_definition,
            metaphor=args.metaphor,
            generate_metaphor=args.generate_metaphor,
            executable_path=args.executable_path,
            working_dir=args.working_dir,
        )
