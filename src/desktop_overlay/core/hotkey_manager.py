'''
HotkeyMenager - class to manage keyboard sequences to trigger the overlay.
It listens for key presses and checks if the current sequence matches the activation sequence.
'''

from PySide6.QtCore import QObject, QThread, Signal, QTimer
from pynput import keyboard

class HotkeyListenerThread(QThread):
    activated = Signal()
    changed = Signal(set)

    def __init__(self, activation_sequence, change_sequence: bool = False):
        super().__init__()
        self.activation_sequence = activation_sequence
        self._current_sequence = set()
        self.listener = None
        self._change_sequence = change_sequence

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
        if self._change_sequence == True:
            self.changed.emit(self._current_sequence.copy())

    def _released(self, key):
        self._current_sequence.discard(key)

    def stop(self):
        self.terminate()
        if self.listener:
            self.listener.stop()

    def change_sequence(self):
        self._change_sequence = not self._change_sequence 


class HotkeyManager(QObject):
    changed = Signal(str)

    def __init__(self, activation_function, sequence: set = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char("0")}, parent=None):
        super().__init__(parent)
        self.activation_sequence = sequence
        self.activation_function = activation_function

        self.listener_thread = HotkeyListenerThread(self.activation_sequence)
        self.listener_thread.activated.connect(self.activation_function)
        self.listener_thread.changed.connect(self._save_new_sequence)
        self.listener_thread.start()

    def _save_new_sequence(self, new_sequence: set):
        print(new_sequence)
        self.activation_sequence = new_sequence
        self.listener_thread.activation_sequence = new_sequence
        self.listener_thread.change_sequence()
        self.changed.emit("+".join(str(s) for s in new_sequence))

    def change_activation_sequence(self):
        self.listener_thread.change_sequence()
        return self.activation_sequence

    def stop(self):
        self.listener_thread.stop()

