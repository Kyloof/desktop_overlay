from typing import Type
import inspect
from desktop_overlay.core.base_mod import BaseMod
import os
import importlib
from desktop_overlay.definitions import ROOT_DIR

#TODO: typing, think about mod_id. is this the best way to do it?
#TODO: Also, it could be a great idea to get rid of the class and go more functional paradigm
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

    #TODO: I feel like this could've been nicer
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
                            for name, obj in inspect.getmembers(module):
                                if inspect.isclass(obj) and "Mod" in name:
                                    module_class = getattr(module, name)
                                    module_class.id = mod_id
                                    mod_id += 1
                                    self.mods[mod_id] = module_class 
                        except ModuleNotFoundError as e:
                            print(f"Failed to import module {file} from path: {e}")
        importlib.invalidate_caches()

    def enable_mod(self, mod_id: int) -> None:
        if mod_id in self.mods:
            mod = self.mods[mod_id]
            self.enabled_mods[mod_id] = mod()

    def enable_all(self) -> None:
        for id in self.mods.keys():
            self.enable_mod(id)

    def disable_mod(self, mod_id: int) -> None:
        if mod_id in self.enabled_mods:
            mod = self.enabled_mods.pop(mod_id)
            mod.remove_state()

    def disable_all(self) -> None:
        for id in self.mods.keys():
            self.disable_mod(id)

    def get_mods_info(self) -> list[tuple[str,str,str]]:
        info = []
        for mod in self.mods.values():
            info.append((mod.id, mod.name, mod.description))
        return info
