"""
OverlayManager - class that adds functionality to the GUI
"""

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QCoreApplication
from PySide6.QtGui import QKeySequence, QAction, QShortcut

from desktop_overlay.ui.core_overlay_ui import UiOverlay
from desktop_overlay.core.hotkey_manager import HotkeyManager
from desktop_overlay.core.mod_manager import ModManager
from desktop_overlay.ui.mod_list_model import ModListModel

import threading

from pynput import keyboard


class OverlayManager(QMainWindow):
    def __init__(self, screen_nr: int = 0):
        super().__init__()
        ### For now, might change in the future, left ctrl + 0
        self.seq = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char("0")}

        self.mod_manager = ModManager()

        self.mod_manager.detect_mods()
        self.mod_manager.enable_all()
        self.model = ModListModel(list(self.mod_manager.enabled_mods.values())) 

        self.ui = UiOverlay()
        self.ui.set_up_ui(self)

        screens = QApplication.screens()

        ### Making it fullscreen
        screen_geometry = screens[screen_nr].geometry()
        self.setGeometry(screen_geometry)

        ### React when the sequence is pressed
        HotkeyManager(self.seq, self._toggle_window_visibility)

        self.ui.mod_list.setModel(self.model)

        ### This button will ultimately hide the overlay but i right now i need something to close the app
        self.ui.exit_button.clicked.connect(QCoreApplication.quit)
        self.ui.settings_button.clicked.connect(self._toggle_settings_visibility)

    def _toggle_window_visibility(self):
        self.setVisible(not self.isVisible())

    def _toggle_settings_visibility(self):
        settings = self.ui.settings_menu
        settings.setVisible(not settings.isVisible())
