"""
OverlayManager - class that adds functionality to the GUI
"""

from PySide6.QtWidgets import QMainWindow, QApplication, QMdiSubWindow
from PySide6.QtCore import QCoreApplication, Qt
from PySide6.QtGui import QKeySequence, QAction, QShortcut

from desktop_overlay.ui.core_overlay_ui import UiOverlay
from desktop_overlay.core.hotkey_manager import HotkeyManager
from desktop_overlay.core.mod_manager import ModManager
from desktop_overlay.core.settings_manager import SettingsManager
from desktop_overlay.ui.mod_list_model import ModListModel

class OverlayManager(QMainWindow):
    
    def __init__(self, screen_number: int = 0):
        super().__init__()
        
        ### Managers
        self.mod_manager = ModManager()
        self.hotkey_manager = HotkeyManager(self._toggle_window_visibility)
        self.settings_manager = SettingsManager(self.hotkey_manager)

        ### Load mods
        self.mod_manager.detect_mods()
        self.mod_manager.enable_all()
        self.enabled_mods = list(self.mod_manager.enabled_mods.values())
        self.model = ModListModel(self.enabled_mods) 

        ### UI
        self.ui = UiOverlay()
        self.ui.set_up_ui(self)
        self.ui.mod_list.setModel(self.model)

        ### Making it fullscreen
        self.screens = QApplication.screens()
        self.settings_manager.setup_screens(self.screens, screen_number)
        self.set_screen()
        
        ### This button will ultimately hide the overlay but i right now i need something to close the app
        self.ui.exit_button.clicked.connect(QCoreApplication.quit)
        self.ui.settings_button.clicked.connect(self._toggle_settings_visibility)

        ### Open mods
        self.ui.mod_list.clicked.connect(self._mod_clicked)
        
        self._toggle_window_visibility()

    def set_screen(self):
        self.setGeometry(self.settings_manager.get_screen_geometry())
    
    def _mod_clicked(self, index):
        mod = self.enabled_mods[index.row()]

        sub = QMdiSubWindow()
        sub.setWidget(mod)
        
        self.ui.mod_windows_area.addSubWindow(sub)
        sub.show()

    def _toggle_window_visibility(self):
        self.setVisible(not self.isVisible())
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)
        self.setFocus()

    def _toggle_settings_visibility(self):
        settings = self.ui.settings_menu
        settings.setVisible(not settings.isVisible())

    def test(self):
        print(self.settings_manager.list_screens())

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    om = OverlayManager()
    om.test()
    om.show()
    sys.exit(app.exec())
