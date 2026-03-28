"""Scraper for DiscCenter.co.il"""
import logging
from typing import List, Dict, Optional
from .base import BaseScraper
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class DiscCenterScraper(BaseScraper):
    """Scraper for DiscCenter.co.il - Most scrapeable Israeli vinyl store"""
    
    def __init__(self):
        config = {
            "name": "DiscCenter",
            "base_url": "https://www.disccenter.co.il",
            "product_selector": "div.item-product",
            "title_selector": "span.product-name",
            "price_selector": "span.price-current",
            "image_selector": "img",
            "stock_selector": "div.stock",
        }
        super().__init__("disccenter", "https://www.disccenter.co.il", config)
        self.products = []
    
    def scrape(self) -> List[Dict]:
        """Scrape DiscCenter product listings"""
        logger.info(f"🔄 Starting DiscCenter scrape...")
        
        try:
            # DiscCenter uses a catalog structure - start with main catalog page
            main_url = f"{self.base_url}/list/1"  # Category ID 1 = Vinyl Records
            
            products = self._scrape_category(main_url)
            
            logger.info(f"✅ DiscCenter scrape completed: {len(products)} products")
            self.records_scraped = len(products)
            return products
        
        except Exception as e:
            error_msg = f"DiscCenter scrape failed: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return []
    
    def _scrape_category(self, category_url: str, max_pages: int = 50) -> List[Dict]:
        """Scrape all products from a category (with pagination)"""
        all_products = []
        page = 1
        scraped_urls = set()
        
        while page <= max_pages:
            # DiscCenter pagination uses carousel-style, but let's try standard pagination
            url = f"{category_url}?p={page}" if "?" not in category_url else f"{category_url}&p={page}"
            
            logger.debug(f"Scraping page {page}: {url}")
            soup = self._get_page(url)
            
            if not soup:
                logger.warning(f"Failed to fetch page {page}, stopping pagination")
                break
            
            # Find all product elements
            products = soup.select(self.config["product_selector"])
            
            if not products:
                logger.info(f"No more products found on page {page}, stopping")
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
        """Parse a single product element into our schema"""
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
            link_elem = product_elem.select_one("a")
            store_url = link_elem.get("href", "") if link_elem else ""
            if store_url and not store_url.startswith("http"):
                store_url = urljoin(self.base_url, store_url)
            
            # Check stock
            stock_text = self._extract_text(product_elem, self.config["stock_selector"])
            in_stock = "אזל" not in stock_text and "חוסר" not in stock_text
            
            # Parse artist + album from title
            # Format is usually "Artist - Album" or "Artist - Album (Format)"
            artist, album = self._parse_artist_album(title)
            
            return {
                'title': title,
                'artist': artist,
                'album': album,
                'format': 'Vinyl',  # DiscCenter primarily sells vinyl
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
        """Parse artist and album from title
        
        Typical format: "Artist - Album" or "Artist - Album (Format)"
        """
        try:
            # Remove format in parentheses
            clean_title = title.split("(")[0].strip()
            
            # Split on " - "
            parts = clean_title.split(" - ", 1)
            
            if len(parts) == 2:
                return parts[0].strip(), parts[1].strip()
            else:
                # If no separator, treat whole title as both (not ideal but fallback)
                return clean_title, clean_title
        
        except Exception:
            return title, title
