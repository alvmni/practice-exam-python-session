import tkinter as tk
from tkinter import ttk, messagebox

class ProjectView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Управление проектами")
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_name = ttk.Entry(form_frame)
        self.ent_name.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Описание:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_desc = ttk.Entry(form_frame)
        self.ent_desc.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Старт:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_start = ttk.Entry(form_frame)
        self.ent_start.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Финиш:").grid(row=1, column=2, padx=5, pady=5)
        self.ent_end = ttk.Entry(form_frame)
        self.ent_end.grid(row=1, column=3, padx=5, pady=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_project).grid(row=2, column=0, pady=5)
        ttk.Button(form_frame, text="Удалить", command=self.delete_project).grid(row=2, column=1, pady=5)
        ttk.Button(form_frame, text="Прогресс", command=self.check_progress).grid(row=2, column=2, pady=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Name", "Desc", "Start", "End", "Status"), show="headings")
        for col in ("ID", "Name", "Desc", "Start", "End", "Status"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_project(self):
        self.controller.add_project(self.ent_name.get(), self.ent_desc.get(), self.ent_start.get() or "2026-01-01", self.ent_end.get() or "2026-12-31")
        self.refresh_data()

    def delete_project(self):
        selected = self.tree.selection()
        if selected:
            self.controller.delete_project(self.tree.item(selected[0])['values'][0])
            self.refresh_data()

    def check_progress(self):
        selected = self.tree.selection()
        if selected:
            p_id = self.tree.item(selected[0])['values'][0]
            prog = self.controller.get_project_progress(p_id)
            messagebox.showinfo("Прогресс проекта", f"Выполнено: {prog:.1f}%")

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in self.controller.get_all_projects():
            self.tree.insert("", tk.END, values=(r.id, r.name, r.description, r.start_date, r.end_date, r.status))