#!/usr/bin/env python3
"""
Gods Ping - Automated Cleanup Script
Removes unused files and organizes project structure
"""

import os
import shutil
from pathlib import Path

# Get project root directory
PROJECT_ROOT = Path(__file__).parent

print("=" * 70)
print("🧹 Gods Ping - Automated Cleanup")
print("=" * 70)
print()

# Files to remove
FILES_TO_REMOVE = [
    # Root test files
    "test_ai_logs.py",
    "test_all_email_formats.py",
    "test_api.py",
    "test_email.py",
    "test_find_trades.py",
    "test_first_run.py",
    "test_force_trades.py",
    "test_forecast.py",
    "test_logging_system.py",
    "test_manual_trade.py",
    "test_profit_protection.py",
    "test_rate_limiter.py",
    "test_run_gods_hand.py",
    "check_db.py",
    "migrate_backend_db.py",
    
    # Temporary files
    "My_request.txt",
    "QUICKSTART.txt",
    
    # Duplicate batch files
    "START_BACKEND.bat",
    "START_FRONTEND.bat",
    
    # Redundant docs
    "BINANCE_TH_ACCESSIBILITY_FIXES.md",
    "BUILD_SUMMARY.md",
    "DEPLOYMENT_CHECKLIST.md",
    "FEATURE_CHECKLIST.md",
    "GIT_SETUP_COMPLETE.md",
    "INSTALLATION_COMPLETE.md",
    "INTEGRATION_COMPLETE.md",
    "MIGRATION_COMPLETE.md",
    "PACKAGE_ERRORS_FIXED.md",
    "PROJECT_COMPLETE.md",
    "VENV_SETUP_COMPLETE.md",
    "GODS_MODE_COMPLETE.md",
    
    # Backend temporary test files
    "backend/test_paper_balance.py",
    "backend/test_price_fetch.py",
    
    # Backup files
    "backend/app/bots.py.backup",
]

def remove_files():
    """Remove unused files"""
    removed = []
    not_found = []
    errors = []
    
    for file_path in FILES_TO_REMOVE:
        full_path = PROJECT_ROOT / file_path
        try:
            if full_path.exists():
                if full_path.is_file():
                    os.remove(full_path)
                    removed.append(file_path)
                    print(f"✅ Removed: {file_path}")
                else:
                    errors.append(f"{file_path} (not a file)")
                    print(f"⚠️  Skipped: {file_path} (not a file)")
            else:
                not_found.append(file_path)
                print(f"ℹ️  Not found: {file_path}")
        except Exception as e:
            errors.append(f"{file_path} ({str(e)})")
            print(f"❌ Error removing {file_path}: {e}")
    
    return removed, not_found, errors

def create_docs_folder():
    """Optional: Organize documentation into docs/ folder"""
    docs_dir = PROJECT_ROOT / "docs"
    
    # Documentation files to move
    docs_to_move = [
        "AI_STRATEGY_GUIDE.md",
        "ARCHITECTURE.md",
        "CONTINUOUS_MODE_AND_POSITION_SIZE_GUIDE.md",
        "DEPLOYMENT.md",
        "GMAIL_SETUP.md",
        "GODS_MODE_GUIDE.md",
        "GODS_MODE_IMPLEMENTATION.md",
        "GODS_MODE_QUICKSTART.md",
        "INCREMENTAL_POSITION_BUILDING_GUIDE.md",
        "INCREMENTAL_QUICK_REFERENCE.md",
        "LOGGING_SYSTEM.md",
        "QUICKSTART.md",
        "RATE_LIMITING_SUMMARY.md",
        "SETUP_GUIDE.md",
        "SOCIAL_SENTIMENT_INTEGRATION.md",
        "SYSTEM_OVERVIEW.md",
        "TIMEZONE_IMPLEMENTATION.md",
    ]
    
    print()
    organize = input("📁 Organize documentation into docs/ folder? (y/N): ").strip().lower()
    
    if organize == 'y':
        docs_dir.mkdir(exist_ok=True)
        moved = []
        
        for doc in docs_to_move:
            src = PROJECT_ROOT / doc
            dst = docs_dir / doc
            
            if src.exists():
                try:
                    shutil.move(str(src), str(dst))
                    moved.append(doc)
                    print(f"✅ Moved to docs/: {doc}")
                except Exception as e:
                    print(f"❌ Error moving {doc}: {e}")
        
        print(f"\n📁 Moved {len(moved)} documentation files to docs/")
        return True
    
    return False

def check_old_db():
    """Check if old gods_ping.db exists in root"""
    old_db = PROJECT_ROOT / "gods_ping.db"
    backend_db = PROJECT_ROOT / "backend" / "gods_ping.db"
    
    if old_db.exists():
        print()
        print("⚠️  WARNING: Found gods_ping.db in root directory")
        print(f"   Root DB size: {old_db.stat().st_size / 1024:.2f} KB")
        
        if backend_db.exists():
            print(f"   Backend DB size: {backend_db.stat().st_size / 1024:.2f} KB")
            print()
            print("   The real database should be in backend/gods_ping.db")
            print("   The root gods_ping.db is likely outdated.")
            print()
            
            remove_old_db = input("   Remove root gods_ping.db? (y/N): ").strip().lower()
            if remove_old_db == 'y':
                try:
                    os.remove(old_db)
                    print("   ✅ Removed old root gods_ping.db")
                    return True
                except Exception as e:
                    print(f"   ❌ Error removing: {e}")
                    return False
        else:
            print("   ⚠️  Backend DB not found! Keep root DB for safety.")
    
    return False

def main():
    """Main cleanup function"""
    print("This script will remove unused files and clean up your project.")
    print()
    print(f"📂 Project root: {PROJECT_ROOT}")
    print(f"📋 Files to remove: {len(FILES_TO_REMOVE)}")
    print()
    
    confirm = input("Proceed with cleanup? (yes/N): ").strip().lower()
    
    if confirm != 'yes':
        print("❌ Cleanup cancelled.")
        return
    
    print()
    print("-" * 70)
    print("🗑️  Removing files...")
    print("-" * 70)
    
    removed, not_found, errors = remove_files()
    
    print()
    print("-" * 70)
    print("📊 Cleanup Summary")
    print("-" * 70)
    print(f"✅ Removed: {len(removed)} files")
    print(f"ℹ️  Not found: {len(not_found)} files")
    print(f"❌ Errors: {len(errors)} files")
    
    if errors:
        print()
        print("Errors encountered:")
        for error in errors:
            print(f"  - {error}")
    
    # Check for old database
    check_old_db()
    
    # Offer to organize docs
    create_docs_folder()
    
    print()
    print("=" * 70)
    print("✨ Cleanup Complete!")
    print("=" * 70)
    print()
    print("Next steps:")
    print("1. Review the changes")
    print("2. Run: git status")
    print("3. If satisfied, commit: git add . && git commit -m 'Clean up project structure'")
    print()

if __name__ == "__main__":
    main()
