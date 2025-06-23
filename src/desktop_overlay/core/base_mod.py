from abc import ABC, ABCMeta, abstractmethod
from PySide6.QtWidgets import QWidget

QWidgetMeta = type(QWidget)


class _BaseModMeta(ABCMeta, QWidgetMeta):
    '''
    Create meta that connects ABCMeta and QWidgetMeta here cuz python
    '''
    pass


class BaseMod(ABC, QWidget, metaclass=_BaseModMeta):
    '''
    Abstract class for all mods that are yet to come
    '''

    @property
    @abstractmethod
    def id(self) -> int:
        '''Mod id - assigned automatically, don't worry about it'''
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        '''Mod name.'''
        pass

    @property
    @abstractmethod
    def description(self) -> str:
        '''Mod description.'''
        pass

    @property
    @abstractmethod
    def icon_path(self) -> str:
        '''path to the mod icon'''
        pass

    @property
    @abstractmethod
    def is_open(self) -> bool:
        '''flag if the mod i currently open'''
        pass

    @property
    @abstractmethod
    def default_size(self) -> tuple[int, int]:
        '''A tuple that takes default (width, height) for a mod window'''
        pass

    @abstractmethod
    def reset_state(self) -> None:
        '''Reset the state of the widget'''
        pass
    
    @abstractmethod
    def remove_state(self) -> None:
        '''Remove the state of the widget'''
        pass
