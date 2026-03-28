"""Package init for scrapers"""
# Phase 1: Easy stores
from .disccenter import DiscCenterScraper
from .thevinylroom import TheVinylRoomScraper

# Phase 2a: WooCommerce stores
from .third_ear import ThirdEarScraper
from .beatnik import BeatnikScraper
from .giora_records import GioraRecordsScraper
from .hasivoov import HasIvoovScraper
from .shablool_records import ShabloolRecordsScraper

# Phase 2b: Custom platforms
from .vinyl_stock import VinylStockScraper
from .tav8 import Tav8Scraper
from .takli_house import TakliHouseScraper

# Phase 2c: Problematic
from .my_records import MyRecordsScraper
from .rollindaise import RollindaiseScraper

__all__ = [
    # Phase 1
    "DiscCenterScraper",
    "TheVinylRoomScraper",
    # Phase 2a
    "ThirdEarScraper",
    "BeatnikScraper",
    "GioraRecordsScraper",
    "HasIvoovScraper",
    "ShabloolRecordsScraper",
    # Phase 2b
    "VinylStockScraper",
    "Tav8Scraper",
    "TakliHouseScraper",
    # Phase 2c
    "MyRecordsScraper",
    "RollindaiseScraper",
]
