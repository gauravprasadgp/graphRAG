import os
from neo4j import GraphDatabase
from vertexai.generative_models import GenerationConfig
from neo4j_graphrag.llm import VertexAILLM
from neo4j_graphrag.embeddings import VertexAIEmbeddings
from neo4j_graphrag.indexes import create_vector_index

URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "SERVICE_FILE.json"

INDEX_NAME = "text_embeddings"
EMBED_MODEL = "text-embedding-005"
LLM_MODEL = "gemini-2.0-flash"

driver = GraphDatabase.driver(URI, auth=AUTH)
embedder = VertexAIEmbeddings(model=EMBED_MODEL)

generation_config = GenerationConfig(temperature=0.0, response_mime_type="application/json")
llm = VertexAILLM(model_name=LLM_MODEL, generation_config=generation_config)

create_vector_index(
    driver,
    name=INDEX_NAME,
    label="Chunk",
    embedding_property="embedding",
    dimensions=768,
    similarity_fn="cosine",
)
