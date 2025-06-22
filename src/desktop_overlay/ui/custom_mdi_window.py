from PySide6.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QStyle, QProxyStyle
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap

class CustomMDIWindow(QMdiSubWindow):
    def __init__(self, mod_name: str, mod_icon:str, parent=None):
        super().__init__(parent)
        ### I tried
        self.setWindowTitle(mod_name)
        self.setWindowIcon(QIcon(mod_icon))
        self.setStyleSheet("""
            color:black; 
            background-color: rgba(128, 128, 128, 150);
        """)


    def closeEvent(self, closeEvent):
        if self.widget():
            self.widget().is_open = False
            self.widget().setParent(None)
        self.setWidget(None)
        return super().closeEvent(closeEvent)