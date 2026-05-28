from datetime import datetime

class Task:
    def __init__(self, title, description, priority, due_date, project_id, assignee_id):
        self.id = None
        self.title = title
        self.description = description
        self.priority = priority  # 1-высокий, 2-средний, 3-низкий
        self.status = 'pending'   # 'pending', 'in_progress', 'completed'
        self.due_date = due_date
        self.project_id = project_id
        self.assignee_id = assignee_id

    def update_status(self, new_status):
        if new_status in ['pending', 'in_progress', 'completed']:
            self.status = new_status

    def is_overdue(self):
        if self.status == 'completed':
            return False
        
        dt = self.due_date
        if isinstance(dt, str):
            try:
                dt = datetime.fromisoformat(dt)
            except ValueError:
                return False
        return datetime.now() > dt

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'priority': self.priority,
            'status': self.status,
            'due_date': self.due_date.isoformat() if isinstance(self.due_date, datetime) else self.due_date,
            'project_id': self.project_id,
            'assignee_id': self.assignee_id
        }