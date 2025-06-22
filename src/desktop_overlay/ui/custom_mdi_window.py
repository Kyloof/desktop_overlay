from PySide6.QtWidgets import QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QStyle, QProxyStyle
from PySide6.QtCore import Qt, QSize, QEvent
from PySide6.QtGui import QIcon, QPalette, QColor, QPixmap

from desktop_overlay.core.base_mod import BaseMod

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

    # If done this way all calls from outside the class will also set the default size, maybe not ideal but acceptable.
    # Also had to add widget type QWidget | None. In docs it's QWidget* so i think that's the same shit
    def setWidget(self, widget: QWidget | None):
        ''' setWidget that also resizes the window for the default size'''
        super().setWidget(widget)  # Here it says that it's wrong but it works so who cares
        if isinstance(widget, BaseMod):
            if hasattr(widget, "default_size"):
                w, h = widget.default_size
                self.resize(w, h)

    def closeEvent(self, closeEvent):
        if self.widget():
            self.widget().is_open = False
            self.widget().setParent(None)
            self.widget().remove_state()
        self.setWidget(None)
        return super().closeEvent(closeEvent)
