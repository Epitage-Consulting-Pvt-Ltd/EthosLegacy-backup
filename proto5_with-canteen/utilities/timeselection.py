# TODO: Code not used, needs reviwe and removal if required
from PyQt5.QtWidgets import QApplication, QMainWindow, QTimeEdit
from PyQt5.QtCore import QTime
import sys

def create_time_edit(interval=30):
    time_edit = QTimeEdit()
    time_edit.setTime(QTime.currentTime())
    time_edit.stepBy(interval)
    return time_edit

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.timeEdit = create_time_edit()
        self.timeEdit.timeChanged.connect(self.print_selected_time)

        self.setCentralWidget(self.timeEdit)

        self.show()

    def print_selected_time(self):
        selected_time = self.timeEdit.time()
        print("Selected Time:", selected_time.toString("hh:mm:ss"))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    sys.exit(app.exec_())
