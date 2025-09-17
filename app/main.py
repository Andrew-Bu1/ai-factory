from fastapi import FastAPI
from fastapi.responses import JSONResponse
from app.api.v1 import router_v1
from app.core.logging import setup_logging
from app.api.errors import APIError

setup_logging()

app = FastAPI(
    title="AI Factory", 
    version="1.0.0",
    docs_url="/swagger",
    description="API documentation for AI Factory",
    openapi_url="/openapi.json",
)
app.include_router(router_v1)

@app.exception_handler(APIError)
async def api_error_handler(request, exc: APIError):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail},
    )