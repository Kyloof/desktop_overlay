from PySide6.QtWidgets import QPushButton
from PySide6.QtGui import QIcon
from PySide6.QtCore import QSize

### Settings and close buttons have the same styling options so i made this 
def style_navigation_buttons(button: QPushButton, dim: int, icon_path: str):
    button.setFixedSize(dim, dim)
    button.setIcon(QIcon(icon_path))
    button.setIconSize(QSize(dim, dim))
    ### Little hover effect :O
    button.setStyleSheet("""
        QPushButton {
            background-color: transparent;
            border: none;
        }
        QPushButton:hover {
            background-color: rgba(255, 255, 255, 30);
        }
    """)