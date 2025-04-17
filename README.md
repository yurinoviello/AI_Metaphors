# AI Metaphors

This Python module generates metaphors, associated classes, descriptions, and Manim animation code for a given term. It integrates several providers, including **GrazieProvider** and **ManimProvider**, to produce results and animations.

## **Overview**

The script performs the following steps:

1. **Input**: A term name and its definition.
2. **Metaphor Generation**: Optionally generates a metaphor using the Grazie API.
3. **Class Creation**: Produces JSON-formatted classes based on the term and metaphor.
4. **Description Generation**: Generates a description of the metaphor's animation.
5. **Manim Code**: Creates animation code using Manim based on the provided term, metaphor, classes, and description.
6. **Execution**: Runs the generated Manim script to produce the animation.

---

## **Dependencies**

Ensure the following tools and libraries are installed:

- **Python 3.10+**
- **Manim Community Edition** (refer to the [official page](https://github.com/ManimCommunity/manim) for installation troubles)
- Hugging Face **datasets**
- **Grazie API Client Library**

---

## **Folder and Token Requirements**

1. **Token File**:  
   Place the following tokens in a file named `.env` inside the project root folder.
   - `GRAZIE_JWT_TOKEN`: it will be used to authenticate via the `GrazieApiGatewayClient`
   - `POETRY_HTTP_BASIC_SPACE_GRAZIE_ML_USERNAME`
   - `POETRY_HTTP_BASIC_SPACE_GRAZIE_ML_PASSWORD`
   - `OPENAI_API_KEY`: it will be used to execute the video evaluation and text-to-speech feature

   You can rename the example file `.env.example` to `.env` and add your tokens inside it.

   ```
   ./AI_Metaphors/.env.example
   ```

2. **Manim working dir**:  
   Specify a directory in which the code related with animations and the output videos will be placed.

   For example:
   ```
   ./AI_Metaphors/animations
   ```
---

## Suggested Installation
To set up the project and install all dependencies, follow these steps using **Poetry**:
To set up the project and install all dependencies using **Poetry**, follow these steps:

1. **Clone the Repository**  
   Clone the project from GitHub to your local machine:

   ```bash
   git clone https://git.jetbrains.team/edu-research/AI_Metaphors.git
   cd AI_Metaphors
   ```

2. **Add the tokens to the local environment**

   Execute the following command to export the tokens in your shell.
   It will allow you to install the `grazie-api-gateway-client` package:

   ```bash
   set -o allexport && source .env && set +o allexport
   ```

3. **Install Dependencies**  
   Use Poetry to create a virtual environment and install all dependencies:

   ```bash
   poetry lock --no-update
   poetry install
   ```

   This command will:
   - Create a virtual environment for the project.
   - Install all required dependencies specified in `pyproject.toml`.

4. **Activate the Virtual Environment**  
   To activate the virtual environment created by Poetry, run:

   ```bash
   poetry shell
   ```

4. **Verify the Installation**  
   Run the following command to check that all dependencies are installed correctly:

   ```bash
   poetry run python ai_metaphors/main.py --help
   ```
   or simply
   ```bash
   ai-metaphors --help
   ```

---

## Alternative Installation with `pip`

1. **Add Tokens**
You can add the access token to the [pip config file](https://pip.pypa.io/en/stable/topics/configuration/).

2. **Install dependencies**
```bash
   pip install -r requirements.txt
```

3. **Additional Dependencies** (if needed)
```bash
   brew install cairo pkg-config
```
```bash
   brew install portaudio
```

4. **Run**
```bash
   python3 -m ai_metaphors.main --help
```
---

## **Usage**

Run the script with the following arguments:

### Command-Line Options

```bash
ai-metaphors [OPTIONS]
```

| **Option**                 | **Type** | **Description**                                                                                                                                    |
|----------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `--use-dataset-example`    | `int`    | Use an example from the dataset (index between 0 and 13). Set `-1` to disable. Default is `-1`.                                                    |
| `--term-name`              | `str`    | The name of the term (required if `use-dataset-example` is not set).                                                                               |
| `--term-definition`        | `str`    | Definition of the term (required).                                                                                                                 |
| `--metaphor`               | `str`    | The metaphor associated with the term. If `--generate-metaphor` is set, this will be ignored.                                                      |
| `--generate-metaphor-text` | `flag`   | Flag to generate the metaphor automatically.                                                                                                       |
| `--animation-type`         | `str`    | Type of animation to generate: `basic` (default, simple animation), `voice` (adds voice-over), or `avatar` (adds animated avatar with voice-over). |
| `--bin-directory`          | `str`    | Path to the executable for Manim. Default is `.venv/bin`.                                                                                          |
| `--working-dir`            | `str`    | Working directory for Manim output. Default: `./animations`.                                                                                       |
| `--llm-provider`           | `str`    | LLM provider service. Default: `grazie`.                                                                                                           |
| `--model`                  | `str`    | Language model to process with. Default: `openai-gpt-4o`.                                                                                          |
| `--model-manim`            | `str`    | LLM to process only the Manim script. Default: `default`.                                                                                          |
| `--temperature`            | `float`  | Temperature value to be used by the chosen language model. Default: `0.1`.                                                                         |
| `--vllm-fix`               | `flag`   | **Experimental** Perform an automatic vLLM analysis and code correction.                                                                           |
| `--auto-play`              | `flag`   | Automatically play the animation at the end of the execution.                                                                                      |
| `--high-quality`           | `flag`   | Generate a high-quality animation (1080p60). If not set, the default is 480p15.                                                                    |
| `--debug`                  | `flag`   | Activate debug mode.                                                                                                                               |
| `--config`                 | `str`    | Path to the config file from which other arguments will be read. If not provided, the arguments will be read from the command line.                |
### Example Usage

1. **With Manually Provided Inputs**:
   ```bash
   ai-metaphors --term-name Boolean --term-definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --metaphor "Imagine a light switch in your house. The switch can only be in one of two positions: ON or OFF.\n\n- When the switch is ON, it represents "true" – the light is working.\n- When the switch is OFF, it represents "false" – the light is not working.\n\nA Boolean is like this light switch. It can only hold one of two states: true (ON) or false (OFF)."
   ```

2. **Generating a Metaphor**:
   ```bash
   ai-metaphors --term-name Boolean --term-definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --generate-metaphor
   ```

3. **Using a Dataset Example**:
   ```bash
   ai-metaphors --use-dataset-example 0
   ```
   You can use terms, metaphors, and definitions from this dataset:

   | index | term                  |
   |-------|-----------------------|
   | 0     | `Boolean`             |
   | 1     | `append`              |
   | 2     | `break`               |
   | 3     | `else branch`         |
   | 4     | `replace`             |
   | 5     | `val`                 |
   | 6     | `var`                 |
   | 7     | `Class`               |
   | 8     | `Companion object`    |
   | 9     | `Extension functions` |
   | 10    | `Map`                 |
   | 11    | `Type alias `         |
   | 12    | `reversed`            |
   | 13    | `shuffled`            |

### Configuration File

You can use a YAML configuration file to set default values for command-line arguments. This is useful for:
- Saving commonly used settings
- Setting up different configurations for different use cases
- Sharing configurations with others

A sample configuration file is provided at `config/config.yaml` in the project directory.

**Usage with Configuration File**:
```bash
# Use a specific configuration file
ai-metaphors --config config/config.yaml
```
---

## **Output**

1. **Console Outputs**:
   - Displays the term name, term definition, generated metaphor, and progress messages for each step.
   - Outputs errors for missing paths or inputs.

2. **Manim Animation**:
   - The generated Manim script will be written to the working directory specified by `--working-dir`.
   - Manim will execute the script to generate the animation.

---

## **Error Handling**

The script checks for:
1. **Missing executable paths**:  
   If the `--bin-directory` does not exist, the script exits with an error.
2. **Missing working directories**:  
   If the `--working-dir` does not exist, the script exits with an error.
3. **Empty required inputs**:  
   If `--term-name` or `--term-definition` is empty, the script exits with an error.
4. **Metaphor Requirements**:  
   If `--generate-metaphor` is **not** used, a metaphor must be provided.

---

## Usage with Docker Compose

1. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   You can find example configurations in `.env.example` file.

2. **Configure your `.env` file**:

   Add _one of these_ LLM provider tokens (required):
   - `GRAZIE_JWT_TOKEN` or
   - `OPENAI_API_KEY`

   Note: Poetry authentication tokens are not needed for Docker setup.

3. **Configure the application**:
   Edit the `config/config.yaml` file to set your desired parameters.

4. **Build and run with Docker Compose**:
   ```bash
   # Build the container
   docker-compose build

   # Run the application
   docker-compose up
   ```

5. **Access Generated Content**:
   - Generated animations will be available in the `/animations` folder
   - This folder is mapped as a volume in [`docker-compose.yml`](docker-compose.yml)

Notes:
- Make sure Docker and Docker Compose are installed on your system
- The first run will take longer as it needs to build the container
- All dependencies will be automatically installed in the container
- All configuration is now done through the `config/config.yaml` file instead of command-line arguments

**Development Notes**:
- When making changes to the configuration or dependencies:
  ```bash
  docker-compose build --no-cache
  ```
