from database.database_manager import DatabaseManager
from controllers.task_controller import TaskController
from controllers.project_controller import ProjectController
from controllers.user_controller import UserController
from views.main_window import MainWindow

def main():
    # Инициализация слоя данных
    db_manager = DatabaseManager("tasks.db")
    
    # Инициализация контроллеров
    task_controller = TaskController(db_manager)
    project_controller = ProjectController(db_manager)
    user_controller = UserController(db_manager)
    
    # Запуск GUI приложения
    app = MainWindow(task_controller, project_controller, user_controller)
    app.mainloop()

if __name__ == "__main__":
    main()