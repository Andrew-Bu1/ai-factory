from fastapi import FastAPI
from app.api.v1 import router_v1

app = FastAPI(
    title="AI Factory", 
    version="1.0.0",
    docs_url="/swagger",
    description="API documentation for AI Factory",
    openapi_url="/openapi.json",
)
app.include_router(router_v1)