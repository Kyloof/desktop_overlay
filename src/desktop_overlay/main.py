'''
This runs everything
'''

from PySide6.QtWidgets import QApplication
from desktop_overlay.core.overlay_manager import OverlayManager
import sys

def main():
    app = QApplication(sys.argv)
    window = OverlayManager()
    window.show()

    sys.exit(app.exec())
