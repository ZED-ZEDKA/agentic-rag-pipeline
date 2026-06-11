"""Unit tests for configuration."""

import pytest

from src.config import Settings, get_settings


class TestSettings:
    """Test settings configuration."""

    def test_settings_singleton(self):
        """Test that settings is a singleton."""
        settings1 = get_settings()
        settings2 = get_settings()
        assert settings1 is settings2

    def test_settings_loading(self):
        """Test settings loading."""
        settings = get_settings()
        assert settings.app.app_name == "agentic-rag-pipeline"
        assert settings.fastapi.fastapi_port == 8000

    def test_qdrant_url_construction(self):
        """Test Qdrant URL construction."""
        settings = get_settings()
        expected_url = f"http://{settings.qdrant.qdrant_host}:{settings.qdrant.qdrant_port}"
        assert settings.qdrant.qdrant_url == expected_url

    def test_redis_url_construction(self):
        """Test Redis URL construction."""
        settings = get_settings()
        assert "redis://" in settings.redis.redis_url


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
