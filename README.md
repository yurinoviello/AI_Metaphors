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

- Python 3.10+
- Manim Community Edition
- Hugging Face `datasets`
- Grazie API Client Library


### Suggested Installation
To set up the project and install all dependencies, follow these steps using **Poetry**:
To set up the project and install all dependencies using **Poetry**, follow these steps:

1. **Clone the Repository**  
   Clone the project from GitHub to your local machine:

   ```bash
   git clone https://github.com/your-username/AI_Metaphors.git
   cd AI_Metaphors
   ```

2. **Install Dependencies**  
   Use Poetry to create a virtual environment and install all dependencies:

   ```bash
   poetry install
   ```

   This command will:
   - Create a virtual environment for the project.
   - Install all required dependencies specified in `pyproject.toml`.

3. **Activate the Virtual Environment**  
   To activate the virtual environment created by Poetry, run:

   ```bash
   poetry shell
   ```

4. **Verify the Installation**  
   Run the following command to check that all dependencies are installed correctly:

   ```bash
   poetry run python ai_metaphors/main.py --help
   ```
   or
   ```bash
   python ai_metaphors/main.py --help
   ```

---


### Manual Installation (not advised)

Install the required Python libraries with (TO IMPROVE):

```bash
pip install -r requirements.txt
```
TODO
...
---

## **Folder and File Requirements**

1. **Token File**:  
   Place your Grazie JWT token in a file named `token.secret` inside the project root folder:

   ```
   ./AI_Metaphors/token.secret
   ```

2. **Manim working dir**:  
   Specify a directory in which the code related with animations and the output videos will be placed.

   For example:
   ```
   ./AI_Metaphors/animations
   ```
---

## **Usage**

Run the script with the following arguments:

### Command-Line Options

```bash
python main.py [OPTIONS]
```

| **Option**               | **Type**  | **Description**                                                                                       |
|--------------------------|-----------|-------------------------------------------------------------------------------------------------------|
| `--use_dataset_example`  | `int`     | Use an example from the dataset (index between 0 and 13). Set `-1` to disable. Default is `-1`.       |
| `--term_name`            | `str`     | The name of the term (required if `use_dataset_example` is not set).                                  |
| `--term_definition`      | `str`     | Definition of the term (required).                                                                    |
| `--metaphor`             | `str`     | The metaphor associated with the term. If `--generate_metaphor` is set, this will be ignored.         |
| `--generate_metaphor`    | `flag`    | Flag to generate the metaphor automatically using the Grazie API.                                     |
| `--executable_path`      | `str`     | Path to the executable for Manim. Default: `""`. Not needed if the project was installed with poetry. |
| `--working_dir`          | `str`     | Working directory for Manim output. Default: `./animations`.                                          |

### Example Usage

1. **With Manually Provided Inputs**:
   ```bash
   python ai_metaphors/main.py --term_name Boolean --term_definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --metaphor "Imagine a light switch in your house. The switch can only be in one of two positions: ON or OFF.\n\n- When the switch is ON, it represents "true" – the light is working.\n- When the switch is OFF, it represents "false" – the light is not working.\n\nA Boolean is like this light switch. It can only hold one of two states: true (ON) or false (OFF)."
   ```

2. **Generating a Metaphor**:
   ```bash
   python ai_metaphors/main.py --term_name Boolean --term_definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --generate_metaphor
   ```

3. **Using a Dataset Example**:
   ```bash
   python ai_metaphors/main.py --use_dataset_example 0
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


---

## **Output**

1. **Console Outputs**:
   - Displays the term name, term definition, generated metaphor, and progress messages for each step.
   - Outputs errors for missing paths or inputs.

2. **Manim Animation**:
   - The generated Manim script will be written to the working directory specified by `--working_dir`.
   - Manim will execute the script to generate the animation.

---

## **Error Handling**

The script checks for:
1. **Missing executable paths**:  
   If the `--executable_path` does not exist, the script exits with an error.
2. **Missing working directories**:  
   If the `--working_dir` does not exist, the script exits with an error.
3. **Empty required inputs**:  
   If `term_name` or `term_definition` is empty, the script exits with an error.
4. **Metaphor Requirements**:  
   If `--generate_metaphor` is **not** used, a metaphor must be provided.

---

## **Troubleshooting**

1. **Token Issues**:
   - Ensure your `token.secret` file contains a valid Grazie JWT token.

2. **Manim Issues**:
   - Verify that the Manim installation is functional and accessible through the provided executable path.

---