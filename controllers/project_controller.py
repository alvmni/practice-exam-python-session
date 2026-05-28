from models.project import Project

class ProjectController:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def add_project(self, name, description, start_date, end_date):
        project = Project(name, description, start_date, end_date)
        return self.db_manager.add_project(project)

    def get_project(self, project_id):
        row = self.db_manager.get_project_by_id(project_id)
        if not row: return None
        p = Project(row['name'], row['description'], row['start_date'], row['end_date'])
        p.id = row['id']
        p.status = row['status']
        return p

    def get_all_projects(self):
        rows = self.db_manager.get_all_projects()
        projects = []
        for row in rows:
            p = Project(row['name'], row['description'], row['start_date'], row['end_date'])
            p.id = row['id']
            p.status = row['status']
            projects.append(p)
        return projects

    def update_project(self, project_id, **kwargs):
        self.db_manager.update_project(project_id, **kwargs)

    def delete_project(self, project_id):
        self.db_manager.delete_project(project_id)

    def update_project_status(self, project_id, new_status):
        self.db_manager.update_project(project_id, status=new_status)

    def get_project_progress(self, project_id):
        tasks = self.db_manager.get_tasks_by_project(project_id)
        if not tasks: return 0.0
        completed = sum(1 for t in tasks if t['status'] == 'completed')
        return float((completed / len(tasks)) * 100)