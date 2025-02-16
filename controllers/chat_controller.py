from fastapi import APIRouter, File, Query, UploadFile
from pydantic import BaseModel
from services.chatbot_service import answer_question, answer_question_plain, handle_clear_database, handle_upload

router = APIRouter()

class QuestionRequest(BaseModel):
    question: str

@router.post("/ask", tags=["Ask"])
async def ask_question(request: QuestionRequest, context: str = Query(None)):
    """
    Endpoint to ask a question and get a response from the local model.
    """
    try:
        if context is None:
            answer = answer_question_plain(request.question)
            return {"question": request.question, "answer": answer}

        answer = answer_question(request.question, context)
        return {"question": request.question, "answer": answer}
    except Exception as e:
        return {"error": str(e)}


@router.post('/upload', tags=["Ask"])
async def upload_file(file: UploadFile = File(...)):
    """
    Endpoint to upload a file.
    """
    try:
        res = await handle_upload(file)
        return {"message": res}
    except Exception as e:
        return {"error": str(e)}


@router.get("/clear", tags=["Ask"])
def clear_database(context: str = Query(...)):
    """
    Endpoint to clear the database.
    """
    try:
        msg = handle_clear_database(context)
        return {"message": msg}
    except Exception as e:
        return {"error": str(e)}