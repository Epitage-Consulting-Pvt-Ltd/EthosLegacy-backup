import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QWidget, QComboBox, QHBoxLayout, QApplication, QCompleter, QCheckBox, QLabel

def completion(word_list, widget, i=True):
    """ Autocompletion of sender and subject """
    word_set = set(word_list)
    completer = QCompleter(word_set)
    if i:
        completer.setCaseSensitivity(QtCore.Qt.CaseInsensitive)
    else:
        completer.setCaseSensitivity(QtCore.Qt.CaseSensitive)
    widget.setCompleter(completer)

class Autocomplete(QComboBox):
    def __init__(self, items, parent=None, i=False, allow_duplicates=True):
        super(Autocomplete, self).__init__(parent)
        self.items = items
        self.insensitivity = i
        self.allowDuplicates = allow_duplicates
        self.init()

    def init(self):
        self.setEditable(True)
        self.setDuplicatesEnabled(self.allowDuplicates)
        self.addItems(self.items)
        self.setAutocompletion(self.items, i=self.insensitivity)
        self.lineEdit().installEventFilter(self)

    def setAutocompletion(self, items, i):
        completion(items, self, i)

    def eventFilter(self, obj, event):
        if event.type() == QtCore.QEvent.KeyPress:
            key = event.key()
            if key == QtCore.Qt.Key_Return or key == QtCore.Qt.Key_Enter:
                self.onEnterPressed()
                return True
        return super(Autocomplete, self).eventFilter(obj, event)

    def onEnterPressed(self):
        text = self.currentText()
        if text not in self.items:
            self.addItem(text)
        self.setCurrentText(text)

class Widget(QWidget):
    def __init__(self, items, parent=None, fixed=True, allow_duplicates=True):
        super(Widget, self).__init__()
        self.items = items
        self.checkbox = QCheckBox()
        self.labelItemCounter = QLabel()
        self.autocomplete = Autocomplete(self.items, 
            parent=self, i=True, allow_duplicates=allow_duplicates
        )
        if fixed:
            self.autocomplete.setInsertPolicy(QComboBox.NoInsert)        
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.layout.addWidget(self.checkbox)
        self.layout.addWidget(self.autocomplete)
        self.layout.addWidget(self.labelItemCounter)
        self.labelItemCounter.setText(f'{self.autocomplete.count()}')
        self.checkbox.stateChanged.connect(lambda: self.tuneAutocompletion())

    def tuneAutocompletion(self):
        if self.checkbox.isChecked():
            self.autocomplete.setAutocompletion(self.items, True)
        else:
            self.autocomplete.setAutocompletion(self.items, False)

    def currentText(self):
        print("text: ", self.setCurrentText())
        return self.autocomplete.currentText()
    

    def currentIndex(self):        
        return self.autocomplete.currentIndex()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = QWidget()
    l = ['Captain America', 'Hulk', 'Iron Man', 'hulk', 'Iron Man ', 'Captain America0', 'Captain America1', 'Captain America2' ]
    cb = Widget(l, parent=w)    
    layout = QHBoxLayout()
    layout.addWidget(cb)
    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())
