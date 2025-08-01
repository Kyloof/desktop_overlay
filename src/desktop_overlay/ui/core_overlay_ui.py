'''
UiOverlay - class with GUI of the overlay
'''
from desktop_overlay.definitions import ROOT_DIR

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import (QFrame, QHBoxLayout, QLabel,
    QListView, QMainWindow, QMdiArea, 
    QPushButton, QSizePolicy, QSpacerItem, 
    QVBoxLayout, QWidget, QGraphicsDropShadowEffect, QTextBrowser)
from PySide6.QtWidgets import QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QColor, QBrush, QIcon, QPixmap
from desktop_overlay.ui.themes import style_navigation_buttons
from PySide6.QtWidgets import QComboBox

class UiOverlay(object):
    def set_up_ui(self, MainWindow: QMainWindow):
        
        MainWindow.setWindowFlags(
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.X11BypassWindowManagerHint
        )
        MainWindow.setAttribute(Qt.WA_TranslucentBackground)
        MainWindow.setStyleSheet("background-color: rgba(23, 23, 23, 150);")


        self.central_widget = QWidget()
        ### I don't know why but to make it stick to the window sides it has to be set to -9
        self.central_widget.setContentsMargins(-9,-9,-9,-9)
        MainWindow.setCentralWidget(self.central_widget)
        self.main_horizontal = QHBoxLayout(self.central_widget)

        self._set_up_settings_menu()
        self._set_up_main_panel()


    def _set_up_settings_menu(self):
        '''
        Setting up the settings menu which is to the left of the screen
        '''

        self.settings_menu = QFrame(self.central_widget)
        self.settings_menu.setMinimumSize(400,0)
        self.settings_menu.setStyleSheet("""
            background-color: #141414;
            border-top-right-radius: 20px;
            border-bottom-right-radius: 20px;
            border-top-left-radius: 0px;
            border-bottom-left-radius: 0px;
                                         
            padding-top: 7px;
        """)
        self.settings_menu.setFrameShape(QFrame.Shape.StyledPanel)
        self.settings_menu_vl = QVBoxLayout(self.settings_menu)
        self.settings_label = QLabel(self.settings_menu)
        self.settings_label.setText("Settings")
        self.settings_label.setStyleSheet("font: 24px;")
        self.settings_label.setAlignment(Qt.AlignHCenter)

        self.settings_menu_vl.addWidget(self.settings_label)
        
        ### Frame for the shortcut edit
        tmp_set_frame = QFrame(self.settings_menu)
        tmp_set_frame.setFixedHeight(125)
        tmp_set_frame.setFrameShape(QFrame.Shape.StyledPanel)
        
        tmp_set_frame.setStyleSheet("""
            background-color: #5e5e5e;
            border-radius: 20px;
            margin-top: 32px;
            margin-left: 20px;
            margin-right: 20px;
            padding:0px;
        """)
        
        tmp_set_hl = QHBoxLayout(tmp_set_frame)
        tmp_set_hl.setContentsMargins(20, 20, 20, 20)
        tmp_set_hl.setSpacing(16)

        hotkey_lab = QLabel(tmp_set_frame)
        hotkey_lab.setMaximumHeight(50)
        hotkey_lab.setText("Overlay shortcut")
        hotkey_lab.setStyleSheet("""
            color: #fafafa;
            font-size: 20px;
            font-weight: 500;
            margin:0px;
        """)

        tmp_set_hl.addWidget(hotkey_lab, stretch=1)

        ### Short cut is displayed here
        self.saved_shortcut = QTextBrowser(tmp_set_frame)
        self.saved_shortcut.setMaximumHeight(40)
        self.saved_shortcut.setFixedWidth(170)
        self.saved_shortcut.setText("Ctrl + 0")
        self.saved_shortcut.setStyleSheet("""
            background: #232323;
            color: #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            padding: 6px 12px;
            margin:0px
        """)

        tmp_set_hl.addWidget(self.saved_shortcut)

        ### This button initializes the short cut change (for more info see HotKeyManager) 
        self.edit_shortcut = QPushButton(tmp_set_frame)
        self.edit_shortcut.setText('Edit')
        self.edit_shortcut.setStyleSheet("""
            QPushButton {
            background-color: #2d8cf0;
            color: #fff;
            border: none;
            border-radius: 6px;
            padding: 8px 18px;
            font-size: 16px;
            margin:0px;
            }
            QPushButton:hover {
            background-color: #1a73e8;
            }
        """)

        tmp_set_hl.addWidget(self.edit_shortcut)
        
        self.settings_menu_vl.addWidget(tmp_set_frame)

        
        ### Frame for choosing the display
        tmp_set_frame1 = QFrame(self.settings_menu)
        tmp_set_frame1.setFixedHeight(125)
        tmp_set_frame1.setFrameShape(QFrame.Shape.StyledPanel)
        
        tmp_set_frame1.setStyleSheet("""
            background-color: #5e5e5e;
            border-radius: 20px;
            margin-top: 32px;
            margin-left: 20px;
            margin-right: 20px;
            padding:0px;
        """)
        
        tmp_set_hl1 = QHBoxLayout(tmp_set_frame1)
        tmp_set_hl1.setContentsMargins(20, 20, 20, 20)
        tmp_set_hl1.setSpacing(16)

        display_lab = QLabel(tmp_set_frame1)
        display_lab.setMaximumHeight(50)
        display_lab.setText("Display selection")
        display_lab.setStyleSheet("""
            color: #fafafa;
            font-size: 20px;
            font-weight: 500;
            margin:0px;
        """)

        tmp_set_hl1.addWidget(display_lab)

        ### Here you choose (José) the display 
        self.display_selector = QComboBox(tmp_set_frame1)
        self.display_selector.setFixedHeight(40)
        self.display_selector.setStyleSheet("""
            background: #232323;
            color: #e0e0e0;
            border-radius: 10px;
            font-size: 16px;
            font-weight: 600;
            padding: 6px;
            margin:0px
        """)
        

        tmp_set_hl1.addWidget(self.display_selector)

        self.settings_menu_vl.addWidget(tmp_set_frame1)

        ### Making it stink to the top
        self.settings_menu_vertical_spacer = QSpacerItem(20, 40, QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Expanding)

        self.settings_menu_vl.addItem(self.settings_menu_vertical_spacer)

        self.settings_menu.hide()

        self.main_horizontal.addWidget(self.settings_menu)

    def _set_up_main_panel(self):
        '''
        The Main meat of the UI
        Consists of 
            the top bar (settings and close buttons)
            the MDIArea in the middle
            the mod dock on the bottom
        '''
        self.main_panel = QFrame(self.central_widget)
        self.main_panel.setStyleSheet("background-color: transparent;")

        self.panel_v_layout = QVBoxLayout(self.main_panel)
        self.panel_v_layout.setContentsMargins(20,20,20,20)
        
        self._set_up_top_bar()

        ### This is where the mods' windows are displayed  
        self.mod_windows_area = QMdiArea(self.main_panel)
        transparent_brush = QBrush(QColor(0, 0, 0, 0))
        self.mod_windows_area.setBackground(transparent_brush)

        self.panel_v_layout.addWidget(self.mod_windows_area)

        self._set_up_bottom_bar()

        ### Streches the MDIArea
        self.panel_v_layout.setStretch(1, 1)

        self.main_horizontal.addWidget(self.main_panel)

    def _set_up_top_bar(self):
        '''
        The top bar of the main panel
        Settings and close buttons
        '''
        self.top_bar = QFrame(self.main_panel)
        self.top_h_layout = QHBoxLayout(self.top_bar)

        self.settings_button = QPushButton(self.top_bar)
        style_navigation_buttons(self.settings_button, 72, f"{ROOT_DIR}/ui/assets/overlay_settings.png")
        self.top_h_layout.addWidget(self.settings_button)

        self.center_spacer_top = QSpacerItem(20, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.top_h_layout.addItem(self.center_spacer_top)

        self.exit_button = QPushButton(self.top_bar)
        style_navigation_buttons(self.exit_button, 68, f"{ROOT_DIR}/ui/assets/overlay_close.png")
        
        self.top_h_layout.addWidget(self.exit_button)

        self.panel_v_layout.addWidget(self.top_bar)

    def _set_up_bottom_bar(self):
        '''
        The Bottom of the main panel
        The mods' dock  
        '''
        
        ### Frame for the bottom bar
        self.bottom_bar = QFrame(self.main_panel)
        self.bottom_horizontal_layout = QHBoxLayout(self.bottom_bar)
        
        ### Spacers to make it centered 
        self.left_spacer_bottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bottom_horizontal_layout.addItem(self.left_spacer_bottom)

        ###Fram for the mods' dock
        self.mod_dock = QFrame(self.bottom_bar)

        self.mod_dock.setMinimumSize(QSize(80, 70))
        self.mod_dock.setMaximumSize(QSize(900, 70))

        self.mod_dock.setStyleSheet("""
            background-color: rgba(128, 128, 128, 220);
            border-radius: 20px;
        """)
        self.mod_dock.setFrameShadow(QFrame.Shadow.Raised)
        
        self.dock_horizontal_layout = QHBoxLayout(self.mod_dock)
        self.dock_horizontal_layout.setContentsMargins(20,10,20,10)
        
        ### List for the mods' icons
        self.mod_list = QListView(self.mod_dock)
        self.mod_list.setStyleSheet("""
            background-color: transparent;                        
        """)
        self.mod_list.setFlow(QListView.Flow.LeftToRight)
        self.mod_list.setWrapping(True)
        self.mod_list.setIconSize(QSize(48,48))

        self.dock_horizontal_layout.addWidget(self.mod_list)

        self.bottom_horizontal_layout.addWidget(self.mod_dock)

        self.right_spacer_bottom = QSpacerItem(40, 20, QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Minimum)
        self.bottom_horizontal_layout.addItem(self.right_spacer_bottom)
        
        self.bottom_horizontal_layout.setStretch(1,1)
        
        self.panel_v_layout.addWidget(self.bottom_bar)

   
