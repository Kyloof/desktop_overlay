from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR

from PySide6.QtCore import Qt, QThread, Signal, QByteArray
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import ( QFrame, QHBoxLayout, QLabel, QProgressBar,
                                QPushButton, QSizePolicy, QSpacerItem, QVBoxLayout)

import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os
import time
import requests

load_dotenv()

CLIENT_ID = os.getenv('CLIENT_ID')
CLIENT_SECRET = os.getenv('CLIENT_SECRET')
REDIRECT_URI = os.getenv('REDIRECT_URI')

class SpotifyListenerThread(QThread):
    # Signal: song info (artist - song name), progress, duration , URL to album art
    playback = Signal(str, int, int ,str)

    def __init__(self):
        super().__init__()
        ### Being able to check currently playing song and to skip etc
        self.scope = "user-read-playback-state", "user-modify-playback-state"
        self.sp = spotipy.Spotify(
            auth_manager=SpotifyOAuth(
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                redirect_uri=REDIRECT_URI,
                scope=self.scope
            )
        )
        self._running = True
        self.album_art_url = None


    def run(self):
        while self._running:
            self._get_data()
            time.sleep(2)
    
    def _get_data(self):
        '''
        The plan is simple we go in, take the data and disappear like nothing ever happend.
        (Just collects neccessary data form API)
        '''
        playback = self.sp.current_playback()
    
        if playback and playback['item']:
            name = f'{playback['item']['artists'][0]['name']} - {playback['item']['name']}'
            progress = int(playback['progress_ms'])
            duration = int(playback['item']['duration_ms'])
            
            if not self.album_art_url is playback['item']['album']['images'][1]['url']: 
                self.album_art_url = playback['item']['album']['images'][1]['url']
                self.playback.emit(name, progress, duration, self.album_art_url)
            else:
                self.playback.emit(name, progress, duration, None)

    def stop(self):
        self.terminate()
    
    def next_song(self):
        '''Code so good it doesn't need a comment'''
        self.sp.next_track()
        self._get_data()

    def prev_song(self):
        '''Code so good it doesn't need a comment'''
        self.sp.previous_track()
        self._get_data()

    def is_playing(self):
        '''Checks if a song is playing(True)/paused(False) or the spotify is closed (None)'''
        playback = self.sp.current_playback()

        if playback:
            return playback['is_playing']
        
        return None


class SpotifyMod(BaseMod):
    name = "Spotify Mod"
    description = "Shows what is currentlly playing on spotify."
    is_open = False
    id = None
    icon_path = f"{ROOT_DIR}/mods/spotify_mod/assets/spotify_icon.png"
    default_size = (300,350)

    def __init__(self):
        super().__init__()
        self.main_frame = None
        self.main_layout = QVBoxLayout(self)
        self.load_state()

        self.spoti_listener = SpotifyListenerThread()
        self.spoti_listener.playback.connect(self._update_mod)
        self.spoti_listener.start()

    def load_state(self):
        '''Check BaseMod comments'''
        vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.main_layout.addItem(vertical_spacer)
        self.main_frame = QFrame(self)
        self.main_frame.setStyleSheet("""
            background-color: transparent;
        """)
        main_frame_vl = QVBoxLayout(self.main_frame)

        ### Image frame
        img_frame = QFrame(self.main_frame)
        img_frame_hl = QHBoxLayout(img_frame)

        ### Adding Spacers to make the img centered 
        img_frame_hl.addItem(
            QSpacerItem(381, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        ### Image is a button :O
        self.song_img = QPushButton(self.main_frame)
        self.song_img.setIcon(QIcon(self.icon_path))
        self.song_img.setIconSize(QPixmap(self.icon_path).size())
        self.song_img.setFixedSize(300, 300)
        self.song_img.clicked.connect(self._toggle_playing_state)
        
        img_frame_hl.addWidget(self.song_img)

        img_frame_hl.addItem(
            QSpacerItem(381, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        )

        main_frame_vl.addWidget(img_frame)

        ### Song name label (Changed dynamically)
        self.song_name = QLabel(self.main_frame)
        self.song_name.setText("Nothing is currently playing.")
        self.song_name.setStyleSheet("""
            font-size: 18px;
            font-weight: 500;
            color: #EDEDED
        """)
        self.song_name.setAlignment(Qt.AlignmentFlag.AlignCenter)

        main_frame_vl.addWidget(self.song_name)

        ### Section with navigation buttons annd progress bar
        player_frame = QFrame(self.main_frame)
        player_hl = QHBoxLayout(player_frame)

        ### Previous button
        self.prev_button = QPushButton(player_frame)
        self.prev_button.setStyleSheet("""
            background-color: #EDEDED;
        """)
        self.prev_button.setIcon(QIcon(f"{ROOT_DIR}/mods/spotify_mod/assets/previous_song.png"))
        self.prev_button.clicked.connect(self._prev_song)
        player_hl.addWidget(self.prev_button)
        
        ### Progress bar
        self.song_progress_bar = QProgressBar(player_frame)
        self.song_progress_bar.setValue(0)
        self.song_progress_bar.setTextVisible(False)
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

        # Add a label under the progress bar
        self.progress_label = QLabel(player_frame)
        self.progress_label.setText("")  
        self.progress_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_label.setStyleSheet("""
            font-size: 16px;
            color: #EDEDED;
            font-weight: 500;
        """)
        
        ### Next button
        self.next_button = QPushButton(player_frame)
        self.next_button.setIcon(QIcon(f"{ROOT_DIR}/mods/spotify_mod/assets/next_song.png"))
        self.next_button.setStyleSheet("""
            background-color: #EDEDED;
        """)
        self.next_button.clicked.connect(self._next_song)
        player_hl.addWidget(self.next_button)

        ### Adding this the the layout
        main_frame_vl.addWidget(player_frame)

        main_frame_vl.addWidget(self.progress_label)

        self.main_layout.addWidget(self.main_frame)

    def remove_state(self):
        '''Check BaseMod comments'''
        if self.main_frame:
            self.main_layout.removeWidget(self.main_frame)

            self.main_frame.deleteLater()
            self.main_frame = None

            self.spoti_listener.stop()

    def _next_song(self):
        '''
        Calls spoti_listener to skip to the next song 
        (Can't do this in load_state cuz idk)
        '''
        self.spoti_listener.next_song()

    def _prev_song(self):
        '''
        Calls spoti_listener to go back to the previous song 
        (Can't do this in load_state cuz idk)
        '''
        self.spoti_listener.prev_song()

    def _toggle_playing_state(self):
        '''
        After pressing on the album art it pauses and plays the song on spotify 
        '''
        tmp = self.spoti_listener.is_playing()

        if not tmp is None:
            if tmp is True:
                self.spoti_listener.sp.pause_playback()
            else:
                self.spoti_listener.sp.start_playback()
        
    def _update_mod(self, name: str, progress: int, duration: int ,album_art_url):
        '''
        Takes the data from spoti_listener (API thread) and sets coresponding Widgets
        '''
        def format_time(timestamp: int):
            minutes = (timestamp // 1000) // 60
            seconds = (timestamp // 1000) % 60
            return f'{minutes}:{seconds:02d}'
        
        self.song_name.setText(name)
        self.song_progress_bar.setValue( (progress*100) // duration )
        self.progress_label.setText(f'{format_time(progress)}/{format_time(duration)}')

        if album_art_url:
            response = requests.get(album_art_url)
            image_data = response.content
            
            pixmap = QPixmap()
            pixmap.loadFromData(QByteArray(image_data))
            
            self.song_img.setIcon(QIcon(pixmap))
            self.song_img.setIconSize(pixmap.size())
