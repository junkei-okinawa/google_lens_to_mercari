import urllib.parse
from app.models.product import ProductInfo


class MercariService:
    def __init__(self):
        self.base_url = "https://jp.mercari.com/search"

    def generate_search_url(self, product_info: ProductInfo) -> str:
        # Base query from suggested_query
        query = product_info.suggested_query
        if not query:
            # Fallback to combination of brand and product name
            query_parts = []
            if product_info.brand:
                query_parts.append(product_info.brand)
            if product_info.model_number:
                query_parts.append(product_info.model_number)
            query_parts.append(product_info.product_name)
            query = " ".join([p for p in query_parts if p])

        params = {
            "keyword": query,
            "status": "sold_out",  # 売り切れのみ
            "item_condition_id": "3",  # 目立った傷や汚れなし
            "item_types": "mercari",  # 個人出品のみ
            "sort": "created_time",  # 新しい順（直近の履歴）
            "order": "desc",
        }

        url_params = urllib.parse.urlencode(params, quote_via=urllib.parse.quote)
        return f"{self.base_url}?{url_params}"
