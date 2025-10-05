# GraphRAG FastAPI Application

This project provides a **modular FastAPI-based service** that integrates:
- **Neo4j Graph Database**
- **Vertex AI Embeddings & LLM (Gemini)**
- **GraphRAG (Graph-based Retrieval-Augmented Generation)**

It enables:
- 🧠 **Ingestion** of PDF documents into a Neo4j Knowledge Graph  
- 🔍 **Querying** the knowledge graph using a Vertex AI LLM with RAG-style retrieval  

---

## 🧩 Project Structure

```
graphrag_app/
│
├── app/
│   ├── core/
│   │   └── config.py               # Configuration for Neo4j, VertexAI, and model setup
│   ├── services/
│   │   ├── ingestion_service.py    # Logic for PDF ingestion using GraphRAG
│   │   └── query_service.py        # Logic for semantic retrieval and LLM query generation
│   ├── routers/
│   │   ├── ingest_router.py        # `/api/ingest` route handler
│   │   └── query_router.py         # `/api/query` route handler
│   └── main.py                     # FastAPI application entrypoint
│
└── README.md
```

---

## ⚙️ Setup Instructions

### 1️⃣ **Run Neo4j using Docker**

If you don’t have Docker yet:
```bash
# Install Docker (if not already installed)
https://docs.docker.com/get-docker/
```

Then start Neo4j with APOC enabled:
```bash
docker run -d   --name neo4j   -p 7474:7474 -p 7687:7687   -e NEO4J_AUTH=neo4j/password   -e NEO4JLABS_PLUGINS='["apoc"]'   -e NEO4J_apoc_export_file_enabled=true   -e NEO4J_apoc_import_file_enabled=true   -e NEO4J_apoc_uuid_enabled=true   -v $HOME/neo4j/data:/data   neo4j
```

✅ After running this:
- Neo4j Browser: [http://localhost:7474](http://localhost:7474)
- Username: `neo4j`
- Password: `password`
- Bolt URI: `neo4j://localhost:7687`

Keep this container running — your FastAPI app will connect to it automatically.

---

### 3️⃣ **Create a Virtual Environment**
```bash
python3 -m venv venv
source venv/bin/activate      # macOS/Linux
venv\Scripts\activate       # Windows
```

---

### 4️⃣ **Install Dependencies**
```bash
pip install -r requirements.txt
```

If it fails, install manually:
```bash
pip install fastapi uvicorn neo4j google-cloud-aiplatform neo4j-graphrag python-multipart
```

---

### 5️⃣ **Configure Vertex AI Credentials**
Set your Google service account credentials:
```bash
export GOOGLE_APPLICATION_CREDENTIALS="SERVICE_FILE.json"
```

Ensure that the `SERVICE_FILE.json` file has permission for **Vertex AI embeddings** and **Gemini LLM** APIs.

---

### 6️⃣ **Verify Config**
Check that your Neo4j configuration matches in `app/core/config.py`:
```python
URI = "neo4j://localhost:7687"
AUTH = ("neo4j", "password")
```

---

### 7️⃣ **Run the FastAPI App**
```bash
uvicorn app.main:app --reload
```

Expected output:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

---

## 🧭 Test the API

### 🩺 **Health Check**
```bash
curl http://localhost:8000/health
```
Response:
```json
{"status": "ok"}
```

---

### 📥 **Ingest PDF**
Uploads and ingests a document into Neo4j.
```bash
curl -X POST "http://localhost:8000/api/ingest"      -F "file=@file_to_ingest.pdf"
```
Response:
```json
{
  "status": "success",
  "message": "File distance.pdf ingested successfully."
}
```

---

### 🔍 **Query the Knowledge Graph**
Ask questions and get contextual answers from LLM.
```bash
curl -X POST "http://localhost:8000/api/query"      -F "query=how to calculate the distance"
```
Response:
```json
{
  "query": "how to calculate the distance",
  "retrieved_contexts": ["chunk1...", "chunk2..."],
  "llm_response": "Distance can be calculated by ..."
}
```

---

## 🧰 Useful Neo4j Commands

| Command | Description |
|----------|-------------|
| `docker stop neo4j` | Stop Neo4j container |
| `docker start neo4j` | Start Neo4j container |
| `docker logs -f neo4j` | Tail logs for Neo4j container |

---

## 🧪 Explore API Docs

- Swagger UI → [http://localhost:8000/docs](http://localhost:8000/docs)
- ReDoc UI → [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

## 🧠 How It Works

### Ingestion Flow:
1. PDF is uploaded via `/api/ingest`
2. `SimpleKGPipeline` splits text → generates embeddings → stores chunks in Neo4j
3. Vector index is auto-created on startup

### Query Flow:
1. User query → vectorized via `VertexAIEmbeddings`
2. `VectorRetriever` fetches top chunks from Neo4j
3. Context is passed to `VertexAI LLM` for answer generation

---

## 🧰 Key Technologies

| Component | Description |
|------------|-------------|
| **FastAPI** | Web framework for serving ingestion & retrieval APIs |
| **Neo4j (Docker)** | Graph database to store chunks and embeddings |
| **Vertex AI** | Embeddings & LLM (Gemini-2.0-flash) for RAG |
| **GraphRAG** | Handles KG pipeline, embedding, and vector retrieval |

---

## 🧪 Future Enhancements
- ✅ Add **streaming responses** for LLM output  
- ✅ Introduce **background task queue** for async ingestion (Celery / Redis)  
- ✅ Add **auth & rate limiting**

---

## 🧑‍💻 Author
**Gaurav Prasad**  
AI & Full Stack | GraphRAG / Vertex AI / Spring Boot / FastAPI 

---

## 🪪 License
MIT License © 2025 Gaurav Prasad
