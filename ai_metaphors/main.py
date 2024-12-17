import datasets, argparse, os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from ai_metaphors.utils.text_utils import extract_json, extract_content
from ai_metaphors.providers.grazie_provider import GrazieProvider
from ai_metaphors.providers.manim_provider import ManimProvider
from grazie.api.client.gateway import AuthType, GrazieApiGatewayClient, GrazieAgent
from grazie.api.client.endpoints import GrazieApiGatewayUrls



def main(term_name: str = "", term_definition: str = "", metaphor: str = "", generate_metaphor: bool = False, executable_path: str = "", working_dir: str = "") :

    with open("/home/ynoviello/PycharmProjects/AI_Metaphors/token.secret", 'r') as t:
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
    term = {"value": term_name, "definition": term_definition,}

    if generate_metaphor:
        metaphor = extract_content(provider.get_metaphor(term))
    print(f"Metaphor: {metaphor}")


    # Creating classes
    classes = provider.get_classes(term, metaphor)
    print("Classes created")

    classes_dict = extract_json(classes)
    print("Classes extracted")
    
    desc = provider.get_description(term, metaphor, str(classes_dict))
    print("Description created")
    manim_code = provider.get_manim(term, metaphor, str(classes_dict), desc)
    print("Manim code created")
    manim_provider = ManimProvider(provider, term,
                                   executable=executable_path,
                                   working_dir=working_dir)
    manim_provider.write_python(manim_code, font_path="ai_metaphors/resources/JetBrainsSans-Regular.ttf", )
    error = manim_provider.execute_manim_script()
    return error


def parse_arguments():
    parser = argparse.ArgumentParser(description="Process term name, term definition, and metaphor.")
    parser.add_argument("--use_dataset_example", type=int, choices=range(-1, 14), default=-1,
                        help="Index of the example in the dataset to use directly")
    parser.add_argument("--term_name", type=str, default="", help="Name of the term")
    parser.add_argument("--term_definition", type=str, default="", help="Definition of the term")
    parser.add_argument("--metaphor", type=str, default="", help="Metaphor associated with the term")
    parser.add_argument("--generate_metaphor", action="store_true", default=False, help="Flag to generate the metaphor")
    
    parser.add_argument("--executable_path", type=str, default="~/anaconda3/envs/jetbrains/bin",
                        help="Path to the executable for ManimProvider")
    parser.add_argument("--working_dir", type=str, default="./manim_stuff",
                        help="Working directory for ManimProvider")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_arguments()

    # Check if the executable path exists
    if not os.path.exists(os.path.expanduser(args.executable_path)):
        print(f"Error: The executable path '{args.executable_path}' does not exist.")
        exit(1)

    # Check if the working directory exists
    if not os.path.isdir(args.working_dir):
        print(f"Error: The working directory '{args.working_dir}' does not exist.")
        exit(1)
    
    if args.use_dataset_example != -1:
        ds = datasets.load_from_disk("ai_metaphors/resources/subset")
        main(term_name=ds[args.use_dataset_example]["value"],
             term_definition=ds[args.use_dataset_example]["definition"],
             metaphor=ds[args.use_dataset_example]["metaphor"],
             executable_path=os.path.expanduser(args.executable_path),
             working_dir=args.working_dir)
    else:
        if not args.term_name.strip():
            print("Error: Term must not be empty.")
            exit(1)  # Exit the program with an error code
        if not args.term_definition.strip():
            print("Error: Definition must not be empty.")
            exit(1)  # Exit the program with an error code
        if not args.generate_metaphor:
            if not args.metaphor.strip():
                print("Error: Metaphor must not be empty if not generating it.")
                exit(1)  # Exit the program with an error code
        main(term_name=args.term_name,
             term_definition=args.term_definition,
             metaphor=args.metaphor,
             generate_metaphor=args.generate_metaphor,
             executable_path=os.path.expanduser(args.executable_path),
             working_dir=args.working_dir)
