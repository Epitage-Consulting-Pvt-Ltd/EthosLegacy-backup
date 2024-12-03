# TODO: Code cleanup and reuse in other code calls review requried.
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QGridLayout, QLabel, QVBoxLayout, \
    QCalendarWidget, QAbstractItemView, QHBoxLayout
from PyQt5.QtCore import Qt, pyqtSignal, QDate
from PyQt5.QtWidgets import QFrame


class MonthSelector(QWidget):
    month_selected = pyqtSignal(int)
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        layout = QGridLayout()
        self.setLayout(layout)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                       'July', 'August', 'September', 'October', 'November', 'December']
        for i, month in enumerate(self.months, 1):
            row = (i - 1) // 3
            col = (i - 1) % 3
            btn = QPushButton(month)
            btn.clicked.connect(lambda checked, m=i: self.month_selected.emit(m))
            layout.addWidget(btn, row, col)

class DateSelector(QWidget):
    date_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)

        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.calendar = QCalendarWidget()
        self.calendar.setGridVisible(True)
        self.calendar.setSelectedDate(QDate.currentDate())
        self.calendar.selectionChanged.connect(self.handleDateSelected)
        self.calendar.setStyleSheet(
                        """
                        QCalendarWidget QAbstractItemView {
                            selection-background-color: #D3D3D3;
                            color: black;
                            border: none;
                            font-size: 8pt;
                        }
                        QCalendarWidget QAbstractItemView:item:selected:active {
                            background-color: #FFD700; 
                        }
                        QCalendarWidget QWidget#qt_calendar_navigationbar {
                            border: none;
                            background-color: #ffffff; 
                        }
                        QCalendarWidget QToolButton {
                            border: none;
                            background-color: #ffffff; 
                            color: black;
                        }
                        QCalendarWidget QToolButton:hover {
                            background-color: #eeeeee; 
                        }
                        """
                    )

        layout.addWidget(self.calendar)
    def handleDateSelected(self):
        selected_date = self.calendar.selectedDate().day()
        self.date_selected.emit(selected_date)


class YearSelector(QWidget):
    year_selected = pyqtSignal(int)
    def __init__(self, start_year, end_year):
        super().__init__()
        self.start_year = start_year
        self.end_year = end_year
        self.current_page = (QDate.currentDate().year() - start_year) // 16
        self.setWindowFlags(Qt.FramelessWindowHint) # | Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        # layout.addWidget(self.page_label)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.page_label = QLabel()
        self.prev_btn = QPushButton('<<')
        self.prev_btn.setFixedWidth(60)
        self.prev_btn.clicked.connect(self.prevPage)
        # layout.addWidget(self.prev_btn)
        self.next_btn = QPushButton('>>')
        self.next_btn.setFixedWidth(60)
        self.next_btn.clicked.connect(self.nextPage)
        # layout.addWidget(self.next_btn)
        top_layout = QHBoxLayout()  # New horizontal layout for buttons
        layout.addLayout(top_layout)
        top_layout.addWidget(self.prev_btn)  # Add previous button to top layout
        top_layout.addStretch()
        top_layout.addWidget(self.next_btn)  # Add next button to top layout
        self.grid = QGridLayout()
        layout.addLayout(self.grid)
        self.updatePage()

    def updatePage(self):
        self.page_label.setText(f"Page {self.current_page + 1}")
        # Clear previous buttons
        for i in reversed(range(self.grid.count())):
            self.grid.itemAt(i).widget().setParent(None)
        start = self.current_page * 12
        end = min((self.current_page + 1) * 12, self.end_year - self.start_year + 1)
        for i in range(start, end):
            year = self.start_year + i
            btn = QPushButton(str(year))
            btn.clicked.connect(lambda checked, y=year: self.year_selected.emit(y))
            row = (i - start) // 3
            col = (i - start) % 3
            self.grid.addWidget(btn, row, col)

    def nextPage(self):
        if self.current_page < (self.end_year - self.start_year) // 16:
            self.current_page += 1
            self.updatePage()

    def prevPage(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.updatePage()


class Calendar(QWidget):
    date_selected = pyqtSignal(str)  # Define a signal for emitting the selected date
    def __init__(self):
        super().__init__()
        self.current_year = None
        self.current_month = None
        self.current_date = None        
        self.setWindowFlags(Qt.FramelessWindowHint) # | Qt.WindowStaysOnTopHint)
        self.initUI()

    def initUI(self):
        self.year_selector = YearSelector(1900, 2100)
        self.year_selector.hide()
        self.year_selector.year_selected.connect(self.openMonthSelector)
        self.month_selector = MonthSelector()
        self.month_selector.hide()
        self.month_selector.month_selected.connect(self.openDateSelector)
        self.date_selector = DateSelector()
        self.date_selector.hide()
        self.date_selector.date_selected.connect(self.handleDateSelected)
        self.showYearSelector()

    def showYearSelector(self):
        self.year_selector.raise_()
        self.year_selector.show()

    def openMonthSelector(self, year):
        self.current_year = year
        self.year_selector.hide()
        self.month_selector.raise_()
        self.month_selector.show()

    def openDateSelector(self, month):
        self.current_month = month
        self.month_selector.hide()
        self.date_selector.raise_()
        self.date_selector.show()

    def handleDateSelected(self, date):
        self.current_date = date
        print(f"Selected date: {self.current_year}-{self.current_month}-{self.current_date}")
        selected_date = f"{self.current_year}-{self.current_month}-{date}"
        self.date_selected.emit(selected_date)
        # Close the application
        QApplication.quit()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Calendar()
    sys.exit(app.exec_())
