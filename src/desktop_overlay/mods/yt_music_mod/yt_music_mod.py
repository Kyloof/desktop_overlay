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

    def __init__(self):
        super().__init__()
        self.ytmusic = YTMusic()
        self.current_song_label = None
        self.search_input = None
        self.search_results_list = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)

        # Show the current song
        self.current_song_label = QLabel("Current Song: Unknown")
        layout.addWidget(self.current_song_label)

        # Search input field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search for a song...")
        layout.addWidget(self.search_input)

        # Search button
        search_button = QPushButton("Search")
        search_button.clicked.connect(self.search_song)
        layout.addWidget(search_button)

        # Search results display
        self.search_results_list = QListWidget()
        layout.addWidget(self.search_results_list)

    def search_song(self):
        query = self.search_input.text()
        if not query:
            return

        self.search_results_list.clear()

        def do_search():
            try:
                results = self.ytmusic.search(query)
                for item in results[:10]:
                    title = item.get("title", "Unknown Title")
                    artist = item.get("artists", [{}])[0].get(
                        "name", "Unknown Artist")
                    self.search_results_list.addItem(f"{title} - {artist}")
            except Exception as e:
                print(f"[YTMusicMod] Search error: {e}")
                self.search_results_list.addItem("Error during search.")

        threading.Thread(target=do_search, daemon=True).start()
