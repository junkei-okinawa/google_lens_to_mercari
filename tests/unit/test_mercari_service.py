import pytest
from app.services.mercari_service import MercariService
from app.models.product import ProductInfo


def test_generate_search_url_with_suggested_query():
    service = MercariService()
    product = ProductInfo(
        brand="Nike", product_name="Air Jordan", suggested_query="Nike Air Jordan AJ1"
    )
    url = service.generate_search_url(product)
    assert "keyword=Nike%20Air%20Jordan%20AJ1" in url
    assert "status=sold_out%7Ctrading" in url
    assert "sort=created_time" in url
    assert "order=desc" in url


def test_generate_search_url_fallback():
    service = MercariService()
    product = ProductInfo(
        brand="Uniqlo",
        model_number="123-456",
        product_name="T-shirt",
        suggested_query="",  # Empty fallback
    )
    url = service.generate_search_url(product)
    assert "keyword=Uniqlo%20123-456%20T-shirt" in url


def test_generate_search_url_minimal():
    service = MercariService()
    product = ProductInfo(product_name="Mystery Item", suggested_query="")
    url = service.generate_search_url(product)
    assert "keyword=Mystery%20Item" in url
