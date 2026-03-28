"""Scraper for Tav8 Records (tav8.co.il)"""
import logging
from typing import List, Dict, Optional
from .base import BaseScraper
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class Tav8Scraper(BaseScraper):
    """Scraper for Tav8 Records - Custom aspx platform"""
    
    def __init__(self):
        config = {
            "name": "Tav8 Records",
            "base_url": "https://www.tav8.co.il",
            "product_selector": "div.product-item, div.product",
            "title_selector": "span.product-name, h3.product-title, div.product-name",
            "price_selector": "span.product-price, span.price, div.price",
            "image_selector": "img.product-image, img",
            "stock_selector": "div.stock-status, span.stock, p.stock",
        }
        super().__init__("tav8", "https://www.tav8.co.il", config)
    
    def scrape(self) -> List[Dict]:
        """Scrape Tav8 product listings"""
        logger.info(f"🔄 Starting Tav8 scrape...")
        
        try:
            # Tav8 uses custom ASP.NET structure
            base_url = f"{self.base_url}/store-products.aspx"
            products = self._scrape_category_pages(base_url)
            
            logger.info(f"✅ Tav8 scrape completed: {len(products)} products")
            self.records_scraped = len(products)
            return products
        
        except Exception as e:
            error_msg = f"Tav8 scrape failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    def _scrape_category_pages(self, base_url: str, max_categories: int = 10) -> List[Dict]:
        """Scrape products across multiple category pages"""
        all_products = []
        scraped_urls = set()
        
        # Try various category IDs (common pattern)
        for category_id in range(1, max_categories + 1):
            url = f"{base_url}?StoreCategoryId={category_id}"
            
            logger.debug(f"Scraping category {category_id}: {url}")
            soup = self._get_page(url)
            
            if not soup:
                logger.debug(f"Failed to fetch category {category_id}")
                continue
            
            products = soup.select(self.config["product_selector"])
            
            if not products:
                logger.debug(f"No products found for category {category_id}")
                continue
            
            category_products = 0
            for product_elem in products:
                try:
                    product = self._parse_product(product_elem)
                    
                    if product and product['store_url'] not in scraped_urls:
                        all_products.append(product)
                        scraped_urls.add(product['store_url'])
                        category_products += 1
                
                except Exception as e:
                    logger.debug(f"Error parsing product: {e}")
                    continue
            
            logger.info(f"Category {category_id}: {category_products} products")
        
        return all_products
    
    def _parse_product(self, product_elem) -> Optional[Dict]:
        """Parse a single product element"""
        try:
            title = self._extract_text(product_elem, self.config["title_selector"])
            if not title:
                return None
            
            price_str = self._extract_text(product_elem, self.config["price_selector"])
            price = self._parse_price(price_str) if price_str else 0.0
            
            cover_url = self._extract_attribute(product_elem, self.config["image_selector"], "src")
            if cover_url and not cover_url.startswith("http"):
                cover_url = urljoin(self.base_url, cover_url)
            
            link_elem = product_elem.select_one("a")
            store_url = link_elem.get("href", "") if link_elem else ""
            if store_url and not store_url.startswith("http"):
                store_url = urljoin(self.base_url, store_url)
            
            stock_text = self._extract_text(product_elem, self.config["stock_selector"])
            in_stock = "אזל" not in stock_text and "Out of stock" not in stock_text
            
            artist, album = self._parse_artist_album(title)
            
            return {
                'title': title,
                'artist': artist,
                'album': album,
                'format': 'Vinyl',
                'cover_art_url': cover_url,
                'cover_art_full_url': cover_url,
                'price_ils': price,
                'in_stock': in_stock,
                'quantity_available': 1 if in_stock else 0,
                'store_url': store_url,
            }
        
        except Exception as e:
            logger.debug(f"Error parsing product: {e}")
            return None
    
    def _parse_artist_album(self, title: str) -> tuple[str, str]:
        """Parse artist and album from title"""
        try:
            clean_title = title.split("(")[0].strip()
            parts = clean_title.split(" - ", 1)
            
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
            else:
                return clean_title, clean_title
        
        except Exception:
            return title, title
