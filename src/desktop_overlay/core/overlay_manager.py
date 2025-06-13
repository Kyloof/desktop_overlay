'''
Overlay_manager - class that adds functionality to the GUI
'''

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QKeySequence, QAction, QShortcut
from desktop_overlay.ui.core_overlay_ui import Ui_overlay
from desktop_overlay.core.hotkey_manager import Hotkey_manager

import threading

from pynput import keyboard

class Overlay_manager(QMainWindow):
    def __init__(self):
        super().__init__()
        ### For now, might change in the future, left ctrl + 0
        self.seq = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char('0')}
        
        self.ui = Ui_overlay()
        self.ui.set_up_ui(self)

        ### Making it fullscreen
        screen_geometry = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geometry)
        self.move(0, 0)

        ### React when the sequence is pressed
        Hotkey_manager(self.seq, self.__toggle_visibility)

        self.ui.exit_button.clicked.connect(QCoreApplication.quit)

    def __toggle_visibility(self):
        self.setVisible( not self.isVisible() )
        
