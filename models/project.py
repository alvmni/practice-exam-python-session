from datetime import datetime

class Project:
    def __init__(self, name, description, start_date, end_date):
        self.id = None
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.status = 'active'  # 'active', 'completed', 'on_hold'

    def update_status(self, new_status):
        if new_status in ['active', 'completed', 'on_hold']:
            self.status = new_status

    def get_progress(self):
        # Базовая логика на уровне модели. Расширенная логика находится в контроллере.
        return 100.0 if self.status == 'completed' else 0.0

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'start_date': self.start_date.isoformat() if isinstance(self.start_date, datetime) else self.start_date,
            'end_date': self.end_date.isoformat() if isinstance(self.end_date, datetime) else self.end_date,
            'status': self.status
        }