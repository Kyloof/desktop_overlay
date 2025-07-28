from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QWidget

QWidgetMeta = type(QWidget)


class _BaseModMeta(ABCMeta, QWidgetMeta):
    '''Create BaseModMeta that connects ABCMeta and QWidgetMeta here, to merge them into one Metaclass'''
    pass

class BaseMod(ABC, QWidget, metaclass=_BaseModMeta):
    '''Abstract class for all mods that are yet to come'''

    @property
    @abstractmethod
    def id(self) -> int:
        pass

    @id.setter
    @abstractmethod
    def id(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def icon_path(self) -> str:
        '''Path to the mod icon from the root path, e.g src/desktop_overlay/mods/example/.../example.jpg'''
        pass

    @icon_path.setter
    @abstractmethod
    def icon_path(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        '''bool that shows if the mod is currently open '''
        #TODO: Check if the mod is open without storing the bool
        pass

    @is_open.setter
    @abstractmethod
    def is_open(self, value: bool) -> None:
        pass

    @property
    @abstractmethod
    def default_size(self) -> tuple[int, int]:
        '''Default size (width, height) for a mod window, once it's opened'''
        #TODO: Make it scale with the size of the screen
        pass

    @default_size.setter
    @abstractmethod
    def default_size(self, value: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def reset_state(self) -> None:
        pass

    @abstractmethod
    def remove_state(self) -> None:
        pass
