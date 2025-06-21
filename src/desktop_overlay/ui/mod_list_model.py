from PySide6.QtCore import QAbstractListModel, Qt
from PySide6.QtGui import QIcon
from typing import List
from desktop_overlay.core.base_mod import BaseMod

class ModListModel(QAbstractListModel): 
    
    def __init__(self, mods:List[BaseMod] = [], parent = None):
        QAbstractListModel.__init__(self, parent)
        self._mods = mods

    def rowCount(self, parent):
        return len(self._mods)
    
    def data(self, index, role):
        if not index.isValid() or not (0 <= index.row() < len(self._mods)):
            return None

        mod = self._mods[index.row()]

        if role == Qt.DecorationRole:
            return QIcon(mod.icon_path)
        elif role == Qt.ToolTipRole:
            return mod.name
        elif role == Qt.DisplayRole:
            ### If time allow, fix this 
            return "   "

        
