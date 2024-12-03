from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt, pyqtSignal
from infrastructure.env_config import EnvConfig


class ImgButton(QPushButton):

    clicked = pyqtSignal()

    def __init__(self, parent, image_path, png_width, png_height, button_width, button_height, bg_color, x, y, click_function):
        super().__init__(parent)
        self.config = EnvConfig()

        self.setFixedSize(button_width, button_height)
        self.move(x, y)  # Set x and y coordinates
        self.setStyleSheet(f"background-color: {bg_color};")


        # Create a QLabel for the PNG image
        pixmap = QPixmap(self.config.IMAGE_BASE_PATH + image_path)
        scaled_pixmap = pixmap.scaled(png_width, png_height, Qt.AspectRatioMode.KeepAspectRatio)
        label = QLabel(self)
        label.setPixmap(scaled_pixmap)
        label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

        # Create a vertical layout for the button
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.addWidget(label)
        self.setLayout(layout)
        self.clicked.connect(click_function)

    def mousePressEvent(self, event):
        self.clicked.emit()
        event.accept()



## Example usage

#button = img_button(parent, "image_path.png", 50, 100, "Button Text", "blue", 50, 50, on_button_click)