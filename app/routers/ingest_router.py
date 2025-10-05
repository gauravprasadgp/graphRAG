import os
from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse
from app.services.ingestion_service import ingest_pdf_file

router = APIRouter()

@router.post("/ingest")
async def ingest_pdf(file: UploadFile):
    try:
        temp_path = f"/tmp/{file.filename}"
        with open(temp_path, "wb") as f:
            f.write(await file.read())
        result = await ingest_pdf_file(temp_path)
        return result
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
