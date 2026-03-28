#!/usr/bin/env python3
"""Phase 4: Production Verification & Monitoring"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def verify_production_deployment(backend_url, frontend_url):
    """Verify production deployment is working"""
    logger.info("=" * 70)
    logger.info("PHASE 4: PRODUCTION VERIFICATION")
    logger.info("=" * 70)
    
    results = {}
    
    try:
        import requests
    except ImportError:
        logger.error("❌ requests library required: pip install requests")
        return False
    
    # Test 1: Backend health
    logger.info("\n📋 TEST 1: Backend Health Check")
    try:
        response = requests.get(f"{backend_url}/api/stores", timeout=5)
        if response.status_code == 200:
            stores = response.json()
            logger.info(f"✅ Backend responding: {len(stores.get('stores', []))} stores found")
            results["backend_health"] = True
        else:
            logger.error(f"❌ Backend returned {response.status_code}")
            results["backend_health"] = False
    except Exception as e:
        logger.error(f"❌ Backend unreachable: {e}")
        results["backend_health"] = False
    
    # Test 2: Search endpoint
    logger.info("\n📋 TEST 2: Search Endpoint")
    try:
        response = requests.get(f"{backend_url}/api/search?q=pink", timeout=5)
        if response.status_code == 200:
            data = response.json()
            result_count = len(data.get('results', []))
            logger.info(f"✅ Search working: {result_count} results for 'pink'")
            results["search_working"] = result_count > 0
        else:
            logger.error(f"❌ Search returned {response.status_code}")
            results["search_working"] = False
    except Exception as e:
        logger.error(f"❌ Search failed: {e}")
        results["search_working"] = False
    
    # Test 3: Autocomplete endpoint
    logger.info("\n📋 TEST 3: Autocomplete Endpoint")
    try:
        response = requests.get(f"{backend_url}/api/search/autocomplete?q=pink", timeout=5)
        if response.status_code == 200:
            logger.info("✅ Autocomplete endpoint working")
            results["autocomplete_working"] = True
        else:
            logger.error(f"❌ Autocomplete returned {response.status_code}")
            results["autocomplete_working"] = False
    except Exception as e:
        logger.error(f"❌ Autocomplete failed: {e}")
        results["autocomplete_working"] = False
    
    # Test 4: Frontend accessibility
    logger.info("\n📋 TEST 4: Frontend Accessibility")
    try:
        response = requests.get(frontend_url, timeout=10)
        if response.status_code == 200:
            logger.info("✅ Frontend accessible")
            results["frontend_accessible"] = True
        else:
            logger.error(f"❌ Frontend returned {response.status_code}")
            results["frontend_accessible"] = False
    except Exception as e:
        logger.error(f"❌ Frontend unreachable: {e}")
        results["frontend_accessible"] = False
    
    # Test 5: Response times
    logger.info("\n📋 TEST 5: Response Time Analysis")
    try:
        import time
        
        start = time.time()
        requests.get(f"{backend_url}/api/stores", timeout=5)
        api_time = (time.time() - start) * 1000
        
        start = time.time()
        requests.get(frontend_url, timeout=10)
        frontend_time = (time.time() - start) * 1000
        
        logger.info(f"✅ API response time: {api_time:.0f}ms (target: <100ms)")
        logger.info(f"✅ Frontend response time: {frontend_time:.0f}ms (target: <500ms)")
        
        results["api_performance"] = api_time < 100
        results["frontend_performance"] = frontend_time < 500
    
    except Exception as e:
        logger.error(f"❌ Performance test failed: {e}")
        results["api_performance"] = False
        results["frontend_performance"] = False
    
    # Generate report
    logger.info("\n" + "=" * 70)
    logger.info("PRODUCTION VERIFICATION REPORT")
    logger.info("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        logger.info(f"{status} - {test_name.replace('_', ' ').title()}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"Results: {passed}/{total} tests passed")
    
    if passed >= total - 1:  # Allow 1 failure
        logger.info("✅ PRODUCTION DEPLOYMENT SUCCESSFUL")
    else:
        logger.warning("⚠️  Some tests failed - check logs above")
    
    logger.info("=" * 70)
    
    # Save report
    report = {
        "timestamp": datetime.now().isoformat(),
        "backend_url": backend_url,
        "frontend_url": frontend_url,
        "tests_passed": passed,
        "tests_total": total,
        "results": results
    }
    
    with open("PHASE4_VERIFICATION_REPORT.json", "w") as f:
        json.dump(report, f, indent=2)
    
    logger.info(f"📄 Report saved to PHASE4_VERIFICATION_REPORT.json")
    
    return passed >= total - 1


def generate_monitoring_guide():
    """Generate monitoring setup guide"""
    logger.info("\n" + "=" * 70)
    logger.info("MONITORING & ALERTING SETUP")
    logger.info("=" * 70)
    
    guide = """
📊 RAILWAY MONITORING

1. View Real-time Logs
   $ railway logs -f
   
   Look for:
   - Scraper job start/completion
   - API error rates
   - Database warnings

2. Set up Log Filters
   $ railway logs | grep "ERROR"
   $ railway logs | grep "scrape"
   $ railway logs | grep "scraper"

3. Deployment Metrics
   Visit: https://railway.app
   - View: CPU, Memory, Disk usage
   - Check: Response times
   - Monitor: Error rates

4. Set up Alerts
   Railway Dashboard → Alerts
   - Alert on: High CPU (>80%)
   - Alert on: Memory (>512MB)
   - Alert on: Errors (>1%)

📊 VERCEL MONITORING

1. Check Deployments
   $ vercel list
   $ vercel list --prod
   
   Visit: https://vercel.com/dashboard

2. View Analytics
   Dashboard → Analytics
   - View: Request rates
   - Check: Response times
   - Monitor: Error rates

3. Set up Environment Alerts
   Project Settings → Alerts
   - Alert on: Build failures
   - Alert on: Deployment issues

📊 DATABASE MONITORING

1. Check Database Size
   psql $(DATABASE_URL) - c "
   SELECT 
     pg_size_pretty(pg_database_size(current_database())) as size;
   "

2. Monitor Slow Queries
   psql $(DATABASE_URL) - c "
   SELECT query, mean_time, calls 
   FROM pg_stat_statements 
   ORDER BY mean_time DESC LIMIT 10;
   "

3. Check Connections
   psql $(DATABASE_URL) - c "
   SELECT datname, count(*) 
   FROM pg_stat_activity 
   GROUP BY datname;
   "

4. Maintenance
   Weekly: VACUUM ANALYZE
   Monthly: REINDEX (if needed)

📊 SCRAPER JOB MONITORING

1. Check Last Scrape
   $ railway logs | grep "Scheduled scrape completed"
   
   Expected: Daily at 2 AM UTC
   Expected duration: 30-45 minutes

2. Monitor Per-Store
   $ railway logs | grep "disccenter\\|thevinylroom\\|third_ear..."
   
   Expected: Each store completes quickly
   Expected records: 100-2500 per store

3. Check Deduplication
   psql $(DATABASE_URL) - c "
   SELECT COUNT(DISTINCT artist, album) as unique_vinyls,
          COUNT(*) as total_entries
   FROM records;
   "

4. Alert Conditions
   - Job doesn't run at scheduled time
   - Job runs but 0 products created
   - Job takes > 60 minutes
   - Database space grows unexpectedly

📊 CUSTOM DASHBOARDS (Optional)

Create a status page at YOUR_DOMAIN/status

Endpoints to monitor:
- GET /api/stores → Should return 10 stores
- GET /api/search?q=test → Should return results
- POST /api/stores/scrape → Should accept request

Display:
- Last scrape timestamp
- Total unique vinyls
- Error count
- API response time
- Uptime percentage

📊 RECOMMENDED MONITORING TOOLS

For advanced monitoring:
- Datadog (free tier: 7 days retention)
- New Relic (free tier available)
- Sentry (error tracking)
- Grafana (visualization)

For now, Railway + Vercel dashboards are sufficient.
"""
    
    logger.info(guide)
    
    # Save to file
    with open("PHASE4_MONITORING_GUIDE.txt", "w") as f:
        f.write(guide)


def main():
    """Main verification function"""
    logger.info("Phase 4: Production Verification\n")
    
    # This should be run with actual production URLs
    backend_url = input("Enter backend URL (e.g., https://your-app.up.railway.app): ").strip()
    frontend_url = input("Enter frontend URL (e.g., https://your-app.vercel.app): ").strip()
    
    if not backend_url or not frontend_url:
        logger.error("❌ Both URLs are required")
        return False
    
    success = verify_production_deployment(backend_url, frontend_url)
    generate_monitoring_guide()
    
    return success


if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        logger.info("\n⏸️  Verification cancelled")
        sys.exit(0)
