import google.generativeai as genai
import json
import logging
from jinja2 import Environment, FileSystemLoader
from typing import List, Optional
import os
from app.models.config import settings
from app.models.product import LensResult, ProductInfo


logger = logging.getLogger(__name__)


class ExtractionService:
    def __init__(self, api_key: str = settings.GEMINI_API_KEY):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(
            "gemini-flash-latest",
            generation_config={"response_mime_type": "application/json"},
        )

        # Jinja2 setup for prompt
        template_dir = os.path.join(os.path.dirname(__file__), "templates")
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.template = self.env.get_template("extraction_prompt.txt")

    def extract_product_info(
        self, lens_results: List[LensResult]
    ) -> Optional[ProductInfo]:
        if not lens_results:
            return None

        prompt = self.template.render(results=lens_results)

        try:
            response = self.model.generate_content(prompt)
            data = json.loads(response.text)

            return ProductInfo(
                brand=data.get("brand"),
                model_number=data.get("model_number"),
                product_name=data.get("product_name", "Unknown Product"),
                features=data.get("features", []),
                suggested_query=data.get("suggested_query", ""),
            )
        except Exception as e:
            logger.error(f"Error in ExtractionService: {e}")
            return None
