from desktop_overlay.core.hotkey_manager import HotkeyManager
from PySide6.QtGui import QScreen
from PySide6.QtCore import QRect


#TODO: this class is pretty solid, could think on how to insert more settings here
#TODO: Also go more functional paradigm, class is not necessary here
class SettingsManager():
    '''
    Settings Manager is responsible for all functionality settings-wise in OverlayManager,
    it's role is to manage settings and be a middleman between user and software settings.
    '''
    def __init__(self, hotkey_manager: HotkeyManager):
        self.hotkey_manager = hotkey_manager
        self.screens: list[QScreen] = []
        self.active_screen: QScreen | None = None
        self.active_screen_number = None

    def change_overlay_shortcut(self) -> None:
        '''Change overlay shorcut'''
        self.hotkey_manager.change_activation_sequence()

    def select_screen(self, selected_screen_nr: int) -> tuple[QRect, int, int]:
        '''Select on which screen to run the overlay'''
        self.active_screen = self.screens[selected_screen_nr]
        self.selected_screen_nr = selected_screen_nr
        if len(self.screens) > selected_screen_nr:
            self.active_screen = self.screens[selected_screen_nr]
        return self._get_screen_geometry()

    def setup_screens(self, screens: list[QScreen], selected_screen_nr: int) -> None:
        '''Initializes and setups the screens for settings'''
        self.screens = screens
        if len(self.screens) > selected_screen_nr:
            #print(selected_screen_nr)
            self.active_screen = self.screens[selected_screen_nr]

    def list_screens(self) -> list[tuple[int, QScreen]]:
        '''Lists available screens'''
        return [(idx, screen) for idx, screen in enumerate(self.screens)]
    
    def get_screens_strings(self) -> list[str]:
        '''Returns a list of strings representing each detected screen'''
        tmp = self.list_screens()

        return [f"  {idx} - {disp.name()}" for idx, disp in tmp]

    def _get_screen_geometry(self) -> tuple[QRect, int, int]:
        '''Returns active screen geometry'''
        if not self.active_screen:
            raise RuntimeError("No active screen selected.")
        screen_geometry = self.active_screen.geometry()
        center_x = screen_geometry.x() 
        center_y = screen_geometry.y() 
        return screen_geometry, center_x, center_y
