from PySide6.QtCore import QUrl
from desktop_overlay.core.base_mod import BaseMod
from ._web_ui import create_ui

class WebMod(BaseMod):
    def __init__(self):
        super().__init__()
        self.ui = None

    def load(self, url=QUrl("https://www.google.com/")):
        self.ui = create_ui(url)

    def unload(self):
        self.ui = None
    
    def run(self):
        pass

    def stop(self):
        pass

    def resume(self):
        pass
        

'''
    @abstractmethod
    dl ef load(self):
          pass

      @abstractmethod
      def unload(self):
          pass

      @abstractmethod
      def run(self):
          pass

      @abstractmethod
      def stop(self):
          pass

      @abstractmethod
      def resume(self):
          pass'''
