"""Configuration management using Pydantic BaseSettings."""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings


class ApplicationSettings(BaseSettings):
    """Application-level settings."""

    app_name: str = "agentic-rag-pipeline"
    app_env: str = "development"
    debug: bool = True
    log_level: str = "INFO"


class FastAPISettings(BaseSettings):
    """FastAPI configuration."""

    fastapi_host: str = "0.0.0.0"
    fastapi_port: int = 8000
    fastapi_reload: bool = True
    fastapi_workers: int = 4
    allowed_origins: list[str] = ["*"]


class LLMSettings(BaseSettings):
    """LLM and OpenAI configuration."""

    openai_api_key: str
    openai_model: str = "gpt-4-turbo"
    openai_embedding_model: str = "text-embedding-3-small"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2048


class QdrantSettings(BaseSettings):
    """Qdrant vector database configuration."""

    qdrant_host: str = "qdrant"
    qdrant_port: int = 6333
    qdrant_collection_name: str = "documents"
    qdrant_vector_size: int = 1536
    qdrant_timeout: int = 30

    @property
    def qdrant_url(self) -> str:
        """Construct Qdrant URL."""
        return f"http://{self.qdrant_host}:{self.qdrant_port}"


class RedisSettings(BaseSettings):
    """Redis configuration."""

    redis_host: str = "redis"
    redis_port: int = 6379
    redis_db: int = 0
    redis_password: Optional[str] = None

    @property
    def redis_url(self) -> str:
        """Construct Redis URL."""
        if self.redis_password:
            return f"redis://:{self.redis_password}@{self.redis_host}:{self.redis_port}/{self.redis_db}"
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class CelerySettings(BaseSettings):
    """Celery configuration."""

    celery_broker_url: str = "redis://redis:6379/0"
    celery_result_backend: str = "redis://redis:6379/1"
    celery_task_serializer: str = "json"
    celery_result_serializer: str = "json"
    celery_accept_content: list[str] = ["json"]
    celery_timezone: str = "UTC"
    celery_enable_utc: bool = True


class ObservabilitySettings(BaseSettings):
    """Phoenix and OpenTelemetry configuration."""

    phoenix_host: str = "phoenix"
    phoenix_port: int = 6006
    enable_phoenix_tracing: bool = True
    otel_exporter_otlp_endpoint: str = "http://localhost:4317"


class EvaluationSettings(BaseSettings):
    """Evaluation and quality metric thresholds."""

    eval_threshold_context_relevance: float = 0.7
    eval_threshold_faithfulness: float = 0.8
    eval_threshold_answer_relevance: float = 0.75


class IngestionSettings(BaseSettings):
    """Document ingestion configuration."""

    chunk_size_child: int = 128
    chunk_size_parent: int = 512
    chunk_overlap: int = 20
    semantic_chunking_enabled: bool = True
    semantic_similarity_threshold: float = 0.5


class RetrievalSettings(BaseSettings):
    """Retrieval system configuration."""

    retrieval_top_k: int = 5
    bm25_weight: float = 0.4
    dense_weight: float = 0.6
    rrf_k: int = 60


class DatabaseSettings(BaseSettings):
    """Database configuration."""

    db_host: str = "postgres"
    db_port: int = 5432
    db_name: str = "agentic_rag"
    db_user: str = "postgres"
    db_password: str = "password"

    @property
    def db_url(self) -> str:
        """Construct database URL."""
        return f"postgresql://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


class FeatureFlagsSettings(BaseSettings):
    """Feature flags for optional functionality."""

    enable_self_correction: bool = True
    enable_intent_routing: bool = True
    enable_hybrid_retrieval: bool = True
    enable_streaming_responses: bool = False


class Settings(BaseSettings):
    """Main settings configuration aggregating all sub-settings."""

    app: ApplicationSettings = ApplicationSettings()
    fastapi: FastAPISettings = FastAPISettings()
    llm: LLMSettings = LLMSettings()
    qdrant: QdrantSettings = QdrantSettings()
    redis: RedisSettings = RedisSettings()
    celery: CelerySettings = CelerySettings()
    observability: ObservabilitySettings = ObservabilitySettings()
    evaluation: EvaluationSettings = EvaluationSettings()
    ingestion: IngestionSettings = IngestionSettings()
    retrieval: RetrievalSettings = RetrievalSettings()
    database: DatabaseSettings = DatabaseSettings()
    feature_flags: FeatureFlagsSettings = FeatureFlagsSettings()

    class Config:
        """Pydantic configuration."""

        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Get cached settings singleton."""
    return Settings()
