from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR

from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import ( QFrame, QHBoxLayout, QLabel, QProgressBar,
                                QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout)

class SpotifyMod(BaseMod):
    name = "Spotify Mod"
    description = "Shows what is currentlly playing on spotify."
    is_open = False
    id = None
    icon_path = f"{ROOT_DIR}/mods/spotify_mod/assets/spotify_icon.png"
    default_size = (250,350)

    def __init__(self):
        super().__init__()
        self.main_frame = None
        self.main_layout = QVBoxLayout(self)
        self.load_state()

    def load_state(self):
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(vertical_spacer)
        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet("""
            background-color: transparent;
        """)
        main_frame_vl = QVBoxLayout(self.main_frame)

        img_frame = QFrame(self.main_frame)
        img_frame_hl = QHBoxLayout(img_frame)

        img_frame_hl.addItem(
            QSpacerItem(381, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        self.song_img = QLabel(self.main_frame)
        self.song_img.setPixmap(QPixmap(self.icon_path))
        self.song_img.setFixedSize(250,250)
        self.song_img.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        img_frame_hl.addWidget(self.song_img)

        img_frame_hl.addItem(
            QSpacerItem(381, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        main_frame_vl.addWidget(img_frame)

        self.song_name = QLabel(self.main_frame)
        self.song_name.setText("Nothing is currently playing.")
        self.song_name.setStyleSheet("""
            font-size: 18px;
            font-weight: 500;
            color: #EDEDED
        """)
        self.song_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_frame_vl.addWidget(self.song_name)

        player_frame = QFrame(self.main_frame)
        player_hl = QHBoxLayout(player_frame)

        self.prev_button = QPushButton(player_frame)
        self.prev_button.setStyleSheet("""
            background-color: #EDEDED;
        """)
        self.prev_button.setIcon(QIcon(f"{ROOT_DIR}/mods/spotify_mod/assets/previous_song.png"))
        player_hl.addWidget(self.prev_button)


        self.song_progress_bar = QProgressBar(player_frame)
        self.song_progress_bar.setValue(0)
        self.song_progress_bar.setStyleSheet("""
            QProgressBar {
            background-color: #141414;
            border: 1px solid #222;
            border-radius: 5px;
            font-weight: 500;
            text-align: center;
            color: #EDEDED;
            }
            QProgressBar::chunk {
            background-color: #1DB954;
            border-radius: 5px;
            }
        """)


        player_hl.addWidget(self.song_progress_bar)

        self.next_button = QPushButton(player_frame)
        self.next_button.setIcon(QIcon(f"{ROOT_DIR}/mods/spotify_mod/assets/next_song.png"))
        self.next_button.setStyleSheet("""
            background-color: #EDEDED;
        """)
        player_hl.addWidget(self.next_button)

        main_frame_vl.addWidget(player_frame)

        self.main_layout.addWidget(self.main_frame)



    def remove_state(self):
        if self.main_frame:
            self.main_layout.removeWidget(self.main_frame)

            self.main_frame.deleteLater()
            self.main_frame = None