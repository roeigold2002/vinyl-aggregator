"""Scraper for Takli House (taklithouse.com)"""
import logging
from typing import List, Dict, Optional
from .base import BaseScraper
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class TakliHouseScraper(BaseScraper):
    """Scraper for Takli House - Wix/modal-based store (HARD - needs manual updates)"""
    
    def __init__(self):
        config = {
            "name": "Takli House",
            "base_url": "https://www.taklithouse.com",
            "product_selector": "div.product-card, div.product-item",
            "title_selector": "h3.product-title, span.product-name",
            "price_selector": "span.product-price, span.price",
            "image_selector": "img.product-image, img",
            "stock_selector": "span.stock, div.availability",
        }
        super().__init__("takli_house", "https://www.taklithouse.com", config)
    
    def scrape(self) -> List[Dict]:
        """Scrape Takli House product listings
        
        NOTE: This store uses Wix with modal-based product display.
        Requires browser automation or manual CSS selector updates.
        Attempting static scraping as fallback.
        """
        logger.warning("⚠️  Takli House uses modal-based display. Attempting partial scrape...")
        
        try:
            base_url = f"{self.base_url}/catalog/vinyl"
            products = self._attempt_static_scrape(base_url)
            
            if products:
                logger.info(f"✅ Takli House partial scrape: {len(products)} products")
            else:
                logger.warning("⚠️  Takli House returned 0 products (requires Selenium for full coverage)")
            
            self.records_scraped = len(products)
            return products
        
        except Exception as e:
            error_msg = f"Takli House scrape failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    def _attempt_static_scrape(self, base_url: str, max_pages: int = 20) -> List[Dict]:
        """Attempt static scraping (may have limited results due to Wix modal structure)"""
        all_products = []
        scraped_urls = set()
        
        # Try main catalog page
        logger.debug(f"Attempting catalog page: {base_url}")
        soup = self._get_page(base_url)
        
        if not soup:
            logger.warning("Failed to fetch Takli House catalog page")
            return []
        
        products = soup.select(self.config["product_selector"])
        
        logger.info(f"Found {len(products)} product elements on catalog page")
        
        for product_elem in products:
            try:
                product = self._parse_product(product_elem)
                
                if product and product['store_url'] not in scraped_urls:
                    all_products.append(product)
                    scraped_urls.add(product['store_url'])
            
            except Exception as e:
                logger.debug(f"Error parsing product: {e}")
                continue
        
        # Try pagination if available
        for page in range(2, max_pages):
            url = f"{base_url}?page={page}"
            logger.debug(f"Trying page {page}: {url}")
            
            soup = self._get_page(url)
            if not soup:
                break
            
            products = soup.select(self.config["product_selector"])
            if not products:
                break
            
            for product_elem in products:
                try:
                    product = self._parse_product(product_elem)
                    
                    if product and product['store_url'] not in scraped_urls:
                        all_products.append(product)
                        scraped_urls.add(product['store_url'])
                
                except Exception as e:
                    logger.debug(f"Error parsing product: {e}")
                    continue
        
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
