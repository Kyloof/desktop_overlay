from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR
from PySide6.QtWidgets import (
    QVBoxLayout, QLabel, QPushButton, QLineEdit, QListWidget, QMessageBox
)
from ytmusicapi import YTMusic
import threading


class YtMusicMod(BaseMod):
    name = "YTMusic Mod"
    description = "View currently played song on YT Music and control it."
    icon_path = f"{ROOT_DIR}/mods/yt_music_mod/assets/yt_music_icon.png"
    is_open = False
    id = None
    default_size = (475,550)

    def __init__(self):
        super().__init__()
        self.ytmusic = YTMusic()
        self.current_song_label = None
        self.search_input = None
        self.search_results_list = None
        self.main_layout = QVBoxLayout(self)
    
    def load_state(self) -> None:
        pass
    
    def remove_state(self) -> None:
        pass
