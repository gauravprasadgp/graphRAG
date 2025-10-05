import os

from fastapi import FastAPI
from app.routers import ingest_router, query_router

app = FastAPI(
    title="GraphRAG Modular FastAPI",
    description="RAG app with Neo4j + Vertex AI integration",
    version="1.0.0",
)

app.include_router(ingest_router.router, prefix="/api")
app.include_router(query_router.router, prefix="/api")

@app.get("/health")
async def health_check():
    return {"status": "ok"}
