# TODO: Code not required, need to remove
import sys
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QGridLayout, QPushButton, QLineEdit

import os
os.environ['QT_QPA_PLATFORM'] = 'eglfs'

class CalculatorApp(QWidget):
    def _init_(self):
        super()._init_()

        self.setWindowTitle("Basic Calculator")
        self.setGeometry(100, 100, 800, 480)

        self.init_ui()

    def init_ui(self):
        # Create a layout for the main window
        main_layout = QVBoxLayout()

        # Create a line edit for displaying input and results
        self.display = QLineEdit(self)
        self.display.setFixedHeight(80)
        self.display.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.display)

        # Create buttons for numbers and operators
        buttons_layout = QGridLayout()
        buttons = [
            '7', '8', '9', '/',
            '4', '5', '6', '*',
            '1', '2', '3', '-',
            '0', '.', '=', '+'
        ]

        # Define the layout of the buttons
        row, col = 0, 0
        for button_text in buttons:
            button = QPushButton(button_text, self)
            button.clicked.connect(self.button_clicked)
            buttons_layout.addWidget(button, row, col, 1, 1)
            col += 1
            if col > 3:
                col = 0
                row += 1

        # Create layout for the number and operator buttons
        main_layout.addLayout(buttons_layout)

        # Set the main layout for the widget
        self.setLayout(main_layout)

    def button_clicked(self):
        clicked_button = self.sender()
        current_text = self.display.text()

        if clicked_button.text() == '=':
            try:
                result = eval(current_text)
                self.display.setText(str(result))
            except Exception as e:
                self.display.setText("Error")
        else:
            new_text = current_text + clicked_button.text()
            self.display.setText(new_text)

if _name_ == '_main_':
    app = QApplication(sys.argv)
    calc_app = CalculatorApp()
    calc_app.show()
    sys.exit(app.exec_())