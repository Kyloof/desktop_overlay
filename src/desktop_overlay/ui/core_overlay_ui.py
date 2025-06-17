'''
Ui_overlay - class with GUI of the overlay
'''

from PySide6.QtWidgets import QMainWindow, QApplication, QLabel, QPushButton, QWidget, QStyle, QVBoxLayout
from PySide6.QtCore import Qt, QSize, QCoreApplication
from PySide6.QtGui import QPainter, QColor
import sys

class UiOverlay(object):
    def set_up_ui(self, MainWindow: QMainWindow):
        
        MainWindow.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )

        self.central_widget = QWidget()
        MainWindow.setCentralWidget(self.central_widget)
        vbox = QVBoxLayout(self.central_widget)

        self.exit_button = QPushButton('Exit')

        vbox.addWidget(self.exit_button, alignment=Qt.AlignHCenter)
