from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import Qt, QTimer, QDateTime

class VirtualKeyboard(QtWidgets.QDialog):
    def __init__(self, target, parent=None):
        super().__init__(parent)
        self.target = target

        self.setWindowTitle("Virtual Keyboard")
        self.setGeometry(0, 550, 300, 200)
        self.setWindowFlag(Qt.FramelessWindowHint)

        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

        self.text_edit = QtWidgets.QTextEdit()
        layout.addWidget(self.text_edit)

        #TODO small case to be added.
        #TODO text edits should be same for both windows.

        button_wrapper_layout = QtWidgets.QVBoxLayout()  # Added wrapper layout
        layout.addLayout(button_wrapper_layout)  # Added wrapper layout to main layout

        buttons = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L"],
            ["Z", "X", "C", "V", "B", "N", "M", "<-"],
            ["Enter"]  # Added row with "Enter" button
        ]

        for row_buttons in buttons:
            button_layout = QtWidgets.QHBoxLayout()
            button_wrapper_layout.addLayout(button_layout)

            for button_text in row_buttons:
                button = QtWidgets.QPushButton(button_text)
                button.setFixedSize(40, 30)
                button.clicked.connect(self.button_clicked)
                button_layout.addWidget(button)

    def button_clicked(self):
        button = self.sender()
        if button:
            button_text = button.text()
            if button_text == "<-":
                cursor = self.text_edit.textCursor()
                cursor.deletePreviousChar()
            elif button_text == "Enter":  # Close the keyboard on "Enter" button press
                self.accept()
            else:
                self.text_edit.insertPlainText(button_text)
                self.target.setText(self.text_edit.toPlainText())


class DemoWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.setGeometry(100, 100, 300, 100)  # Set window size and position

        label = QtWidgets.QLabel("Text Input:")
        self.text_input = QtWidgets.QLineEdit()
        self.text_input.installEventFilter(self)
        self.text_input.setGeometry(10,10,300,100 )

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(self.text_input)

        central_widget = QtWidgets.QWidget()
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)
        self.setWindowTitle("Keyboard")

    def eventFilter(self, obj, event):
        if obj == self.text_input and event.type() == QtCore.QEvent.MouseButtonPress:
            virtual_keyboard = VirtualKeyboard(self.text_input)
            if virtual_keyboard.exec_() == QtWidgets.QDialog.Accepted:
                pass  # Optional code to handle the keyboard being closed
        return super().eventFilter(obj, event)


if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    demo_window = DemoWindow()
    demo_window.show()
    app.exec_()
