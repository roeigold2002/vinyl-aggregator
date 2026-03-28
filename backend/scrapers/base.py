"""Base scraper class for all store scrapers"""
import logging
import time
import random
from abc import ABC, abstractmethod
from typing import List, Dict, Optional
from datetime import datetime
from requests import Session
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry
from bs4 import BeautifulSoup
from models import Record, Price

logger = logging.getLogger(__name__)


class BaseScraper(ABC):
    """Base class for all store scrapers"""
    
    def __init__(self, store_key: str, base_url: str, config: Dict):
        self.store_key = store_key
        self.base_url = base_url
        self.config = config
        self.session = self._create_session()
        self.records_scraped = 0
        self.errors = []
    
    def _create_session(self) -> Session:
        """Create session with retry strategy"""
        session = Session()
        
        # Configure retry strategy
        retry = Retry(
            total=3,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )
        adapter = HTTPAdapter(max_retries=retry)
        session.mount('http://', adapter)
        session.mount('https://', adapter)
        
        # Set reasonable user agent
        session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        
        return session
    
    def _get_page(self, url: str) -> Optional[BeautifulSoup]:
        """Fetch a page with rate limiting"""
        try:
            # Add jitter to delay
            delay = random.uniform(2, 3.5)
            time.sleep(delay)
            
            response = self.session.get(url, timeout=30)
            response.raise_for_status()
            
            return BeautifulSoup(response.content, 'html.parser')
        except Exception as e:
            error_msg = f"Error fetching {url}: {str(e)}"
            logger.error(error_msg)
            self.errors.append(error_msg)
            return None
    
    def _extract_text(self, element, selector: str) -> str:
        """Extract text from CSS selector"""
        if not element:
            return ""
        
        try:
            found = element.select_one(selector)
            if found:
                return found.get_text(strip=True)
        except Exception as e:
            logger.debug(f"Error extracting {selector}: {e}")
        
        return ""
    
    def _extract_attribute(self, element, selector: str, attr: str) -> str:
        """Extract attribute from CSS selector"""
        if not element:
            return ""
        
        try:
            found = element.select_one(selector)
            if found:
                return found.get(attr, "")
        except Exception as e:
            logger.debug(f"Error extracting {selector}@{attr}: {e}")
        
        return ""
    
    def _parse_price(self, price_str: str) -> float:
        """Parse price string to float (handle ₪ and commas)"""
        try:
            # Remove currency symbols and whitespace
            clean = price_str.replace("₪", "").replace(",", ".").strip()
            return float(clean)
        except ValueError:
            logger.warning(f"Could not parse price: {price_str}")
            return 0.0
    
    @abstractmethod
    def scrape(self) -> List[Dict]:
        """Scrape store and return list of product dicts
        
        Each dict should have:
        {
            'title': str,
            'artist': str,
            'album': str,
            'format': str (optional),
            'cover_art_url': str (optional),
            'price_ils': float,
            'in_stock': bool,
            'quantity_available': int,
            'store_url': str,
        }
        """
        pass
    
    def get_results(self) -> Dict:
        """Get scrape results summary"""
        return {
            'store_key': self.store_key,
            'records_scraped': self.records_scraped,
            'errors': self.errors,
            'error_count': len(self.errors),
        }
    
    def __del__(self):
        """Cleanup session"""
        if hasattr(self, 'session'):
            self.session.close()
