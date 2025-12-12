import customtkinter as ctk
from core.settings import save_settings


class WelcomeWindow(ctk.CTk):
    def __init__(self, on_finish):
        super().__init__()

        self.on_finish = on_finish

        self.title("Ласкаво просимо")
        self.geometry("500x400")
        self.resizable(False, False)

        ctk.CTkLabel(
            self,
            text="Вітаю 👋",
            font=ctk.CTkFont(size=26, weight="bold")
        ).pack(pady=(30, 10))

        self.name_entry = ctk.CTkEntry(self, placeholder_text="Твоє імʼя")
        self.name_entry.pack(pady=10)

        self.lang = ctk.StringVar(value="uk")
        ctk.CTkOptionMenu(
            self,
            values=["uk", "en"],
            variable=self.lang
        ).pack(pady=10)

        self.theme = ctk.StringVar(value="dark")
        ctk.CTkOptionMenu(
            self,
            values=["dark", "light"],
            variable=self.theme
        ).pack(pady=10)

        ctk.CTkButton(
            self,
            text="Почати",
            command=self.finish
        ).pack(pady=30)

    def finish(self):
        settings = {
            "name": self.name_entry.get() or "User",
            "language": self.lang.get(),
            "theme": self.theme.get(),
            "first_run": False
        }

        save_settings(settings)
        self.destroy()
        self.on_finish()
