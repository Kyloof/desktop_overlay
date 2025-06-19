from typing import Type
from .base_mod import BaseMod
import os
import types
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
        self.mods: dict[int, Type[BaseMod]] = {}
        self.enabled_mods: dict[int, BaseMod] = {}

        self.MODS_PATH = os.path.join(ROOT_DIR, "mods")

    def detect_mods(self) -> None:
        '''Detect installed mod packages from the mod folder.'''
        mod_id = 0
        for path in os.listdir(self.MODS_PATH):
            module_path = f"{self.MODS_PATH}/{path}"
            if os.path.isdir(module_path) and module_path.endswith("mod"):
                for file in os.listdir(module_path):
                    if file.endswith(".py") and not file.startswith("_"):
                        try:
                            module_file = f"desktop_overlay.mods.{file[:-3]}.{file[:-3]}"
                            module = importlib.import_module(module_file)

                            class_name = ("".join(list(map(lambda x: x.capitalize(), file[:-3].split("_")))))
                            module_class = getattr(module, class_name)
                            module_class.id = mod_id
                            mod_id += 1

                            self.mods[mod_id] = module_class 

                        except ModuleNotFoundError as e:
                            print(f"Failed to import module {file} from path: {e}")
        importlib.invalidate_caches()

    def enable_mod(self, mod_id: int):
        '''Enable the mod'''
        if mod_id in self.mods:
            mod = self.mods[mod_id]
            self.enabled_mods[mod_id] = mod()

    def disable_mod(self, mod_id: int):
        '''Disable the mod'''
        if mod_id in self.enabled_mods:
            mod = self.enabled_mods.pop(mod_id)
            mod.unload()

    def load_mod(self, mod_id: int):
        '''Load the mod:D'''
        if mod_id in self.enabled_mods:
            module = self.enabled_mods[mod_id]
            module.load()
    
    def get_mods_info(self):
        info = []
        for mod in self.mods.values():
            info.append((mod.id, mod.name, mod.description))
        return info

mm = ModManager()
mm.detect_mods()
print(mm.get_mods_info())
