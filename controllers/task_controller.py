from models.task import Task
from datetime import datetime

class TaskController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_task(self, title, description, priority, due_date, project_id, assignee_id):
        task = Task(title, description, priority, due_date, project_id, assignee_id)
        return self.db_manager.add_task(task)

    def _row_to_obj(self, row):
        t = Task(row['title'], row['description'], row['priority'], row['due_date'], row['project_id'], row['assignee_id'])
        t.id = row['id']
        t.status = row['status']
        return t

    def get_task(self, task_id):
        row = self.db_manager.get_task_by_id(task_id)
        return self._row_to_obj(row) if row else None

    def get_all_tasks(self):
        return [self._row_to_obj(r) for r in self.db_manager.get_all_tasks()]

    def update_task(self, task_id, **kwargs):
        self.db_manager.update_task(task_id, **kwargs)

    def delete_task(self, task_id):
        self.db_manager.delete_task(task_id)

    def search_tasks(self, query):
        return [self._row_to_obj(r) for r in self.db_manager.search_tasks(query)]

    def update_task_status(self, task_id, new_status):
        self.db_manager.update_task(task_id, status=new_status)

    def get_overdue_tasks(self):
        tasks = self.get_all_tasks()
        overdue = []
        for t in tasks:
            due = t.due_date
            if isinstance(due, str):
                try: due = datetime.fromisoformat(due)
                except ValueError: continue
            if datetime.now() > due and t.status != 'completed':
                overdue.append(t)
        return overdue

    def get_tasks_by_project(self, project_id):
        return [self._row_to_obj(r) for r in self.db_manager.get_tasks_by_project(project_id)]

    def get_tasks_by_user(self, user_id):
        return [self._row_to_obj(r) for r in self.db_manager.get_tasks_by_user(user_id)]