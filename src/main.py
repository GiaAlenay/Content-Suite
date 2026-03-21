from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings

app = FastAPI(title="Content Suite AI API")

# Configuración de CORS para Bolt.new / v0.dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # En producción usa tu URL de Render
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"status": "online", "message": "Content Suite AI Backend"}
