# TODO: Code not required, used in time slots code in pyside-6 gui folder.
from PyQt5.QtWidgets import QLabel, QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QPushButton, QLabel
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QSize


# Declarations
btn_size_normal = (90, 40)
btn_size_big = (100, 50)

def create_button(text, parent, position, size, clicked_slot):
    button = QPushButton(text, parent)
    button.move(*position)
    button.setFixedSize(*size)
    button.clicked.connect(clicked_slot)
    return button


def create_labeled_textbox(label_text, parent, label_position, textbox_position, textbox_size,placeholdertext):
    label = QLabel(label_text, parent)
    label.move(*label_position)
    label.setParent(parent)

    textbox = QLineEdit(parent)
    textbox.move(*textbox_position)
    textbox.resize(*textbox_size)
    textbox.setEnabled(True)
    textbox.setParent(parent)
    textbox.setPlaceholderText(placeholdertext)

    label.show()
    textbox.show()

    return label, textbox

from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout ,QHBoxLayout
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtCore import Qt
def create_img_button(parent, image_path, png_size, button_size, position, on_click, text, bg_color):
    # Create a container widget
    container = QWidget(parent)
    container.setGeometry(*position, button_size, button_size)

    # Set the background self of the container
    container.setStyleSheet(f"background-color: {bg_color};")

    # Create a vertical layout for the container
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Create a QLabel for the PNG image
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(png_size, png_size, Qt.AspectRatioMode.KeepAspectRatio)
    label = QLabel(container)
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

    # Create a QLabel for the text
    text_label = QLabel(container)
    text_label.setAlignment(Qt.AlignCenter)
    text_label.setFont(QFont("inika", 15))
    text_label.setText(text)
    text_label.setContentsMargins(0, -15, 0, 0)

    # Add the labels to the layout
    layout.addWidget(label)
    layout.addWidget(text_label)

    # Set the layout for the container
    container.setLayout(layout)

    # Set up custom event handling for mouse clicks
    def mousePressEvent(event):
        if callable(on_click):
            on_click()
        event.accept()

    container.mousePressEvent = mousePressEvent

    return container

def create_img_button_H(parent, image_path, png_size, button_size, position, on_click, text, bg_color):
    # Create a container widget
    container = QWidget(parent)
    container.setGeometry(*position, button_size, button_size)

    # Set the background self of the container
    container.setStyleSheet(f"background-color: {bg_color};")

    layout = QHBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Create a QLabel for the PNG image
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(png_size, png_size, Qt.AspectRatioMode.KeepAspectRatio)
    label = QLabel(container)
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter | Qt.AlignHCenter)

    # Create a QLabel for the text
    text_label = QLabel(container)
    text_label.setAlignment(Qt.AlignCenter)
    text_label.setFont(QFont("inika", 15))
    text_label.setText(text)
    text_label.setContentsMargins(0, -15, 0, 0)

    # Add the labels to the layout
    layout.addWidget(label)
    layout.addWidget(text_label)

    # Set the layout for the container
    container.setLayout(layout)

    # Set up custom event handling for mouse clicks
    def mousePressEvent(event):
        if callable(on_click):
            on_click()
        event.accept()

    container.mousePressEvent = mousePressEvent

    return container

# self.thumb_btn = create_thumb_button(self, 'images/userMainThumb.jpg', 120, (330, 600), self.close)

from PyQt5 import QtWidgets, QtCore, QtGui
import csv

class Completer(QtWidgets.QCompleter):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

def load_combobox_with_autofill(combobox, filepath, column_name, autofill_textbox):
    combobox.clear()
    combobox.setEditable(True)

    completer = Completer(combobox)
    combobox.setCompleter(completer)
    #combobox.completer().setCompletionMode(QtWidgets.QCompleter.PopupCompletion)

    wordlist = ["name"]  # Placeholder text

    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        available_columns = [column.strip() for column in reader.fieldnames]
        print("Available columns:", available_columns)
        for row in reader:
            wordlist.append(row[column_name.strip()])

    model = QtCore.QStringListModel(wordlist)
    combobox.setModel(model)


    combobox.currentIndexChanged.connect(lambda index: update_autofill_textbox(index, combobox, filepath, column_name, autofill_textbox))

def update_autofill_textbox(index, combobox, filepath, search_column, autofill_textbox):
    if index > 0:  # Skip the placeholder item
        selected_name = combobox.currentText()
        selected_row = get_row_from_csv(filepath, search_column, selected_name)
        if selected_row is not None:
            autofill_textbox.setText(selected_row['EmpId'])
        else:
            autofill_textbox.clear()
    else:
        autofill_textbox.clear()

def get_row_from_csv(filepath, search_column, search_value):
    with open(filepath, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row[search_column] == search_value:
                return row
    return None


def ImgButton(parent, image_path, png_size, button_size, position, on_clicked):
    # Create a container widget
    container = QWidget(parent)
    container.setGeometry(*position, button_size, button_size)

    # Create a vertical layout for the container
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Create a QLabel for the PNG image
    label = QLabel(container)
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(png_size, png_size, Qt.AspectRatioMode.KeepAspectRatio)
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter)

    # Add the label to the layout
    layout.addWidget(label)

    # Set the layout for the container
    container.setLayout(layout)

    # Set the container as the clickable widget
    container.mousePressEvent = on_clicked

    return container


def imgbutton2(parent, image_path, png_size, button_size, position, on_clicked):
    # Create a QPushButton
    button = QPushButton(parent)
    button.setGeometry(*position, button_size, button_size)
    button.setIcon(QIcon(image_path))
    button.setIconSize(QSize(png_size, png_size))
    button.clicked.connect(on_clicked)

    return button

def imgbutton(parent, image_path, png_size, button_size, position, on_clicked):
    # Create a container widget
    container = QWidget(parent)
    container.setGeometry(*position, button_size, button_size)

    # Create a vertical layout for the container
    layout = QVBoxLayout(container)
    layout.setContentsMargins(0, 0, 0, 0)
    layout.setSpacing(0)

    # Create a QLabel for the PNG image
    label = QLabel(container)
    pixmap = QPixmap(image_path)
    scaled_pixmap = pixmap.scaled(png_size, png_size, Qt.AspectRatioMode.KeepAspectRatio)
    label.setPixmap(scaled_pixmap)
    label.setAlignment(Qt.AlignCenter)

    # Add the label to the layout
    layout.addWidget(label)

    # Set the layout for the container
    container.setLayout(layout)

    # Set the container as the clickable widget
    container.mousePressEvent = on_clicked

    return container


