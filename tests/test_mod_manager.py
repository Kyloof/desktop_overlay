import shutil
import tempfile
from unittest.mock import Mock, patch
import pytest
from desktop_overlay.core.mod_manager import ModManager
from desktop_overlay.core.base_mod import BaseMod

@pytest.fixture
def mod_manager():
    manager = ModManager()
    manager.MODS_PATH = tempfile.mkdtemp()
    yield manager
    shutil.rmtree(manager.MODS_PATH)

@pytest.fixture
def mock_mod():
    cls = Mock(spec=BaseMod)
    cls.__name__ = "TestMod"
    cls.id = 1
    cls.name = "Test Mod"
    cls.description = "A test mod"
    return cls

def test_detect_mods_no_mods(mod_manager):
    with patch("os.listdir", return_value=[]):
        mod_manager.detect_mods()
    assert mod_manager.mods == {}

def test_enable_mod_success(mod_manager, mock_mod):
    mod_manager.mods[1] = mock_mod
    mod_manager.enable_mod(1)
    mock_mod.assert_called_once()
    assert 1 in mod_manager.enabled_mods

def test_disable_mod_success(mod_manager):
    mock_instance = Mock()
    mod_manager.enabled_mods[1] = mock_instance
    mod_manager.disable_mod(1)
    mock_instance.remove_state.assert_called_once()
    assert 1 not in mod_manager.enabled_mods


class Mod:
    def __init__(self, id, name, description):
        self.id = id
        self.name = name
        self.description = description

def test_get_mods_info(mod_manager):
    mod1 = Mod(1, "Mod1", "Desc1")
    mod2 = Mod(2, "Mod2", "Desc2")
    mod_manager.mods = {1: mod1, 2: mod2}
    info = mod_manager.get_mods_info()
    assert info == [(1, "Mod1", "Desc1"), (2, "Mod2", "Desc2")]

