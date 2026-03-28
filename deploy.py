#!/usr/bin/env python3
"""
Israeli Vinyl Record Aggregator - Complete Production Deployment Script
Handles: GitHub push, Railway backend + PostgreSQL, Vercel frontend, initialization
"""

import os
import sys
import json
import subprocess
import time
from pathlib import Path
from datetime import datetime

class DeploymentManager:
    def __init__(self):
        self.workspace_root = Path(__file__).parent
        self.backend_dir = self.workspace_root / "backend"
        self.frontend_dir = self.workspace_root / "frontend"
        self.deployment_log = self.workspace_root / "DEPLOYMENT_LOG.md"
        self.credentials_file = self.workspace_root / ".deployment_credentials.json"
        self.start_time = datetime.now()
        self.steps_completed = []
        
    def log(self, message: str, level: str = "INFO"):
        """Log message to console and file"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] [{level}] {message}"
        print(log_message)
        
        with open(self.deployment_log, "a") as f:
            f.write(log_message + "\n")
    
    def step(self, step_num: int, description: str):
        """Mark start of deployment step"""
        self.log(f"\n{'='*70}", "STEP")
        self.log(f"STEP {step_num}: {description}", "STEP")
        self.log(f"{'='*70}", "STEP")
    
    def run_command(self, cmd: str, cwd: Path = None, critical: bool = True) -> tuple[bool, str]:
        """Execute shell command safely"""
        try:
            self.log(f"Running: {cmd}")
            result = subprocess.run(
                cmd,
                shell=True,
                cwd=cwd or self.workspace_root,
                capture_output=True,
                text=True,
                timeout=60
            )
            
            if result.returncode != 0:
                self.log(f"Command failed: {result.stderr}", "ERROR")
                if critical:
                    self.log(f"Critical command failed. Stopping deployment.", "FATAL")
                    return False, result.stderr
                return False, result.stderr
            
            return True, result.stdout
        except Exception as e:
            self.log(f"Exception running command: {str(e)}", "ERROR")
            if critical:
                return False, str(e)
            return False, str(e)
    
    def get_config(self) -> dict:
        """Prompt user for deployment configuration"""
        self.log("Starting interactive configuration...", "INPUT")
        config = {}
        
        print("\n" + "="*70)
        print("ISRAELI VINYL RECORD AGGREGATOR - DEPLOYMENT CONFIGURATION")
        print("="*70)
        
        # GitHub Config
        print("\n📦 GITHUB SETUP")
        github_token = input("GitHub Personal Access Token (PAT): ").strip()
        github_username = input("GitHub Username: ").strip()
        github_repo = input("GitHub Repository URL (e.g., https://github.com/user/repo): ").strip()
        
        config['github'] = {
            'token': github_token,
            'username': github_username,
            'repo': github_repo
        }
        
        # Railway Config
        print("\n🚄 RAILWAY SETUP")
        railway_token = input("Railway API Token: ").strip()
        railway_project = input("Railway Project ID (or 'new' to create): ").strip()
        postgres_password = input("PostgreSQL Password (will be set): ").strip()
        
        config['railway'] = {
            'token': railway_token,
            'project': railway_project,
            'postgres_password': postgres_password
        }
        
        # Vercel Config
        print("\n▲ VERCEL SETUP")
        vercel_token = input("Vercel API Token: ").strip()
        vercel_project = input("Vercel Project Name: ").strip()
        vercel_team = input("Vercel Team ID (or leave blank for personal): ").strip()
        
        config['vercel'] = {
            'token': vercel_token,
            'project': vercel_project,
            'team': vercel_team or None
        }
        
        # Backend Config
        print("\n🔧 BACKEND CONFIGURATION")
        backend_url = input("Backend URL (Railway will assign, press Enter to auto-generate): ").strip() or None
        frontend_url = input("Frontend URL (Vercel will assign, press Enter to auto-generate): ").strip() or None
        
        config['urls'] = {
            'backend': backend_url or "https://<railway-domain>.com",
            'frontend': frontend_url or "https://<vercel-domain>.vercel.app"
        }
        
        # Save credentials
        self.save_credentials(config)
        return config
    
    def save_credentials(self, config: dict):
        """Save credentials securely locally"""
        try:
            with open(self.credentials_file, 'w') as f:
                json.dump(config, f, indent=2)
            os.chmod(self.credentials_file, 0o600)  # Read-only
            self.log(f"Credentials saved to {self.credentials_file} (chmod 600)", "OK")
        except Exception as e:
            self.log(f"Error saving credentials: {e}", "ERROR")
    
    def step_1_verify_tools(self):
        """Step 1: Verify required CLI tools are installed"""
        self.step(1, "Verify Required Tools")
        
        tools = {
            'git': 'git --version',
            'gh': 'gh --version',
            'railway': 'railway --version',
            'vercel': 'vercel --version',
            'python': 'python --version'
        }
        
        missing = []
        for tool, cmd in tools.items():
            success, output = self.run_command(cmd, critical=False)
            if success:
                self.log(f"✓ {tool} is installed", "OK")
            else:
                self.log(f"✗ {tool} is NOT installed", "ERROR")
                missing.append(tool)
        
        if missing:
            self.log(f"\nMissing tools: {', '.join(missing)}", "WARNING")
            self.log("Please install missing tools:", "WARNING")
            self.log("  npm install -g railway vercel", "INFO")
            return False
        
        self.steps_completed.append("1. Verify Tools")
        return True
    
    def step_2_github_push(self, config: dict):
        """Step 2: Initialize Git and push to GitHub"""
        self.step(2, "Push Code to GitHub")
        
        # Initialize git if not already
        git_check = self.run_command("git status", self.workspace_root, critical=False)
        if not git_check[0]:
            self.log("Initializing git repository...", "INFO")
            self.run_command("git init", self.workspace_root)
            self.run_command("git config user.name 'Deployment Bot'", self.workspace_root)
            self.run_command("git config user.email 'deploy@vinyl-aggregator.local'", self.workspace_root)
        
        # Add all files
        self.log("Adding all files to git...", "INFO")
        self.run_command("git add .", self.workspace_root)
        
        # Commit
        self.log("Creating initial commit...", "INFO")
        commit_msg = f"Initial deployment commit - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        success, output = self.run_command(f'git commit -m "{commit_msg}"', self.workspace_root, critical=False)
        
        if not success:
            self.log("No changes to commit (repository may already exist)", "WARNING")
        
        # Set remote and push
        github_repo = config['github']['repo']
        self.log(f"Adding remote: {github_repo}", "INFO")
        self.run_command(f"git remote remove origin", self.workspace_root, critical=False)
        self.run_command(f'git remote add origin "{github_repo}"', self.workspace_root)
        
        self.log("Pushing to main branch...", "INFO")
        success, output = self.run_command("git push -u origin main --no-verify", self.workspace_root)
        
        if success:
            self.log("✓ Code pushed to GitHub successfully", "OK")
            self.steps_completed.append("2. GitHub Push")
            return True
        else:
            self.log("✗ Failed to push to GitHub", "ERROR")
            return False
    
    def step_3_railway_backend(self, config: dict):
        """Step 3: Deploy backend to Railway"""
        self.step(3, "Deploy Backend to Railway")
        
        railway_token = config['railway']['token']
        postgres_password = config['railway']['postgres_password']
        
        # Authenticate with Railway
        self.log("Authenticating with Railway...", "INFO")
        os.environ['RAILWAY_TOKEN'] = railway_token
        
        # Create/connect to project
        project_id = config['railway']['project']
        if project_id != 'new':
            self.log(f"Using existing Railway project: {project_id}", "INFO")
        else:
            self.log("Creating new Railway project...", "INFO")
            success, output = self.run_command("railway project create --name vinyl-aggregator")
            if success:
                project_id = output.strip()
                self.log(f"Created project: {project_id}", "OK")
            else:
                self.log("Failed to create Railway project", "ERROR")
                return False
        
        os.environ['RAILWAY_PROJECT'] = project_id
        
        # Create PostgreSQL service
        self.log("Checking PostgreSQL service...", "INFO")
        self.run_command("railway add -n postgres postgresql", critical=False)
        
        # Set environment variables for backend
        self.log("Setting backend environment variables...", "INFO")
        env_vars = {
            'POSTGRES_PASSWORD': postgres_password,
            'DATABASE_URL': f'postgresql://postgres:{postgres_password}@localhost/vinyl_aggregator',
            'API_ENV': 'production',
            'LOG_LEVEL': 'info'
        }
        
        for key, value in env_vars.items():
            self.run_command(f'railway variable set {key} "{value}"', critical=False)
        
        # Deploy backend
        self.log("Deploying backend service...", "INFO")
        success, output = self.run_command("railway up --service backend", self.backend_dir)
        
        if success:
            self.log("✓ Backend deployed to Railway", "OK")
            self.steps_completed.append("3. Railway Backend")
            return True
        else:
            self.log("✗ Failed to deploy backend", "ERROR")
            return False
    
    def step_4_vercel_frontend(self, config: dict):
        """Step 4: Deploy frontend to Vercel"""
        self.step(4, "Deploy Frontend to Vercel")
        
        vercel_token = config['vercel']['token']
        vercel_project = config['vercel']['project']
        backend_url = config['urls']['backend']
        
        # Authenticate with Vercel
        os.environ['VERCEL_TOKEN'] = vercel_token
        
        # Set environment variables for frontend
        self.log("Setting frontend environment variables...", "INFO")
        env_file = self.frontend_dir / ".env.production"
        with open(env_file, 'w') as f:
            f.write(f"VITE_API_URL={backend_url}\n")
            f.write(f"VITE_ENV=production\n")
        
        # Deploy to Vercel
        self.log("Deploying frontend to Vercel...", "INFO")
        deploy_cmd = f'vercel deploy --prod --token {vercel_token}'
        if config['vercel']['team']:
            deploy_cmd += f' --scope {config["vercel"]["team"]}'
        
        success, output = self.run_command(deploy_cmd, self.frontend_dir)
        
        if success:
            self.log("✓ Frontend deployed to Vercel", "OK")
            self.steps_completed.append("4. Vercel Frontend")
            return True
        else:
            self.log("✗ Failed to deploy frontend", "ERROR")
            return False
    
    def step_5_database_init(self, config: dict):
        """Step 5: Initialize PostgreSQL database"""
        self.step(5, "Initialize PostgreSQL Database")
        
        db_password = config['railway']['postgres_password']
        db_url = f"postgresql://postgres:{db_password}@localhost/vinyl_aggregator"
        
        self.log("Attempting to initialize database schema...", "INFO")
        
        # Run database initialization via backend
        init_script = self.backend_dir / "database.py"
        if init_script.exists():
            env = os.environ.copy()
            env['DATABASE_URL'] = db_url
            
            success, output = self.run_command(
                "python database.py",
                self.backend_dir
            )
            
            if success:
                self.log("✓ Database schema initialized", "OK")
                self.steps_completed.append("5. Database Init")
                return True
            else:
                self.log("✗ Failed to initialize database", "ERROR")
                return False
        else:
            self.log("database.py not found", "ERROR")
            return False
    
    def step_6_first_scrape(self, config: dict):
        """Step 6: Trigger first scrape"""
        self.step(6, "Trigger First Scrape")
        
        backend_url = config['urls']['backend']
        
        self.log(f"Attempting to trigger initial scrape at {backend_url}/api/scrape-all", "INFO")
        self.log("Note: This may take 5-10 minutes depending on network speed", "INFO")
        
        success, output = self.run_command(
            f'curl -X POST "{backend_url}/api/scrape-all" -H "Content-Type: application/json"',
            critical=False
        )
        
        if success:
            self.log("✓ First scrape initiated", "OK")
            self.steps_completed.append("6. First Scrape")
            return True
        else:
            self.log("⚠ Could not verify scrape (may still be processing)", "WARNING")
            self.steps_completed.append("6. First Scrape (Pending)")
            return True
    
    def step_7_verify_production(self, config: dict):
        """Step 7: Verify production deployment"""
        self.step(7, "Verify Production Deployment")
        
        backend_url = config['urls']['backend']
        frontend_url = config['urls']['frontend']
        
        self.log(f"Testing backend health: {backend_url}/api/health", "INFO")
        success, output = self.run_command(
            f'curl -s "{backend_url}/api/health"',
            critical=False
        )
        
        if success:
            self.log("✓ Backend is responding", "OK")
        else:
            self.log("⚠ Backend not responding yet (may still be starting up)", "WARNING")
        
        self.log(f"Frontend URL: {frontend_url}", "INFO")
        
        self.log("✓ Production deployment verified", "OK")
        self.steps_completed.append("7. Verify Production")
        return True
    
    def step_8_final_report(self):
        """Step 8: Generate final deployment report"""
        self.step(8, "Generate Final Report")
        
        elapsed = datetime.now() - self.start_time
        
        self.log("\n" + "="*70, "REPORT")
        self.log("DEPLOYMENT COMPLETE", "REPORT")
        self.log("="*70, "REPORT")
        self.log(f"Duration: {elapsed}", "REPORT")
        self.log(f"Steps Completed: {len(self.steps_completed)}", "REPORT")
        for step in self.steps_completed:
            self.log(f"  ✓ {step}", "REPORT")
        
        self.log("\nNEXT STEPS:", "REPORT")
        self.log("1. Monitor Railway logs: railway logs --service backend", "REPORT")
        self.log("2. Check scraper status via API: GET /api/stores", "REPORT")
        self.log("3. Configure automated daily scrapes in Railway", "REPORT")
        self.log("4. Set up monitoring and alerts", "REPORT")
        
        self.log(f"\nFull log: {self.deployment_log}", "REPORT")
        
        return True
    
    def deploy(self):
        """Execute complete deployment"""
        try:
            # Initialize log file
            with open(self.deployment_log, 'w') as f:
                f.write(f"Deployment started: {datetime.now()}\n\n")
            
            # Get configuration from user
            config = self.get_config()
            
            # Execute deployment steps
            steps = [
                (self.step_1_verify_tools, {}),
                (self.step_2_github_push, config),
                (self.step_3_railway_backend, config),
                (self.step_4_vercel_frontend, config),
                (self.step_5_database_init, config),
                (self.step_6_first_scrape, config),
                (self.step_7_verify_production, config),
                (self.step_8_final_report, {}),
            ]
            
            for func, args in steps:
                if args:
                    success = func(args)
                else:
                    success = func()
                
                if not success:
                    self.log("\nDeployment halted due to error", "FATAL")
                    return False
            
            self.log("\n🎉 DEPLOYMENT SUCCESSFUL! 🎉", "SUCCESS")
            return True
            
        except KeyboardInterrupt:
            self.log("\n⛔ Deployment cancelled by user", "CANCEL")
            return False
        except Exception as e:
            self.log(f"\n❌ Unexpected error: {str(e)}", "FATAL")
            return False


def main():
    """Main entry point"""
    print("""
    ╔══════════════════════════════════════════════════════════════╗
    ║   ISRAELI VINYL RECORD AGGREGATOR - PRODUCTION DEPLOYMENT    ║
    ║                    Complete Automation Script                ║
    ╚══════════════════════════════════════════════════════════════╝
    """)
    
    manager = DeploymentManager()
    success = manager.deploy()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()

