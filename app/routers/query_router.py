from fastapi import APIRouter, Form
from app.services.query_service import query_graph_data

router = APIRouter()

@router.post("/query")
async def query_graph(query: str = Form(...)):
    return await query_graph_data(query)
