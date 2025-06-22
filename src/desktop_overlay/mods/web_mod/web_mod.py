from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl


class WebMod(BaseMod):
    name = "Web Mod"
    description = "Enables web browser usage."
    is_open = False
    id = None
    icon_path = f"{ROOT_DIR}/mods/web_mod/assets/web_icon.png"
    default_size = (1000,600)

    def __init__(self, url=QUrl("https://www.google.com/")):
        super().__init__()
        self.url = url
        self.web_view = None
        self.main_layout = QVBoxLayout(self)

    def load_state(self):
        self.web_view = QWebEngineView(self)
        self.main_layout.addWidget(self.web_view)
        self.web_view.setUrl(self.url)

    def remove_state(self):
        if self.web_view:
            self.main_layout.removeWidget(self.web_view)
            self.web_view.deleteLater()
            self.web_view = None

