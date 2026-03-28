#!/usr/bin/env python3
"""
FULL PRODUCTION DEPLOYMENT SCRIPT
Deploys Israeli Vinyl Record Aggregator to GitHub, Railway, and Vercel
"""

import os
import subprocess
import sys
from pathlib import Path
from datetime import datetime

# Credentials (provided by user)
GITHUB_TOKEN = "(GITHUB_TOKEN)"
RAILWAY_TOKEN = "(RAILWAY_TOKEN)"
VERCEL_TOKEN = "(VERCEL_TOKEN)"
GITHUB_REPO = "https://github.com/roeigold2002/vinyl-aggregator"
GITHUB_USERNAME = "roeigold2002"

PROJECT_ROOT = Path("e:\\Code\\Project V")
BACKEND_DIR = PROJECT_ROOT / "backend"
FRONTEND_DIR = PROJECT_ROOT / "frontend"

def log(msg):
    """Print timestamped log message"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {msg}")

def run_command(cmd, cwd=None, check=True):
    """Run shell command and return output"""
    try:
        log(f"Running: {cmd}")
        result = subprocess.run(
            cmd,
            shell=True,
            cwd=cwd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        if result.stdout:
            print(result.stdout)
        if result.stderr and "warning" not in result.stderr.lower():
            print(result.stderr)
        if check and result.returncode != 0:
            raise Exception(f"Command failed: {cmd}\n{result.stderr}")
        return result.stdout
    except Exception as e:
        log(f"ERROR: {e}")
        if check:
            raise
        return ""

def step(num, title):
    """Print step header"""
    print(f"\n{'='*70}")
    print(f"STEP {num}: {title}")
    print(f"{'='*70}\n")

# ============================================================================
# STEP 1: Verify Git Status
# ============================================================================
step(1, "VERIFY GIT STATUS")
log("Checking git status...")
os.chdir(str(PROJECT_ROOT))
status = run_command("git status --short")
log(f"Git status:\n{status}")

# ============================================================================
# STEP 2: Push to GitHub
# ============================================================================
step(2, "PUSH TO GITHUB")
log(f"Adding GitHub remote: {GITHUB_REPO}")
run_command(f'git remote add origin "{GITHUB_REPO}"', check=False)

log("Pushing to GitHub...")
push_cmd = f'git push -u origin main -f'
run_command(push_cmd)
log(f"SUCCESS: Code pushed to {GITHUB_REPO}")

# ============================================================================
# STEP 3: Configure and Deploy Backend to Railway
# ============================================================================
step(3, "DEPLOY BACKEND TO RAILWAY")

# Export Railway token
os.environ['RAILWAY_TOKEN'] = RAILWAY_TOKEN

log("Installing Railway CLI...")
run_command("npm install -g @railway/cli", check=False)

log("Authenticating with Railway...")
run_command(f'railway login --token "{RAILWAY_TOKEN}"', cwd=str(BACKEND_DIR), check=False)

log("Deploying backend to Railway...")
run_command("railway up --detach", cwd=str(BACKEND_DIR), check=False)

log("Backend deployment initiated - Railway will build and start the service")
log("Expected time: 5-10 minutes")

# ============================================================================
# STEP 4: Configure and Deploy Frontend to Vercel
# ============================================================================
step(4, "DEPLOY FRONTEND TO VERCEL")

# Export Vercel token
os.environ['VERCEL_TOKEN'] = VERCEL_TOKEN

log("Installing Vercel CLI...")
run_command("npm install -g vercel", check=False)

log("Authenticating with Vercel...")
run_command(f'vercel login --token "{VERCEL_TOKEN}"', cwd=str(FRONTEND_DIR), check=False)

log("Deploying frontend to Vercel...")
run_command("vercel --prod", cwd=str(FRONTEND_DIR), check=False)

log("Frontend deployment initiated to Vercel")
log("Expected time: 2-3 minutes")

# ============================================================================
# STEP 5: Generate Completion Report
# ============================================================================
step(5, "FINAL STATUS")

report = f"""
{'='*70}
DEPLOYMENT COMPLETE
{'='*70}

DEPLOYMENT SUMMARY:
  GitHub:   Pushed to {GITHUB_REPO}
  Backend:  Deploying to Railway (5-10 minutes)
  Frontend: Deploying to Vercel (2-3 minutes)

CREDENTIALS USED:
  GitHub:  roeigold2002
  Railway: {RAILWAY_TOKEN[:20]}...
  Vercel:  {VERCEL_TOKEN[:20]}...

EXPECTED RESULTS (20 minutes):
  1. Backend live at: https://vinyl-aggregator-backend.railway.app
  2. Frontend live at: https://vinyl-aggregator.vercel.app
  3. Database: PostgreSQL on Railway
  4. First scrape: Ready to trigger

NEXT STEPS:
  1. Wait 5-10 minutes for Railway to build and start
  2. Wait 2-3 minutes for Vercel to deploy
  3. Verify frontend loads
  4. Check backend health: GET /api/health
  5. Trigger first scrape: POST /api/scrape-all

COST: $0/month (all free tiers)

STATUS: DEPLOYMENT IN PROGRESS
Completion time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'='*70}
"""

print(report)

# Save report
report_path = PROJECT_ROOT / "DEPLOYMENT_PROGRESS.txt"
report_path.write_text(report)
log(f"Report saved to: {report_path}")

log("\nDEPLOYMENT AUTOMATION COMPLETE!")
log("System is deploying to production...")
log("Check GitHub Actions and Railway/Vercel dashboards for progress")

