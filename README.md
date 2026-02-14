# AI Metaphors

This Python module generates metaphors, associated classes, descriptions, and Manim animation code for a given term. It integrates several providers, including **GrazieProvider** and **ManimProvider**, to produce results and animations.

## Project Structure

The project is organized into three main components:

#### Common Module
The `ai_metaphors/common` directory contains shared functionality used by # Alternative Installation with `pip`

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
---both the CLI and server components:
- **Core utilities**: Base functionality for processing metaphors, handling paths, and working with different term types
- **Video generation**: Components for generating videos from different sources (academic definitions, code, general definitions)
- **Avatar**: Functionality for creating animated avatars
- **Output structure**: Standardized output formats

#### CLI Module
The `ai_metaphors/cli` directory contains the command-line interface for the application:
- **main.py**: Entry point for CLI execution with argument parsing
- **config_arg_parser**: Utilities for parsing configuration from files and command line arguments

#### Server Module
The `ai_metaphors/server` directory contains the FastAPI server implementation:
- **API endpoints**: REST API endpoints for video generation and status checking
- **Database models**: Data models for storing video tasks
- **Schemas**: Pydantic models for request/response validation
- **Services**: Business logic for processing video generation tasks
- **Settings**: Server configuration

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

## Environment Variables

The following environment variables are required to run the application (see `.env.example`):

- **GRAZIE_JWT_TOKEN**: Authentication token for the Grazie API
- **OPENAI_API_KEY**: API key for OpenAI services (used for video evaluation and text-to-speech)
- **BUCKET_NAME**: AWS S3 bucket name for storing generated videos (server mode)
- **AWS_ACCESS_KEY_ID**: AWS access key for S3 storage
- **AWS_SECRET_ACCESS_KEY**: AWS secret key for S3 storage

### Running with Docker Compose

There are two ways to run the application using Docker Compose:

#### 1. CLI Mode

CLI mode runs the application as a one-time process that generates a video based on the configuration in `config/config.yaml`.

```bash
# Build the container
docker-compose build ai-metaphors-cli

# Run the application in CLI mode
docker-compose run ai-metaphors-cli
```

The CLI mode:
- Uses the configuration from `config/config.yaml`
- Generates a single video based on the configuration
- Outputs the video to the `/animations` directory
- Exits after completion

#### 2. Server Mode

Server mode runs the application as a REST API service that can accept multiple video generation requests.

```bash
# Build the container
docker-compose build ai-metaphors-server

# Run the application in server mode
docker-compose up ai-metaphors-server
```

The server mode:
- Starts a FastAPI server on port 8898
- Provides REST API endpoints for video generation
- Processes video generation tasks asynchronously
- Stores videos in an S3 bucket
- Provides endpoints to check task status

API endpoints:
- `POST /video`: Submit a new video generation task
- `GET /video/tasks/{task_id}`: Check the status of a specific task
- `GET /video/tasks`: List all tasks

## **Usage**

Run the script with the following arguments:
```bash
ai-metaphors [OPTIONS]
```

| **Option**                 | **Type** | **Description**                                                                                                                                    |
|----------------------------|----------|----------------------------------------------------------------------------------------------------------------------------------------------------|
| `--use-dataset-example`    | `int`    | Use an example from the dataset (index between 0 and 13). Set `-1` to disable. Default is `-1`.                                                    |
| `--term-name`              | `str`    | The name of the term (required if `use-dataset-example` is not set).                                                                               |
| `--term-definition`        | `str`    | Definition of the term (required).                                                                                                                 |
| `--term-type`              | `str`    | Type of term: `code`, `definition`, or `academic-definition`. Default is `definition`.                                                             |
| `--metaphor`               | `str`    | The metaphor associated with the term. If `--generate-metaphor` is set, this will be ignored.                                                      |
| `--generate-metaphor-text` | `flag`   | Flag to generate the metaphor automatically.                                                                                                       |
| `--animation-type`         | `str`    | Type of animation to generate: `basic` (default, simple animation), `voice` (adds voice-over), `avatar` (adds animated avatar with voice-over), or `cartoon-avatar` (adds cartoon-style avatar with voice-over). |
| `--bin-directory`          | `str`    | Path to the executable for Manim. Default is `.venv/bin`.                                                                                          |
| `--working-dir`            | `str`    | Working directory for Manim output. Default: `./animations`.                                                                                       |
| `--model`                  | `str`    | Language model to process with. Default: `openai-gpt-5-2`.                                                                                          |
| `--model-classes`          | `str`    | LLM to be used specifically for processing classes. Default: `default`.                                                                            |
| `--model-manim`            | `str`    | LLM to process only the Manim script. Default: `default`.                                                                      |
| `--temperature`            | `float`  | Temperature value to be used by the chosen language model. Default: `0.1`.                                                                         |
| `--vllm-fix`               | `flag`   | **Experimental** Perform an automatic vLLM analysis and code correction.                                                                           |
| `--auto-play`              | `flag`   | Automatically play the animation at the end of the execution.                                                                                      |
| `--high-quality`           | `flag`   | Generate a high-quality animation (1080p60). If not set, the default is 480p15.                                                                    |
| `--debug`                  | `flag`   | Activate debug mode.                                                                                                                               |
| `--config`                 | `str`    | Path to the config file from which other arguments will be read. If not provided, the arguments will be read from the command line.                 |

### Example Usage

1. **With Manually Provided Inputs**:
   ```bash
   ai-metaphors --term-name Boolean --term-definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --metaphor "Imagine a light switch in your house. The switch can only be in one of two positions: ON or OFF.\n\n- When the switch is ON, it represents "true" – the light is working.\n- When the switch is OFF, it represents "false" – the light is not working.\n\nA Boolean is like this light switch. It can only hold one of two states: true (ON) or false (OFF)."
   ```

2. **Generating a Metaphor**:
   ```bash
   ai-metaphors --term-name Boolean --term-definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --generate-metaphor-text
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
   If `--generate-metaphor-text` is **not** used, a metaphor must be provided.

---

**Development Notes**:
- When making changes to the configuration or dependencies:
  ```bash
  docker-compose build --no-cache
  ```