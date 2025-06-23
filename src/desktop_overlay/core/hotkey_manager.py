'''
HotkeyManager - class to manage keyboard sequences to trigger the overlay.
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
        self._max_sequence = set()         
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
        if self._change_sequence and len(self._current_sequence) > len(self._max_sequence):
            self._max_sequence = self._current_sequence.copy()
        if self._current_sequence == self.activation_sequence:
            self.activated.emit()

    def _released(self, key):
        self._current_sequence.discard(key)
        if self._change_sequence and len(self._current_sequence) == 0 and len(self._max_sequence) > 0:
            self.changed.emit(self._max_sequence.copy())
            self._max_sequence.clear()

    def stop(self):
        self.terminate()
        if self.listener:
            self.listener.stop()

    def change_sequence(self):
        self._change_sequence = not self._change_sequence
        if self._change_sequence:
            self._max_sequence.clear()


class HotkeyManager(QObject):
    changed = Signal(str)
    capture_started = Signal()
    capture_finished = Signal()

    def __init__(self, activation_function, sequence: set = {keyboard.Key.ctrl_l, keyboard.KeyCode.from_char("0")}, parent=None):
        super().__init__(parent)
        self.activation_sequence = sequence
        self.activation_function = activation_function

        self.capture_timer = QTimer()
        self.capture_timer.timeout.connect(self._stop_hotkey_capture)
        self.capture_timer.setSingleShot(True)

        self.is_capturing = False

        self.listener_thread = HotkeyListenerThread(self.activation_sequence)
        self.listener_thread.activated.connect(self.activation_function)
        self.listener_thread.changed.connect(self._save_new_sequence)
        self.listener_thread.start()

    def _save_new_sequence(self, new_sequence: set):
        if len(new_sequence) > 0:
            self.activation_sequence = new_sequence
            self.listener_thread.activation_sequence = new_sequence

            if self.is_capturing:
                self._stop_hotkey_capture()
            
            self.changed.emit("+".join(str(s) for s in new_sequence))

    def change_activation_sequence(self):
        '''Start the hotkey capture process'''
        if self.is_capturing:
            return self.activation_sequence

        self.is_capturing = True
        self.listener_thread.change_sequence()
        self.capture_timer.start(3000)

        self.capture_started.emit()
        
        return self.activation_sequence

    def _stop_hotkey_capture(self):
        '''Stop hotkey capture'''
        if not self.is_capturing:
            return
        self.is_capturing = False
        if self.capture_timer.isActive():
            self.capture_timer.stop()

        self.listener_thread.change_sequence()
        self.capture_finished.emit()

    def stop(self):
        '''Stop the hotkey manager completely'''
        if self.is_capturing:
            self._stop_hotkey_capture()
        self.listener_thread.stop()
