'''
ModListModel - custom model for the list of mods' icons on the dock
'''
    

from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QIcon
from typing import List
from desktop_overlay.core.base_mod import BaseMod

class ModListModel(QAbstractListModel): 
    
    def __init__(self, mods:List[BaseMod] = [], parent = None):
        QAbstractListModel.__init__(self, parent)
        self._mods = mods

    def rowCount(self, parent):
        '''Tells the list how many items to display'''
        return len(self._mods)
    
    def data(self, index, role):
        '''Tells the list how to style the items'''
        if not index.isValid() or not (0 <= index.row() < len(self._mods)):
            return None

        mod = self._mods[index.row()]

        if role == Qt.DecorationRole:
            return QIcon(mod.icon_path)
        elif role == Qt.ToolTipRole:
            return mod.name
        elif role == Qt.DisplayRole:
            ### If time allow, fix this (Time didn't allow XD)
            return "   "

        
