from .base_mod import BaseMod
import os
import importlib


class ModManager:
    '''
    The Mod Manager. 
    Mod Manager detects and loads BaseMod subclasses from your mod packages and, if they're not fucked up, 
    after refreshing mods, should display them in installed mods section in UI. 
    There you can enable or disable them which would invoke the load or unload mod function in ModManager.
    '''
    def __init__(self):
        #NOTE: mods[False] -> disabled mods, mods[True] -> enabled mods
        self.mods: dict[bool, dict[int, BaseMod]] = {}
        self.BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        self.MODS_PATH = os.path.abspath(os.path.join(self.BASE_DIR, '..', 'mods'))

    def detect_mods(self) -> None:
        '''
        Detect installed mod packages from the mod folder.
        '''
        mod_id = 0
        for path in os.listdir(self.MODS_PATH):
            mod_path = os.path.join(self.MODS_PATH, path)
            if os.path.isdir(mod_path) and mod_path.endswith("mod"):
                try:
                    module = importlib.import_module(path)
                except ModuleNotFoundError as e:
                    print(f"failed to import {path}: {e}")
                    continue
            #TODO:detect subclasses of BaseMod from a module and save them into the mods dictionary

    def load_mod(self, mod_id: int):
        '''
        Load the mod and make it work:D
        '''
        if mod_id in self.mods[False]:
            module = self.mods[False].pop(mod_id)
            module.load()
            self.mods[True][mod_id] = module

    def unload_moad(self, mod_id: int):
        '''
        Unload the mod and stop the mod:c
        '''
        if mod_id in self.mods[True]:
            module = self.mods[True].pop(mod_id)
            module.unload()
            self.mods[False][mod_id] = module

