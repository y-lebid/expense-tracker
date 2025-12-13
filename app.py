import customtkinter as ctk
from core.settings import load_settings
from ui.main_window import MainWindow
from ui.welcome_window import WelcomeWindow
import tkinter as tk

def _silent_bgerror(*args):
    pass

tk.Tk.report_callback_exception = _silent_bgerror

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

def main():
    settings = load_settings()
    
    app = None

    def start_main():
        nonlocal app    
        new_settings = load_settings()
        ctk.set_appearance_mode(new_settings["theme"])
        app = MainWindow(new_settings)
        app.mainloop()


    if not settings or settings.get("first_run", True):
        welcome = WelcomeWindow(on_finish=start_main)
        welcome.mainloop() 
    else:

        ctk.set_appearance_mode(settings["theme"])
        app = MainWindow(settings)
        app.mainloop()


if __name__ == "__main__":
    main()