'''
This runs everything
'''

from PySide6.QtWidgets import QApplication
from desktop_overlay.core.overlay_manager import Overlay_manager
import sys

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Overlay_manager()
    window.show()
    
    sys.exit(app.exec())