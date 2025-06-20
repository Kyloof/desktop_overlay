from desktop_overlay.core.base_mod import BaseMod
#from ._web_ui import create_ui
from desktop_overlay.definitions import ROOT_DIR
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl

class WebMod(BaseMod):
    name = "Web Mod"
    description = "Enables web browser usage."
    icon_path = f"{ROOT_DIR}/mods/web_mod/assets/web_icon.png" 
    id = None
    
    def __init__(self, url=QUrl("https://www.google.com/")):
        super().__init__()
        self.url = url
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.web_view = QWebEngineView(self)
        layout.addWidget(self.web_view)
        self.web_view.setUrl(self.url)

    def load(self):
        self.show()

    def unload(self):
        self.hide()

    def run(self):
        pass

    def stop(self):
        pass

    def resume(self):
        pass
