"""FastAPI application factory and route handlers."""

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


class HealthResponse(BaseModel):
    """Health check response model."""

    status: str
    app: str


class QueryRequest(BaseModel):
    """Query request model."""

    query_text: str


class QueryResponse(BaseModel):
    """Query response model."""

    query: str
    answer: str
    context: list[str]
    metrics: dict


class IngestRequest(BaseModel):
    """Document ingestion request model."""

    document: str


class IngestResponse(BaseModel):
    """Document ingestion response model."""

    status: str
    document_id: str
    message: str


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan context manager."""
    logger.info(f"Starting {settings.app.app_name}")
    yield
    logger.info(f"Shutting down {settings.app.app_name}")


app = FastAPI(
    title=settings.app.app_name,
    version="0.1.0",
    description="Production-grade Agentic RAG Pipeline",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.fastapi.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """Health check endpoint."""
    return HealthResponse(status="healthy", app=settings.app.app_name)


@app.post("/query", response_model=QueryResponse)
async def query(request: QueryRequest) -> QueryResponse:
    """Query the RAG system.

    Args:
        request: Query request with query text

    Returns:
        Query response with answer, context, and metrics
    """
    logger.info(f"Received query: {request.query_text}")

    # TODO: Implement RAG query logic
    # 1. Route intent
    # 2. Retrieve context (hybrid search)
    # 3. Generate answer
    # 4. Self-correct
    # 5. Return results

    return QueryResponse(
        query=request.query_text,
        answer="Placeholder response",
        context=[],
        metrics={
            "context_relevance": 0.0,
            "faithfulness": 0.0,
            "latency_ms": 0.0,
        },
    )


@app.post("/ingest", response_model=IngestResponse)
async def ingest(request: IngestRequest) -> IngestResponse:
    """Ingest a document into the RAG system.

    Args:
        request: Ingest request with document content

    Returns:
        Ingest response with document ID and status
    """
    logger.info(f"Received document ingestion request")

    # TODO: Implement document ingestion
    # 1. Create document record
    # 2. Queue Celery task for processing
    # 3. Return document ID

    return IngestResponse(
        status="processing",
        document_id="doc_123",
        message="Document queued for ingestion",
    )
