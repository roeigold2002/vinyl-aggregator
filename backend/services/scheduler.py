"""Scheduler service for periodic scraping jobs"""
import logging
import time
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from sqlalchemy.orm import Session

# Phase 1: Easy stores (Custom)
from scrapers.disccenter import DiscCenterScraper
from scrapers.thevinylroom import TheVinylRoomScraper

# Phase 2a: WooCommerce stores
from scrapers.third_ear import ThirdEarScraper
from scrapers.beatnik import BeatnikScraper
from scrapers.giora_records import GioraRecordsScraper
from scrapers.hasivoov import HasIvoovScraper
from scrapers.shablool_records import ShabloolRecordsScraper

# Phase 2b: Custom platforms
from scrapers.vinyl_stock import VinylStockScraper
from scrapers.tav8 import Tav8Scraper
from scrapers.takli_house import TakliHouseScraper

# Phase 2c: Problematic (blocked)
from scrapers.my_records import MyRecordsScraper
from scrapers.rollindaise import RollindaiseScraper

from services.aggregator import AggregationService
from models import Store

logger = logging.getLogger(__name__)

# Global scheduler instance
scheduler: BackgroundScheduler = None

# Scraper registry - maps store_key to scraper class
SCRAPER_REGISTRY = {
    # Phase 1: Easy stores
    "disccenter": DiscCenterScraper,
    "thevinylroom": TheVinylRoomScraper,
    
    # Phase 2a: WooCommerce stores
    "third_ear": ThirdEarScraper,
    "beatnik": BeatnikScraper,
    "giora_records": GioraRecordsScraper,
    "hasivoov": HasIvoovScraper,
    "shablool_records": ShabloolRecordsScraper,
    
    # Phase 2b: Custom platforms
    "vinyl_stock": VinylStockScraper,
    "tav8": Tav8Scraper,
    "takli_house": TakliHouseScraper,
    
    # Phase 2c: Problematic (blocked)
    "my_records": MyRecordsScraper,
    "rollindaise": RollindaiseScraper,
}


def init_scheduler(db_session_factory):
    """Initialize scheduler"""
    global scheduler
    
    scheduler = BackgroundScheduler()
    
    # Schedule scraping job for 2 AM IST daily
    # IST is UTC+2, so 2 AM IST = 12 AM UTC (midnight UTC in winter, 11 PM UTC in summer)
    scheduler.add_job(
        scrape_all_stores,
        CronTrigger(hour=0, minute=0, timezone='UTC'),  # Adjust based on actual IST offset
        args=[db_session_factory],
        id='scrape_all_stores',
        name='Scrape all vinyl stores',
        replace_existing=True,
    )
    
    scheduler.start()
    logger.info("✅ Scheduler initialized")


def stop_scheduler():
    """Stop scheduler"""
    global scheduler
    if scheduler and scheduler.running:
        scheduler.shutdown()
        logger.info("✅ Scheduler stopped")


def scrape_all_stores(db_session_factory):
    """Scrape all configured stores from registry"""
    logger.info(f"🔄 Starting scheduled scrape of {len(SCRAPER_REGISTRY)} stores...")
    
    start_time = time.time()
    results = {}
    
    db = db_session_factory()
    try:
        aggregator = AggregationService(db)
        
        for store_key, scraper_class in SCRAPER_REGISTRY.items():
            logger.info(f"📍 Starting {store_key} scrape...")
            
            # Find store in database
            store = db.query(Store).filter(Store.store_key == store_key).first()
            if not store:
                logger.warning(f"⚠️  Store '{store_key}' not found in database, skipping")
                continue
            
            try:
                # Instantiate and run scraper
                scraper = scraper_class()
                products = scraper.scrape()
                
                # Aggregate results
                if products:
                    created, updated, errors = aggregator.aggregate_scrape_results(
                        store.id,
                        products
                    )
                    results[store_key] = {
                        "created": created,
                        "updated": updated,
                        "errors": len(errors),
                        "status": "success"
                    }
                    logger.info(
                        f"✅ {store_key}: {created} created, {updated} updated, "
                        f"{len(errors)} errors"
                    )
                else:
                    results[store_key] = {
                        "created": 0,
                        "updated": 0,
                        "errors": 0,
                        "status": "no_products"
                    }
                    logger.warning(f"⚠️  {store_key} returned 0 products")
            
            except Exception as e:
                results[store_key] = {
                    "created": 0,
                    "updated": 0,
                    "errors": 1,
                    "status": "failed",
                    "error_message": str(e)
                }
                logger.error(f"❌ {store_key} scrape failed: {e}")
            
            # Delay between requests (respectful scraping)
            time.sleep(3)
        
        # Summary
        elapsed = time.time() - start_time
        total_created = sum(r.get("created", 0) for r in results.values())
        total_updated = sum(r.get("updated", 0) for r in results.values())
        successful = sum(1 for r in results.values() if r["status"] == "success")
        
        logger.info(
            f"✅ Scheduled scrape completed in {elapsed:.2f}s: "
            f"{successful}/{len(SCRAPER_REGISTRY)} stores, "
            f"{total_created} created, {total_updated} updated"
        )
    
    except Exception as e:
        logger.error(f"❌ Scheduled scrape failed: {e}")
    
    finally:
        db.close()


def trigger_scrape_manually(db_session_factory):
    """Manually trigger a full scrape (useful for testing/API)"""
    scrape_all_stores(db_session_factory)
