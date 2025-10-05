import asyncio
import logging
from neo4j_graphrag.experimental.components.text_splitters.fixed_size_splitter import FixedSizeSplitter
from neo4j_graphrag.experimental.pipeline.kg_builder import SimpleKGPipeline
from app.core.config import llm, driver, embedder

logging.basicConfig(level=logging.INFO)

async def ingest_pdf_file(file_path: str):
    try:
        kg_builder_pdf = SimpleKGPipeline(
            llm=llm,
            driver=driver,
            text_splitter=FixedSizeSplitter(chunk_size=500, chunk_overlap=100),
            embedder=embedder,
            from_pdf=True,
        )
        await kg_builder_pdf.run_async(file_path=file_path)
        return {"status": "success", "message": f"File {file_path} ingested successfully."}
    except Exception as e:
        logging.exception("Error during PDF ingestion")
        raise e
