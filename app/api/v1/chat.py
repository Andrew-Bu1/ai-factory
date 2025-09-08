from fastapi import APIRouter, Depends

router = APIRouter()


@router.post("/chat")
async def chat():
    return