from fastapi import APIRouter


router = APIRouter()

@router.get("/", tags=["Root"])
async def root():
    return {"message": "Welcome to the API. Visit /docs for API documentation."}


@router.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}