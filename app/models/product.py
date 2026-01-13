from pydantic import BaseModel
from typing import List, Optional


class ProductInfo(BaseModel):
    brand: Optional[str] = None
    model_number: Optional[str] = None
    product_name: str
    features: List[str] = []
    suggested_query: str


class LensResult(BaseModel):
    title: str
    link: str
    snippet: Optional[str] = None
    source: Optional[str] = None
