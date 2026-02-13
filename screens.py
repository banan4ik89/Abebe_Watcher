import tkinter as tk
import os
import winsound
from utils import block_esc, get_exe_dir
from config import DATA_DIR

def show_image_fullscreen(root, image, sound=None, duration=5000):
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    block_esc(win)

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    win.geometry(f"{sw}x{sh}+0+0")

    canvas = tk.Canvas(win, bg="black", highlightthickness=0)
    canvas.pack(fill="both", expand=True)

    img_path = os.path.join(get_exe_dir(), DATA_DIR, image)
    img = tk.PhotoImage(file=img_path)
    canvas.create_image(sw // 2, sh // 2, image=img)
    canvas.image = img

    if sound:
        winsound.PlaySound(
            os.path.join(get_exe_dir(), DATA_DIR, sound),
            winsound.SND_FILENAME | winsound.SND_ASYNC
        )

    win.after(duration, win.destroy)


def show_poor_virus_message(root):
    win = tk.Toplevel(root)
    win.overrideredirect(True)
    block_esc(win)
    win.geometry("+400+250")

    frame = tk.Frame(win, bg="white", bd=2, relief="ridge")
    frame.pack(fill="both", expand=True)

    tk.Label(frame, text="Сообщение от вируса",
             font=("Arial", 14, "bold"), bg="white").pack(pady=10)

    msg = (
        "Здравствуйте!\n\n"
        "Я бедный вирус из Албании 🇦🇱\n"
        "Бюджет не выделили 😢\n\n"
        "Удалите System32 сами 🙏"
    )

    tk.Label(frame, text=msg, bg="white",
             justify="center", wraplength=480).pack(pady=10)

    tk.Button(frame, text="ОК",
              command=root.destroy).pack(pady=10)
