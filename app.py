from fastapi import FastAPI

from services.logger_service import logger
from services.huggingface_service import login_huggingface, download_huggingface_model, logout_huggingface
from controllers.app_controller import router as app_router
from controllers.chat_controller import router as chat_router

app = FastAPI()

app.include_router(app_router)
app.include_router(chat_router)

@app.on_event("startup")
async def startup_event():
    # login_huggingface()
    # download_huggingface_model()
    logger.info("Application startup complete. Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)")

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down the application...")
    logout_huggingface()
