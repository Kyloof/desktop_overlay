from .base_mod import BaseMod
import os
import importlib
from ..definitions import ROOT_DIR

class ModManager:
    '''
    ModManager - middleman between the user and the mods

    Mod Manager detects and loads BaseMod subclasses from your mod packages and, if they're not fucked up, 
    after refreshing mods, should display them in installed mods section in UI. 
    There you can enable or disable them which would invoke the load or unload mod function in ModManager.
    '''
    def __init__(self):
        #NOTE: mods[False] -> disabled mods, mods[True] -> enabled mods
        self.mods: dict[bool, dict[int, BaseMod]] = {}
        self.MODS_PATH = os.path.join(ROOT_DIR, "mods")

    def detect_mods(self) -> None:
        '''Detect installed mod packages from the mod folder.'''
        for path in os.listdir(self.MODS_PATH):
            module_path = f"{self.MODS_PATH}/{path}"
            if os.path.isdir(module_path) and module_path.endswith("mod"):
                for file in os.listdir(module_path):
                    if file.endswith(".py") and not file.startswith("_"):
                        module_file = f"{module_path}/{file}"
                        print(module_file)
                        module = importlib.import_module(module_file)

    def load_mod(self, mod_id: int):
        '''Load the mod:D'''
        if mod_id in self.mods[False]:
            module = self.mods[False].pop(mod_id)
            module.load()
            self.mods[True][mod_id] = module

    def unload_moad(self, mod_id: int):
        '''Unload the mod:c'''
        if mod_id in self.mods[True]:
            module = self.mods[True].pop(mod_id)
            module.unload()
            self.mods[False][mod_id] = module

mm = ModManager()
mm.detect_mods()
