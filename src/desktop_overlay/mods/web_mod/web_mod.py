from desktop_overlay.core.base_mod import BaseMod
from desktop_overlay.definitions import ROOT_DIR

from PySide6.QtWidgets import QVBoxLayout, QFrame, QHBoxLayout, QPushButton, QLineEdit
from PySide6.QtWebEngineWidgets import QWebEngineView
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon


class WebMod(BaseMod):
    name = "Web Mod"
    description = "Enables web browser usage."
    is_open = False
    id = None
    icon_path = f"{ROOT_DIR}/mods/web_mod/assets/web_icon.png"
    default_size = (1000,600)

    def __init__(self, home_url=QUrl("https://www.google.com/")):
        super().__init__()
        self.home_url = home_url
        self.web_view = None
        self.main_layout = QVBoxLayout(self)
        self.load_state()

    def load_state(self):
        ### Web engine
        self.web_view = QWebEngineView(self)
        self.web_view.setUrl(self.home_url)

        self.navigation_frame = QFrame(self)
        self.navigation_frame.setContentsMargins(-7,-7,-7,-7)
        self.navigation_frame.setStyleSheet("""
            background-color: transparent;
        """)
        nav_f_hl = QHBoxLayout(self.navigation_frame)

        ### Go back button
        self.go_back = QPushButton(self.navigation_frame)
        self.go_back.setIcon(QIcon(f"{ROOT_DIR}/mods/web_mod/assets/go_back.png"))
        self.go_back.setStyleSheet("""
            background-color: #EDEDED;
        """)

        self.go_back.clicked.connect(self.web_view.back)
        nav_f_hl.addWidget(self.go_back)

        ### Go forward button
        self.go_next = QPushButton(self.navigation_frame)
        self.go_next.setIcon(QIcon(f"{ROOT_DIR}/mods/web_mod/assets/go_next.png"))
        self.go_next.setStyleSheet("""
            background-color: #EDEDED;
        """)

        self.go_next.clicked.connect(self.web_view.forward)
        nav_f_hl.addWidget(self.go_next)

        ### Refresh button
        self.refresh = QPushButton(self.navigation_frame)
        self.refresh.setIcon(QIcon(f"{ROOT_DIR}/mods/web_mod/assets/reload.png"))
        self.refresh.setStyleSheet("""
            background-color: #EDEDED;
        """)


        self.refresh.clicked.connect(self.web_view.reload)
        nav_f_hl.addWidget(self.refresh)
        
        ### Search bar
        self.search_bar = QLineEdit(self.navigation_frame)
        self.search_bar.returnPressed.connect(self._load_url)
        self.search_bar.setStyleSheet("""
            background-color: #EDEDED;
            border-radius: 10px;
            padding-top: 1px;
            padding-bottom: 1px;
            padding-left: 10px;
            padding-right: 10px;
            margin-left: 20px;
        """)
        self.search_bar.setPlaceholderText("Search here...")

        nav_f_hl.addWidget(self.search_bar)

        self.main_layout.addWidget(self.navigation_frame)
        self.main_layout.addWidget(self.web_view)

        self.main_layout.setStretch(1,1)
    
    def _load_url(self):
        text = self.search_bar.text().strip()
        if text.startswith("http://") or text.startswith("https://"):
            url = QUrl(text)
        else:
            url = QUrl(f"https://www.google.com/search?q={QUrl.toPercentEncoding(text).data().decode()}")
        
        self.web_view.load(url)
        self.search_bar.setText("")

    def remove_state(self):
        if self.web_view:
            self.main_layout.removeWidget(self.web_view)
            self.main_layout.removeWidget(self.navigation_frame)
            
            self.navigation_frame.deleteLater()
            self.web_view.deleteLater()
            
            self.navigation_frame = None
            self.web_view = None

    def reset_state(self):
        self.web_view.setUrl(self.home_url)

