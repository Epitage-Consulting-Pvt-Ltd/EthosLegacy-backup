# TODO: Code cleanup and review required.
import os
import sys
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt, QThread, pyqtSignal
from img_button import ImgButton  


class AttentionBox(QMainWindow):
    def __init__(self):
        super().__init__()

        self.current_directory = os.getcwd()
        self.width = 480
        self.height = 250
        self.setGeometry(0, 550, self.width, self.height)
        self.setWindowFlag(Qt.FramelessWindowHint)

        self.Background = QLabel(self)
        self.Background.setPixmap(QPixmap(os.path.join(
            self.current_directory, "AttentionBox.png")))
        self.Background.setGeometry(0, 0, self.width, self.height)

        self.ok_btn = ImgButton(
            self, "OK_btn.png", 85, 35, 85, 35, "#D9D9D9", 388, 180, self.close)

        self.cancel_btn = ImgButton(
            self, "Cancel_btn.png", 85, 35, 85, 35, "#D9D9D9", 287, 180, self.close)


class AttentionBoxThread(QThread):
    finished = pyqtSignal()

    def __init__(self):
        super().__init__()

    def run(self):
        app = QApplication(sys.argv)
        attention_box = AttentionBox()
        attention_box.show()
        app.exec_()
        self.finished.emit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    thread = AttentionBoxThread()
    thread.finished.connect(app.quit)
    thread.start()
    sys.exit(app.exec_())
