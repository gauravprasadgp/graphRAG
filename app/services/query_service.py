import logging
from fastapi.responses import JSONResponse
from neo4j_graphrag.retrievers import VectorRetriever
from app.core.config import driver, embedder, llm, INDEX_NAME

async def query_graph_data(query: str):
    try:
        vector_retriever = VectorRetriever(
            driver,
            index_name=INDEX_NAME,
            embedder=embedder,
            return_properties=["text"],
        )
        results = vector_retriever.get_search_results(query_text=query, top_k=3)
        contexts = [r["text"] for r in results.records]

        prompt = f"Answer based on the following context:\n{contexts}\nQuestion: {query}"
        response = llm.generate_text(prompt)

        return {
            "query": query,
            "retrieved_contexts": contexts,
            "llm_response": response.text if hasattr(response, "text") else str(response),
        }
    except Exception as e:
        logging.exception("Error during query")
        return JSONResponse(status_code=500, content={"error": str(e)})
