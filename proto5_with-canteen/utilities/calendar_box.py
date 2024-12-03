# TODO: Code not required, need to remove
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QCalendarWidget,
    QGridLayout,
    QWidget,
    QLabel,
    QToolButton,
    QPushButton
)
from PyQt5.QtCore import QDate, Qt
from PyQt5.QtWidgets import QComboBox
from PyQt5.QtGui import QFont


class YearSelectionWidget(QWidget):
    def __init__(self, start_year, end_year, current_year, parent=None):
        super().__init__(parent)
        self.start_year = start_year  # Add start_year attribute
        layout = QGridLayout(self)
        self.buttons = []

        for year in range(start_year, end_year + 1):
            button = QPushButton(str(year))
            button.clicked.connect(lambda checked, y=year: self.year_selected(y))
            layout.addWidget(button, (year - start_year) // 4, (year - start_year) % 4)
            self.buttons.append(button)

        self.set_current_year(current_year)

    def set_current_year(self, current_year):
        for button in self.buttons:
            button.setEnabled(True)
        self.buttons[current_year - self.start_year].setDisabled(True)

    def year_selected(self, year):
        self.parent().handle_year_changed(year)
        self.hide()  # Hide the widget after a year is selected


class CalendarWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Basic layout
        grid = QGridLayout(self)

        # Calendar widget
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.setGridVisible(True)
        self.calendar.setMinimumDate(QDate(1932, 1, 1))
        self.calendar.setMaximumDate(QDate(2999, 12, 31))
        self.calendar.selectionChanged.connect(self.handle_date_changed)
        grid.addWidget(self.calendar, 0, 0, 1, 5)

        # Year selection
        self.year_label = QLabel("Year:")
        self.year_label.setAlignment(Qt.AlignRight)
        grid.addWidget(self.year_label, 1, 0)
        self.year_button = QToolButton()
        self.update_year_button()
        # self.year_button.setText(str(self.calendar.selectedDate().year()))
        self.year_button.clicked.connect(self.show_year_menu)
        grid.addWidget(self.year_button, 1, 1)

        # Navigation buttons (optional)
        # You can add custom buttons here for month navigation

        # Today's date
        self.today_label = QLabel("Today:")
        self.today_label.setAlignment(Qt.AlignRight)
        grid.addWidget(self.today_label, 2, 0)
        self.today_button = QToolButton()
        self.today_button.setText(str(QDate.currentDate()))
        self.today_button.clicked.connect(self.set_today)
        grid.addWidget(self.today_button, 2, 1)

        # Week number (optional)
        # You can add a label here to display the week number

        # Styling (customize further)
        font = QFont("Segoe UI", 10)
        self.setFont(font)
        self.setStyleSheet(
            """
            QCalendarWidget QPushButton {
                border: none;
                background-color: #f7f7f7;
            }
            QCalendarWidget QAbstractItemView::indicator {
                background-color: #3498db;
            }
            """
        )

        self.setWindowTitle("PyQt5 Calendar")
        self.show()

    def show_year_menu(self):
        # Create a combo box for year selection
        self.year_combo = QComboBox(self)
        current_year = QDate.currentDate().year()        
        # Populate the combo box with years from 2000 to 2999
        for year in range(1932, current_year + 1):
            self.year_combo.addItem(str(year))
        
        # # Set the current year as the selected year
        current_year = self.calendar.selectedDate().year()
        index = self.year_combo.findText(str(current_year))
        if index >= 0:
            self.year_combo.setCurrentIndex(index)
        
        # Connect the combo box signal to handle year change
        self.year_combo.currentIndexChanged.connect(self.handle_year_changed)
        
        # Show the combo box
        self.year_combo.show()
        # Set the current year as the selected year
        current_index = self.year_combo.findText(str(self.calendar.selectedDate().year()))
        self.year_combo.setCurrentIndex(current_index)
        self.year_combo.currentIndexChanged.connect(self.handle_year_changed)
        self.year_combo.show()

        # if not hasattr(self, 'year_combo') or not self.year_combo.isVisible():
        #     self.year_combo = YearSelectionWidget(1932, QDate.currentDate().year(), self.calendar.selectedDate().year(), parent=self)
        #     self.year_combo.move(self.year_button.mapToGlobal(self.year_button.rect().bottomLeft()))
        #     self.year_combo.show()
    
    def handle_year_changed(self, index):
        # Get the selected year from the combo box
        selected_year = int(self.year_combo.currentText())
        
        # Update the calendar's selected year
        current_date = self.calendar.selectedDate()
        new_date = QDate(selected_year, current_date.month(), current_date.day())
        self.calendar.setSelectedDate(new_date)

    def set_today(self):
        self.calendar.setSelectedDate(QDate.currentDate())

    def handle_date_changed(self):
        selected_date = self.calendar.selectedDate()
        print(f"Selected date: {selected_date.toString('yyyy-MM-dd')}")

    def update_year_button(self):
        current_year = QDate.currentDate().year()
        self.year_button.setText(str(current_year))


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = CalendarWidget()
    sys.exit(app.exec_())
