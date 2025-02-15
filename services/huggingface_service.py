import os
import logging
from huggingface_hub import snapshot_download, login, logout
from services.logger_service import logger

from dotenv import load_dotenv
load_dotenv()

def login_huggingface():
    try:
        # Replace with your actual token or use environment variables for security
        login(token=os.getenv("HUGGINGFACE_TOKEN"))
        logger.info("Successfully logged in to Hugging Face Hub")
    except Exception as e:
        logger.error(f"Failed to login to Hugging Face: {str(e)}")
        raise

def download_huggingface_model():
    """
    Downloads a model from Hugging Face Hub.
    """
    model_repo = "jony-jas/DeepSeek-R1-Distill-Llama-8B-Electrical-engineering"
    local_dir = f"./model/{model_repo.replace('/', '--')}"
    
    try:
        logger.info("Starting model download...")
        snapshot_download(
            repo_id=model_repo,
            local_dir=local_dir
        )
        abs_path = os.path.abspath(local_dir)
        logger.info(f"Successfully downloaded model to {abs_path}")
    
    except Exception as e:
        logger.error(f"Failed to download model: {str(e)}")
        raise

def logout_huggingface():
    try:
        logout()
        logger.info("Successfully logged out of Hugging Face Hub")
    except Exception as e:
        logger.error(f"Failed to logout of Hugging Face: {str(e)}")
        raise
