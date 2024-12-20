job("Python Build") {
    // Trigger: Start the pipeline on every push
    startOn {
        gitPush {}
    }
    // Environment variables
    env["JETBRAINS_MONO_VERSION"] = "2.304"
    env["PYTHON_VERSION"] = "3.10"

    pipeline {
        stage("Setup Environment") {
            container("ubuntu:latest") {
                kotlinScript {
                    scriptContent = """
                        # Checkout code
                        git clone ${'$'}{repo.url}

                        # Install system dependencies
                        sudo apt-get update
                        sudo apt-get install -y \
                            libpango1.0-dev \
                            libcairo2-dev \
                            pkg-config

                        # Install Poetry
                        curl -sSL https://install.python-poetry.org | python3 -
                        echo "$HOME/.local/bin" >> ${'$'}PATH

                        # Install project dependencies
                        poetry lock --no-update
                        poetry install
                    """.trimIndent()
                }
            }
        }

        stage("Code Style Checks") {
            container("ubuntu:latest") {
                kotlinScript {
                    scriptContent = """
                        # Checkout code
                        git clone ${'$'}{repo.url}

                        # Install Python
                        sudo apt install -y python${'$'}PYTHON_VERSION python3-pip

                        # Install Ruff linter/formatter
                        pip install ruff

                        # Lint the code
                        ruff check --output-format=github

                        # Format the code
                        ruff format --check
                    """.trimIndent()
                }
            }
        }
    }
}
