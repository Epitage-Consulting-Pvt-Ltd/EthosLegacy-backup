# TODO: Code not required, need to remove
#!/usr/bin/python

import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtCore import Slot, Qt
import os

# Import Tkinter
import tkinter as tk
from tkinter import Button

# Set the environment variable for the Qt platform to 'eglfs'
os.environ['QT_QPA_PLATFORM'] = 'eglfs'

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Create the central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a layout for the central widget
        layout = QVBoxLayout(central_widget)

        # Embed Tkinter button in PyQt5 layout
        tk_frame = TkinterFrame(central_widget)
        layout.addWidget(tk_frame)

        # PyQt5 button
        button_pyside = QPushButton("PyQt5 Button", self)
        button_pyside.clicked.connect(self.say_hello_pyside)
        layout.addWidget(button_pyside)

    @Slot()
    def say_hello_pyside(self):
        print("PyQt5 Button clicked, Hello!")

# Tkinter frame within PyQt5
class TkinterFrame(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Create a Tkinter frame
        self.tk_frame = tk.Frame(self)
        self.embed_tkinter_button()

    def embed_tkinter_button(self):
        # Tkinter button
        button_tkinter = Button(self.tk_frame, text="Tkinter Button", command=self.say_hello_tkinter)
        button_tkinter.pack()

        # Embed Tkinter frame into PyQt5 layout
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tk_frame)

    def say_hello_tkinter(self):
        print("Tkinter Button clicked, Hello!")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec())
