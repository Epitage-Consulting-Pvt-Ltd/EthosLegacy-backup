# TODO: Code cleanup and review required.
# year_selector.py

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QCalendarWidget, QMessageBox, QGridLayout
from PyQt5.QtCore import Qt, QEvent, QRect, QSize, QDate, pyqtSignal

class YearSelector(QWidget):
    year_selected = pyqtSignal(int)

    def __init__(self, start_year, end_year):
        super().__init__()
        self.start_year = start_year
        self.end_year = end_year
        self.current_page = (QDate.currentDate().year() - start_year) // 16
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.page_label = QLabel()
        self.prev_btn = QPushButton('<<')
        self.prev_btn.setFixedWidth(60)
        self.prev_btn.clicked.connect(self.prevPage)
        self.next_btn = QPushButton('>>')
        self.next_btn.setFixedWidth(60)
        self.next_btn.clicked.connect(self.nextPage)
        top_layout = QHBoxLayout()
        layout.addLayout(top_layout)
        top_layout.addWidget(self.prev_btn)
        top_layout.addStretch()
        top_layout.addWidget(self.next_btn)
        self.grid = QGridLayout()
        layout.addLayout(self.grid)
        self.updatePage()

        # self.calendar_widget = QCalendarWidget(self)
        # self.calendar_widget.setStyleSheet("QCalendarWidget QHeaderView { background-color: #CCCCCC; }")
        # self.calendar_widget.hide()
        # self.calendar_widget.clicked.connect(self.handle_date_selection)

    def updatePage(self):
        self.page_label.setText(f"Page {self.current_page + 1}")
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

    # def show_calendar(self, parent):
    #     self.setGeometry(QRect(parent.mapToGlobal(parent.rect().bottomLeft()), QSize(150, 150)))
    #     self.show()
    #     self.raise_()

    # def show_month_calendar(self, year, parent):
    #     self.calendar_widget.setSelectedDate(QDate(year, self.calendar_widget.selectedDate().month(), 1))
    #     bottom_left = parent.mapToGlobal(parent.rect().bottomLeft())
    #     self.calendar_widget.setGeometry(bottom_left.x(), bottom_left.y(), 300, 300)
    #     self.calendar_widget.show()
    #     self.calendar_widget.raise_()

    # def updateYearInCalendar(self, year):
    #     self.calendar_widget.setSelectedDate(QDate(year, self.calendar_widget.selectedDate().month(), 1))
    #     self.hide()
    #     bottom_left = self.parentWidget().mapToGlobal(self.parentWidget().rect().bottomLeft())
    #     self.calendar_widget.setGeometry(bottom_left.x(), bottom_left.y(), 300, 300)
    #     self.calendar_widget.show()
    #     self.calendar_widget.raise_()

    # def handle_date_selection(self, date):
    #     self.hide()
    #     self.parentWidget().setText(date.toString(Qt.ISODate))
