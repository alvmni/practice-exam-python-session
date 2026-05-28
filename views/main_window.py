import tkinter as tk
from tkinter import ttk
from views.task_view import TaskView
from views.project_view import ProjectView
from views.user_view import UserView

class MainWindow(tk.Tk):
    def __init__(self, task_controller, project_controller, user_controller):
        super().__init__()
        self.title("Система управления задачами")
        self.geometry("850x600")

        notebook = ttk.Notebook(self)
        notebook.pack(fill=tk.BOTH, expand=True)

        self.task_view = TaskView(notebook, task_controller, project_controller, user_controller)
        self.project_view = ProjectView(notebook, project_controller)
        self.user_view = UserView(notebook, user_controller)

        notebook.add(self.task_view, text="Задачи")
        notebook.add(self.project_view, text="Проекты")
        notebook.add(self.user_view, text="Пользователи")

