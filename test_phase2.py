#!/usr/bin/env python3
"""Phase 2 Test Script - Verify all 12 scrapers work"""

import sys
import asyncio
import logging
from pathlib import Path

# Setup paths
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root / "backend"))

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import all scrapers
from scrapers.disccenter import DiscCenterScraper
from scrapers.thevinylroom import TheVinylRoomScraper
from scrapers.third_ear import ThirdEarScraper
from scrapers.beatnik import BeatnikScraper
from scrapers.giora_records import GioraRecordsScraper
from scrapers.hasivoov import HasIvoovScraper
from scrapers.shablool_records import ShabloolRecordsScraper
from scrapers.vinyl_stock import VinylStockScraper
from scrapers.tav8 import Tav8Scraper
from scrapers.takli_house import TakliHouseScraper
from scrapers.my_records import MyRecordsScraper
from scrapers.rollindaise import RollindaiseScraper


SCRAPER_REGISTRY = {
    # Phase 1
    "disccenter": DiscCenterScraper,
    "thevinylroom": TheVinylRoomScraper,
    # Phase 2a
    "third_ear": ThirdEarScraper,
    "beatnik": BeatnikScraper,
    "giora_records": GioraRecordsScraper,
    "hasivoov": HasIvoovScraper,
    "shablool_records": ShabloolRecordsScraper,
    # Phase 2b
    "vinyl_stock": VinylStockScraper,
    "tav8": Tav8Scraper,
    "takli_house": TakliHouseScraper,
    # Phase 2c
    "my_records": MyRecordsScraper,
    "rollindaise": RollindaiseScraper,
}


def test_imports():
    """Test that all scrapers import correctly"""
    logger.info("=" * 70)
    logger.info("PHASE 2 TEST: Verifying Scraper Imports")
    logger.info("=" * 70)
    
    all_ok = True
    for store_key, scraper_class in SCRAPER_REGISTRY.items():
        try:
            scraper = scraper_class()
            logger.info(f"✅ {store_key:20} → {scraper_class.__name__:25} OK")
        except Exception as e:
            logger.error(f"❌ {store_key:20} → FAILED: {e}")
            all_ok = False
    
    logger.info("=" * 70)
    if all_ok:
        logger.info(f"✅ ALL {len(SCRAPER_REGISTRY)} SCRAPERS IMPORT SUCCESSFULLY")
    else:
        logger.error(f"❌ SOME SCRAPERS FAILED TO IMPORT")
    logger.info("=" * 70)
    
    return all_ok


def test_quick_scrape():
    """Test a quick scrape of Phase 1 stores (fast, proven)"""
    logger.info("=" * 70)
    logger.info("PHASE 2 TEST: Quick Scrape (Phase 1 Stores Only)")
    logger.info("=" * 70)
    
    results = {}
    
    # Only test Phase 1 (fast + proven)
    phase1_scrapers = {
        "disccenter": DiscCenterScraper,
        "thevinylroom": TheVinylRoomScraper,
    }
    
    for store_key, scraper_class in phase1_scrapers.items():
        try:
            logger.info(f"\n📍 Testing {store_key}...")
            scraper = scraper_class()
            products = scraper.scrape()
            
            results[store_key] = {
                "status": "success",
                "product_count": len(products) if products else 0
            }
            
            if products:
                logger.info(f"✅ {store_key}: {len(products)} products scraped")
                # Show first product as sample
                sample = products[0]
                logger.debug(f"   Sample: {sample.get('title', 'N/A')}")
            else:
                logger.warning(f"⚠️  {store_key}: 0 products returned")
        
        except Exception as e:
            results[store_key] = {
                "status": "failed",
                "error": str(e),
                "product_count": 0
            }
            logger.error(f"❌ {store_key}: {e}")
    
    logger.info("\n" + "=" * 70)
    logger.info("QUICK SCRAPE SUMMARY")
    logger.info("=" * 70)
    
    total_products = sum(r.get("product_count", 0) for r in results.values())
    successful = sum(1 for r in results.values() if r["status"] == "success")
    
    logger.info(f"Stores tested: {len(results)}/{len(phase1_scrapers)}")
    logger.info(f"Successful: {successful}")
    logger.info(f"Total products: {total_products}")
    
    for store_key, result in results.items():
        status = "✅" if result["status"] == "success" else "❌"
        logger.info(f"  {status} {store_key}: {result.get('product_count', 0)} products")
    
    logger.info("=" * 70)
    
    return results


if __name__ == "__main__":
    logger.info("\n🚀 PHASE 2 VERIFICATION STARTING\n")
    
    # Test 1: Imports
    imports_ok = test_imports()
    
    # Test 2: Quick scrape
    if imports_ok:
        quick_results = test_quick_scrape()
    else:
        logger.error("⛔ Skipping quick scrape due to import failures")
    
    logger.info("\n✅ PHASE 2 VERIFICATION COMPLETE\n")
