from abc import ABC, abstractmethod
from PySide6.QtWidgets import QWidget


class BaseMod(ABC, QWidget):
    @abstractmethod
    def load(self):
        pass

    @abstractmethod
    def unload(self):
        pass

    @abstractmethod
    def run(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def resume(self):
        pass
