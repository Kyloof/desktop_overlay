from PySide6.QtWidgets import QWidget
from core.base_mod import BaseMod
import os
import importlib


class ModManager:
    def __init__(self):
        self.mods: List[BaseMod] = []
        self.enabled_mods: List[BaseMod] = []
        self.MODS_PATH = "mods"

    def detect_mods(self) -> None:
        for path in os.listdir(self.MODS_PATH):
            if path.endswith(".py"):
