//job("Python build") {
//    container(image = "python:3.10") {
//        shellScript {
//            content = """
//                echo "Setting up Python environment..."
//
//                echo "Installing system dependencies..."
//                apt-get update
//                apt-get install -y \
//                    libpango1.0-dev \
//                    libcairo2-dev \
//                    pkg-config
//
//                echo "Installing Poetry..."
//                curl -sSL https://install.python-poetry.org | python3 -
//                export PATH="/root/.local/bin:${'$'}PATH"
//
//                echo "Installing project dependencies..."
//                poetry lock --no-update
//                poetry install
//            """
//        }
//    }
//}

job("Code style check and format") {
    startOn {
        gitPush {}
    }

    container(image = "python:3.10") {

        shellScript {
            content = """
                echo "Setting up Python environment for code style check..."

                echo "Installing Ruff..."
                pip install ruff

                echo "Checking the code..."
                ruff check --output-format=github

                echo "Formatting the code..."
                ruff format --check
            """
        }
    }
}
