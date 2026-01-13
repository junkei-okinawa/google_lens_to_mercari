import unittest
from unittest.mock import patch, MagicMock
import pytest
from app.services.lens_service import LensService


class TestLensService:
    @pytest.fixture
    def service(self):
        return LensService(api_key="test_api_key")

    @pytest.mark.asyncio
    @patch("httpx.AsyncClient.get")
    async def test_search_by_image_url_success(self, mock_get, service):
        # Mocking the response from SerpAPI
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "visual_matches": [
                {
                    "title": "Vintage Denim Jacket",
                    "link": "https://example.com/item1",
                    "snippet": "A cool jacket",
                    "source": "Example Store",
                }
            ]
        }
        mock_get.return_value = mock_response

        results = await service.search_by_image_url("https://example.com/image.jpg")

        assert len(results) == 1
        assert results[0].title == "Vintage Denim Jacket"
        mock_get.assert_called_once()
        args, kwargs = mock_get.call_args
        assert kwargs["params"]["url"] == "https://example.com/image.jpg"

    def test_parse_results(self, service):
        data = {
            "visual_matches": [
                {
                    "title": "Test Item",
                    "link": "https://test.com",
                    "snippet": "Test snippet",
                    "source": "Test source",
                }
            ]
        }
        results = service._parse_results(data)
        assert len(results) == 1
        assert results[0].title == "Test Item"

    def test_parse_results_empty(self, service):
        assert service._parse_results({}) == []
