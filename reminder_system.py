import time
import threading
from datetime import datetime, timedelta
from typing import List, Dict
import tkinter as tk
from tkinter import messagebox

# Try to import notification libraries
try:
    from plyer import notification
    PLYER_AVAILABLE = True
except ImportError:
    PLYER_AVAILABLE = False

try:
    import win10toast
    WIN10TOAST_AVAILABLE = True
except ImportError:
    WIN10TOAST_AVAILABLE = False

class ReminderSystem:
    def __init__(self, task_manager, check_interval: int = 60):
        """
        Initialize reminder system

        Args:
            task_manager: TaskManager instance
            check_interval: How often to check for reminders (in seconds)
        """
        self.task_manager = task_manager
        self.check_interval = check_interval
        self.running = False
        self.notified_tasks = set()  # Track already notified tasks

        # Initialize notification system
        if WIN10TOAST_AVAILABLE:
            self.toaster = win10toast.ToastNotifier()
        else:
            self.toaster = None

    def start(self):
        """Start the reminder system"""
        self.running = True
        print("Reminder system started")

        while self.running:
            try:
                self.check_reminders()
                time.sleep(self.check_interval)
            except Exception as e:
                print(f"Error in reminder system: {e}")
                time.sleep(self.check_interval)

    def stop(self):
        """Stop the reminder system"""
        self.running = False
        print("Reminder system stopped")

    def check_reminders(self):
        """Check for tasks that need reminders"""
        now = datetime.now()

        # Get tasks due soon (within next hour) and overdue tasks
        due_soon = self.task_manager.get_tasks_due_soon(1)  # 1 hour
        overdue = self.task_manager.get_overdue_tasks()

        # Process due soon tasks
        for task in due_soon:
            if task['id'] not in self.notified_tasks:
                time_until_due = task['due_date'] - now
                minutes_until_due = int(time_until_due.total_seconds() / 60)

                if minutes_until_due <= 60:  # Within 1 hour
                    self.send_notification(
                        f"Task Due Soon: {task['description']}",
                        f"Due in {minutes_until_due} minutes"
                    )
                    self.notified_tasks.add(task['id'])

        # Process overdue tasks
        for task in overdue:
            if task['id'] not in self.notified_tasks:
                time_overdue = now - task['due_date']
                hours_overdue = int(time_overdue.total_seconds() / 3600)

                self.send_notification(
                    f"Overdue Task: {task['description']}",
                    f"Overdue by {hours_overdue} hours"
                )
                self.notified_tasks.add(task['id'])

        # Clean up notified tasks for completed ones
        completed_task_ids = {task['id'] for task in self.task_manager.get_completed_tasks()}
        self.notified_tasks -= completed_task_ids

    def send_notification(self, title: str, message: str):
        """Send a desktop notification"""
        print(f"Notification: {title} - {message}")

        # Try different notification methods
        if self.send_win10_toast(title, message):
            return
        elif self.send_plyer_notification(title, message):
            return
        else:
            # Fallback to tkinter messagebox (will only work if GUI is active)
            self.send_tkinter_notification(title, message)

    def send_win10_toast(self, title: str, message: str) -> bool:
        """Send notification using win10toast"""
        if WIN10TOAST_AVAILABLE and self.toaster:
            try:
                self.toaster.show_toast(
                    title,
                    message,
                    duration=10,
                    icon_path=None,
                    threaded=True
                )
                return True
            except Exception as e:
                print(f"Error sending win10toast notification: {e}")
        return False

    def send_plyer_notification(self, title: str, message: str) -> bool:
        """Send notification using plyer"""
        if PLYER_AVAILABLE:
            try:
                notification.notify(
                    title=title,
                    message=message,
                    timeout=10
                )
                return True
            except Exception as e:
                print(f"Error sending plyer notification: {e}")
        return False

    def send_tkinter_notification(self, title: str, message: str):
        """Send notification using tkinter messagebox (fallback)"""
        try:
            # This will only work if the main GUI is running
            def show_popup():
                popup = tk.Toplevel()
                popup.title("Task Reminder")
                popup.geometry("300x100")
                popup.attributes('-topmost', True)

                tk.Label(popup, text=title, font=("Arial", 10, "bold")).pack(pady=5)
                tk.Label(popup, text=message, wraplength=250).pack(pady=5)

                tk.Button(popup, text="OK", command=popup.destroy).pack(pady=10)

                # Auto-close after 10 seconds
                popup.after(10000, popup.destroy)

            # Schedule the popup to run in the main thread
            threading.Thread(target=show_popup, daemon=True).start()
        except Exception as e:
            print(f"Error sending tkinter notification: {e}")

    def add_custom_reminder(self, task_id: str, remind_minutes_before: int = 30):
        """Add a custom reminder for a specific task"""
        task = self.task_manager.get_task_by_id(task_id)
        if task and task['due_date']:
            reminder_time = task['due_date'] - timedelta(minutes=remind_minutes_before)

            def reminder_callback():
                if not self.task_manager.get_task_by_id(task_id)['completed']:
                    self.send_notification(
                        f"Reminder: {task['description']}",
                        f"Due in {remind_minutes_before} minutes"
                    )

            # Schedule the reminder
            delay = (reminder_time - datetime.now()).total_seconds()
            if delay > 0:
                timer = threading.Timer(delay, reminder_callback)
                timer.daemon = True
                timer.start()
                return True
        return False

    def get_notification_status(self) -> Dict[str, bool]:
        """Get status of available notification systems"""
        return {
            'win10toast_available': WIN10TOAST_AVAILABLE,
            'plyer_available': PLYER_AVAILABLE,
            'system_running': self.running
        }

# Test function to verify notification systems
def test_notifications():
    """Test all available notification methods"""
    print("Testing notification systems...")

    reminder = ReminderSystem(None)

    print(f"Available systems: {reminder.get_notification_status()}")

    # Test notification
    reminder.send_notification("Test Notification", "This is a test message")

    print("Test completed")

if __name__ == "__main__":
    test_notifications()
