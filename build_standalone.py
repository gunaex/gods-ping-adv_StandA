import PyInstaller.__main__
import os
import shutil

# Ensure frontend is built
if not os.path.exists("frontend/dist"):
    print("Frontend build not found! Please run 'npm run build' in frontend directory first.")
    exit(1)

# Clean previous builds
if os.path.exists("dist"):
    shutil.rmtree("dist")
if os.path.exists("build"):
    shutil.rmtree("build")

# PyInstaller arguments
args = [
    'backend/app/main.py',  # Entry point
    '--name=GodsPing',
    '--onefile',
    '--clean',
    '--icon=icon.ico',
    # Add frontend files
    '--add-data=frontend/dist;frontend/dist',
    # Add backend app package
    # We don't need to add-data for python files if they are imported, 
    # but we might need it for templates or other non-python files if any.
    # However, we need to make sure 'app' is importable.
    '--paths=backend',
    # Hidden imports that might be missed
    '--hidden-import=uvicorn',
    '--hidden-import=passlib.handlers.bcrypt',
    '--hidden-import=sqlalchemy.sql.default_comparator',
    '--hidden-import=engineio.async_drivers.aiohttp',
]

print("Building standalone executable...")
PyInstaller.__main__.run(args)
print("Build complete. Executable is in 'dist' folder.")
