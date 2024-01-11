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
                print(temp, "temp")

            for key, value in transition.inArcs.items():
                weight = value[0].weightValue
                temp[next(iter(value[1].keys()))] = -weight
                temp = dict(sorted(temp.items()))


            for key, value in transition.outArcs.items():
                weight = value[0].weightValue
                temp[next(iter(value[2].keys()))] = weight
                temp = dict(sorted(temp.items()))

            print(temp, "temp")
            for key, value in temp.items():
                ab.append(value)

            print(ab, "ab")
            print(len(ab), 'len')
            self.c.append(ab)


        # print(self.c)
        if self.c:
            # print("XD")
            self.table_widget2.setRowCount(len(self.c))
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
        #aktywnosc ze znakowania
        if len(self.c) > 0:
            if len(self.c[0]) > 0:
                for col in range(len(self.c[0])):
                    for row in range(len(self.c)):
                        if self.c[row][col] < 0:
                            sum += self.c[row][col]
                    if sum < 0:
                        temp.append(abs(sum))
                    else:
                        temp.append(999)

                    sum = 0

                print(self.m, "3?")
                for col in range(len(self.c[0])):

                    if self.m[col] >= temp[col]:
                        self.u.append(1)
                    else:
                        self.u.append(0)

                self.c = np.add(self.c, self.varActivity())
                self.mNew = np.add(self.m, np.matmul(self.u, self.c))

        # self.varActivity()

    #aktywnosc ze zmiennych
    def varActivity(self):
        varC = []
        temp = self.item.variableDict
        print(temp)

        if len(self.item.transitionsDict) > 0:
            for key, value in self.item.transitionsDict.items():
                sp = value.variables.split()
                if len(sp) == 0:
                    varC.append(1)
                    print(varC, "var0")
                elif len(sp) == 1:
                    if sp[0][0] == "~":
                        varC.append(not temp[sp[0][1:]])
                    else:
                        varC.append(temp[sp[0]])
                    print(varC, "var1")
                else:
                    if sp[0][0] == "~":
                        temp1 = not temp[sp[0][1:]]
                    else:
                        temp1 = temp[sp[0]]
                    for x in range(1, len(sp)-1):
                        if sp[x] == "OR":
                            if sp[x+1][0] == "~":
                                temp1 += not temp[sp[x+1][1:]]
                                temp1 = bool(temp1)
                            else:
                                temp1 += temp[sp[x+1]]
                                temp1 = bool(temp1)
                        else:
                            if sp[x+1][0] == "~":
                                temp2 = not temp[sp[x+1][1:]]
                                temp2 = bool(temp2)
                                temp1 = temp1 * temp2
                                temp1 = bool(temp1)
                            else:
                                temp2 = temp[sp[x + 1]]
                                temp2 = bool(temp2)
                                temp1 = temp1 * temp2
                                temp1 = bool(temp1)
                    varC.append(int(temp1))
            return(varC)

    def refresh(self):
        for col in range(len(self.places)):
            self.table_widget.setItem(0, col, QTableWidgetItem(str((self.places[col]).tokens)))



