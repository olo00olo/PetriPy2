from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QComboBox, QDialog, QMessageBox
import sys

class Matrix(QDialog):
    def __init__(self, item):
        super().__init__()

        places = []

        for key, value in item.placesDict.items():
            places.append(value)

        layout = QVBoxLayout()

        table_widget = QTableWidget(self)
        table_widget.setRowCount(2)  # Dwie kolumny
        table_widget.setColumnCount(len(places))
        table_widget.setVerticalHeaderLabels(["m", "k"])


        for col in range(len(places)):
            table_widget.setHorizontalHeaderItem(col, QTableWidgetItem("P" + str((places[col]).id)))
            # table_widget.setItem(0, col, QTableWidgetItem("XD"))

            print((places[col]).capacityValue)
            table_widget.setItem(0, col, QTableWidgetItem(str((places[col]).tokens)))
            table_widget.setItem(1, col, QTableWidgetItem(str((places[col]).capacityValue)))


        # for row in range():
        #     for col, value in enumerate(values):
        #         item = QTableWidgetItem(value)
        #         table_widget.setItem(row, col, item)




        layout.addWidget(table_widget)

        self.setLayout(layout)
