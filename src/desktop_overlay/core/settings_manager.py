from desktop_overlay.core.hotkey_manager import HotkeyManager
from PySide6.QtGui import QScreen

class SettingsManager():
    '''
    Settings Manager is responsible for all functionality settings-wise in OverlayManager,
    it's role is to manage settings and be a middleman between user and software settings.
    '''
    def __init__(self, hotkey_manager: HotkeyManager):
        self.hotkey_manager = hotkey_manager
        self.screens: list[QScreen] = []
        self.active_screen: QScreen | None = None

    def change_overlay_shortcut(self) -> None:
        '''Change overlay shorcut and return the new shortcut as a string'''
        self.hotkey_manager.change_activation_sequence()

    def select_screen(self, selected_screen_nr):
        '''Select on which screen to run the overlay'''
        self.active_screen = self.screens[selected_screen_nr]
        if len(self.screens) > selected_screen_nr:
            self.active_screen = self.screens[selected_screen_nr]

    def setup_screens(self, screens: list[QScreen], selected_screen_nr: int):
        '''Initializes and setups the screens for settings'''
        self.screens = screens
        if len(self.screens) > selected_screen_nr:
            #print(selected_screen_nr)
            self.active_screen = self.screens[selected_screen_nr]

    def list_screens(self):
        '''Lists available screens'''
        return [(idx, screen) for idx, screen in enumerate(self.screens)]
    
    def get_screens_strings(self):
        '''Returns a list of strings representing each detected screen'''
        tmp = self.list_screens()

        return [f"  {idx} - {disp.name()}" for idx, disp in tmp]

    def get_screen_geometry(self):
        '''Returns active screen geometry'''
        if not self.active_screen:
            raise RuntimeError("No active screen selected.")
        return self.active_screen.geometry()
