@echo off
setlocal

:: Configuration
set ENV_NAME=venv
set REQUIREMENTS_FILE=requirements.txt
set APP_ENTRYPOINT=app:app
set ENV_PATH=%CD%\%ENV_NAME%

:: Check if conda is available
where conda >nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo Error: Conda is not installed or not in PATH
    exit /b 1
)

:: Check if environment exists
if not exist "%ENV_PATH%" (
    echo Creating conda environment in the current directory: %ENV_NAME%
    call conda create --prefix "%ENV_PATH%" python=3.11 -y
    if %ERRORLEVEL% neq 0 (
        echo Failed to create environment
        exit /b 1
    )
    echo Environment created successfully
)

:: check if database, model, pdfs folder exists else create
if not exist "%CD%\database" (
    mkdir "%CD%\database"
    echo Database folder created
)
if not exist "%CD%\model" (
    mkdir "%CD%\model"
    echo Model folder created
)
if not exist "%CD%\pdfs" (
    mkdir "%CD%\pdfs"
    echo PDFs folder created
)

:: Activate environment
echo Activating conda environment: %ENV_NAME%
call conda activate "%ENV_PATH%"
if %ERRORLEVEL% neq 0 (
    echo Failed to activate environment
    exit /b 1
)

:: Install requirements
if exist %REQUIREMENTS_FILE% (
    echo Installing requirements from %REQUIREMENTS_FILE%
    pip install -r %REQUIREMENTS_FILE%
    if %ERRORLEVEL% neq 0 (
        echo Failed to install requirements
        exit /b 1
    )
) else (
    echo Error: Requirements file %REQUIREMENTS_FILE% not found
    exit /b 1
)

:: Run the FastAPI application
echo Starting FastAPI application...
uvicorn %APP_ENTRYPOINT% --reload

endlocal
