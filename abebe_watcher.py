# abebe_watcher.py
import tkinter as tk
import random
import os

from utils import get_exe_dir
from config import DATA_DIR

# ===================== СОСТОЯНИЯ =====================
STATE_NEUTRAL = "neutral"
STATE_HAPPY = "happy"
STATE_ANGRY = "angry"

# ===================== ФАЙЛЫ GIF =====================
GIFS = {
    STATE_NEUTRAL: "abebe_neutral.gif",
    STATE_HAPPY: "abebe_happy.gif",
    STATE_ANGRY: "abebe_angry.gif"
}

# ===================== ДИАЛОГИ =====================
DIALOGS = {
    STATE_NEUTRAL: [
        "I am watching.",
        "Continue.",
        "Enter the code.",
        "I see you."
    ],
    STATE_HAPPY: [
        "Good. You understand.",
        "You are doing well.",
        "Think about the system.",
        "You are one of us."
    ],
    STATE_ANGRY: [
        "Do not lie to me.",
        "You make me nervous.",
        "Your words are suspicious.",
        "I am losing patience."
    ]
}


# ===================== УТИЛИТА ПЕРЕТАСКИВАНИЯ =====================
def make_draggable(win, bar):
    def start(e):
        win.x = e.x
        win.y = e.y

    def move(e):
        win.geometry(f"+{e.x_root - win.x}+{e.y_root - win.y}")

    bar.bind("<Button-1>", start)
    bar.bind("<B1-Motion>", move)


# ===================== КЛАСС ABEBE =====================
class AbebeWatcher:
    def __init__(self, root, trust_system):
        self.root = root
        self.trust_system = trust_system

        self.state = STATE_NEUTRAL
        self.frames = []
        self.frame_index = 0
        self.shake_job = None

        self._create_window()
        self._create_text_window()
        self._load_gif()
        self._animate()

    # ===================== ОКНО GIF =====================
    def _create_window(self):
        self.win = tk.Toplevel(self.root)
        self.win.overrideredirect(True)
        self.win.configure(bg="black")
        self.win.attributes("-topmost", True)
        self.win.geometry("320x420+30+100")

        # TITLE BAR
        self.title_bar = tk.Frame(self.win, bg="#C0C0C0", height=24)
        self.title_bar.pack(fill="x", side="top")

        tk.Label(
            self.title_bar,
            text="ABEBE_WATCHER.EXE",
            bg="#C0C0C0",
            fg="black",
            font=("Terminal", 10)
        ).pack(side="left", padx=6)

        self.close_btn = tk.Label(
            self.title_bar,
            text=" ✕ ",
            bg="#C0C0C0",
            fg="black",
            font=("Terminal", 10, "bold"),
            cursor="hand2"
        )
        self.close_btn.pack(side="right", padx=4)
        self.close_btn.bind("<Button-1>", lambda e: self.destroy())
        self.close_btn.bind("<Enter>", lambda e: self.close_btn.config(bg="red", fg="white"))
        self.close_btn.bind("<Leave>", lambda e: self.close_btn.config(bg="#C0C0C0", fg="black"))

        make_draggable(self.win, self.title_bar)

        # GIF
        self.gif_label = tk.Label(self.win, bg="black")
        self.gif_label.pack(pady=10)

    # ===================== ОТДЕЛЬНОЕ ОКНО ТЕКСТА =====================
    def _create_text_window(self):
        self.text_win = tk.Toplevel(self.root)
        self.text_win.overrideredirect(True)
        self.text_win.configure(bg="black")
        self.text_win.attributes("-topmost", True)
        self.text_win.geometry("380x120+370+100")

        # TITLE BAR
        self.text_title = tk.Frame(self.text_win, bg="#C0C0C0", height=24)
        self.text_title.pack(fill="x", side="top")

        tk.Label(
            self.text_title,
            text="ABEBE DIALOG",
            bg="#C0C0C0",
            fg="black",
            font=("Terminal", 10)
        ).pack(side="left", padx=6)

        self.text_close = tk.Label(
            self.text_title,
            text=" ✕ ",
            bg="#C0C0C0",
            fg="black",
            font=("Terminal", 10, "bold"),
            cursor="hand2"
        )
        self.text_close.pack(side="right", padx=4)
        self.text_close.bind("<Button-1>", lambda e: self.text_win.destroy())
        self.text_close.bind("<Enter>", lambda e: self.text_close.config(bg="red", fg="white"))
        self.text_close.bind("<Leave>", lambda e: self.text_close.config(bg="#C0C0C0", fg="black"))

        make_draggable(self.text_win, self.text_title)

        # LABEL
        self.text_label = tk.Label(
            self.text_win,
            text="",
            fg="white",
            bg="black",
            font=("Terminal", 16),
            wraplength=360,
            justify="center"
        )
        self.text_label.pack(padx=10, pady=10, anchor="center")

    # ===================== ЗАГРУЗКА GIF =====================
    def _load_gif(self):
        self.frames.clear()
        self.frame_index = 0
        gif_name = GIFS[self.state]
        gif_path = os.path.join(get_exe_dir(), DATA_DIR, gif_name)
        i = 0
        while True:
            try:
                frame = tk.PhotoImage(file=gif_path, format=f"gif -index {i}")
                self.frames.append(frame)
                i += 1
            except:
                break

    # ===================== АНИМАЦИЯ =====================
    def _animate(self):
        if not self.win.winfo_exists():
            return
        if self.frames:
            self.gif_label.config(image=self.frames[self.frame_index])
            self.frame_index = (self.frame_index + 1) % len(self.frames)
        self.win.after(90, self._animate)

    # ===================== ОБНОВЛЕНИЕ СОСТОЯНИЯ =====================
    def update_state(self):
        if self.trust_system.is_suspicious():
            new_state = STATE_ANGRY
        elif self.trust_system.trust >= 70:
            new_state = STATE_HAPPY
        else:
            new_state = STATE_NEUTRAL

        if new_state != self.state:
            self.state = new_state
            self._load_gif()
            self.show_dialog()

    # ===================== ПОКАЗ ДИАЛОГА =====================
    def show_dialog(self, custom_text=None):
        self._stop_shake()
        text = custom_text if custom_text else random.choice(DIALOGS[self.state])
        self.text_label.config(text=text)
        if self.state == STATE_ANGRY:
            self._start_shake()

    # ===================== ЭФФЕКТ ДРОЖАНИЯ =====================
    def _start_shake(self, intensity=4, speed=40):
        def jitter():
            dx = random.randint(-intensity, intensity)
            dy = random.randint(-intensity, intensity)
            self.text_label.place(
                x=190 + dx,
                y=60 + dy,
                anchor="center"
            )
            self.shake_job = self.text_label.after(speed, jitter)

        self.text_label.place(x=190, y=60, anchor="center")
        jitter()

    def _stop_shake(self):
        if self.shake_job:
            self.text_label.after_cancel(self.shake_job)
            self.shake_job = None
        self.text_label.place_forget()
        self.text_label.pack(padx=10, pady=10, anchor="center")

    # ===================== ВНЕШНИЙ ВЫЗОВ =====================
    def on_user_input(self, text):
        self.update_state()
        self.show_dialog()

    # ===================== ЗАКРЫТИЕ =====================
    def destroy(self):
        if self.win.winfo_exists():
            self.win.destroy()
        if self.text_win.winfo_exists():
            self.text_win.destroy()
