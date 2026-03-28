"""Scraper for HasIvoov (hasivoov.co.il)"""
import logging
from typing import List, Dict, Optional
from .base import BaseScraper
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class HasIvoovScraper(BaseScraper):
    """Scraper for HasIvoov - WooCommerce structure"""
    
    def __init__(self):
        config = {
            "name": "Has Ivoov",
            "base_url": "https://hasivoov.co.il",
            "product_selector": "div.product, li.product",
            "title_selector": "h2.product-title, h2.woocommerce-loop-product__title",
            "price_selector": "span.price, span.woocommerce-price-amount",
            "image_selector": "img.wp-post-image, img.product-image",
            "stock_selector": "p.stock, span.stock",
        }
        super().__init__("hasivoov", "https://hasivoov.co.il", config)
    
    def scrape(self) -> List[Dict]:
        """Scrape HasIvoov product listings"""
        logger.info(f"🔄 Starting HasIvoov scrape...")
        
        try:
            base_url = f"{self.base_url}/shop"
            products = self._scrape_with_pagination(base_url, category="vinyl")
            
            logger.info(f"✅ HasIvoov scrape completed: {len(products)} products")
            self.records_scraped = len(products)
            return products
        
        except Exception as e:
            error_msg = f"HasIvoov scrape failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    def _scrape_with_pagination(self, base_url: str, category: str = "vinyl", max_pages: int = 50) -> List[Dict]:
        """Scrape all products with WooCommerce pagination"""
        all_products = []
        page = 1
        scraped_urls = set()
        
        while page <= max_pages:
            url = f"{base_url}/?product_cat={category}&paged={page}"
            
            logger.debug(f"Scraping page {page}: {url}")
            soup = self._get_page(url)
            
            if not soup:
                logger.warning(f"Failed to fetch page {page}, stopping pagination")
                break
            
            products = soup.select(self.config["product_selector"])
            
            if not products:
                logger.info(f"No products found on page {page}, stopping")
                break
            
            page_products = 0
            for product_elem in products:
                try:
                    product = self._parse_product(product_elem)
                    
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
