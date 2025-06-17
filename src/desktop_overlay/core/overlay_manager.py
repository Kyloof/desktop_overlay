'''
Overlay_manager - class that adds functionality to the GUI
'''

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QKeySequence, QAction, QShortcut
from desktop_overlay.ui.core_overlay_ui import UiOverlay
from desktop_overlay.core.hotkey_manager import HotkeyManager

import threading

from pynput import keyboard

class OverlayManager(QMainWindow):
    def __init__(self):
        super().__init__()
        ### For now, might change in the future, left ctrl + 0
        self.seq = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('0')}
        
        self.ui = UiOverlay()
        self.ui.set_up_ui(self)

        ### Making it fullscreen
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.move(0, 0)

        ### React when the sequence is pressed
        HotkeyManager(self.seq, self._toggle_visibility)

        self.ui.exit_button.clicked.connect(QCoreApplication.quit)

    def _toggle_visibility(self):
        self.setVisible( not self.isVisible() )
        
