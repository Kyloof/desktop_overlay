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
        self.mods: dict[bool, dict[int, BaseMod]] = {False: {}, True: {}}
        self.MODS_PATH = os.path.join(ROOT_DIR, "mods")

    def detect_mods(self) -> None:
        mod_id = 0
        '''Detect installed mod packages from the mod folder.'''
        for path in os.listdir(self.MODS_PATH):
            module_path = f"{self.MODS_PATH}/{path}"
            if os.path.isdir(module_path) and module_path.endswith("mod"):
                for file in os.listdir(module_path):
                    if file.endswith(".py") and not file.startswith("_"):
                        try:
                            module_file = f"desktop_overlay.mods.{file[:-3]}.{file[:-3]}"
                            module = importlib.import_module(module_file)
                            class_name = ("".join(list(map(lambda x: x.capitalize(), file[:-3].split("_")))))
                            self.mods[False][mod_id] = getattr(module, class_name)
                            mod_id += 1
                        except ModuleNotFoundError as e:
                            print(f"Failed to import module {file} from path: {e}")
        importlib.invalidate_caches()

        print(self.mods)

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
