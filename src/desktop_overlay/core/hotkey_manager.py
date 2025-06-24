'''
HotkeyManager - class to manage keyboard sequences to trigger the overlay.
It listens for key presses and checks if the current sequence matches the activation sequence.
'''

from PySide6.QtCore import QObject, QThread, Signal, QTimer
from pynput import keyboard

class HotkeyListenerThread(QThread):
    activated = Signal()
    changed = Signal(set)

    def __init__(self, activation_sequence):
        super().__init__()
        self.activation_sequence = activation_sequence
        self._current_sequence = set()
        #NOTE: _max_sequence is used for holding the key combo for changing the activation sequence
        self._max_sequence = set()
        self.listener = None
        self._change_sequence = False

    def run(self):
        with keyboard.Listener(
            on_press=self._pressed,
            on_release=self._released
        ) as self.listener:
            self.listener.join()

    def _pressed(self, key):
        ''' _pressed listens for:
                - If the activation sequence is clicked it signals activate.
                - Saves max_sequence which is used for changing shortcut.
        '''
        self._current_sequence.add(key)
        if self._change_sequence and len(self._current_sequence) > len(self._max_sequence):
            self._max_sequence = self._current_sequence.copy()
        if self._current_sequence == self.activation_sequence:
            self.activated.emit()

    def _released(self, key):
        ''' _released checks if max_sequence typing is finished, then signals changed. '''
        self._current_sequence.discard(key)
        if self._change_sequence and len(self._current_sequence) == 0 and len(self._max_sequence) > 0:
            self.changed.emit(self._max_sequence.copy())
            self._max_sequence.clear()

    def stop(self):
        ''' Stop the thread. '''
        self.terminate()
        if self.listener:
            self.listener.stop()

    def change_sequence(self):
        ''' Send a signal to the function that the sequence will be changed '''
        self._change_sequence = not self._change_sequence
        if self._change_sequence:
            self._max_sequence.clear()


class HotkeyManager(QObject):
    changed = Signal(str)

    def __init__(self, activation_function, sequence={keyboard.Key.ctrl_l, keyboard.KeyCode.from_char("0")}, parent=None):
        super().__init__(parent)
        self.activation_sequence = sequence
        self.activation_function = activation_function

        #NOTE: Timer is needed for actually allowing the user to input more than one keystroke, whenever activation_sequence is changed
        self.capture_timer = QTimer()
        self.capture_timer.timeout.connect(self._stop_hotkey_capture)
        self.capture_timer.setSingleShot(True)

        self.is_capturing = False

        self.listener_thread = HotkeyListenerThread(self.activation_sequence)
        self.listener_thread.activated.connect(self.activation_function)
        self.listener_thread.changed.connect(self.save_new_sequence)
        self.listener_thread.start()

    def save_new_sequence(self, new_sequence):
        '''Save new activation sequence.'''
        if len(new_sequence) > 0:
            self.activation_sequence = new_sequence
            self.listener_thread.activation_sequence = new_sequence
            if self.is_capturing:
                self._stop_hotkey_capture()
            self.changed.emit("+".join(str(s) for s in new_sequence))

    def change_activation_sequence(self):
        '''Start the hotkey capture process.'''
        if self.is_capturing:
            # If is already capturing
            return self.activation_sequence

        self.is_capturing = True
        self.listener_thread.change_sequence()
        self.capture_timer.start(3000)

        return self.activation_sequence

    def _stop_hotkey_capture(self):
        '''Stop hotkey capture'''
        if not self.is_capturing:
            return
        self.is_capturing = False
        if self.capture_timer.isActive():
            self.capture_timer.stop()

        self.listener_thread.change_sequence()

    def activation_sequence_to_string(self):
        return ("+".join(str(s) for s in self.activation_sequence))

    def stop(self):
        '''Stop the hotkey manager completely'''
        if self.is_capturing:
            self._stop_hotkey_capture()
        self.listener_thread.stop()
