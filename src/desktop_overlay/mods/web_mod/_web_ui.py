from PySide6.QtWidgets import QApplication, QWidget, QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

def create_ui(url: QUrl) -> QWidget:
    window = QWidget()
    layout = QVBoxLayout()

    view = QWebEngineView()
    layout.addWidget(view)

    view.setUrl(url)
    window.setLayout(layout)
    
    return window
