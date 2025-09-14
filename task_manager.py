import json
import os
import uuid
from datetime import datetime
from typing import List, Dict, Optional

class TaskManager:
    def __init__(self, data_file: str = "tasks.json"):
        self.data_file = data_file
        self.tasks = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as file:
                    data = json.load(file)
                    self.tasks = []
                    for task_data in data:
                        task = task_data.copy()
                        # Convert string dates back to datetime objects
                        if task['due_date']:
                            task['due_date'] = datetime.fromisoformat(task['due_date'])
                        if task['created_at']:
                            task['created_at'] = datetime.fromisoformat(task['created_at'])
                        if task['completed_at']:
                            task['completed_at'] = datetime.fromisoformat(task['completed_at'])
                        self.tasks.append(task)
            except (json.JSONDecodeError, KeyError, ValueError) as e:
                print(f"Error loading tasks: {e}")
                self.tasks = []
        else:
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file"""
        try:
            # Convert datetime objects to strings for JSON serialization
            serializable_tasks = []
            for task in self.tasks:
                task_copy = task.copy()
                if task_copy['due_date']:
                    task_copy['due_date'] = task_copy['due_date'].isoformat()
                if task_copy['created_at']:
                    task_copy['created_at'] = task_copy['created_at'].isoformat()
                if task_copy['completed_at']:
                    task_copy['completed_at'] = task_copy['completed_at'].isoformat()
                serializable_tasks.append(task_copy)

            with open(self.data_file, 'w', encoding='utf-8') as file:
                json.dump(serializable_tasks, file, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, description: str, due_date: Optional[datetime] = None, 
                 priority: str = "Medium") -> str:
        """Add a new task"""
        task_id = str(uuid.uuid4())
        task = {
            'id': task_id,
            'description': description,
            'due_date': due_date,
            'priority': priority,
            'completed': False,
            'created_at': datetime.now(),
            'completed_at': None
        }
        self.tasks.append(task)
        self.save_tasks()
        return task_id

    def update_task(self, task_id: str, description: Optional[str] = None, 
                   due_date: Optional[datetime] = None, priority: Optional[str] = None) -> bool:
        """Update an existing task"""
        for task in self.tasks:
            if task['id'] == task_id:
                if description is not None:
                    task['description'] = description
                if due_date is not None:
                    task['due_date'] = due_date
                if priority is not None:
                    task['priority'] = priority
                self.save_tasks()
                return True
        return False

    def delete_task(self, task_id: str) -> bool:
        """Delete a task"""
        for i, task in enumerate(self.tasks):
            if task['id'] == task_id:
                del self.tasks[i]
                self.save_tasks()
                return True
        return False

    def mark_complete(self, task_id: str) -> bool:
        """Mark a task as completed"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = True
                task['completed_at'] = datetime.now()
                self.save_tasks()
                return True
        return False

    def mark_incomplete(self, task_id: str) -> bool:
        """Mark a task as incomplete"""
        for task in self.tasks:
            if task['id'] == task_id:
                task['completed'] = False
                task['completed_at'] = None
                self.save_tasks()
                return True
        return False

    def get_all_tasks(self) -> List[Dict]:
        """Get all tasks"""
        return self.tasks.copy()

    def get_pending_tasks(self) -> List[Dict]:
        """Get all incomplete tasks"""
        return [task for task in self.tasks if not task['completed']]

    def get_completed_tasks(self) -> List[Dict]:
        """Get all completed tasks"""
        return [task for task in self.tasks if task['completed']]

    def get_overdue_tasks(self) -> List[Dict]:
        """Get all overdue tasks"""
        now = datetime.now()
        return [task for task in self.tasks 
                if not task['completed'] and task['due_date'] and task['due_date'] < now]

    def get_tasks_due_soon(self, hours: int = 24) -> List[Dict]:
        """Get tasks due within specified hours"""
        from datetime import timedelta
        now = datetime.now()
        cutoff = now + timedelta(hours=hours)

        return [task for task in self.tasks 
                if not task['completed'] and task['due_date'] 
                and now <= task['due_date'] <= cutoff]

    def search_tasks(self, query: str) -> List[Dict]:
        """Search tasks by description"""
        query_lower = query.lower()
        return [task for task in self.tasks 
                if query_lower in task['description'].lower()]

    def get_task_by_id(self, task_id: str) -> Optional[Dict]:
        """Get a specific task by ID"""
        for task in self.tasks:
            if task['id'] == task_id:
                return task.copy()
        return None

    def get_task_stats(self) -> Dict:
        """Get statistics about tasks"""
        total = len(self.tasks)
        completed = len(self.get_completed_tasks())
        pending = len(self.get_pending_tasks())
        overdue = len(self.get_overdue_tasks())

        return {
            'total': total,
            'completed': completed,
            'pending': pending,
            'overdue': overdue,
            'completion_rate': (completed / total * 100) if total > 0 else 0
        }
