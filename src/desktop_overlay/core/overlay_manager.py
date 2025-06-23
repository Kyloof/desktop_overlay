"""
OverlayManager - class that adds functionality to the GUI
"""

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import QCoreApplication, Qt

from desktop_overlay.core import mod_manager
from desktop_overlay.ui.core_overlay_ui import UiOverlay
from desktop_overlay.core.hotkey_manager import HotkeyManager
from desktop_overlay.core.mod_manager import ModManager
from desktop_overlay.core.settings_manager import SettingsManager
from desktop_overlay.ui.mod_list_model import ModListModel
from desktop_overlay.ui.custom_mdi_window import CustomMDIWindow
from desktop_overlay.ui.system_tray import OverlayTray

class OverlayManager(QMainWindow):
    
    def __init__(self, screen_number: int = 0):
        super().__init__()

        ### Qt.X11BypassWindowManagerHint needs to stay,
        ### it fucks everything up but for the love of god it needs to stay
        ### oterwise everything will be even more fucked
        self.setWindowFlags(
            Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.X11BypassWindowManagerHint
        )
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setFocusPolicy(Qt.StrongFocus)

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
        self.ui.saved_shortcut.setText("+".join(str(s) for s in self.hotkey_manager.activation_sequence))
        self.overlay_tray = OverlayTray()
        self.overlay_tray.open_action.triggered.connect(self._toggle_window_visibility)
        self.overlay_tray.quit_action.triggered.connect(QCoreApplication.quit)
        self.overlay_tray.quit_action.triggered.connect(self.hotkey_manager.stop)
        self.overlay_tray.quit_action.triggered.connect(self.mod_manager.disable_all)

        ### Making it fullscreen
        self.screens = QApplication.screens()
        self.settings_manager.setup_screens(self.screens, screen_number)
        self._set_screen(0) #should be saved value
        
        self.hotkey_manager.changed.connect(self._change_displayed_shortcut)
        self.ui.settings_button.clicked.connect(self._toggle_settings_visibility)
        self.ui.exit_button.clicked.connect(self._toggle_window_visibility)

        ### Open mods
        self.ui.mod_list.clicked.connect(self._mod_clicked)
        
        ### Connecting settings
        ### changing the shortcut is not working yet
        self.ui.edit_shortcut.clicked.connect(self.settings_manager.change_overlay_shortcut)
        self.ui.display_selector.addItems(self.settings_manager.get_screens_strings())
        self.ui.display_selector.currentIndexChanged.connect(self._set_screen)


        self._toggle_window_visibility()

    def _set_screen(self, index):
        geometry, center_x, center_y = self.settings_manager.select_screen(index)
        self.setGeometry(geometry)
        self.move(center_x, center_y)

    def _mod_clicked(self, index):
        mod = self.enabled_mods[index.row()]

        if not mod.is_open:
            sub = CustomMDIWindow(mod_name=mod.name, mod_icon=mod.icon_path)
            sub.setWidget(mod)
        
            self.ui.mod_windows_area.addSubWindow(sub)
            sub.show()

            mod.is_open = True

            ### God bless tomascapek from stackoverflow <3
            ### https://stackoverflow.com/questions/33244271/window-doesnt-get-focus-when-using-qtx11bypasswindowmanagerhint-flag
            ### Proof that stackoverflow is better than AI
            ### this piece of shit of a line fixes everything
            self.activateWindow()
        else:
            print('Mod is already opened')

    def _toggle_window_visibility(self):
        if not self.isVisible():
            self.show()
            self.raise_()
            self.activateWindow()
            self.setFocus()
        else:
            self.hide()

    def _toggle_settings_visibility(self):
        settings = self.ui.settings_menu
        settings.setVisible(not settings.isVisible())

    def _change_displayed_shortcut(self, new_shortuct: str) -> None:
        self.ui.saved_shortcut.setText(new_shortuct)

