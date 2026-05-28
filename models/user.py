from datetime import datetime

class User:
    def __init__(self, username, email, role):
        self.id = None
        self.username = username
        self.email = email
        self.role = role  # 'admin', 'manager', 'developer'
        self.registration_date = datetime.now()

    def update_info(self, username=None, email=None, role=None):
        if username is not None:
            self.username = username
        if email is not None:
            self.email = email
        if role is not None:
            self.role = role

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'registration_date': self.registration_date.isoformat() if isinstance(self.registration_date, datetime) else self.registration_date
        }