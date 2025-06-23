'''
This runs everything
'''

from PySide6.QtWidgets import QApplication
from desktop_overlay.core.overlay_manager import OverlayManager
import sys

def main():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QToolTip {
            color: white;
            padding: 3px;
            font-size: 14px;
            border: 1px solid white;
        }    
    """)

    window = OverlayManager()
    window.show()

    sys.exit(app.exec())

if __name__ == '__main__':
    main()