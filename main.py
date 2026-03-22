import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
src_path = os.path.join(current_dir, "src")
sys.path.insert(0, src_path)

from dddpy.shared.logging.logging import Logger
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import ValidationError

from api.brand.router import router as router_brand
from api.manual_record.router import router as router_manual_record
from api.brand_manual_vector.router import router as router_brand_manual_vector
from api.content_log.router import router as router_content_log


from dddpy.shared.schemas.response_schema import (
    ResponseErrorSchema,
)


logger = Logger("content_suite")
logger.add_inside_method("startup")
logger.info("Starting content_suite app")
print("aca toy")


app = FastAPI(title="Content Suite AI API")

origins = [
    "http://localhost:8080",
    "http://localhost:3000",
    "http://localhost:8000",
]

# Configuración de CORS para Bolt.new / v0.dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # En producción usa tu URL de Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "online", "message": "Content Suite AI Backend"}


@app.exception_handler(ValidationError)
async def pydantic_exception_handler(request: Request, exc: ValidationError):

    error_response = ResponseErrorSchema(success=False, message=str(exc))
    return JSONResponse(content=error_response.dict(), status_code=400)


@app.exception_handler(ValueError)
async def valueError_exception_handler(request: Request, exc: ValueError):
    error_response = ResponseErrorSchema(success=False, message=str(exc))
    return JSONResponse(content=error_response.dict(), status_code=400)


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    error_response = ResponseErrorSchema(success=False, message=str(exc))
    return JSONResponse(content=error_response.dict(), status_code=500)


app.include_router(router_brand, prefix="/brand")
app.include_router(router_manual_record, prefix="/manual_record")
app.include_router(router_brand_manual_vector, prefix="/brand_manual_vector")
app.include_router(router_content_log, prefix="/content_log")
