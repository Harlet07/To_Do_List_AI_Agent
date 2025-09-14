# Personal To-Do List Assistant - Quick Start Guide

## 🚀 For Users (Non-Programmers)

### Option 1: Download Executable
1. Go to the GitHub releases page
2. Download `PersonalTodoAssistant.exe`
3. Double-click to run - no installation needed!

## 👩‍💻 For Developers

### Option 1: Run from Source
```bash
# Clone or download the project
git clone [repository-url]
cd personal-todo-assistant

# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Option 2: Use the Launcher (Recommended for beginners)
```bash
python launcher.py
```
The launcher will:
- Check Python version
- Install missing packages automatically
- Verify all files exist
- Launch the application

### Option 3: Run Tests First
```bash
python test.py
```
This will verify everything is working before you start.

### Build Your Own Executable
```bash
python build_exe.py
```
Creates a standalone `.exe` file in the `release/` folder.

## 📋 Features You Can Use

### Basic Task Management
- ➕ Add new tasks with descriptions
- 📅 Set due dates and times
- 🎯 Assign priority levels (High/Medium/Low)
- ✅ Mark tasks as complete
- ✏️ Edit existing tasks
- 🗑️ Delete tasks

### Smart Reminders
- 🔔 Desktop notifications for due tasks
- ⏰ Automatic reminders for overdue items
- 📱 Works even when app is minimized

### Data Management
- 💾 All data stored locally (no internet needed)
- 📄 JSON format for easy backup
- 🔄 Automatic save on every change

## 🛠️ Troubleshooting

### "Module not found" error:
```bash
pip install -r requirements.txt
```

### No notifications appearing:
- Check Windows notification settings
- Try running as administrator
- Install notification packages:
```bash
pip install plyer win10toast
```

### App won't start:
```bash
python launcher.py
```
This will diagnose and fix common issues.

## 📁 Project Files

| File | Purpose |
|------|---------|
| `main.py` | Main application with GUI |
| `task_manager.py` | Task operations and storage |
| `reminder_system.py` | Notifications and reminders |
| `launcher.py` | Smart launcher with error checking |
| `test.py` | Test suite to verify functionality |
| `build_exe.py` | Creates Windows executable |
| `requirements.txt` | Python dependencies |
| `tasks.json` | Your task data (auto-created) |

Happy task managing! 🎉
