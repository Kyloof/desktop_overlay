from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QWidget

QWidgetMeta = type(QWidget)


class _BaseModMeta(ABCMeta, QWidgetMeta):
    '''Create meta that connects ABCMeta and QWidgetMeta here, to merge them into one Metaclass'''
    pass

class BaseMod(ABC, QWidget, metaclass=_BaseModMeta):
    '''Abstract class for all mods that are yet to come'''

    @property
    @abstractmethod
    def id(self) -> int:
        '''Mod id'''
        pass

    @id.setter
    @abstractmethod
    def id(self, value: int) -> None:
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        '''Mod name.'''
        pass

    @name.setter
    @abstractmethod
    def name(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        '''Mod description.'''
        pass

    @description.setter
    @abstractmethod
    def description(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def icon_path(self) -> str:
        '''Path to the mod icon'''
        pass

    @icon_path.setter
    @abstractmethod
    def icon_path(self, value: str) -> None:
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        '''Flag if the mod is currently open'''
        pass

    @is_open.setter
    @abstractmethod
    def is_open(self, value: bool) -> None:
        pass

    @property
    @abstractmethod
    def default_size(self) -> tuple[int, int]:
        '''A tuple that takes default (width, height) for a mod window'''
        pass

    @default_size.setter
    @abstractmethod
    def default_size(self, value: tuple[int, int]) -> None:
        pass

    @abstractmethod
    def reset_state(self) -> None:
        '''Reset the state of the widget'''
        pass

    @abstractmethod
    def remove_state(self) -> None:
        '''Remove the state of the widget (It's use case is on the app exit)'''
        pass
