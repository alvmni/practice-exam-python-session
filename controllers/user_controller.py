from models.user import User
from models.task import Task

class UserController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_user(self, username, email, role):
        user = User(username, email, role)
        return self.db_manager.add_user(user)

    def _row_to_obj(self, row):
        u = User(row['username'], row['email'], row['role'])
        u.id = row['id']
        u.registration_date = row['registration_date']
        return u

    def get_user(self, user_id):
        row = self.db_manager.get_user_by_id(user_id)
        return self._row_to_obj(row) if row else None

    def get_all_users(self):
        return [self._row_to_obj(r) for r in self.db_manager.get_all_users()]

    def update_user(self, user_id, **kwargs):
        self.db_manager.update_user(user_id, **kwargs)

    def delete_user(self, user_id):
        self.db_manager.delete_user(user_id)

    def get_user_tasks(self, user_id):
        rows = self.db_manager.get_tasks_by_user(user_id)
        tasks = []
        for row in rows:
            t = Task(
                row['title'], 
                row['description'], 
                row['priority'], 
                row['due_date'], 
                row['project_id'], 
                row['assignee_id']
            )
            t.id = row['id']
            t.status = row['status']
            tasks.append(t)
        return tasks