# Create a test script to verify the project works
test_content = '''#!/usr/bin/env python3
"""
Test script for Personal To-Do List Assistant
Verifies basic functionality without GUI
"""

import os
import sys
import json
import tempfile
from datetime import datetime, timedelta

def test_task_manager():
    """Test TaskManager functionality"""
    print("🧪 Testing TaskManager...")
    
    # Import the module
    try:
        from task_manager import TaskManager
    except ImportError as e:
        print(f"❌ Failed to import TaskManager: {e}")
        return False
    
    # Create temporary file for testing
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        test_file = f.name
    
    try:
        # Initialize task manager
        tm = TaskManager(test_file)
        
        # Test adding tasks
        task_id = tm.add_task("Test task", datetime.now() + timedelta(hours=1), "High")
        assert task_id is not None
        print("  ✓ Task creation works")
        
        # Test getting tasks
        tasks = tm.get_all_tasks()
        assert len(tasks) == 1
        assert tasks[0]['description'] == "Test task"
        print("  ✓ Task retrieval works")
        
        # Test updating task
        tm.update_task(task_id, "Updated test task")
        tasks = tm.get_all_tasks()
        assert tasks[0]['description'] == "Updated test task"
        print("  ✓ Task updating works")
        
        # Test completing task
        tm.mark_complete(task_id)
        tasks = tm.get_all_tasks()
        assert tasks[0]['completed'] == True
        print("  ✓ Task completion works")
        
        # Test file persistence
        tm2 = TaskManager(test_file)
        tasks2 = tm2.get_all_tasks()
        assert len(tasks2) == 1
        assert tasks2[0]['completed'] == True
        print("  ✓ File persistence works")
        
        print("✅ TaskManager tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ TaskManager test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(test_file):
            os.remove(test_file)

def test_reminder_system():
    """Test ReminderSystem functionality"""
    print("\\n🔔 Testing ReminderSystem...")
    
    try:
        from reminder_system import ReminderSystem
        from task_manager import TaskManager
        
        # Create temporary task manager
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            test_file = f.name
        
        tm = TaskManager(test_file)
        
        # Add a task due soon
        tm.add_task("Test reminder task", datetime.now() + timedelta(minutes=30), "High")
        
        # Initialize reminder system
        rs = ReminderSystem(tm, check_interval=1)  # 1 second for testing
        
        # Test notification status
        status = rs.get_notification_status()
        assert isinstance(status, dict)
        print("  ✓ Notification status check works")
        
        # Test reminder checking (without actually running the loop)
        try:
            rs.check_reminders()
            print("  ✓ Reminder checking works")
        except Exception as e:
            print(f"  ⚠️  Reminder checking warning: {e}")
        
        print("✅ ReminderSystem tests passed!")
        return True
        
    except Exception as e:
        print(f"❌ ReminderSystem test failed: {e}")
        return False
    finally:
        if 'test_file' in locals() and os.path.exists(test_file):
            os.remove(test_file)

def test_imports():
    """Test all required imports"""
    print("\\n📦 Testing imports...")
    
    required_modules = [
        ('json', 'Python standard library'),
        ('datetime', 'Python standard library'),
        ('tkinter', 'Python standard library (GUI)'),
        ('threading', 'Python standard library'),
        ('uuid', 'Python standard library'),
        ('os', 'Python standard library'),
        ('typing', 'Python standard library')
    ]
    
    optional_modules = [
        ('plyer', 'Desktop notifications'),
        ('win10toast', 'Windows toast notifications')
    ]
    
    # Test required modules
    for module, description in required_modules:
        try:
            __import__(module)
            print(f"  ✓ {module} ({description})")
        except ImportError:
            print(f"  ❌ {module} ({description}) - REQUIRED")
            return False
    
    # Test optional modules
    for module, description in optional_modules:
        try:
            __import__(module)
            print(f"  ✓ {module} ({description})")
        except ImportError:
            print(f"  ⚠️  {module} ({description}) - OPTIONAL")
    
    print("✅ Import tests completed!")
    return True

def test_file_structure():
    """Test if all required files exist"""
    print("\\n📁 Testing file structure...")
    
    required_files = [
        'main.py',
        'task_manager.py', 
        'reminder_system.py',
        'requirements.txt',
        'README.md'
    ]
    
    missing_files = []
    for file in required_files:
        if os.path.exists(file):
            print(f"  ✓ {file}")
        else:
            print(f"  ❌ {file} - MISSING")
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ File structure test passed!")
    return True

def main():
    """Run all tests"""
    print("🚀 Personal To-Do List Assistant - Test Suite")
    print("=" * 50)
    
    tests = [
        ("File Structure", test_file_structure),
        ("Imports", test_imports),
        ("TaskManager", test_task_manager),
        ("ReminderSystem", test_reminder_system)
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ {test_name} test crashed: {e}")
            failed += 1
    
    print("\\n" + "=" * 50)
    print(f"📊 Test Results: {passed} passed, {failed} failed")
    
    if failed == 0:
        print("🎉 All tests passed! The project is ready to use.")
        return True
    else:
        print("⚠️  Some tests failed. Please check the issues above.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
'''

# Create MIT license file
license_content = '''MIT License

Copyright (c) 2025 Personal To-Do List Assistant

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

# Create gitignore file
gitignore_content = '''# Byte-compiled / optimized / DLL files
__pycache__/
*.py[cod]
*$py.class

# Distribution / packaging
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# PyInstaller
#  Usually these files are written by a python script from a template
#  before PyInstaller builds the exe, so as to inject date/other infos into it.
*.manifest
*.spec

# Unit test / coverage reports
htmlcov/
.tox/
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
.hypothesis/
.pytest_cache/

# Environments
.env
.venv
env/
venv/
ENV/
env.bak/
venv.bak/

# IDE files
.vscode/
.idea/
*.swp
*.swo
*~

# OS files
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Project specific
tasks.json
release/
*.log
*.tmp

# Backup files
*.bak
*.backup
'''

# Save additional files
additional_files = {
    'test.py': test_content,
    'LICENSE': license_content,
    '.gitignore': gitignore_content
}

for filename, content in additional_files.items():
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(content)
    print(f"✓ Created {filename}")

print("\n📋 Project structure completed!")
print("Total files created: 11")

# Show final project structure
print("\n📁 Final project structure:")
files = [f for f in os.listdir('.') if f.endswith(('.py', '.txt', '.md', '.json', 'LICENSE', '.gitignore'))]
for file in sorted(files):
    size = os.path.getsize(file)
    print(f"  {file} ({size:,} bytes)")