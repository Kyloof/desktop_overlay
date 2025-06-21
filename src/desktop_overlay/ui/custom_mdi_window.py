from PySide6.QtWidgets import  QMdiSubWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QToolButton, QStyle
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon, QPalette

class CustomMDIWindow(QMdiSubWindow):
    def __init__(self, parent=None):
        super().__init__(parent)

    def closeEvent(self, closeEvent):
        widget = self.widget()

        if widget:
            widget.is_open = False
            widget.setParent(None)
        
        self.setWidget(None)

        return super().closeEvent(closeEvent)


class MyTitleBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.ColorRole.Highlight)
        self.initial_pos = None
        title_bar_layout = QHBoxLayout(self)
        title_bar_layout.setContentsMargins(1,1,1,1)
        title_bar_layout.setSpacing(2)

        self.title = QLabel(f"{self.__class__.__name__}", self)
        self.title.setStyleSheet("""
            font-weight: bold;
            margin: 2px;
        """)

        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.title.setText(parent.windowTitle())

        title_bar_layout.addWidget(self.title)
        self.close_button = QToolButton(self)
        close_icon = self.style().standardIcon(
            QStyle.StandardPixmap.SP_TitleBarCloseButton
        )
        self.close_button.setIcon(close_icon)
        self.close_button.clicked.connect(self.window().close)

        self.close_button.setFocusPolicy(Qt.FocusPolicy.NoFocus)
        self.close_button.setFixedSize(QSize(28,28))

        title_bar_layout.addWidget(self.close_button)
