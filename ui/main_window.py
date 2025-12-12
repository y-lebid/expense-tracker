import customtkinter as ctk
from datetime import datetime

from core.parser import parse_expense
from core.database import (
    init_db,
    add_expense,
    get_all_expenses,
    delete_expense
)


class MainWindow(ctk.CTk):
    def __init__(self, settings):
        super().__init__()

        self._is_closing = False
        self.protocol("WM_DELETE_WINDOW", self.on_close)

        self.settings = settings
        self.total_amount = 0
        self.expense_widgets = {}

        self.title("Expense Tracker")
        self.geometry("850x520")

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.build_sidebar()
        self.build_history()

        init_db()
        self.load_expenses_from_db()

    def on_close(self):
        if self._is_closing:
            return

        self._is_closing = True
        self.after_idle(self.destroy)

    def build_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=240, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_rowconfigure(99, weight=1)

        ctk.CTkLabel(
            self.sidebar,
            text="Додати витрату",
            font=ctk.CTkFont(size=22, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(25, 10))

        self.entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Кава 75",
            height=40
        )
        self.entry.grid(row=1, column=0, padx=20, pady=10, sticky="ew")
        self.entry.bind("<Return>", lambda e: self.add_expense_handler())

        self.add_button = ctk.CTkButton(
            self.sidebar,
            text="Додати",
            height=40,
            command=self.add_expense_handler
        )
        self.add_button.grid(row=2, column=0, padx=20, pady=(5, 20), sticky="ew")

        self.status_label = ctk.CTkLabel(self.sidebar, text="")
        self.status_label.grid(row=3, column=0, padx=20)

        self.total_label = ctk.CTkLabel(
            self.sidebar,
            text="Всього: 0 грн",
            font=ctk.CTkFont(size=18, weight="bold")
        )
        self.total_label.grid(row=100, column=0, padx=20, pady=20)


    # ---------- HISTORY ----------
    def build_history(self):
        self.history = ctk.CTkScrollableFrame(
            self,
            label_text="Історія витрат"
        )
        self.history.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.history.grid_columnconfigure(0, weight=1)

    # ---------- LOAD FROM DB ----------
    def load_expenses_from_db(self):
        expenses = get_all_expenses()

        for expense_id, title, amount, created_at in expenses:
            self.render_expense(expense_id, title, amount)
            self.total_amount += amount

        self.total_label.configure(
            text=f"Всього: {self.total_amount} грн"
        )

    # ADD
    def add_expense_handler(self):
        text = self.entry.get()
        parsed = parse_expense(text)

        if not parsed:
            self.status_label.configure(
                text="❌ Формат: Назва Сума",
                text_color="red"
            )
            return

        title, amount = parsed
        expense_id = add_expense(title, amount)

        self.render_expense(expense_id, title, amount)

        self.total_amount += amount
        self.total_label.configure(text=f"Всього: {self.total_amount} грн")

        self.entry.delete(0, "end")
        self.status_label.configure(text="✅ Додано", text_color="green")

    # RENDER 
    def render_expense(self, expense_id, title, amount):
        frame = ctk.CTkFrame(self.history)
        frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(
            frame,
            text=title,
            anchor="w"
        ).pack(side="left", padx=10)

        ctk.CTkLabel(
            frame,
            text=f"-{amount} грн",
            text_color="#ff6666"
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            frame,
            text="✕",
            width=30,
            fg_color="transparent",
            text_color="gray",
            command=lambda: self.remove_expense(expense_id)
        ).pack(side="right", padx=10)

        self.expense_widgets[expense_id] = frame

    # ---------- DELETE ----------
    def remove_expense(self, expense_id):
        frame = self.expense_widgets.get(expense_id)
        if not frame:
            return

        amount_label = frame.winfo_children()[1]
        amount = int(amount_label.cget("text").replace("-", "").replace(" грн", ""))

        delete_expense(expense_id)

        frame.destroy()
        del self.expense_widgets[expense_id]

        self.total_amount -= amount
        self.total_label.configure(text=f"Всього: {self.total_amount} грн")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

