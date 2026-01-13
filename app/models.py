from typing import List, Optional
from urllib.parse import urlparse
from pydantic import BaseModel, field_validator


class CrawlRequest(BaseModel):
    url: str
    
    @field_validator('url')
    @classmethod
    def validate_url(cls, v: str) -> str:
        parsed = urlparse(v)
        if not parsed.scheme:
            raise ValueError("URL must include a scheme (http:// or https://)")
        if parsed.scheme not in ('http', 'https'):
            raise ValueError("URL scheme must be http or https")
        if not parsed.netloc:
            raise ValueError("URL must include a domain")
        return v


class BatchCrawlRequest(BaseModel):
    urls: List[str]
    
    @field_validator('urls')
    @classmethod
    def validate_urls(cls, v: List[str]) -> List[str]:
        if not v:
            raise ValueError("List of URLs cannot be empty")
        for url in v:
            parsed = urlparse(url)
            if not parsed.scheme or not parsed.netloc:
                 raise ValueError(f"Invalid URL: {url}")
        return v


class ProductData(BaseModel):
    id: Optional[str] = None
    sku: Optional[str] = None
    upc: Optional[str] = None
    mfr_number: Optional[str] = None
    brand: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    category: Optional[str] = None
    sub_category: Optional[str] = None
    recommended_age: Optional[str] = None
    language: Optional[str] = None
    price: Optional[str] = None
    currency: Optional[str] = None
    availability: Optional[str] = None
    images: list[str] = []
    url: str


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
