#!/usr/bin/env python3
"""
Comprehensive Pre-Deployment Validator
Ensures system is ready for production deployment
"""

import os
import sys
import json
import subprocess
from pathlib import Path
from datetime import datetime

class DeploymentValidator:
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.backend_dir = self.project_root / "backend"
        self.frontend_dir = self.project_root / "frontend"
        self.errors = []
        self.warnings = []
        self.checks_passed = 0
        self.checks_total = 0
    
    def check(self, name: str, condition: bool, error_msg: str = ""):
        """Record a check result"""
        self.checks_total += 1
        if condition:
            print(f"  ✓ {name}")
            self.checks_passed += 1
        else:
            print(f"  ✗ {name}")
            if error_msg:
                self.errors.append(f"{name}: {error_msg}")
    
    def warn(self, message: str):
        """Record a warning"""
        print(f"  ⚠ {message}")
        self.warnings.append(message)
    
    def validate_structure(self):
        """Validate project structure"""
        print("\n📁 CHECKING PROJECT STRUCTURE")
        
        # Check directories exist
        self.check("Backend directory exists", self.backend_dir.exists())
        self.check("Frontend directory exists", self.frontend_dir.exists())
        
        # Check critical backend files
        critical_backend = [
            "main.py",
            "config.py",
            "database.py",
            "models.py"
        ]
        
        for file in critical_backend:
            file_path = self.backend_dir / file
            self.check(f"Backend {file} exists", file_path.exists())
        
        # Check critical frontend files
        frontend_src = self.frontend_dir / "src"
        self.check("Frontend src directory exists", frontend_src.exists())
        self.check("Frontend package.json exists", (self.frontend_dir / "package.json").exists())
        
        # Check docker-compose
        self.check("docker-compose.yml exists", (self.project_root / "docker-compose.yml").exists())
    
    def validate_backend_code(self):
        """Validate backend code is deployable"""
        print("\n🔧 CHECKING BACKEND CODE")
        
        # Check main.py imports
        main_py = self.backend_dir / "main.py"
        if main_py.exists():
            try:
                with open(main_py, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.check("FastAPI imported", "from fastapi import FastAPI" in content)
                    self.check("CORS configured", "CORSMiddleware" in content)
                    self.check("Routes included", "router" in content or "routes" in content)
            except Exception as e:
                self.warn(f"Could not read main.py: {e}")
        
        # Check config.py
        config_py = self.backend_dir / "config.py"
        if config_py.exists():
            try:
                with open(config_py, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.check("STORE_CONFIGS defined", "STORE_CONFIGS" in content)
                    self.check("Multiple stores configured", content.count("'") > 20)  # Has many store entries
            except Exception as e:
                self.warn(f"Could not read config.py: {e}")
        
        # Check database.py
        db_py = self.backend_dir / "database.py"
        if db_py.exists():
            try:
                with open(db_py, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                    self.check("SQLAlchemy imported", "SQLAlchemy" in content or "sqlalchemy" in content)
                    self.check("Database models defined", "Base" in content or "declarative_base" in content)
            except Exception as e:
                self.warn(f"Could not read database.py: {e}")
    
    def validate_frontend_code(self):
        """Validate frontend code is deployable"""
        print("\n⚛️  CHECKING FRONTEND CODE")
        
        # Check package.json
        pkg_json = self.frontend_dir / "package.json"
        if pkg_json.exists():
            with open(pkg_json, 'r') as f:
                content = json.load(f)
                self.check("React dependency exists", "react" in content.get("dependencies", {}))
                self.check("Vite build tool exists", "vite" in content.get("devDependencies", {}))
                self.check("Build script defined", "build" in content.get("scripts", {}))
        
        # Check src directory
        src_dir = self.frontend_dir / "src"
        if src_dir.exists():
            self.check("App.jsx/tsx exists", 
                      (src_dir / "App.jsx").exists() or (src_dir / "App.tsx").exists())
            self.check("Components directory exists", (src_dir / "components").exists())
            pages_dir = src_dir / "pages"
            self.check("Pages directory exists", pages_dir.exists())
    
    def validate_documentation(self):
        """Validate deployment documentation"""
        print("\n📚 CHECKING DOCUMENTATION")
        
        docs = [
            "QUICK_START.md",
            "YOUR_ACTION_ITEMS.md",
            "DEPLOY_README.md",
            "DEPLOYMENT_INDEX.md"
        ]
        
        for doc in docs:
            doc_path = self.project_root / doc
            self.check(f"{doc} exists", doc_path.exists())
    
    def validate_deployment_scripts(self):
        """Validate deployment scripts exist and are executable"""
        print("\n🚀 CHECKING DEPLOYMENT SCRIPTS")
        
        scripts = [
            "quick_deploy.py",
            "deploy.py"
        ]
        
        for script in scripts:
            script_path = self.project_root / script
            exists = script_path.exists()
            self.check(f"{script} exists", exists)
            
            if exists:
                # Check it's valid Python
                try:
                    with open(script_path, 'r', encoding='utf-8', errors='ignore') as f:
                        compile(f.read(), script, 'exec')
                    self.check(f"{script} is valid Python", True)
                except SyntaxError as e:
                    self.check(f"{script} is valid Python", False, str(e))
                except Exception as e:
                    self.warn(f"Could not validate {script}: {e}")
    
    def validate_python_version(self):
        """Validate Python version"""
        print("\n🐍 CHECKING PYTHON")
        
        version = sys.version_info
        is_valid = version.major == 3 and version.minor >= 11
        self.check(f"Python 3.11+ (current: {version.major}.{version.minor})", is_valid)
    
    def validate_git(self):
        """Validate git is available"""
        print("\n📦 CHECKING GIT")
        
        result = subprocess.run("git --version", shell=True, capture_output=True)
        self.check("Git is installed", result.returncode == 0)
    
    def generate_report(self):
        """Generate validation report"""
        print("\n" + "="*70)
        print("VALIDATION REPORT")
        print("="*70)
        
        pct = (self.checks_passed / self.checks_total * 100) if self.checks_total > 0 else 0
        print(f"\nChecks Passed: {self.checks_passed}/{self.checks_total} ({pct:.0f}%)")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  - {warning}")
        
        if self.errors:
            print(f"\n❌ Errors ({len(self.errors)}):")
            for error in self.errors:
                print(f"  - {error}")
            return False
        
        print("\n✅ ALL CHECKS PASSED - System is ready for deployment!")
        return True
    
    def validate(self):
        """Run all validations"""
        print("""
        ╔═══════════════════════════════════════════════════════════╗
        ║     PRODUCTION DEPLOYMENT - SYSTEM VALIDATION            ║
        ║      Israeli Vinyl Record Aggregator                     ║
        ╚═══════════════════════════════════════════════════════════╝
        """)
        
        self.validate_python_version()
        self.validate_git()
        self.validate_structure()
        self.validate_backend_code()
        self.validate_frontend_code()
        self.validate_deployment_scripts()
        self.validate_documentation()
        
        ready = self.generate_report()
        
        if ready:
            print("\n" + "="*70)
            print("NEXT STEPS")
            print("="*70)
            print("""
1. Read QUICK_START.md for deployment overview

2. Get your credentials:
   - GitHub token: https://github.com/settings/tokens
   - Railway token: https://railway.app (Account Settings)
   - Vercel token: https://vercel.com/account/settings/tokens

3. Run deployment:
   python quick_deploy.py

4. Follow the interactive prompts

5. Your system will be live in 15-25 minutes!
            """)
            return True
        else:
            print("\nPlease fix the errors above before proceeding.")
            return False

def main():
    validator = DeploymentValidator()
    success = validator.validate()
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()

