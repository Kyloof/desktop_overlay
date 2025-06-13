from pynput import keyboard
import threading

class Hotkey_manager:
    def __init__(self, sequence: set, activation_function):
        self.activation_sequence = sequence
        self.activation_function = activation_function
        self.__current_sequence = set()

        listener_thread = threading.Thread(target=self.__start, daemon=True)
        listener_thread.start()

    def __start(self):
        with keyboard.Listener(
            on_press= self.__pressed,
            on_release= self.__release 
        ) as listener:
            listener.join()

    def __pressed(self, key):
        self.__current_sequence.add(key)
        if self.__current_sequence == self.activation_sequence:
            self.activation_function()

    def __release(self, key):
        self.__current_sequence.discard(key)
