#!/bin/bash
set -e  # Exit immediately if a command exits with a non-zero status

# Configuration
ENV_NAME="venv"
REQUIREMENTS_FILE="requirements.txt"
APP_ENTRYPOINT="app:app"
ENV_PATH="$(pwd)/$ENV_NAME"

# Check if conda is available
if ! command -v conda >/dev/null 2>&1; then
    echo "Error: Conda is not installed or not in PATH"
    exit 1
fi

# Source conda.sh to enable 'conda activate'
CONDA_BASE=$(conda info --base)
if [ -f "$CONDA_BASE/etc/profile.d/conda.sh" ]; then
    source "$CONDA_BASE/etc/profile.d/conda.sh"
else
    echo "Warning: conda.sh not found. Conda activation may fail."
fi

# Check if the conda environment exists; if not, create it
if [ ! -d "$ENV_PATH" ]; then
    echo "Creating conda environment in the current directory: $ENV_NAME"
    conda create --prefix "$ENV_PATH" python=3.11 -y
    if [ $? -ne 0 ]; then
        echo "Failed to create environment"
        exit 1
    fi
    echo "Environment created successfully"
fi

# Ensure the necessary folders exist; create them if they don't
for dir in "database" "model" "pdfs"; do
    if [ ! -d "$(pwd)/$dir" ]; then
        mkdir "$(pwd)/$dir"
        echo "$dir folder created"
    fi
done

# Activate the conda environment
echo "Activating conda environment: $ENV_NAME"
conda activate "$ENV_PATH"
if [ $? -ne 0 ]; then
    echo "Failed to activate environment"
    exit 1
fi

# Install requirements if the requirements file exists
if [ -f "$REQUIREMENTS_FILE" ]; then
    echo "Installing requirements from $REQUIREMENTS_FILE"
    pip install -r "$REQUIREMENTS_FILE"
    if [ $? -ne 0 ]; then
        echo "Failed to install requirements"
        exit 1
    fi
else
    echo "Error: Requirements file $REQUIREMENTS_FILE not found"
    exit 1
fi

# Run the FastAPI application using uvicorn
echo "Starting FastAPI application..."
uvicorn "$APP_ENTRYPOINT" --reload
