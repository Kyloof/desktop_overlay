import pytest
from unittest.mock import Mock, patch
from desktop_overlay.core.settings_manager import SettingsManager

@pytest.fixture
def mock_screens():
    screen1 = Mock()
    screen1.name.return_value = "Screen 1"
    screen1.geometry().x.return_value = 100
    screen1.geometry().y.return_value = 200

    screen2 = Mock()
    screen2.name.return_value = "Screen 2"
    screen2.geometry().x.return_value = 300
    screen2.geometry().y.return_value = 400

    return [screen1, screen2]

@pytest.fixture
def settings_manager():
    return SettingsManager(Mock())

def test_init(settings_manager):
    assert settings_manager.screens == []
    assert settings_manager.active_screen is None

def test_change_overlay_shortcut(settings_manager):
    settings_manager.change_overlay_shortcut()
    settings_manager.hotkey_manager.change_activation_sequence.assert_called_once()

def test_setup_screens(settings_manager, mock_screens):
    settings_manager.setup_screens(mock_screens, 0)
    assert settings_manager.active_screen == mock_screens[0]

def test_setup_screens_invalid_index(settings_manager, mock_screens):
    settings_manager.setup_screens(mock_screens, 10)
    assert settings_manager.active_screen is None

def test_list_screens(settings_manager, mock_screens):
    settings_manager.screens = mock_screens
    result = settings_manager.list_screens()
    assert result == [(0, mock_screens[0]), (1, mock_screens[1])]

def test_get_screens_strings(settings_manager, mock_screens):
    settings_manager.screens = mock_screens
    result = settings_manager.get_screens_strings()
    assert result == ["  0 - Screen 1", "  1 - Screen 2"]

def test_get_screen_geometry_success(settings_manager, mock_screens):
    settings_manager.active_screen = mock_screens[0]
    geometry, x, y = settings_manager._get_screen_geometry()
    assert x == 100 and y == 200

def test_get_screen_geometry_no_active_screen(settings_manager):
    with pytest.raises(RuntimeError, match="No active screen selected."):
        settings_manager._get_screen_geometry()
