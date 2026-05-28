import tkinter as tk
from tkinter import ttk

class UserView(ttk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.create_widgets()
        self.refresh_data()

    def create_widgets(self):
        form_frame = ttk.LabelFrame(self, text="Управление пользователями")
        form_frame.pack(side=tk.TOP, fill=tk.X, padx=5, pady=5)

        ttk.Label(form_frame, text="Имя:").grid(row=0, column=0, padx=5, pady=5)
        self.ent_username = ttk.Entry(form_frame)
        self.ent_username.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(form_frame, text="Email:").grid(row=0, column=2, padx=5, pady=5)
        self.ent_email = ttk.Entry(form_frame)
        self.ent_email.grid(row=0, column=3, padx=5, pady=5)

        ttk.Label(form_frame, text="Роль:").grid(row=1, column=0, padx=5, pady=5)
        self.ent_role = ttk.Entry(form_frame)
        self.ent_role.grid(row=1, column=1, padx=5, pady=5)

        ttk.Button(form_frame, text="Добавить", command=self.add_user).grid(row=1, column=2, padx=5)
        ttk.Button(form_frame, text="Удалить", command=self.delete_user).grid(row=1, column=3, padx=5)

        self.tree = ttk.Treeview(self, columns=("ID", "Username", "Email", "Role", "Registered"), show="headings")
        for col in ("ID", "Username", "Email", "Role", "Registered"):
            self.tree.heading(col, text=col)
            self.tree.column(col, width=100)
        self.tree.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def add_user(self):
        self.controller.add_user(self.ent_username.get(), self.ent_email.get(), self.ent_role.get())
        self.refresh_data()

    def delete_user(self):
        selected = self.tree.selection()
        if selected:
            self.controller.delete_user(self.tree.item(selected[0])['values'][0])
            self.refresh_data()

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for r in self.controller.get_all_users():
            self.tree.insert("", tk.END, values=(r.id, r.username, r.email, r.role, r.registration_date))