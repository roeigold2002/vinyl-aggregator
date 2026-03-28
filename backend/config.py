"""Configuration management for vinyl aggregator"""
import os
from pydantic_settings import BaseSettings
from typing import Dict, Any

class Settings(BaseSettings):
    """Application settings"""
    # Database
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "postgresql://user:password@localhost:5432/vinyl_aggregator"
    )
    
    # Redis
    REDIS_URL: str = os.getenv("REDIS_URL", "redis://localhost:6379")
    
    # API
    API_PREFIX: str = "/api"
    DEBUG: bool = os.getenv("DEBUG", "True").lower() == "true"
    
    # CORS
    CORS_ORIGINS: list = ["http://localhost:3000", "http://localhost:5173"]
    
    # Scraper settings
    REQUEST_TIMEOUT: int = 30
    RETRY_ATTEMPTS: int = 3
    RATE_LIMIT_DELAY: float = 2.5  # seconds between requests
    
    class Config:
        env_file = ".env"

settings = Settings()

# Store configurations with CSS selectors and pagination patterns
STORE_CONFIGS: Dict[str, Any] = {
    "disccenter": {
        "id": "disccenter",
        "name": "DiscCenter",
        "base_url": "https://www.disccenter.co.il",
        "category_url": "{base_url}/list/{category_id}",
        "product_selector": "div.product-item",
        "title_selector": "span.product-name",
        "price_selector": "span.product-price",
        "image_selector": "img.product-image",
        "stock_selector": "div.stock-status",
        "difficulty": "easy",
        "pagination": "carousel",
        "estimated_products": 2500,
    },
    "thevinylroom": {
        "id": "thevinylroom",
        "name": "The Vinyl Room",
        "base_url": "https://thevinylroom.co.il",
        "category_url": "{base_url}/product-category/vinyl/page/{page}",
        "product_selector": "div.product-wrapper",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "div.stock",
        "difficulty": "easy",
        "pagination": "numeric",
        "estimated_products": 1200,
    },
    "third_ear": {
        "id": "third_ear",
        "name": "The Third Ear",
        "base_url": "https://www.third-ear.com",
        "category_url": "{base_url}/product-category/vinyls/?paged={page}",
        "product_selector": "div.product",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 800,
    },
    "beatnik": {
        "id": "beatnik",
        "name": "Beatnik",
        "base_url": "https://www.beatnik.co.il",
        "category_url": "{base_url}/online-store/?paged={page}",
        "product_selector": "div.product-item",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock-status",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 1500,
    },
    "giora_records": {
        "id": "giora_records",
        "name": "Giora Records",
        "base_url": "https://www.giorarecords.co.il",
        "category_url": "{base_url}/product-category/vinyl/page/{page}",
        "product_selector": "div.product",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 700,
    },
    "hasivoov": {
        "id": "hasivoov",
        "name": "Has Ivoov",
        "base_url": "https://hasivoov.co.il",
        "category_url": "{base_url}/shop/?product_cat=vinyl&paged={page}",
        "product_selector": "div.product",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 500,
    },
    "shablool_records": {
        "id": "shablool_records",
        "name": "Shablool Records",
        "base_url": "https://shabloolrecords.co.il",
        "category_url": "{base_url}/product-category/vinyl/page/{page}",
        "product_selector": "div.product-wrapper",
        "title_selector": "h2.product-title",
        "price_selector": "span.price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 550,
    },
    "vinyl_stock": {
        "id": "vinyl_stock",
        "name": "Vinyl Stock",
        "base_url": "https://www.vinylstock.co.il",
        "category_url": "{base_url}/store/vinyl/page/{page}",
        "product_selector": "div.product-item",
        "title_selector": "h3.product-title",
        "price_selector": "span.product-price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock-badge",
        "difficulty": "medium",
        "pagination": "numeric",
        "estimated_products": 1800,
    },
    "tav8": {
        "id": "tav8",
        "name": "Tav8 Records",
        "base_url": "https://www.tav8.co.il",
        "category_url": "{base_url}/store-products.aspx?StoreCategoryId=1",
        "product_selector": "div.product-item",
        "title_selector": "span.product-name",
        "price_selector": "span.product-price",
        "image_selector": "img.product-image",
        "stock_selector": "div.stock-status",
        "difficulty": "medium",
        "pagination": "page",
        "estimated_products": 1000,
    },
    "takli_house": {
        "id": "takli_house",
        "name": "Takli House",
        "base_url": "https://www.taklithouse.com",
        "category_url": "{base_url}/catalog/vinyl",
        "product_selector": "div.product-card",
        "title_selector": "h3.product-title",
        "price_selector": "span.product-price",
        "image_selector": "img.product-image",
        "stock_selector": "span.stock",
        "difficulty": "hard",
        "pagination": "modal",
        "estimated_products": 450,
    },
}
