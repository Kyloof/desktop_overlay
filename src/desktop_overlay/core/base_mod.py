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

    @abstractmethod
    def load(self):
        '''
        Load the mod into the overlay, but dont run it just yet..
        Should preferably get it's own thread???
        '''
        pass

    @abstractmethod
    def unload(self):
        '''
        Unload the mod from the overlay
        '''
        pass

    @abstractmethod
    def run(self):
        '''
        Finally, run the mod:DD
        Or maybe assign thread here more likely
        '''
        pass

    @abstractmethod
    def stop(self):
        '''
        Stop the mod, f.e when the overlay is minimalized
        Put the thread to sleep i think
        '''
        pass

    @abstractmethod
    def resume(self):
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
