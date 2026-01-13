from unittest.mock import MagicMock, patch
from app.services.extraction_service import ExtractionService
from app.models.product import LensResult


@patch("google.generativeai.GenerativeModel")
def test_extract_product_info_success(mock_model_class):
    # Mock behavior
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = '{"brand": "Nike", "model_number": "AJ1", "product_name": "Air Jordan 1", "features": ["red", "high cut"], "suggested_query": "Nike AJ1 Air Jordan 1"}'
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model

    service = ExtractionService(api_key="test_key")
    lens_results = [
        LensResult(title="Nike Shoe", link="http://nike", snippet="Classic Air Jordan")
    ]

    result = service.extract_product_info(lens_results)

    assert result is not None
    assert result.brand == "Nike"
    assert result.model_number == "AJ1"
    assert "red" in result.features
    assert result.suggested_query == "Nike AJ1 Air Jordan 1"


def test_extract_product_info_empty():
    service = ExtractionService(api_key="test_key")
    assert service.extract_product_info([]) is None


@patch("google.generativeai.GenerativeModel")
def test_extract_product_info_json_error(mock_model_class):
    mock_model = MagicMock()
    mock_response = MagicMock()
    mock_response.text = "invalid json"
    mock_model.generate_content.return_value = mock_response
    mock_model_class.return_value = mock_model

    service = ExtractionService(api_key="test_key")
    lens_results = [LensResult(title="Item", link="http://item")]

    result = service.extract_product_info(lens_results)
    assert result is None


@patch("google.generativeai.GenerativeModel")
def test_extract_product_info_api_error(mock_model_class):
    mock_model = MagicMock()
    mock_model.generate_content.side_effect = Exception("API Error")
    mock_model_class.return_value = mock_model

    service = ExtractionService(api_key="test_key")
    lens_results = [LensResult(title="Item", link="http://item")]

    result = service.extract_product_info(lens_results)
    assert result is None
