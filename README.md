# Expense Tracker

Offline desktop expense tracker for Windows.  
No accounts. No cloud. Data is stored locally.

---

## Screenshots

### First launch (Welcome screen)
![Welcome screen](screenshots/welcome.png)

### Main application window
![Main window](screenshots/main.png)

---

## Features
- Desktop app (Python + CustomTkinter)
- Local SQLite database (`expenses.db`)
- Add expenses via simple input:
- Delete expenses
- Data persists after restart
- Automatic total calculation
- Dark theme
- Light theme

---

## Tech Stack
- Python 3.14
- CustomTkinter
- SQLite
- matplotlib
- pyinstaller
- pillow

---

## Run
```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Status
Previous version 1 — 30-40% of core functionality implemented.
UI and features will evolve.

License
MIT