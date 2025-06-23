from PySide6.QtWidgets import QSystemTrayIcon, QMenu 
from PySide6.QtGui import QIcon, QAction
from desktop_overlay.definitions import ROOT_DIR


class OverlayTray:
    def __init__(self):
        self.icon = QIcon(f"{ROOT_DIR}/ui/assets/overlay_icon.png")
        self.tray = QSystemTrayIcon(self.icon)
        self.tray.setToolTip("Desktop Overlay")

        self.menu = QMenu()

        self.quit_action = QAction("Quit")
        self.menu.addAction(self.quit_action)

        self.open_action = QAction("Open")
        self.menu.addAction(self.open_action)

        self.tray.setContextMenu(self.menu)
        self.tray.show()
