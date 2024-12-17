# AI Metaphors Pipeline

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
- Grazie API Client Library (custom implementation)

Install the required Python libraries with:

```bash
pip install -r requirements.txt
```

---

## **Folder and File Requirements**

1. **Token File**:  
   Place your Grazie JWT token in a file named `token.secret` inside the project root folder:

   ```
   ./AI_Metaphors/token.secret
   ```

2. **Manim working dir**:  
   If you plan to use preloaded term examples, place a Hugging Face dataset in:  
   ```
   ./AI_Metaphors/manim_stuff
   ```
---

## **Usage**

Run the script with the following arguments:

### Command-Line Options

```bash
python main.py [OPTIONS]
```

| **Option**               | **Type**  | **Description**                                                                                                                                         |
|--------------------------|-----------|---------------------------------------------------------------------------------------------------------------------------------------------------------|
| `--use_dataset_example`  | `int`     | Use an example from the dataset (index between 0 and 15). Set `-1` to disable. Default is `-1`.                                                         |
| `--term_name`            | `str`     | The name of the term (required if `use_dataset_example` is not set).                                                                                    |
| `--term_definition`      | `str`     | Definition of the term (required).                                                                                                                     |
| `--metaphor`             | `str`     | The metaphor associated with the term. If `--generate_metaphor` is set, this will be ignored.                                                          |
| `--generate_metaphor`    | `flag`    | Flag to generate the metaphor automatically using the Grazie API.                                                                                      |
| `--executable_path`      | `str`     | Path to the executable for Manim. Default: `~/anaconda3/envs/jetbrains/bin`.                                                                            |
| `--working_dir`          | `str`     | Working directory for Manim output. Default: `./manim_stuff`.                                                                                          |

### Example Usage

1. **With Manually Provided Inputs**:
   ```bash
   python main.py --term_name "Black Hole" --term_definition "A region of space where gravity is so strong that nothing can escape."
   ```

2. **Generating a Metaphor**:
   ```bash
   python ai_metaphors/main.py --term_name Boolean --term_definition 'A data type that has one of two possible values (usually denoted true and false) intended to represent the two truth values of logic and Boolean algebra.' --metaphor "Imagine a light switch in your house. The switch can only be in one of two positions: ON or OFF.\n\n- When the switch is ON, it represents "true" – the light is working.\n- When the switch is OFF, it represents "false" – the light is not working.\n\nA Boolean is like this light switch. It can only hold one of two states: true (ON) or false (OFF)."
   ```

3. **Using a Dataset Example**:
   ```bash
   python ai_metaphors/main.py --use_dataset_example 3
   ```

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