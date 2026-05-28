import sqlite3
from datetime import datetime

class DatabaseManager:
    def __init__(self, db_path="tasks.db"):
        self.db_path = db_path
        self.conn = sqlite3.connect(self.db_path)
        self.conn.row_factory = sqlite3.Row
        self.create_tables()

    def create_tables(self):
        """Метод, который явно вызывается в ваших автотестах"""
        self.create_user_table()
        self.create_project_table()
        self.create_task_table()

    def close(self):
        if self.conn:
            self.conn.close()

    # --- Таблицы ---
    def create_task_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                priority INTEGER,
                status TEXT,
                due_date TEXT,
                project_id INTEGER,
                assignee_id INTEGER
            )
        """)
        self.conn.commit()

    def create_project_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                start_date TEXT,
                end_date TEXT,
                status TEXT
            )
        """)
        self.conn.commit()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                email TEXT,
                role TEXT,
                registration_date TEXT
            )
        """)
        self.conn.commit()

    # --- CRUD Операции ---
    def add_task(self, task):
        cursor = self.conn.cursor()
        due_str = task.due_date.isoformat() if isinstance(task.due_date, datetime) else task.due_date
        cursor.execute("""
            INSERT INTO tasks (title, description, priority, status, due_date, project_id, assignee_id)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (task.title, task.description, task.priority, task.status, due_str, task.project_id, task.assignee_id))
        self.conn.commit()
        task.id = cursor.lastrowid
        return task.id

    def get_task_by_id(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_tasks(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks")
        return [dict(row) for row in cursor.fetchall()]

    def update_task(self, task_id, **kwargs):
        if not kwargs: return
        cursor = self.conn.cursor()
        keys = [f"{k} = ?" for k in kwargs.keys()]
        values = list(kwargs.values())
        values.append(task_id)
        cursor.execute(f"UPDATE tasks SET {', '.join(keys)} WHERE id = ?", values)
        self.conn.commit()

    def delete_task(self, task_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
        self.conn.commit()

    def search_tasks(self, query):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE title LIKE ? OR description LIKE ?", (f"%{query}%", f"%{query}%"))
        return [dict(row) for row in cursor.fetchall()]

    def get_tasks_by_project(self, project_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE project_id = ?", (project_id,))
        return [dict(row) for row in cursor.fetchall()]

    def get_tasks_by_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM tasks WHERE assignee_id = ?", (user_id,))
        return [dict(row) for row in cursor.fetchall()]

    def add_project(self, project):
        cursor = self.conn.cursor()
        start_str = project.start_date.isoformat() if isinstance(project.start_date, datetime) else project.start_date
        end_str = project.end_date.isoformat() if isinstance(project.end_date, datetime) else project.end_date
        cursor.execute("""
            INSERT INTO projects (name, description, start_date, end_date, status)
            VALUES (?, ?, ?, ?, ?)
        """, (project.name, project.description, start_str, end_str, project.status))
        self.conn.commit()
        project.id = cursor.lastrowid
        return project.id

    def get_project_by_id(self, project_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE id = ?", (project_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_projects(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM projects")
        return [dict(row) for row in cursor.fetchall()]

    def update_project(self, project_id, **kwargs):
        if not kwargs: return
        cursor = self.conn.cursor()
        keys = [f"{k} = ?" for k in kwargs.keys()]
        values = list(kwargs.values())
        values.append(project_id)
        cursor.execute(f"UPDATE projects SET {', '.join(keys)} WHERE id = ?", values)
        self.conn.commit()

    def delete_project(self, project_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM projects WHERE id = ?", (project_id,))
        self.conn.commit()

    def add_user(self, user):
        cursor = self.conn.cursor()
        reg_str = user.registration_date.isoformat() if isinstance(user.registration_date, datetime) else user.registration_date
        cursor.execute("""
            INSERT INTO users (username, email, role, registration_date)
            VALUES (?, ?, ?, ?)
        """, (user.username, user.email, user.role, reg_str))
        self.conn.commit()
        user.id = cursor.lastrowid
        return user.id

    def get_user_by_id(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def get_all_users(self):
        cursor = self.conn.cursor()
        cursor.execute("SELECT * FROM users")
        return [dict(row) for row in cursor.fetchall()]

    def update_user(self, user_id, **kwargs):
        if not kwargs: return
        cursor = self.conn.cursor()
        keys = [f"{k} = ?" for k in kwargs.keys()]
        values = list(kwargs.values())
        values.append(user_id)
        cursor.execute(f"UPDATE users SET {', '.join(keys)} WHERE id = ?", values)
        self.conn.commit()

    def delete_user(self, user_id):
        cursor = self.conn.cursor()
        cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
        self.conn.commit()