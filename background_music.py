import winsound
import os
from utils import get_exe_dir
from config import DATA_DIR

_current_music = None

def play_music(filename):
    global _current_music
    _current_music = filename

    path = os.path.join(get_exe_dir(), DATA_DIR, filename)
    if os.path.exists(path):
        winsound.PlaySound(
            path,
            winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP
        )

def stop_music():
    winsound.PlaySound(None, winsound.SND_PURGE)

def resume_music():
    if _current_music:
        play_music(_current_music)
