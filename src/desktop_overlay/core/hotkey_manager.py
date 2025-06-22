'''
HotkeyMenager - class to manage keyboard sequences to trigger the overlay.
It listens for key presses and checks if the current sequence matches the activation sequence.
'''

from PySide6.QtCore import QObject, QThread, Signal
from pynput import keyboard

class HotkeyListenerThread(QThread):
    activated = Signal()

    def __init__(self, activation_sequence):
        super().__init__()
        self.activation_sequence = activation_sequence
        self._current_sequence = set()
        self.listener = None

    def run(self):
        with keyboard.Listener(
            on_press=self._pressed,
            on_release=self._released
        ) as self.listener:
            self.listener.join()

    def _pressed(self, key):
        self._current_sequence.add(key)
        if self._current_sequence == self.activation_sequence:
            self.activated.emit()

    def _released(self, key):
        self._current_sequence.discard(key)

    def stop(self):
        self.terminate()
        if self.listener:
            self.listener.stop()


class HotkeyManager(QObject):
    def __init__(self, activation_function, sequence: set = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char("0")}, parent=None):
        super().__init__(parent)
        self.activation_sequence = sequence
        self.activation_function = activation_function

        self.listener_thread = HotkeyListenerThread(self.activation_sequence)
        self.listener_thread.activated.connect(self.activation_function)
        self.listener_thread.start()

    def change_activation_sequence(self, new_sequence: set):
        pass

    def stop(self):
        self.listener_thread.stop()

