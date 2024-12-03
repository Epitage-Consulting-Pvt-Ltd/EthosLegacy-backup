# TODO: Code not required, need to remove
from PyQt5.QtWidgets import QApplication, QComboBox, QVBoxLayout, QWidget, QCompleter
from PyQt5.QtSql import QSqlDatabase, QSqlQueryModel, QSqlQuery
from utilities.keyboard import VirtualKeyboard


def custom_combobox(geometry, database_path, table_name, display_column, parent=None):
    # Create the main widget
    widget = QWidget(parent)
    #widget.setGeometry(*geometry)

    # Create the QComboBox
    combo_box = QComboBox(widget)
    combo_box.setEditable(True)
    combo_box.setGeometry(*geometry)
    combo_box.show()
    combo_box.raise_()


    # Set up the database connection
    database = QSqlDatabase.addDatabase("QSQLITE")
    database.setDatabaseName(database_path)

    if not database.open():
        raise Exception(f"Failed to open database: {database.lastError().text()}")

    # Fetch data from the database
    query = QSqlQuery(f"SELECT {display_column} FROM {table_name}", database)

    # Populate the QComboBox with data
    model = QSqlQueryModel()
    model.setQuery(query)

    combo_box.setModel(model)
    combo_box.setModelColumn(model.record().indexOf(display_column))

    # Create a completer for autocompletion
    completer = QCompleter()
    completer.setModel(model)
    completer.setCaseSensitivity(False)
    completer.setCompletionColumn(model.record().indexOf(display_column))
    combo_box.setCompleter(completer)

    combo_box.setStyleSheet("""
        QComboBox {
            /* Set the background color */
            background-color: lightgray;
            /* Set the border style and color */
            border: 1px solid darkgray;
            /* Set the padding */
            padding: 2px;
            /* Set the border-radius for rounded corners */
            border-radius: 5px;
            height: 35px;
        }

        QComboBox::drop-down {
            /* Set the appearance of the down arrow */
            subcontrol-origin: padding;
            subcontrol-position: right top;
            width: 15px;
            border-left-width: 1px;
            border-left-color: darkgray;
            border-left-style: solid;
        }

        QComboBox::down-arrow {
            /* Set the down arrow icon */
            image: url("magnifying-glass.png");
            /* Scale and position the down arrow icon */
            width: 20px; /* Width of the square icon */
            height: 20px; /* Height of the square icon */
            subcontrol-position: center right;
        }
    """)

    virtual_keyboard = VirtualKeyboard()

    def open_keyboard():
        print('keyboard-activated')
        

    def mouse_pressed(event):
        print('mouse pressed')
        virtual_keyboard.target = combo_box
        virtual_keyboard.show()

    combo_box.activated.connect(open_keyboard)
    combo_box.mousePressEvent = mouse_pressed

    def update_completer(text):
        completer.setCompletionPrefix(text)
        completer.complete()

    # Connect the textChanged signal of the combo box to the update_completer function
    combo_box.lineEdit().textChanged.connect(update_completer)
    

    return combo_box

# Example usage:
# if __name__ == "__main__":
#     app = QApplication([])

#     # Specify your database path and table name
#     database_path = "app/infrastructure/database/ethos_firmware.db"
#     table_name = "employee"
#     display_column = "emp_name"

#     # Specify the geometry as (x, y, width, height)
#     geometry = (100, 100, 200, 30)

#     # Call the function to create the QComboBox
#     combo_box_widget = custom_combobox(geometry, database_path, table_name, display_column)
#     combo_box_widget.show()

#     app.exec_()
