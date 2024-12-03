# TODO: Code not required, need to remove
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QHBoxLayout
from PyQt5.QtCore import Qt

class CheckBoxDemo(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('CheckBox Demo')
        self.setGeometry(100, 100, 400, 200)

          # Set the window size
        self.resize(100, 80)

        # Make the window frameless
        self.setWindowFlags(Qt.FramelessWindowHint)

        # Create the layout
        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        # Create two horizontal layouts for checkboxes
        checkbox_layout1 = QHBoxLayout()
        checkbox_layout2 = QHBoxLayout()

        # Define texts for each checkbox
        checkbox_texts = [
            'LL', 'LR', 'LM', 'LI', 'LT',
            'RL', 'RR', 'RM', 'RI', 'RT'
        ]

        # Add checkboxes to the layouts with different text
        for i, text in enumerate(checkbox_texts):
            checkbox = QCheckBox(text)
            checkbox.setChecked(False)
            checkbox.setFixedSize(60, 30)
            if i < 5:
                checkbox_layout1.addWidget(checkbox)
            else:
                checkbox_layout2.addWidget(checkbox)

        # Add the checkbox layouts to the main layout
        main_layout.addLayout(checkbox_layout1)
        main_layout.addLayout(checkbox_layout2)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CheckBoxDemo()
    window.show()
    sys.exit(app.exec_())
