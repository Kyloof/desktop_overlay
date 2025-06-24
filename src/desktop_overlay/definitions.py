import os
import sys

if hasattr(sys, '_MEIPASS'):
    ROOT_DIR = os.path.join(sys._MEIPASS, 'desktop_overlay')
else:
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
