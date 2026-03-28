"""Scraper for TheVinylRoom.co.il"""
import logging
from typing import List, Dict, Optional
from .base import BaseScraper
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class TheVinylRoomScraper(BaseScraper):
    """Scraper for TheVinylRoom.co.il - Clean WordPress structure"""
    
    def __init__(self):
        config = {
            "name": "The Vinyl Room",
            "base_url": "https://thevinylroom.co.il",
            "product_selector": "div.product-wrapper",
            "title_selector": "h2.woocommerce-loop-product__title",
            "price_selector": "span.price",
            "image_selector": "img.wp-post-image",
            "stock_selector": "p.stock",
        }
        super().__init__("thevinylroom", "https://thevinylroom.co.il", config)
    
    def scrape(self) -> List[Dict]:
        """Scrape TheVinylRoom product listings"""
        logger.info(f"🔄 Starting TheVinylRoom scrape...")
        
        try:
            # TheVinylRoom uses WooCommerce pagination
            base_url = f"{self.base_url}/product-category/vinyl"
            
            products = self._scrape_with_pagination(base_url)
            
            logger.info(f"✅ TheVinylRoom scrape completed: {len(products)} products")
            self.records_scraped = len(products)
            return products
        
        except Exception as e:
            error_msg = f"TheVinylRoom scrape failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    def _scrape_with_pagination(self, base_url: str, max_pages: int = 50) -> List[Dict]:
        """Scrape all products with pagination"""
        all_products = []
        page = 1
        scraped_urls = set()
        
        while page <= max_pages:
            # WooCommerce pagination pattern: /category/vinyl/page/2
            url = f"{base_url}/page/{page}"
            
            logger.debug(f"Scraping page {page}: {url}")
            soup = self._get_page(url)
            
            if not soup:
                logger.warning(f"Failed to fetch page {page}, stopping pagination")
                break
            
            # Find all product elements
            products = soup.select(self.config["product_selector"])
            
            if not products:
                logger.info(f"No products found on page {page}, stopping")
                break
            
            page_products = 0
            for product_elem in products:
                try:
                    product = self._parse_product(product_elem)
                    
                    # Avoid duplicates
                    if product and product['store_url'] not in scraped_urls:
                        all_products.append(product)
                        scraped_urls.add(product['store_url'])
                        page_products += 1
                
                except Exception as e:
                    logger.debug(f"Error parsing product: {e}")
                    continue
            
            if page_products == 0:
                logger.info(f"No valid products on page {page}, stopping")
                break
            
            logger.info(f"Page {page}: {page_products} products")
            page += 1
        
        return all_products
    
    def _parse_product(self, product_elem) -> Optional[Dict]:
        """Parse a single product element"""
        try:
            title = self._extract_text(product_elem, self.config["title_selector"])
            if not title:
                return None
            
            # Extract price
            price_str = self._extract_text(product_elem, self.config["price_selector"])
            price = self._parse_price(price_str) if price_str else 0.0
            
            # Extract image
            cover_url = self._extract_attribute(product_elem, self.config["image_selector"], "src")
            if cover_url and not cover_url.startswith("http"):
                cover_url = urljoin(self.base_url, cover_url)
            
            # Extract product URL
            link_elem = product_elem.select_one("a.woocommerce-loop-product__link")
            store_url = link_elem.get("href", "") if link_elem else ""
            if store_url and not store_url.startswith("http"):
                store_url = urljoin(self.base_url, store_url)
            
            # Check stock (WooCommerce usually shows "In stock" or "Out of stock")
            stock_text = self._extract_text(product_elem, self.config["stock_selector"])
            in_stock = "אזל" not in stock_text and "Out of stock" not in stock_text
            
            # Parse artist + album from title
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
            # Remove format in parentheses
            clean_title = title.split("(")[0].strip()
            
            # Split on " - "
            parts = clean_title.split(" - ", 1)
            
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
            else:
                return clean_title, clean_title
        
        except Exception:
            return title, title
