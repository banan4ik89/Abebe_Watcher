import os
import sys

def get_exe_dir():
    if getattr(sys, 'frozen', False):
        return sys._MEIPASS      # для --onefile
    return os.path.dirname(os.path.abspath(__file__))

def block_esc(widget):
    widget.bind("<Escape>", lambda e: "break")

def safe_destroy(win):
    try:
        if win and win.winfo_exists():
            win.destroy()
    except:
        pass
