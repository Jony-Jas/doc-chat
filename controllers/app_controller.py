from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "message": "Everything is working fine!"}
