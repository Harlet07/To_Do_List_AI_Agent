#!/usr/bin/env python3
"""
Launcher script for Personal To-Do List Assistant
Handles common startup issues and dependency checking
"""

import sys
import os
import subprocess
import importlib.util

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 7):
        print("❌ Python 3.7 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✓ Python {sys.version.split()[0]} detected")
    return True

def check_and_install_requirements():
    """Check if required packages are installed and install if missing"""
    requirements = ['plyer', 'win10toast']

    missing_packages = []

    for package in requirements:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)

    if missing_packages:
        print(f"📦 Installing missing packages: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", 
                *missing_packages
            ])
            print("✓ Packages installed successfully")
        except subprocess.CalledProcessError:
            print("⚠️  Could not install packages automatically")
            print("Please run: pip install -r requirements.txt")
            return False
    else:
        print("✓ All required packages are installed")

    return True

def check_files():
    """Check if all required files exist"""
    required_files = ['main.py', 'task_manager.py', 'reminder_system.py']

    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)

    if missing_files:
        print(f"❌ Missing files: {', '.join(missing_files)}")
        return False

    print("✓ All required files found")
    return True

def launch_app():
    """Launch the main application"""
    try:
        print("🚀 Starting Personal To-Do List Assistant...")

        # Import and run the main app
        import main

    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("Please ensure all files are in the same directory")
        return False
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        return False

    return True

def main():
    """Main launcher function"""
    print("Personal To-Do List Assistant - Launcher")
    print("=" * 40)

    # Check Python version
    if not check_python_version():
        input("Press Enter to exit...")
        sys.exit(1)

    # Check files
    if not check_files():
        input("Press Enter to exit...")
        sys.exit(1)

    # Check and install requirements
    if not check_and_install_requirements():
        print("\nTry installing manually:")
        print("pip install plyer win10toast")
        input("Press Enter to exit...")
        sys.exit(1)

    print("\n" + "=" * 40)

    # Launch the app
    if not launch_app():
        input("Press Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()
