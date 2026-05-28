import tkinter as tk
from tkinter import ttk, messagebox

class TaskView(ttk.Frame):
    def __init__(self, parent, controller, project_controller, user_controller):
        super().__init__(parent)
        self.controller = controller
        self.project_controller = project_controller
        self.user_controller = user_controller
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Добавить / Обновить задачу")
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_title = ttk.Entry(form_frame)
        self.ent_title.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Описание:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_desc = ttk.Entry(form_frame)
        self.ent_desc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Приоритет (1-3):").grid(row=1, column=0, padx=5, pady=5)
        self.ent_priority = ttk.Entry(form_frame, width=5)
        self.ent_priority.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Срок (ГГГГ-ММ-ДД):").grid(row=1, column=2, padx=5, pady=5)
        self.ent_due = ttk.Entry(form_frame)
        self.ent_due.grid(row=1, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Проекта:").grid(row=2, column=0, padx=5, pady=5)
        self.ent_proj = ttk.Entry(form_frame, width=5)
        self.ent_proj.grid(row=2, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="ID Исполнителя:").grid(row=2, column=2, padx=5, pady=5)
        self.ent_user = ttk.Entry(form_frame, width=5)
        self.ent_user.grid(row=2, column=3, padx=5, pady=5)

        ttk.Button(form_frame, text="Создать", command=self.add_task).grid(row=3, column=0, columnspan=2, pady=5)
        ttk.Button(form_frame, text="Удалить выбранное", command=self.delete_task).grid(row=3, column=2, columnspan=2, pady=5)

        filter_frame = ttk.Frame(self)
        filter_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)
        ttk.Label(filter_frame, text="Поиск:").pack(side=tk.LEFT, padx=5)
        self.ent_search = ttk.Entry(filter_frame)
        self.ent_search.pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Найти", command=self.search_tasks).pack(side=tk.LEFT, padx=5)
        ttk.Button(filter_frame, text="Сброс", command=self.refresh_data).pack(side=tk.LEFT, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Title", "Priority", "Status", "Due", "ProjID", "UserID"), show="headings")
        for col in ("ID", "Title", "Priority", "Status", "Due", "ProjID", "UserID"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=90)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_task(self):
        try:
            p_id = int(self.ent_proj.get()) if self.ent_proj.get() else None
            u_id = int(self.ent_user.get()) if self.ent_user.get() else None
            self.controller.add_task(
                self.ent_title.get(), self.ent_desc.get(),
                int(self.ent_priority.get() or 2), self.ent_due.get() or "2026-12-31",
                p_id, u_id
            )
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Ошибка", str(e))

    def delete_task(self):
        selected = self.tree.selection()
        if selected:
            item = self.tree.item(selected[0])
            self.controller.delete_task(item['values'][0])
            self.refresh_data()

    def search_tasks(self):
        rows = self.controller.search_tasks(self.ent_search.get())
        self.populate_tree(rows)

    def refresh_data(self):
        rows = self.controller.get_all_tasks()
        self.populate_tree(rows)

    def populate_tree(self, rows):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in rows:
            self.tree.insert("", tk.END, values=(r.id, r.title, r.priority, r.status, r.due_date, r.project_id, r.assignee_id))