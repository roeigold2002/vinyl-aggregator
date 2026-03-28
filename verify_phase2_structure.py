#!/usr/bin/env python3
"""Phase 2 Test - Structural Verification (No Dependencies)"""

import sys
import ast
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def verify_scraper_structure(scraper_path):
    """Verify a scraper file has correct structure"""
    try:
        with open(scraper_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        
        # Parse AST
        tree = ast.parse(content)
        
        # Find class definition
        classes = [node for node in tree.body if isinstance(node, ast.ClassDef)]
        if not classes:
            return False, "No class defined"
        
        main_class = classes[0]
        
        # Check required methods
        methods = {node.name for node in main_class.body if isinstance(node, ast.FunctionDef)}
        required = {'__init__', 'scrape'}
        missing = required - methods
        
        if missing:
            return False, f"Missing methods: {missing}"
        
        # Check inheritance
        if not main_class.bases:
            return False, "No base class"
        
        return True, "OK"
    
    except SyntaxError as e:
        return False, f"Syntax error: {e}"
    except Exception as e:
        return False, f"Error: {e}"


def main():
    logger.info("=" * 70)
    logger.info("PHASE 2 STRUCTURAL VERIFICATION")
    logger.info("=" * 70)
    
    backend_path = Path("e:/Code/Project V/backend/scrapers")
    
    scrapers = {
        "disccenter": "DiscCenterScraper",
        "thevinylroom": "TheVinylRoomScraper",
        "third_ear": "ThirdEarScraper",
        "beatnik": "BeatnikScraper",
        "giora_records": "GioraRecordsScraper",
        "hasivoov": "HasIvoovScraper",
        "shablool_records": "ShabloolRecordsScraper",
        "vinyl_stock": "VinylStockScraper",
        "tav8": "Tav8Scraper",
        "takli_house": "TakliHouseScraper",
        "my_records": "MyRecordsScraper",
        "rollindaise": "RollindaiseScraper",
    }
    
    results = {}
    
    for store_key, class_name in scrapers.items():
        scraper_file = backend_path / f"{store_key}.py"
        
        if not scraper_file.exists():
            results[store_key] = (False, "File not found")
            logger.error(f"❌ {store_key:20} - File not found")
            continue
        
        ok, msg = verify_scraper_structure(scraper_file)
        results[store_key] = (ok, msg)
        
        status = "✅" if ok else "❌"
        logger.info(f"{status} {store_key:20} - {class_name:25} - {msg}")
    
    # Summary
    logger.info("=" * 70)
    successful = sum(1 for ok, _ in results.values() if ok)
    logger.info(f"✅ STRUCTURAL VERIFICATION: {successful}/{len(scrapers)} scrapers OK")
    logger.info("=" * 70)
    
    # Verify scheduler imports all
    logger.info("\n" + "=" * 70)
    logger.info("VERIFYING SCHEDULER REGISTRY")
    logger.info("=" * 70)
    
    scheduler_path = Path("e:/Code/Project V/backend/services/scheduler.py")
    with open(scheduler_path, 'r', encoding='utf-8', errors='replace') as f:
        scheduler_content = f.read()
    
    for store_key, class_name in scrapers.items():
        if class_name in scheduler_content:
            logger.info(f"✅ {store_key:20} → imported in scheduler")
        else:
            logger.error(f"❌ {store_key:20} → NOT imported in scheduler")
        
        if f'"{store_key}"' in scheduler_content:
            logger.info(f"✅ {store_key:20} → registered in SCRAPER_REGISTRY")
        else:
            logger.error(f"❌ {store_key:20} → NOT registered in SCRAPER_REGISTRY")
    
    logger.info("=" * 70)
    logger.info("\n✅ PHASE 2 STRUCTURAL VERIFICATION COMPLETE\n")


if __name__ == "__main__":
    main()
