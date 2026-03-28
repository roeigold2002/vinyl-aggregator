#!/usr/bin/env python3
"""
Quick-start deployment launcher with credential validation
"""

import os
import sys
import subprocess
import json
from pathlib import Path
from getpass import getpass

def check_tools():
    """Verify required CLI tools"""
    tools = {
        'git': 'git --version',
        'python': 'python --version'
    }
    
    print("\n🔍 Checking required tools...")
    missing = []
    
    for tool, cmd in tools.items():
        result = subprocess.run(cmd, shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"  ✓ {tool}")
        else:
            print(f"  ✗ {tool} NOT FOUND")
            missing.append(tool)
    
    if missing:
        print(f"\n❌ Missing tools: {', '.join(missing)}")
        return False
    
    print("\n⚠️  Optional but recommended:")
    optional = {
        'gh': 'GitHub CLI (npm install -g gh)',
        'railway': 'Railway CLI (npm install -g railway)',
        'vercel': 'Vercel CLI (npm install -g vercel)'
    }
    
    for tool, install_cmd in optional.items():
        result = subprocess.run(f"{tool} --version", shell=True, capture_output=True)
        if result.returncode == 0:
            print(f"  ✓ {tool}")
        else:
            print(f"  ⚠️  {tool} - {install_cmd}")
    
    return True

def get_credentials():
    """Interactively get deployment credentials"""
    print("\n" + "="*70)
    print("DEPLOYMENT CREDENTIALS COLLECTION")
    print("="*70)
    
    credentials = {}
    
    # GitHub
    print("\n📦 GITHUB")
    print("  Get token: https://github.com/settings/tokens")
    print("  Scopes needed: repo, workflow")
    
    credentials['github_token'] = getpass("  GitHub Personal Access Token: ").strip()
    credentials['github_username'] = input("  GitHub Username: ").strip()
    credentials['github_repo'] = input("  GitHub Repo URL (https://github.com/user/repo): ").strip()
    
    # Railway
    print("\n🚄 RAILWAY")
    print("  Create account: https://railway.app")
    print("  Get token: Account Settings → API Tokens")
    
    credentials['railway_token'] = getpass("  Railway API Token: ").strip()
    credentials['railway_project'] = input("  Railway Project ID (or 'new'): ").strip() or "new"
    credentials['postgres_password'] = getpass("  PostgreSQL Password (choose complex): ").strip()
    
    if len(credentials['postgres_password']) < 12:
        print("  ⚠️  Password should be at least 12 characters")
        return None
    
    # Vercel
    print("\n▲ VERCEL")
    print("  Create account: https://vercel.com")
    print("  Get token: Settings → Tokens")
    
    credentials['vercel_token'] = getpass("  Vercel API Token: ").strip()
    credentials['vercel_project'] = input("  Vercel Project Name: ").strip()
    credentials['vercel_team'] = input("  Vercel Team ID (optional, press Enter): ").strip() or None
    
    return credentials

def validate_credentials(creds):
    """Validate credential format"""
    print("\n🔐 Validating credentials...")
    
    checks = [
        (creds.get('github_token'), "GitHub token", 20),
        (creds.get('railway_token'), "Railway token", 20),
        (creds.get('vercel_token'), "Vercel token", 20),
        (creds.get('postgres_password'), "PostgreSQL password", 12),
        (creds.get('github_username'), "GitHub username", 3),
        (creds.get('github_repo'), "GitHub repo URL", 10),
        (creds.get('vercel_project'), "Vercel project", 3),
    ]
    
    valid = True
    for value, name, min_len in checks:
        if not value or len(value) < min_len:
            print(f"  ✗ {name} is invalid or too short")
            valid = False
        else:
            display = value[:10] + "..." if len(value) > 10 else value
            print(f"  ✓ {name}")
    
    return valid

def save_credentials(creds):
    """Save credentials to file"""
    cred_file = Path("e:/Code/Project V/.deployment_credentials.json")
    
    try:
        with open(cred_file, 'w') as f:
            json.dump(creds, f, indent=2)
        os.chmod(cred_file, 0o600)  # Read-only
        print(f"\n✓ Credentials saved securely to {cred_file}")
        return True
    except Exception as e:
        print(f"\n✗ Failed to save credentials: {e}")
        return False

def start_deployment():
    """Start the actual deployment"""
    print("\n" + "="*70)
    print("STARTING PRODUCTION DEPLOYMENT")
    print("="*70)
    print("\nRunning deploy.py...")
    print("This will take 10-20 minutes depending on network speed.\n")
    
    try:
        subprocess.run([sys.executable, "e:\\Code\\Project V\\deploy.py"], check=True)
        print("\n✅ Deployment completed!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Deployment failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

def main():
    print("""
    ╔═══════════════════════════════════════════════════════════════╗
    ║  ISRAELI VINYL RECORD AGGREGATOR - PRODUCTION DEPLOYMENT      ║
    ║              Quick-Start Launcher (Interactive)               ║
    ╚═══════════════════════════════════════════════════════════════╝
    """)
    
    # Step 1: Check tools
    if not check_tools():
        print("\n❌ Required tools not found. Please install Git and Python 3.11+")
        sys.exit(1)
    
    # Step 2: Get credentials
    credentials = get_credentials()
    if not credentials:
        print("\n❌ Failed to collect credentials")
        sys.exit(1)
    
    # Step 3: Validate
    if not validate_credentials(credentials):
        print("\n❌ Invalid credentials. Please try again.")
        sys.exit(1)
    
    # Step 4: Save
    if not save_credentials(credentials):
        print("\n❌ Failed to save credentials")
        sys.exit(1)
    
    # Step 5: Confirm and start
    print("\n" + "="*70)
    print("DEPLOYMENT CONFIGURATION COMPLETE")
    print("="*70)
    print("\nCredentials collected and validated.")
    print("Ready to deploy to production.")
    
    confirm = input("\nStart deployment now? (yes/no): ").strip().lower()
    if confirm not in ['yes', 'y']:
        print("Deployment cancelled.")
        sys.exit(0)
    
    # Step 6: Deploy
    success = start_deployment()
    
    if success:
        print("\n🎉 Deployment successful!")
        print("\nNext steps:")
        print("1. Monitor Railway logs: railway logs --service backend")
        print("2. Check frontend is loading at your Vercel URL")
        print("3. Test search functionality")
        print("4. Monitor first scrape (5-10 minutes)")
    else:
        print("\n⚠️  Deployment encountered issues. Check DEPLOYMENT_LOG.md for details.")
    
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

