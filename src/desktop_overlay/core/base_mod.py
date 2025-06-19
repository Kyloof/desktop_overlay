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

    @abstractmethod
    def load(self) -> None:
        '''
        Load the mod into the overlay, but dont run it just yet..
        Should preferably get it's own thread???
        '''
        pass

    @abstractmethod
    def unload(self) -> None:
        '''Unload the mod from the overlay'''
        pass

    @abstractmethod
    def run(self) -> None:
        '''Finally, run the mod:DD'''
        pass

    @abstractmethod
    def stop(self) -> None:
        '''
        Stop the mod, f.e when the overlay is minimalized
        Put the thread to sleep i think
        '''
        pass

    @abstractmethod
    def resume(self) -> None:
        '''
        Resume the mod, f.e when the overlay is maximized, and you had it opened previously
        Wake up the thread
        '''
        pass

    #TODO: SETTINGS
    '''
    @abstractmethod
    def settings(self):
        
        Mod settings
        For now TODO
        
        pass
    '''
