# Agentic RAG Pipeline

Production-grade **Retrieval-Augmented Generation (RAG)** system with **LangGraph agentic workflows**, distributed task processing, and enterprise observability.

## 🎯 Architecture Overview

This system implements a sophisticated RAG pipeline that solves enterprise LLM failure modes:

```
┌─────────────────────────────────────────────────────────────────┐
│                    ADVANCED INGESTION PIPELINE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Document Input                                                  │
│      │                                                           │
│      ├─→ Semantic Chunking (sentence embeddings)               │
│      │    - Similarity threshold: 0.5                          │
│      │    - Tracks embedding distances                         │
│      │                                                           │
│      ├─→ Hierarchical Chunking                                 │
│      │    - Child chunks: 128 tokens                           │
│      │    - Parent chunks: 512 tokens                          │
│      │    - Overlap: 20 tokens                                 │
│      │                                                           │
│      ├─→ Embedding Generation (OpenAI text-embedding-3-small) │
│      │    - 1536-dimensional vectors                          │
│      │    - Async batch processing                            │
│      │                                                           │
│      └─→ Celery Tasks (Distributed Processing)                │
│           - Async ingestion                                    │
│           - Retry logic (max 3 attempts)                       │
│           - Time limits (25/30 minutes)                        │
│                                                                   │
│  Storage:                                                        │
│  - Qdrant Vector DB (dense embeddings)                         │
│  - PostgreSQL (metadata)                                        │
│  - Redis (cache layer)                                          │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                   HYBRID RETRIEVAL SYSTEM                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  User Query                                                      │
│      │                                                           │
│      ├─→ Dense Retrieval (Qdrant)                              │
│      │    - Semantic similarity search                         │
│      │    - Vector dimension: 1536                             │
│      │    - Top K results: 5                                   │
│      │                                                           │
│      ├─→ Sparse Retrieval (BM25)                               │
│      │    - Keyword-based ranking                             │
│      │    - Rank-BM25 algorithm                               │
│      │    - Top K results: 5                                   │
│      │                                                           │
│      └─→ Reciprocal Rank Fusion (RRF)                          │
│           - BM25 weight: 0.4                                   │
│           - Dense weight: 0.6                                  │
│           - RRF k parameter: 60                                │
│           - Final ranked results                               │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│              AGENTIC LANGGRAPH LOOP WITH SELF-CORRECTION         │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  1. Intent Router                                               │
│     - Routes query to appropriate handler                       │
│     - Uses Llama-3 or GPT-4-turbo                              │
│     - Semantic intent detection                                │
│                                                                   │
│  2. Retrieve Context                                            │
│     - Hybrid search (BM25 + Dense + RRF)                      │
│     - Top K documents                                          │
│                                                                   │
│  3. Generate Answer                                             │
│     - LLM with system prompt                                   │
│     - Grounded in retrieved context                            │
│                                                                   │
│  4. Self-Correction Loop ← FEEDBACK MECHANISM                  │
│     │                                                           │
│     ├─→ Context Relevance Eval                                │
│     │    - Threshold: 0.7                                     │
│     │    - Evaluates document-query alignment                │
│     │    - If failed → retrieve new context                  │
│     │                                                           │
│     ├─→ Faithfulness Check (Hallucination Detection)          │
│     │    - Threshold: 0.8                                     │
│     │    - Verifies answer grounding in context              │
│     │    - If failed → regenerate with stricter constraints  │
│     │                                                           │
│     └─→ Answer Relevance Metric                               │
│          - Threshold: 0.75                                    │
│          - Measures query-answer semantic alignment           │
│          - If failed → refine query routing                   │
│                                                                   │
│  5. Return Final Answer + Metrics                              │
│     - Answer text                                              │
│     - Retrieved context                                        │
│     - Quality metrics                                          │
│     - Latency measurement                                      │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│           OBSERVABILITY & MLOps INFRASTRUCTURE                   │
├─────────────────────────────────────────────────────────────────┤
│                                                                   │
│  Phoenix Dashboard (localhost:6006)                            │
│  - Real-time RAG query tracing                                │
│  - Context retrieval tracking                                 │
│  - Answer generation metrics                                  │
│  - Latency visualization                                      │
│  - Error tracking                                             │
│                                                                   │
│  OpenTelemetry Integration                                     │
│  - Distributed tracing                                        │
│  - OTLP exporter                                              │
│  - Custom instrumentation                                     │
│                                                                   │
│  TruLens Evaluation                                            │
│  - Quality metrics                                            │
│  - Feedback loops                                             │
│  - Iterative improvement                                      │
│                                                                   │
│  Ragas Framework                                               │
│  - Answer generation quality                                  │
│  - Retrieval quality scoring                                  │
│  - Semantic evaluation                                        │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘
```

---

## 🛠️ Technology Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **API Framework** | FastAPI | 0.104.1 | REST API with async/await |
| **Agentic Workflows** | LangGraph | 0.0.31 | State machine orchestration |
| **LLM Integration** | LangChain | 0.1.9 | LLM abstractions |
| **Vector Database** | Qdrant | 2.7.2 | Dense embedding storage |
| **Sparse Search** | Rank-BM25 | 0.2.2 | BM25 text-based retrieval |
| **Task Queue** | Celery | 5.3.4 | Distributed task processing |
| **Message Broker** | Redis | 5.0.1 | Task queue broker |
| **Config Mgmt** | Pydantic | 2.5.0 | Settings validation |
| **Observability** | Phoenix | 3.11.0 | Real-time tracing |
| **Tracing** | OpenTelemetry | 1.21.0 | Distributed tracing |
| **Evaluation** | TruLens + Ragas | Latest | Quality metrics |
| **Embeddings** | Sentence Transformers | 2.2.2 | Embedding generation |
| **Database** | PostgreSQL | 16 | Metadata storage |
| **Async Support** | Uvicorn | 0.24.0 | ASGI server |

---

## 📋 Key Features

### ✅ Advanced Ingestion
- **Semantic Chunking** with sentence embedding distance tracking
- **Hierarchical Parent-Child Chunking** (128-token children → 512-token parents)
- **Distributed Processing** via Celery + Redis
- **Async Embeddings** with OpenAI text-embedding-3-small

### ✅ Hybrid Retrieval
- **Dense Search** via Qdrant vector similarity
- **Sparse Search** via BM25 text ranking
- **Reciprocal Rank Fusion** combining both (weights: 0.4 BM25 + 0.6 Dense)
- **Top-K Results** (configurable, default: 5)

### ✅ Agentic Loop
- **Intent Router** detects semantic intent
- **Self-Correction Loop** with programmatic critique
- **Context Relevance** metric (threshold: 0.7)
- **Faithfulness Check** for hallucination detection (threshold: 0.8)
- **Answer Relevance** metric (threshold: 0.75)

### ✅ Observability
- **Phoenix Dashboard** at localhost:6006
- **OpenTelemetry** OTLP export
- **TruLens** quality metrics and feedback loops
- **Ragas** answer and retrieval evaluation
- **Structured Logging** with Loguru

### ✅ Enterprise-Ready
- Type-safe Pydantic configuration
- Comprehensive error handling
- Async/await throughout
- Clean separation of concerns
- Full test coverage (unit + integration)

---

## 🚀 Quick Start

### Prerequisites
- Docker & Docker Compose
- OpenAI API key

### Step 1: Clone Repository
```bash
git clone https://github.com/ZED-ZEDKA/agentic-rag-pipeline.git
cd agentic-rag-pipeline
```

### Step 2: Configure Environment
```bash
cp .env.example .env
nano .env
# Add your OpenAI API key: OPENAI_API_KEY=sk-xxxxxxxxxxxxxx
```

### Step 3: Build & Start
```bash
# Build Docker images
docker-compose build

# Start all services
docker-compose up -d

# Verify services
docker-compose ps
```

### Step 4: Test API
```bash
# Health check
curl http://localhost:8000/health

# Query the RAG system
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query_text": "What is LangGraph?"}'

# Ingest a document
curl -X POST http://localhost:8000/ingest \
  -H "Content-Type: application/json" \
  -d '{"document": "Your document content here"}'
```

### Step 5: Access Dashboards
- **API Docs**: http://localhost:8000/docs
- **Phoenix Dashboard**: http://localhost:6006

---

## 🏗️ Project Structure

```
agentic-rag-pipeline/
├── .gitignore                  # Git exclusions
├── .env.example                # Environment template
├── requirements.txt            # Python dependencies
├── pyproject.toml              # PEP 518 build config
├── docker-compose.yml          # Service orchestration
├── Makefile                    # Developer commands
│
├── docker/
│   ├── Dockerfile.app          # FastAPI container
│   └── Dockerfile.celery       # Celery worker container
│
├── src/
│   ├── __init__.py
│   ├── config.py               # Pydantic Settings (12 config classes)
│   ├── api/
│   │   ├── __init__.py
│   │   └── main.py             # FastAPI app factory
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── chunking.py         # Semantic & hierarchical chunking
│   │   └── embeddings.py       # Embedding manager
│   ├── retrieval/
│   │   ├── __init__.py
│   │   └── hybrid_search.py    # BM25 + Dense + RRF
│   ├── agents/
│   │   ├── __init__.py
│   │   └── graph.py            # LangGraph state machine
│   ├── evaluation/
│   │   ├── __init__.py
│   │   └── metrics.py          # TruLens/Ragas metrics
│   ├── tasks/
│   │   ├── __init__.py
│   │   └── celery_app.py       # Celery configuration
│   └── observability/
│       ├── __init__.py
│       └── tracing.py          # Phoenix & OTEL config
│
└── tests/
    ├── __init__.py
    ├── unit/
    │   ├── __init__.py
    │   └── test_config.py
    └── integration/
        ├── __init__.py
        └── test_api.py
```

---

## 📊 API Endpoints

### Health Check
```
GET /health
Response: {"status": "healthy", "app": "agentic-rag-pipeline"}
```

### Query RAG System
```
POST /query
Body: {"query_text": "Your question"}
Response: {
  "query": "Your question",
  "answer": "Generated response",
  "context": ["doc1", "doc2"],
  "metrics": {
    "context_relevance": 0.85,
    "faithfulness": 0.92,
    "latency_ms": 1234
  }
}
```

### Ingest Document
```
POST /ingest
Body: {"document": "Document content"}
Response: {
  "status": "processing",
  "document_id": "doc_123",
  "message": "Document queued for ingestion"
}
```

---

## ⚙️ Configuration

All settings managed via Pydantic BaseSettings:

| Category | Key Variables |
|----------|---------------|
| **Application** | APP_NAME, APP_ENV, DEBUG, LOG_LEVEL |
| **FastAPI** | FASTAPI_HOST, FASTAPI_PORT, ALLOWED_ORIGINS |
| **LLM** | OPENAI_API_KEY, OPENAI_MODEL, OPENAI_TEMPERATURE |
| **Qdrant** | QDRANT_HOST, QDRANT_PORT, QDRANT_COLLECTION_NAME |
| **Redis** | REDIS_HOST, REDIS_PORT, REDIS_PASSWORD |
| **Celery** | CELERY_BROKER_URL, CELERY_RESULT_BACKEND |
| **Observability** | PHOENIX_HOST, OTEL_EXPORTER_OTLP_ENDPOINT |
| **Evaluation** | EVAL_THRESHOLD_CONTEXT_RELEVANCE, EVAL_THRESHOLD_FAITHFULNESS |
| **Ingestion** | CHUNK_SIZE_CHILD, CHUNK_SIZE_PARENT, SEMANTIC_SIMILARITY_THRESHOLD |
| **Retrieval** | RETRIEVAL_TOP_K, BM25_WEIGHT, DENSE_WEIGHT, RRF_K |

---

## 🛠️ Developer Commands

```bash
make install              # Install dependencies
make install-dev          # Install dev dependencies
make clean                # Clean cache
make format               # Format code (black + isort)
make lint                 # Lint code (flake8 + mypy)
make test                 # Run unit tests
make test-integration     # Run integration tests
make test-all             # Run all tests
make run                  # Run FastAPI locally
make run-worker           # Run Celery worker
make run-beat             # Run Celery beat
make docker-build         # Build Docker images
make docker-up            # Start containers
make docker-down          # Stop containers
make docker-logs          # View logs
```

---

## 🔍 Service Endpoints

| Service | URL | Purpose |
|---------|-----|---------|
| FastAPI | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Swagger UI |
| Phoenix | http://localhost:6006 | Observability |
| Qdrant | http://localhost:6333 | Vector DB |
| Redis | localhost:6379 | Message Broker |
| PostgreSQL | localhost:5432 | Metadata DB |

---

## 📈 Monitoring & Debugging

### View Service Logs
```bash
docker-compose logs -f app                # FastAPI
docker-compose logs -f celery-worker      # Celery
docker-compose logs -f qdrant             # Qdrant
```

### Connect to PostgreSQL
```bash
psql postgresql://postgres:password@localhost:5432/agentic_rag
```

### Access Qdrant Web UI
```
http://localhost:6333/dashboard
```

---

## 🚀 Production Deployment

### Kubernetes Deployment
```bash
kubectl apply -f k8s/
```

### Environment Variables
Copy `.env.example` to `.env` and configure for production:
- Update all service URLs to production endpoints
- Set APP_ENV=production
- Disable DEBUG=False
- Configure proper database credentials
- Add real OpenAI API key

### Docker Image Registry
```bash
docker build -t your-registry/agentic-rag:latest -f docker/Dockerfile.app .
docker push your-registry/agentic-rag:latest
```

---

## 📚 Architecture Decisions

### Why LangGraph?
- Declarative state machine workflows
- Built-in support for agents and tool use
- Easy debugging and tracing
- Production-ready evaluation patterns

### Why Qdrant?
- Fast, production-ready vector database
- Hybrid search capabilities
- Excellent client libraries
- Docker support out of the box

### Why Celery + Redis?
- Distributed task processing
- Retry logic and time limits
- Task monitoring and logging
- Horizontal scaling

### Why Phoenix?
- Purpose-built for LLM observability
- Real-time tracing dashboard
- Evals and experiments tracking
- Low-latency ingestion

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

MIT License - see LICENSE file for details

---

## 🎓 References

- [LangGraph Documentation](https://github.com/langchain-ai/langgraph)
- [Qdrant Vector Database](https://qdrant.tech/)
- [FastAPI Guide](https://fastapi.tiangolo.com/)
- [Celery Task Queue](https://docs.celeryproject.io/)
- [Phoenix LLM Observability](https://phoenix.arize.com/)
- [TruLens Framework](https://www.trulens.org/)
- [Ragas Evaluation](https://github.com/explodinggradients/ragas)

---

**Built with ❤️ for enterprise RAG systems**
