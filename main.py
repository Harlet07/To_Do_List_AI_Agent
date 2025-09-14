import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import font
import json
import os
from datetime import datetime, timedelta
import threading
import time
from task_manager import TaskManager
from reminder_system import ReminderSystem

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Personal To-Do List Assistant")
        self.root.geometry("800x600")
        self.root.configure(bg='#f0f0f0')

        # Initialize task manager and reminder system
        self.task_manager = TaskManager()
        self.reminder_system = ReminderSystem(self.task_manager)

        # Start reminder system in background
        self.start_reminder_thread()

        # Create GUI elements
        self.create_widgets()
        self.refresh_task_list()

    def create_widgets(self):
        # Title
        title_font = font.Font(family="Arial", size=16, weight="bold")
        title_label = tk.Label(self.root, text="Personal To-Do List Assistant", 
                              font=title_font, bg='#f0f0f0', fg='#333')
        title_label.pack(pady=10)

        # Input frame
        input_frame = tk.Frame(self.root, bg='#f0f0f0')
        input_frame.pack(pady=10, padx=20, fill='x')

        # Task input
        tk.Label(input_frame, text="Task:", bg='#f0f0f0').grid(row=0, column=0, sticky='w', padx=5)
        self.task_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.task_entry.grid(row=0, column=1, padx=5, pady=2)

        # Due date input
        tk.Label(input_frame, text="Due Date (YYYY-MM-DD HH:MM):", bg='#f0f0f0').grid(row=1, column=0, sticky='w', padx=5)
        self.due_date_entry = tk.Entry(input_frame, width=40, font=("Arial", 10))
        self.due_date_entry.grid(row=1, column=1, padx=5, pady=2)

        # Priority dropdown
        tk.Label(input_frame, text="Priority:", bg='#f0f0f0').grid(row=2, column=0, sticky='w', padx=5)
        self.priority_var = tk.StringVar(value="Medium")
        priority_combo = ttk.Combobox(input_frame, textvariable=self.priority_var, 
                                     values=["High", "Medium", "Low"], state="readonly")
        priority_combo.grid(row=2, column=1, padx=5, pady=2, sticky='w')

        # Buttons
        button_frame = tk.Frame(input_frame, bg='#f0f0f0')
        button_frame.grid(row=3, column=0, columnspan=2, pady=10)

        add_btn = tk.Button(button_frame, text="Add Task", command=self.add_task, 
                           bg='#4CAF50', fg='white', padx=20)
        add_btn.pack(side='left', padx=5)

        update_btn = tk.Button(button_frame, text="Update Task", command=self.update_task, 
                              bg='#2196F3', fg='white', padx=20)
        update_btn.pack(side='left', padx=5)

        delete_btn = tk.Button(button_frame, text="Delete Task", command=self.delete_task, 
                              bg='#f44336', fg='white', padx=20)
        delete_btn.pack(side='left', padx=5)

        # Task list frame
        list_frame = tk.Frame(self.root, bg='#f0f0f0')
        list_frame.pack(pady=10, padx=20, fill='both', expand=True)

        # Task listbox with scrollbar
        list_container = tk.Frame(list_frame, bg='#f0f0f0')
        list_container.pack(fill='both', expand=True)

        scrollbar = tk.Scrollbar(list_container)
        scrollbar.pack(side='right', fill='y')

        self.task_listbox = tk.Listbox(list_container, yscrollcommand=scrollbar.set, 
                                      font=("Arial", 10), selectmode='single')
        self.task_listbox.pack(side='left', fill='both', expand=True)
        scrollbar.config(command=self.task_listbox.yview)

        # Bind double-click to select task for editing
        self.task_listbox.bind('<Double-1>', self.load_selected_task)

        # Control buttons
        control_frame = tk.Frame(self.root, bg='#f0f0f0')
        control_frame.pack(pady=10)

        complete_btn = tk.Button(control_frame, text="Mark Complete", 
                                command=self.mark_complete, bg='#8BC34A', fg='white', padx=20)
        complete_btn.pack(side='left', padx=5)

        refresh_btn = tk.Button(control_frame, text="Refresh", 
                               command=self.refresh_task_list, bg='#9E9E9E', fg='white', padx=20)
        refresh_btn.pack(side='left', padx=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        status_bar = tk.Label(self.root, textvariable=self.status_var, 
                             relief='sunken', anchor='w', bg='#e0e0e0')
        status_bar.pack(side='bottom', fill='x')

    def add_task(self):
        task_desc = self.task_entry.get().strip()
        due_date_str = self.due_date_entry.get().strip()
        priority = self.priority_var.get()

        if not task_desc:
            messagebox.showerror("Error", "Please enter a task description")
            return

        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM")
                return

        # Add task
        self.task_manager.add_task(task_desc, due_date, priority)
        self.clear_inputs()
        self.refresh_task_list()
        self.status_var.set(f"Task '{task_desc}' added successfully")

    def update_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to update")
            return

        task_index = selection[0]
        task_desc = self.task_entry.get().strip()
        due_date_str = self.due_date_entry.get().strip()
        priority = self.priority_var.get()

        if not task_desc:
            messagebox.showerror("Error", "Please enter a task description")
            return

        # Parse due date
        due_date = None
        if due_date_str:
            try:
                due_date = datetime.strptime(due_date_str, "%Y-%m-%d %H:%M")
            except ValueError:
                messagebox.showerror("Error", "Invalid date format. Use YYYY-MM-DD HH:MM")
                return

        # Update task
        tasks = self.task_manager.get_all_tasks()
        if task_index < len(tasks):
            task_id = tasks[task_index]['id']
            self.task_manager.update_task(task_id, task_desc, due_date, priority)
            self.clear_inputs()
            self.refresh_task_list()
            self.status_var.set("Task updated successfully")

    def delete_task(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to delete")
            return

        if messagebox.askyesno("Confirm", "Are you sure you want to delete this task?"):
            task_index = selection[0]
            tasks = self.task_manager.get_all_tasks()
            if task_index < len(tasks):
                task_id = tasks[task_index]['id']
                self.task_manager.delete_task(task_id)
                self.refresh_task_list()
                self.status_var.set("Task deleted successfully")

    def mark_complete(self):
        selection = self.task_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a task to mark as complete")
            return

        task_index = selection[0]
        tasks = self.task_manager.get_all_tasks()
        if task_index < len(tasks):
            task_id = tasks[task_index]['id']
            self.task_manager.mark_complete(task_id)
            self.refresh_task_list()
            self.status_var.set("Task marked as complete")

    def load_selected_task(self, event):
        selection = self.task_listbox.curselection()
        if selection:
            task_index = selection[0]
            tasks = self.task_manager.get_all_tasks()
            if task_index < len(tasks):
                task = tasks[task_index]
                self.task_entry.delete(0, tk.END)
                self.task_entry.insert(0, task['description'])

                if task['due_date']:
                    self.due_date_entry.delete(0, tk.END)
                    self.due_date_entry.insert(0, task['due_date'].strftime("%Y-%m-%d %H:%M"))

                self.priority_var.set(task['priority'])

    def clear_inputs(self):
        self.task_entry.delete(0, tk.END)
        self.due_date_entry.delete(0, tk.END)
        self.priority_var.set("Medium")

    def refresh_task_list(self):
        self.task_listbox.delete(0, tk.END)
        tasks = self.task_manager.get_all_tasks()

        for task in tasks:
            status = "✓" if task['completed'] else "○"
            due_str = ""
            if task['due_date']:
                due_str = f" (Due: {task['due_date'].strftime('%Y-%m-%d %H:%M')})"

            priority_symbol = {"High": "🔴", "Medium": "🟡", "Low": "🟢"}.get(task['priority'], "🟡")

            display_text = f"{status} {priority_symbol} {task['description']}{due_str}"
            self.task_listbox.insert(tk.END, display_text)

        # Update status
        total_tasks = len(tasks)
        completed_tasks = len([t for t in tasks if t['completed']])
        self.status_var.set(f"Total: {total_tasks}, Completed: {completed_tasks}, Pending: {total_tasks - completed_tasks}")

    def start_reminder_thread(self):
        reminder_thread = threading.Thread(target=self.reminder_system.start, daemon=True)
        reminder_thread.start()

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
