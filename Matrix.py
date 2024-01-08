from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QComboBox, QDialog, QMessageBox
import sys

from Place import Place
from Transition import Transition
import numpy as np


class Matrix(QDialog):
    def __init__(self, item):
        super().__init__()

        self.places = []
        self.transitions = []
        self.arcs = []

        self.m = []
        self.k = []
        self.c = []
        self.mNew = []

        self.item = item
        self.table_widget2 = QTableWidget(self)
        self.table_widget = QTableWidget(self)




        layout = QVBoxLayout()

        layout.addWidget(self.table_widget)
        layout.addWidget(self.table_widget2)
        self.setLayout(layout)

    def combo(self):
        self.mNew = []
        self.m = []
        self.k = []
        self.c = []
        self.u = []
        self.initValue()
        self.matrixMK()
        self.matrixC()
        self.matrixU()

    def initValue(self):
        self.places = []
        self.transitions = []
        self.arcs = []

        for key, value in self.item.placesDict.items():
            self.places.append(value)

        for key, value in self.item.transitionsDict.items():
            self.transitions.append(value)

        for key, value in self.item.arcsDict.items():
            self.arcs.append(value)

    def matrixC(self):
        self.c = []

        for transition in self.transitions:
            temp = {}
            ab = []

            for place in self.places:
                temp[place.id] = 0

            for key, value in transition.inArcs.items():
                weight = value[0].weightValue
                temp[next(iter(value[1].keys()))] = -weight
                temp = dict(sorted(temp.items()))


            for key, value in transition.outArcs.items():
                weight = value[0].weightValue
                temp[next(iter(value[2].keys()))] = weight
                temp = dict(sorted(temp.items()))


            for key, value in temp.items():
                ab.append(value)
            self.c.append(ab)


        # print(self.c)
        if self.c:
            # print("XD")
            self.table_widget2.setRowCount(len(self.c))  # Dwie kolumny
            self.table_widget2.setColumnCount(len(self.c[0]))
            # print(self.c)


            for i, row in enumerate(self.c):
                for j, value in enumerate(row):

                    # item = QTableWidgetItem(str(value))
                    # print(i, j, self.item, value)
                    # print("XDDDDD")

                    self.table_widget2.setItem(i, j, QTableWidgetItem(str(value)))



    def matrixMK(self):
        self.table_widget.setRowCount(2)  # Dwie kolumny
        self.table_widget.setColumnCount(len(self.places))
        self.table_widget.setVerticalHeaderLabels(["M", "K"])


        for col in range(len(self.places)):
            self.table_widget.setHorizontalHeaderItem(col, QTableWidgetItem("P" + str((self.places[col]).id)))
            # self.m.append(self.places[col].id)
            # table_widget.setItem(0, col, QTableWidgetItem("XD"))

            self.table_widget.setItem(0, col, QTableWidgetItem(str((self.places[col]).tokens)))
            self.m.append(self.places[col].tokens)

            self.table_widget.setItem(1, col, QTableWidgetItem(str((self.places[col]).capacityValue)))
            self.k.append(self.places[col].capacityValue)


    def matrixU(self):
        sum = 0
        temp = []
        for col in range(len(self.c[0])):
            for row in range(len(self.c)):
                if self.c[row][col] < 0:
                    sum += self.c[row][col]
                    temp.append(abs(sum))
            sum = 0

        for col in range (len(self.c[0])):
            if self.m[col] >= temp[col]:
                self.u.append(1)
            else:
                self.u.append(0)
        # print(temp, "temp", self.u)
        self.mNew = np.add(self.m, np.matmul(self.u, self.c))
        # print(self.mNew)
        #
        # return self.mNew



