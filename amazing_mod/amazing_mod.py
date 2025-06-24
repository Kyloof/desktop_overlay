from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR
from PySide6.QtWidgets import QLabel, QVBoxLayout
from PySide6.QtGui import QPixmap, QImage
from PySide6.QtCore import Qt


class AmazingMod(BaseMod):
    name = "Amazing Mod"
    description = "Amazing."
    is_open = False
    id = None
    icon_path = f"{ROOT_DIR}/mods/amazing_mod/assets/boom_icon.png"
    default_size = (800, 600)

    def __init__(self):
        super().__init__()
        self.image = QImage(f"{ROOT_DIR}/mods/amazing_mod/assets/real.png")
        self.image_label = None
        self.main_layout = QVBoxLayout(self)
        self.load_state()

    def load_state(self):
        self.image_label = QLabel(self)
        pixmap = QPixmap.fromImage(self.image)
        self.image_label.setPixmap(pixmap)
        self.image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.main_layout.addWidget(self.image_label)

    def remove_state(self):
        if self.image_label:
            self.main_layout.removeWidget(self.image_label)
            self.image_label.deleteLater()
            self.image_label = None

    def reset_state(self):
        pass

