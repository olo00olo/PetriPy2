from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QComboBox, QDialog, QMessageBox
import sys

from Saver import saver


class TableWindow(QDialog):
    def __init__(self, item, m, mainWindow):
        super().__init__()

        self.item = item
        self.prevVarDict = self.item.variables

        self.init_ui()

        self.m = m
        self.mainWindow = mainWindow

        self.removeQueue = []


    def init_ui(self):
        # self.setWindowTitle("Table Window")
        #
        # central_widget = QWidget(self)
        # self.setCentralWidget(central_widget)

        layout = QVBoxLayout()

        self.table = QTableWidget(self)
        self.table.setColumnCount(3)  # Zwiększ liczbę kolumn na przycisk usuwania
        self.table.setRowCount(len(self.item.variables))

        # Wstaw dane do tabeli
        self.i = 0
        for key, value in self.item.variables.items():
            for col in range(3):
                if col == 1:  # Dodaj rozwijaną listę w drugiej kolumnie
                    combo_box = QComboBox(self)
                    combo_box.addItems(["False", "True"])
                    combo_box.setCurrentIndex(value)
                    self.table.setCellWidget(self.i, col, combo_box)
                else:
                    item = QTableWidgetItem(key)
                    # print(key, type(key))
                    self.table.setItem(self.i, col, item)

            # Dodaj przycisk usuwania w trzeciej kolumnie
            remove_button = QPushButton("Usuń", self)
            remove_button.clicked.connect(lambda state, row=self.i: self.remove_row(row))
            self.table.setCellWidget(self.i, 2, remove_button)
            self.i += 1

        layout.addWidget(self.table)

        add_row_button = QPushButton("Dodaj wiersz", self)
        add_row_button.clicked.connect(self.add_row)
        layout.addWidget(add_row_button)

        apply_button = QPushButton("Apply", self)
        apply_button.clicked.connect(self.apply_changes)
        layout.addWidget(apply_button)

        # central_widget.setLayout(layout)
        self.setLayout(layout)

        self.table.itemClicked.connect(self.handle_item_click)


        # Dostosuj rozmiar okna do zawartości tabeli
        # self.resize(self.table.horizontalHeader().length() + 20, self.table.verticalHeader().length() + 50)
    def handle_item_click(self, item):
        # Obsługa kliknięcia w komórkę
        item.setBackground(QColor(255, 0, 0))

    def add_row(self):
        current_row_count = self.table.rowCount()
        self.table.setRowCount(current_row_count + 1)

        for col in range(self.table.columnCount()):
            if col == 1:
                combo_box = QComboBox(self)
                combo_box.addItems(["False", "True"])
                self.table.setCellWidget(current_row_count, col, combo_box)
            else:
                item = QTableWidgetItem("")
                self.table.setItem(current_row_count, col, item)
                # self.table.item(current_row_count, 0).clicked.connect((self.table.item(current_row_count, 0)).setBackground(QColor(0, 0, 255)))

        # Dodaj przycisk usuwania w trzeciej kolumnie
        remove_button = QPushButton("Usuń", self)
        remove_button.clicked.connect(lambda state, row=current_row_count: self.remove_row(row))
        self.table.setCellWidget(current_row_count, 2, remove_button)

        # Aktualizuj rozmiar okna po dodaniu nowego wiersza
        # self.resize(self.table.horizontalHeader().length() + 20, self.table.verticalHeader().length() + 50)

    def remove_row(self, row):
        # self.removeQueue.append(self.table.item(row, 0).text())

        self.table.removeRow(row)

        # Aktualizuj rozmiar okna po usunięciu wiersza
        # self.resize(self.table.horizontalHeader().length() + 20, self.table.verticalHeader().length() + 50)

        for r in range(self.table.rowCount()):
            remove_button = self.table.cellWidget(r, 2)
            if remove_button:
                remove_button.clicked.disconnect()
                remove_button.clicked.connect(lambda state, row=r: self.remove_row(row))

    def apply_changes(self):
        newVarDict = {}
        for row in range(self.table.rowCount()):
            for col in range(2):
                item = self.table.item(row, col)
                if item is not None:
                    var = item.text()
                    if var in newVarDict or (var in self.prevVarDict and row >= len(self.item.variables)):
                        msgBox = QMessageBox()
                        msgBox.information(self, "Information", "Variables duplicated")
                        self.table.item(row, col).setBackground((QColor(255, 0, 0)))
                else:
                    widget = self.table.cellWidget(row, col)
                    if isinstance(widget, QComboBox):
                        # print(widget.currentText())
                        if widget.currentText() == "False":
                            state = bool(0)
                        else:
                            state = bool(1)
                    newVarDict.update({var: state})
                    print("XDDDDDDDDD")

                    # self.m.showVariables()


                    # self.m.variables.append(var)

        self.item.variables = newVarDict
        self.item.variablesPrint()

        self.mainWindow.dock_variables.refresh_values()

        self.m.undoHeap.append(saver(self.m, "heap"))
        self.m.redoHeap = []

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     main_window = TableWindow()
#     main_window.show()
#     sys.exit(app.exec_())
