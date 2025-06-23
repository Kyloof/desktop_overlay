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
    default_size = (300,400)

    def __init__(self):
        super().__init__()
        self.main_layout = QVBoxLayout(self)
        self.load_state()

    def load_state(self) -> None:
        self.text_edit = QTextEdit()
        self.text_edit.setStyleSheet("""
            background-color: rgba(255,255,90,120);
            padding: 20px;
            font-size: 18px;
            font-family: 'Fira Mono', 'Consolas', monospace;
            font-weight: 500;
            color: #141414;
            border-radius: 7px;
            selection-background-color: #fff59d;
            selection-color: #000;
        """)
        self.text_edit.setPlaceholderText("Type your notes here...")
        self.text_edit.setAlignment(Qt.AlignTop)
        self.main_layout.addWidget(self.text_edit)

    def remove_state(self) -> None:
        if self.text_edit != None:
            self.main_layout.removeWidget(self.text_edit)
            self.text_edit.deleteLater()
            self.text_edit = None
