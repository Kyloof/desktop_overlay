import pytest
from unittest.mock import Mock
from desktop_overlay.core.hotkey_manager import HotkeyManager

@pytest.fixture
def hotkey_manager():
    return HotkeyManager(Mock())

def test_save_new_sequence(hotkey_manager):
    new_seq = {Mock(), Mock()}
    hotkey_manager._save_new_sequence(new_seq)
    assert hotkey_manager.activation_sequence == new_seq

def test_change_activation_sequence(hotkey_manager):
    result = hotkey_manager.change_activation_sequence()
    assert hotkey_manager.is_capturing
    assert result == hotkey_manager.activation_sequence
