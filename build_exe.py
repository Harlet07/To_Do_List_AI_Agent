#!/usr/bin/env python3
"""
Build script for Personal To-Do List Assistant
Creates a standalone executable using PyInstaller
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def check_requirements():
    """Check if required packages are installed"""
    try:
        import PyInstaller
        print("✓ PyInstaller found")
    except ImportError:
        print("✗ PyInstaller not found. Installing...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("✓ PyInstaller installed")

def clean_build_dirs():
    """Clean previous build directories"""
    dirs_to_clean = ['build', 'dist', '__pycache__']

    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✓ Cleaned {dir_name} directory")

def build_executable():
    """Build the executable using PyInstaller"""
    print("\n🔨 Building executable...")

    # PyInstaller command
    cmd = [
        "pyinstaller",
        "--onefile",           # Single executable file
        "--windowed",          # No console window
        "--name=PersonalTodoAssistant",  # Executable name
        "--icon=app_icon.ico", # Icon file (optional)
        "--add-data=*.py;.",   # Include Python files
        "main.py"              # Main script
    ]

    # Remove icon parameter if icon file doesn't exist
    if not os.path.exists("app_icon.ico"):
        cmd.remove("--icon=app_icon.ico")

    try:
        subprocess.check_call(cmd)
        print("✅ Build completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False

def create_release_package():
    """Create a release package with executable and readme"""
    if not os.path.exists("dist/PersonalTodoAssistant.exe"):
        print("❌ Executable not found in dist folder")
        return False

    # Create release folder
    release_dir = "release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)

    # Copy files to release folder
    files_to_copy = [
        ("dist/PersonalTodoAssistant.exe", "PersonalTodoAssistant.exe"),
        ("README.md", "README.md"),
        ("requirements.txt", "requirements.txt")
    ]

    for src, dst in files_to_copy:
        if os.path.exists(src):
            shutil.copy2(src, os.path.join(release_dir, dst))
            print(f"✓ Copied {src} to release folder")

    print(f"\n📦 Release package created in '{release_dir}' folder")
    print(f"📁 Contents:")
    for file in os.listdir(release_dir):
        size = os.path.getsize(os.path.join(release_dir, file))
        print(f"   - {file} ({size:,} bytes)")

    return True

def main():
    """Main build process"""
    print("🚀 Personal To-Do List Assistant - Build Script")
    print("=" * 50)

    # Step 1: Check requirements
    print("\n1️⃣ Checking requirements...")
    check_requirements()

    # Step 2: Clean previous builds
    print("\n2️⃣ Cleaning previous builds...")
    clean_build_dirs()

    # Step 3: Build executable
    print("\n3️⃣ Building executable...")
    if not build_executable():
        print("\n❌ Build process failed!")
        sys.exit(1)

    # Step 4: Create release package
    print("\n4️⃣ Creating release package...")
    if not create_release_package():
        print("\n⚠️  Release package creation failed!")

    print("\n✅ Build process completed!")
    print("\n📋 Next steps:")
    print("   1. Test the executable in the 'release' folder")
    print("   2. Create a GitHub release with the contents of 'release' folder")
    print("   3. Share the download link with users")

if __name__ == "__main__":
    main()
