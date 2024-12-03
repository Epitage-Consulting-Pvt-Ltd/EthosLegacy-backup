from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton

from PyQt5.QtGui import QPixmap, QFont

from PyQt5.QtCore import Qt,  QEvent #Signal,

class ImgButtonText(QPushButton):

    # clicked = Signal()


    def __init__(self, parent, image_path, png_width, png_height, button_width, button_height, text, bg_color, x, y, click_function):
        super().__init__(parent)

        self.setFixedSize(button_width, button_height)

        self.move(x, y)  # Set x and y coordinates

        self.setStyleSheet(f"background-color: {bg_color};")

        self.setAttribute(Qt.WA_AcceptTouchEvents)


        # Create a QLabel for the PNG image

        pixmap = QPixmap(image_path)

        scaled_pixmap = pixmap.scaled(png_width, png_height, Qt.AspectRatioMode.KeepAspectRatio)

        label = QLabel(self)

        label.setPixmap(scaled_pixmap)

        label.setAlignment(Qt.AlignCenter | Qt.AlignBottom)


        # Create a QLabel for the text

        text_label = QLabel(self)

        text_label.setAlignment(Qt.AlignCenter)

        text_label.setFont(QFont("inika", 14))

        text_label.setText(text)

        text_label.setContentsMargins(0, -15, 0, 0)


        # Create a vertical layout for the button

        layout = QVBoxLayout(self)

        layout.setContentsMargins(0, 0, 0, 0)

        layout.setSpacing(0)


        # Add the labels to the layout

        layout.addWidget(label)

        layout.addWidget(text_label)


        # Set the layout for the button

        self.setLayout(layout)


        # Connect the clicked signal to the provided function

        self.clicked.connect(click_function)


    def mousePressEvent(self, event):

        self.clicked.emit()

        event.accept()
    

    # def touchEvent(self, event):

    #     # Handle touch events here

    #     self.clicked.emit()

    #     event.accept()

    #     print("Touch Event: ", event.touchPoints())


    # def event(self, event):

    #     if event.type() == QEvent.Type.TouchBegin:

    #         self.clicked.emit()

    #         return True

    #     return super().event(event)



## Example usage

#button = img_button(parent, "image_path.png", 50, 100, "Button Text", "blue", 50, 50, on_button_click)