from pynput import keyboard
import threading

class HotkeyManager:
    def __init__(self, sequence: set, activation_function):
        self.activation_sequence = sequence
        self.activation_function = activation_function
        self._current_sequence = set()

        listener_thread = threading.Thread(target=self._start, daemon=True)
        listener_thread.start()

    def _start(self):
        with keyboard.Listener(
            on_press = self._pressed,
            on_release = self._release 
        ) as listener:
            listener.join()

    def _pressed(self, key):
        self._current_sequence.add(key)
        if self._current_sequence == self.activation_sequence:
            self.activation_function()

    def _release(self, key):
        self._current_sequence.discard(key)
