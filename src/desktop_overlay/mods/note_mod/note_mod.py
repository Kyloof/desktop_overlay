from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR
from PySide6.QtWidgets import QVBoxLayout, QTextEdit
from PySide6.QtCore import Qt


class NoteMod(BaseMod):
    name = "Note Mod"
    description = "A simple text box for writing notes."
    icon_path = f"{ROOT_DIR}/mods/note_mod/assets/note_icon.png"
    is_open = False
    id = None
    
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.text_edit = QTextEdit()
        layout.addWidget(self.text_edit)

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
