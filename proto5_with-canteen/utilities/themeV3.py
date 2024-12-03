from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPalette, QColor

# Define theme variables
BACKGROUND_COLOR = QColor('#ffffff')  # white
FOREGROUND_COLOR = QColor('#000000')  # white
ACCENT_COLOR = QColor('#FF4A18')  # orange

BUTTON_STYLE = f"""
    QPushButton {{
        background-color: #FF4A18;
        self: #ffffff;
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: #ff8c00;
    }}
"""
TRANSPARENT_BUTTON = f"""
    QPushButton {{
        background-color: transparent;
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: #ff8c00;
    }}
"""
TABLE_STYLE = f"""
    QTableWidget {{
        background-color: {BACKGROUND_COLOR};
        self: {FOREGROUND_COLOR};
        border-radius: 5px;
    }}
    QHeaderView::section {{
        background-color: #2c3e50;
        self: {FOREGROUND_COLOR};
        font-weight: bold;
    }}
    QTableCornerButton::section {{
        background-color: #2c3e50;
        border: none;
    }}
"""
# Set window background and foreground colors
WINDOW_BACKGROUND_COLOR = Qt.white  # gray
WINDOW_FOREGROUND_COLOR = Qt.white
RFID_WINDOW_FOREGROUND_COLOR = Qt.black

yellow_state ='background-color: yellow; border: 2px solid black; border-radius: 5px; font-size: 14px;'
green_state = 'background-color: red;border: 2px solid black; self: white; font-size: 12px; border-radius: 5px;'

FP_BUTTON_STYLE = f"""
    QPushButton {{
        background-color: {ACCENT_COLOR};
        self: {FOREGROUND_COLOR};
        border-radius: 5px;
    }}
    QPushButton:hover {{
        background-color: #ff8c00;
    }}
"""


EpitageLabel = f"""
    Qlabel {{
    font-size: 20px; 
    font-weight: light;   
            }}
    QPushButton:hover {{
        background-color: #ff8c00;
    }}
"""