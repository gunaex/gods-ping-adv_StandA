"""
First Run Test Script for Gods Ping
Tests all critical components before starting the application
"""
import sys
import subprocess
from pathlib import Path

# Add backend to Python path
sys.path.insert(0, str(Path(__file__).parent / 'backend'))

def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")

def print_success(text):
    print(f"✅ {text}")

def print_error(text):
    print(f"❌ {text}")

def print_info(text):
    print(f"ℹ️  {text}")

def test_python_version():
    """Test Python version"""
    print_header("Test 1: Python Version")
    version = sys.version_info
    print(f"Python {version.major}.{version.minor}.{version.micro}")
    if version.major == 3 and version.minor >= 8:
        print_success("Python version is compatible")
        return True
    else:
        print_error("Python 3.8+ required")
        return False

def test_imports():
    """Test critical Python imports"""
    print_header("Test 2: Python Package Imports")
    
    packages = [
        ('fastapi', 'FastAPI'),
        ('uvicorn', 'Uvicorn'),
        ('sqlalchemy', 'SQLAlchemy'),
        ('pydantic', 'Pydantic'),
    ]
    
    all_ok = True
    for module, name in packages:
        try:
            __import__(module)
            print_success(f"{name} is installed")
        except ImportError:
            print_error(f"{name} is NOT installed")
            all_ok = False
    
    return all_ok

def test_backend_files():
    """Test backend file structure"""
    print_header("Test 3: Backend File Structure")
    
    required_files = [
        'backend/app/main.py',
        'backend/app/db.py',
        'backend/app/models.py',
        'backend/app/auth.py',
        'backend/app/logging_models.py',
        'backend/app/logger.py',
        'backend/app/bots.py',
        'backend/app/ai_engine.py',
        'backend/app/market.py',
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} NOT FOUND")
            all_ok = False
    
    return all_ok

def test_frontend_files():
    """Test frontend file structure"""
    print_header("Test 4: Frontend File Structure")
    
    required_files = [
        'frontend/package.json',
        'frontend/vite.config.ts',
        'frontend/tsconfig.json',
        'frontend/src/main.tsx',
        'frontend/src/App.tsx',
        'frontend/src/components/ShichiFukujin.tsx',
        'frontend/src/components/LogsModal.tsx',
    ]
    
    all_ok = True
    for file_path in required_files:
        if Path(file_path).exists():
            print_success(f"{file_path}")
        else:
            print_error(f"{file_path} NOT FOUND")
            all_ok = False
    
    return all_ok

def test_node_modules():
    """Test if node_modules is installed"""
    print_header("Test 5: Frontend Dependencies")
    
    node_modules = Path('frontend/node_modules')
    if node_modules.exists() and node_modules.is_dir():
        # Count packages
        packages = list(node_modules.iterdir())
        print_success(f"node_modules exists with {len(packages)} packages")
        
        # Check critical packages
        critical = ['react', 'vite', 'axios', 'zustand']
        for pkg in critical:
            if (node_modules / pkg).exists():
                print_success(f"  {pkg} installed")
            else:
                print_error(f"  {pkg} NOT installed")
                return False
        return True
    else:
        print_error("node_modules NOT found - run 'npm install' in frontend/")
        return False

def test_database_models():
    """Test database models can be imported"""
    print_header("Test 6: Database Models")
    
    try:
        from app.db import Base, engine
        from app.models import User, Trade, BotConfig
        from app.logging_models import Log, LogCategory, LogLevel
        
        print_success("Database Base imported")
        print_success("User model imported")
        print_success("Trade model imported")
        print_success("BotConfig model imported")
        print_success("Log model imported")
        print_success(f"LogCategory enum: {len(LogCategory)} categories")
        print_success(f"LogLevel enum: {len(LogLevel)} levels")
        
        return True
    except Exception as e:
        print_error(f"Failed to import models: {e}")
        return False

def test_database_creation():
    """Test database table creation"""
    print_header("Test 7: Database Table Creation")
    
    try:
        from app.db import Base, engine
        from sqlalchemy import inspect
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print_success("Database tables created")
        
        # Inspect tables
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        
        required_tables = ['users', 'trades', 'bot_configs', 'logs']
        for table in required_tables:
            if table in tables:
                columns = inspector.get_columns(table)
                print_success(f"Table '{table}' exists with {len(columns)} columns")
            else:
                print_error(f"Table '{table}' NOT found")
                return False
        
        return True
    except Exception as e:
        print_error(f"Database creation failed: {e}")
        return False

def test_logging_system():
    """Test logging system"""
    print_header("Test 8: Logging System")
    
    try:
        from app.db import get_db
        from app.logger import get_logger
        from app.logging_models import LogCategory, LogLevel
        
        db = next(get_db())
        logger = get_logger(db)
        
        # Test logging methods
        logger.error("Test error log", details="First run test")
        print_success("Error logging works")
        
        logger.ai_thinking(
            symbol="BTCUSDT",
            message="Test AI thinking",
            recommendation="BUY",
            confidence=0.85
        )
        print_success("AI thinking logging works")
        
        logger.ai_action(
            symbol="BTCUSDT",
            message="Test AI action",
            recommendation="BUY",
            executed=True,
            reason="Test execution"
        )
        print_success("AI action logging works")
        
        # Query logs
        from app.logging_models import Log
        log_count = db.query(Log).count()
        print_success(f"Total logs in database: {log_count}")
        
        db.close()
        return True
    except Exception as e:
        print_error(f"Logging system test failed: {e}")
        return False

def test_admin_creation():
    """Test admin user creation"""
    print_header("Test 9: Admin User Creation")
    
    try:
        from app.db import get_db
        from app.auth import ensure_admin_exists, ADMIN_USERNAME
        
        db = next(get_db())
        ensure_admin_exists(db)
        
        from app.models import User
        admin = db.query(User).filter(User.username == ADMIN_USERNAME).first()
        
        if admin:
            print_success(f"Admin user exists: {admin.username}")
            print_info(f"  Default password: admin123")
            print_info(f"  Is admin: {admin.is_admin}")
            db.close()
            return True
        else:
            print_error("Admin user not created")
            db.close()
            return False
    except Exception as e:
        print_error(f"Admin creation test failed: {e}")
        return False

def test_api_endpoints():
    """Test critical API endpoints are defined"""
    print_header("Test 10: API Endpoints")
    
    try:
        from app.main import app
        
        routes = [route.path for route in app.routes if hasattr(route, 'path')]
        
        critical_endpoints = [
            '/',
            '/api/auth/login',
            '/api/logs',
            '/api/logs/categories',
            '/api/logs/ai-actions',
        ]
        
        all_ok = True
        for endpoint in critical_endpoints:
            if endpoint in routes:
                print_success(f"Endpoint {endpoint} defined")
            else:
                print_error(f"Endpoint {endpoint} NOT found")
                all_ok = False
        
        print_info(f"Total routes: {len(routes)}")
        return all_ok
    except Exception as e:
        print_error(f"API endpoint test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("  🎌 GODS PING - FIRST RUN TEST SUITE")
    print("="*60)
    
    tests = [
        test_python_version,
        test_imports,
        test_backend_files,
        test_frontend_files,
        test_node_modules,
        test_database_models,
        test_database_creation,
        test_logging_system,
        test_admin_creation,
        test_api_endpoints,
    ]
    
    results = []
    for test in tests:
        try:
            result = test()
            results.append(result)
        except Exception as e:
            print_error(f"Test crashed: {e}")
            results.append(False)
    
    # Summary
    print_header("TEST SUMMARY")
    passed = sum(results)
    total = len(results)
    
    print(f"Tests Passed: {passed}/{total}")
    print(f"Tests Failed: {total - passed}/{total}")
    
    if all(results):
        print("\n" + "🎉 " * 20)
        print("\n  ✅ ALL TESTS PASSED!")
        print("\n  Your Gods Ping installation is ready to run!")
        print("\n  Next steps:")
        print("    1. cd backend")
        print("    2. uvicorn app.main:app --reload --port 8000")
        print("    3. Open new terminal:")
        print("    4. cd frontend")
        print("    5. npm run dev")
        print("\n" + "🎉 " * 20)
        return 0
    else:
        print("\n" + "⚠️ " * 20)
        print("\n  ❌ SOME TESTS FAILED")
        print("\n  Please fix the errors above before starting.")
        print("\n" + "⚠️ " * 20)
        return 1

if __name__ == "__main__":
    exit(main())
