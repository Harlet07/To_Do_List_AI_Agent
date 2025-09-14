# Personal To-Do List Assistant

An intelligent, locally-running to-do list application built with Python. This app helps you manage daily tasks with deadlines, reminders, and completion tracking - all stored locally on your computer.

![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey.svg)

## Features

✅ **Task Management**: Add, edit, delete, and mark tasks as complete  
⏰ **Smart Reminders**: Desktop notifications for upcoming and overdue tasks  
📅 **Due Date Tracking**: Set deadlines and get notified when tasks are due  
🎯 **Priority Levels**: High, Medium, Low priority classification  
💾 **Local Storage**: All data stored locally in JSON format (no internet required)  
🖥️ **Desktop GUI**: Clean, user-friendly interface built with Tkinter  
📊 **Task Statistics**: Track completion rates and productivity  

## Screenshots

*GUI Interface showing task list with priorities and due dates*

## Quick Start

### Option 1: Download Executable (Easiest)
1. Go to the [Releases](../../releases) page
2. Download the latest `PersonalTodoAssistant.exe`
3. Run the executable - no Python installation required!

### Option 2: Run from Source Code

#### Prerequisites
- Python 3.7 or higher
- Windows OS (for notifications)

#### Installation Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/personal-todo-assistant.git
   cd personal-todo-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python main.py
   ```

## Usage Guide

### Adding Tasks
1. Enter task description in the "Task" field
2. Set due date in format: `YYYY-MM-DD HH:MM` (optional)
3. Choose priority level (High, Medium, Low)
4. Click "Add Task"

### Managing Tasks
- **Edit Task**: Double-click on a task to load it for editing
- **Update Task**: Select task, modify fields, click "Update Task"
- **Delete Task**: Select task and click "Delete Task"
- **Mark Complete**: Select task and click "Mark Complete"

### Reminders
- The app automatically checks for due tasks every minute
- Desktop notifications appear for:
  - Tasks due within 1 hour
  - Overdue tasks
- Notifications work even when the app is minimized

## File Structure

```
personal-todo-assistant/
│
├── main.py              # Main application with GUI
├── task_manager.py      # Task operations and JSON storage
├── reminder_system.py   # Notification and reminder logic
├── requirements.txt     # Python dependencies
├── build_exe.py         # Script to build executable
├── tasks.json          # Your task data (created automatically)
└── README.md           # This file
```

## Building Executable

To create your own executable:

1. **Install PyInstaller**
   ```bash
   pip install pyinstaller
   ```

2. **Run build script**
   ```bash
   python build_exe.py
   ```
   OR manually:
   ```bash
   pyinstaller --onefile --windowed --name="PersonalTodoAssistant" main.py
   ```

3. Find the executable in the `dist/` folder

## Data Storage

- All tasks are stored in `tasks.json` in the application directory
- Data format is human-readable JSON
- Automatic backup on each save operation
- No internet connection required

## Troubleshooting

### Common Issues

**Q: Notifications not appearing**
- Make sure Windows notifications are enabled
- Run as administrator if needed
- Check if antivirus is blocking notifications

**Q: Application won't start**
- Ensure Python 3.7+ is installed
- Install all requirements: `pip install -r requirements.txt`
- Check console for error messages

**Q: Tasks not saving**
- Check file permissions in application directory
- Ensure `tasks.json` is not read-only

### Error Messages

| Error | Solution |
|-------|----------|
| "Invalid date format" | Use YYYY-MM-DD HH:MM format |
| "Module not found" | Install requirements: `pip install -r requirements.txt` |
| "Permission denied" | Run as administrator or check file permissions |

## Contributing

Contributions are welcome! Here's how you can help:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup

1. Clone the repo and install dependencies
2. Make your changes
3. Test thoroughly on Windows
4. Update documentation as needed
5. Submit PR with clear description

## Roadmap

- [ ] Multi-language support
- [ ] Task categories and tags
- [ ] Data export/import features
- [ ] Custom notification sounds
- [ ] Task templates
- [ ] Calendar integration
- [ ] Dark/Light theme toggle
- [ ] Subtasks support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built with Python and Tkinter
- Notifications powered by `plyer` and `win10toast`
- Icons from [source if applicable]

## Support

If you find this project helpful, please:
- ⭐ Star the repository
- 🐛 Report bugs via [Issues](../../issues)
- 💡 Suggest features via [Issues](../../issues)
- 📢 Share with friends and colleagues

## Author

**Your Name**
- GitHub: [@yourusername](https://github.com/yourusername)
- Email: your.email@example.com

---
*Made with ❤️ for productivity enthusiasts*
