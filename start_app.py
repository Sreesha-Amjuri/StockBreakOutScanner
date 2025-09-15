#!/usr/bin/env python3
"""
StockBreak Pro Application Launcher
Starts both backend and frontend with proper error handling
"""

import subprocess
import sys
import time
import os
import signal
import requests
from pathlib import Path

class StockBreakProLauncher:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.base_dir = Path(__file__).parent

    def check_prerequisites(self):
        """Check if all prerequisites are installed"""
        print("🔍 Checking prerequisites...")
        
        # Check Python
        try:
            result = subprocess.run([sys.executable, "--version"], capture_output=True, text=True)
            print(f"✅ Python: {result.stdout.strip()}")
        except:
            print("❌ Python not found")
            return False
        
        # Check Node.js
        try:
            result = subprocess.run(["node", "--version"], capture_output=True, text=True)
            print(f"✅ Node.js: {result.stdout.strip()}")
        except:
            print("❌ Node.js not found")
            return False
        
        # Check if backend dependencies are installed
        backend_dir = self.base_dir / "backend"
        if not (backend_dir / "requirements.txt").exists():
            print("❌ Backend requirements.txt not found")
            return False
        
        # Check if frontend dependencies are installed
        frontend_dir = self.base_dir / "frontend"
        if not (frontend_dir / "package.json").exists():
            print("❌ Frontend package.json not found")
            return False
        
        print("✅ All prerequisites found")
        return True

    def setup_environment(self):
        """Setup environment files"""
        print("⚙️  Setting up environment...")
        
        # Create backend .env if it doesn't exist
        backend_env = self.base_dir / "backend" / ".env"
        if not backend_env.exists():
            with open(backend_env, 'w') as f:
                f.write("""MONGO_URL=mongodb://localhost:27017
DB_NAME=stockbreak_pro
CORS_ORIGINS=http://localhost:3000
DEBUG=true
DEFAULT_SCAN_LIMIT=200
MAX_CONCURRENT_REQUESTS=10
""")
            print("✅ Created backend .env file")
        
        # Create frontend .env if it doesn't exist
        frontend_env = self.base_dir / "frontend" / ".env"
        if not frontend_env.exists():
            with open(frontend_env, 'w') as f:
                f.write("""REACT_APP_BACKEND_URL=http://localhost:8001
REACT_APP_NAME=StockBreak Pro
REACT_APP_VERSION=2.0.0
""")
            print("✅ Created frontend .env file")

    def install_dependencies(self):
        """Install backend and frontend dependencies"""
        print("📦 Installing dependencies...")
        
        # Install backend dependencies
        backend_dir = self.base_dir / "backend"
        print("Installing Python dependencies...")
        try:
            subprocess.run([
                sys.executable, "-m", "pip", "install", "-r", "requirements.txt"
            ], cwd=backend_dir, check=True, capture_output=True)
            print("✅ Backend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install backend dependencies: {e}")
            return False
        
        # Install frontend dependencies
        frontend_dir = self.base_dir / "frontend"
        print("Installing Node.js dependencies...")
        try:
            subprocess.run(["npm", "install"], cwd=frontend_dir, check=True, capture_output=True)
            print("✅ Frontend dependencies installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install frontend dependencies: {e}")
            return False
        
        return True

    def start_backend(self):
        """Start the backend server"""
        print("🚀 Starting backend server...")
        
        backend_dir = self.base_dir / "backend"
        
        try:
            self.backend_process = subprocess.Popen([
                sys.executable, "-m", "uvicorn", "server:app", 
                "--host", "0.0.0.0", "--port", "8001", "--reload"
            ], cwd=backend_dir)
            
            # Wait for backend to start
            for i in range(30):  # Wait up to 30 seconds
                try:
                    response = requests.get("http://localhost:8001/api/health", timeout=2)
                    if response.status_code == 200:
                        print("✅ Backend server started successfully")
                        return True
                except:
                    pass
                time.sleep(1)
                print(f"Waiting for backend... ({i+1}/30)")
            
            print("❌ Backend server failed to start within 30 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start backend: {e}")
            return False

    def start_frontend(self):
        """Start the frontend development server"""
        print("🎨 Starting frontend server...")
        
        frontend_dir = self.base_dir / "frontend"
        
        try:
            # Set environment variable to prevent browser auto-opening
            env = os.environ.copy()
            env["BROWSER"] = "none"
            
            self.frontend_process = subprocess.Popen([
                "npm", "start"
            ], cwd=frontend_dir, env=env)
            
            # Wait for frontend to start
            for i in range(60):  # Wait up to 60 seconds
                try:
                    response = requests.get("http://localhost:3000", timeout=2)
                    if response.status_code == 200:
                        print("✅ Frontend server started successfully")
                        return True
                except:
                    pass
                time.sleep(1)
                if i % 10 == 9:  # Print every 10 seconds
                    print(f"Waiting for frontend... ({i+1}/60)")
            
            print("❌ Frontend server failed to start within 60 seconds")
            return False
            
        except Exception as e:
            print(f"❌ Failed to start frontend: {e}")
            return False

    def run_tests(self):
        """Run comprehensive tests"""
        print("🧪 Running comprehensive tests...")
        
        try:
            test_script = self.base_dir / "test_comprehensive.py"
            result = subprocess.run([sys.executable, str(test_script)], 
                                  capture_output=True, text=True, timeout=300)
            
            print("📊 TEST RESULTS:")
            print(result.stdout)
            
            if result.stderr:
                print("⚠️  Test Warnings/Errors:")
                print(result.stderr)
            
            return result.returncode == 0
            
        except subprocess.TimeoutExpired:
            print("❌ Tests timed out after 5 minutes")
            return False
        except Exception as e:
            print(f"❌ Failed to run tests: {e}")
            return False

    def cleanup(self):
        """Clean up processes"""
        print("\n🧹 Cleaning up...")
        
        if self.backend_process:
            self.backend_process.terminate()
            try:
                self.backend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
            print("✅ Backend server stopped")
        
        if self.frontend_process:
            self.frontend_process.terminate()
            try:
                self.frontend_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
            print("✅ Frontend server stopped")

    def launch(self):
        """Main launch sequence"""
        print("🚀 STOCKBREAK PRO LAUNCHER")
        print("=" * 50)
        
        try:
            # Check prerequisites
            if not self.check_prerequisites():
                print("❌ Prerequisites check failed")
                return False
            
            # Setup environment
            self.setup_environment()
            
            # Install dependencies
            if not self.install_dependencies():
                print("❌ Dependency installation failed")
                return False
            
            # Start backend
            if not self.start_backend():
                print("❌ Backend startup failed")
                return False
            
            # Start frontend
            if not self.start_frontend():
                print("❌ Frontend startup failed")
                return False
            
            print("\n🎉 STOCKBREAK PRO STARTED SUCCESSFULLY!")
            print("=" * 50)
            print("🌐 Frontend: http://localhost:3000")
            print("🔧 Backend:  http://localhost:8001")
            print("📚 API Docs: http://localhost:8001/docs")
            print("=" * 50)
            
            # Run tests
            print("\n🧪 Running comprehensive tests...")
            test_success = self.run_tests()
            
            if test_success:
                print("\n✅ All tests passed! Application is ready for use.")
            else:
                print("\n⚠️  Some tests failed. Check the output above for details.")
            
            print("\n📝 Application is running. Press Ctrl+C to stop.")
            
            # Keep running until interrupted
            try:
                while True:
                    time.sleep(1)
            except KeyboardInterrupt:
                print("\n\n🛑 Shutdown requested by user")
            
            return True
            
        except Exception as e:
            print(f"\n💥 Unexpected error: {e}")
            return False
        finally:
            self.cleanup()

def main():
    launcher = StockBreakProLauncher()
    success = launcher.launch()
    return 0 if success else 1

if __name__ == "__main__":
    sys.exit(main())