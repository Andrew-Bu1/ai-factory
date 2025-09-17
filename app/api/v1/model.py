from fastapi import APIRouter


router = APIRouter(tags=["Model"])

@router.get("/models")
async def list_models():
    return


@router.get("/models/{model_id}")
async def get_model(model_id: str):
    return

@router.put("/models/{model_id}")
async def update_model(model_id: str):
    return

@router.delete("/models/{model_id}")
async def delete_model(model_id: str):
    return

@router.post("/models")
async def create_model():
    return  