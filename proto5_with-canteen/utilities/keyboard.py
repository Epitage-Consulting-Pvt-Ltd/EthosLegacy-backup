# TODO: Code cleanup and rename required
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QApplication, QDesktopWidget
from PyQt5.QtCore import Qt, QEvent, pyqtSignal
from PyQt5.QtGui import QGuiApplication, QFont
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QGridLayout, QApplication, QGroupBox, QLineEdit


class VirtualKeyboard(QWidget):
    keyClicked = pyqtSignal(str)
    enterClicked = pyqtSignal()

    def __init__(self):
    # def __init__(self, target: object, parent: object = None) -> object:
        super().__init__()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setAttribute(Qt.WA_AcceptTouchEvents)

        self.target = None
        self.uppercase = True
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout(self)
        # self.setLayout(layout)
      

        buttons = [
            '1', '2', '3', '4', '5', '6', '7', '8', '9', '0',
            'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
            'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
            'Z', 'X', 'C', 'V', 'B', 'N', 'M', '↼⇀', '⇐',
            '↵', '↥'
        ]

        grid_layout = QGridLayout()
        layout.addLayout(grid_layout)
        font = QFont()  # Create a QFont object
        font.setPointSize(16)  # Set the font size to 16 (change this to your desired size)

        for i, button_label in enumerate(buttons):
            row = i // 10
            col = i % 10
            button = QPushButton(button_label)
            button.setFixedSize(40, 40)
            if button_label == '↵':
                button.clicked.connect(self.handleEnterClicked)
            elif button_label == '↥':
                button.setObjectName('caseButton')
                button.clicked.connect(
                    lambda _, text=button_label: self.onButtonClick(text))
            else:
                button.clicked.connect(
                    lambda _, text=button_label: self.onButtonClick(text))
            grid_layout.addWidget(button, row, col)

    def handleEnterClicked(self):
        self.enterClicked.emit()
        self.close()

    def onButtonClick(self, text):
        if text == '↼⇀':
            if self.target:
                # self.target.setCurrentText(self.target.currentText() + ' ')
                self.target.setText(self.target.text() + ' ')
        elif text == '⇐':
            if self.target:
                # current_text = self.target.currentText()
                # self.target.setCurrentText(current_text[:-1])
                text = self.target.text()
                self.target.setText(text[:-1])
        elif text == '↥':
            self.uppercase = not self.uppercase
            self.updateButtons()  # Update all alphabet buttons
            self.updateCaseButton()  # Update the "Case" button text
        else:
            if self.target:
                if not self.uppercase:  # Check if lowercase mode is active
                    text = text.lower()  # Convert the text to lowercase if necessary
                # Set the text to the target QComboBox
                # self.target.setCurrentText(self.target.currentText() + text)
                self.target.setText(self.target.text() + text)
                self.keyClicked.emit(text)  # Emit the signal for the key clicked


    def updateButtons(self):
        # Get all buttons and update their labels according to uppercase/lowercase mode
        buttons = self.findChildren(QPushButton)
        for button in buttons:
            text = button.text()
            if text.isalpha():
                if self.uppercase:
                    button.setText(text.upper())
                else:
                    button.setText(text.lower())

    def updateCaseButton(self):
        case_button = self.findChild(QPushButton, 'caseButton')
        if case_button:
            case_button.setText('↥' if self.uppercase else '↧')

    def eventFilter(self, obj, event):
        if obj == self.target and event.type() == QEvent.MouseButtonPress:
            self.showVirtualKeyboard()
            return True
        return super().eventFilter(obj, event)
    
    def hide_virtual_keyboard(self):
        self.close()

    




