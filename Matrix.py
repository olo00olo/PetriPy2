from PyQt5.QtCore import Qt
from PyQt5.QtGui import QWindow, QColor
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget, \
    QPushButton, QComboBox, QDialog, QMessageBox
import sys

from Place import Place
from Transition import Transition
import numpy as np

from parser import parser


class Matrix(QDialog):
    def __init__(self, item, mainWindow):
        super().__init__()

        self.setWindowTitle("Matrix")

        self.places = []
        self.transitions = []
        self.arcs = []

        self.m = []
        self.k = []
        self.c = []
        self.mNew = []

        self.item = item
        self.mainWindow = mainWindow
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



        if self.c:

            self.table_widget2.setRowCount(len(self.c))
            self.table_widget2.setColumnCount(len(self.c[0]))


            for i, row in enumerate(self.c):
                for j, value in enumerate(row):
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
            self.m.append(int(self.places[col].tokens))

            self.table_widget.setItem(1, col, QTableWidgetItem(str((self.places[col]).capacityValue)))
            self.k.append(self.places[col].capacityValue)

    def matrixU(self):

        # sum = 0

        if len(self.item.transitionsDict) == 1 and len(self.item.placesDict) == 0:
            self.mNew = self.m

        elif len(self.item.transitionsDict) == 0 and len(self.item.placesDict) == 1:
            self.mNew = self.m

        elif len(self.item.transitionsDict) == 1 and len(self.item.placesDict) == 1:
            if len(self.item.arcsDict) == 1:
                u = 0
                uCap = 0
                self.c = self.c[0]
                if self.c[0] < 0:
                    if self.m[0] >= abs(self.c[0]):
                        u = 1
                    else:
                        u = 0
                else:
                    u = 1

                if self.k[0] - self.m[0] >= self.c[0]:
                    uCap = 1

                uVar = (self.varActivity())[0]

                if u + uCap + uVar == 3:
                    self.mNew.append(self.c[0] + self.m[0])

                if self.c[0] < 0 and u + uCap + uVar == 3:
                    for key, value in self.item.placesDict.items():
                        for key2, value2 in value.variables.items():
                            print(self.item.variableDict, "variableDict8")

                            self.item.variableDict.update({key2: value2})
                            print(self.item.variableDict, "variableDict9")

                    self.mainWindow.dock_variables.refresh_table()


        elif len(self.item.transitionsDict) > 1 and len(self.item.placesDict) == 1:
            if len(self.item.arcsDict) > 0:
                u = []
                uCap = []

                for row in range(len(self.c)):
                    if self.c[row][0] < 0:
                        if self.m[0] >= abs(self.c[row][0]):
                            u.append(1)
                        else:
                            u.append(0)
                    else:
                        u.append(1)

                    if self.c[row][0] > 0:
                        if self.k[0] - self.m[0] >= self.c[row][0]:
                            uCap.append(1)
                        else:
                            uCap.append(0)
                    else:
                        uCap.append(1)
                uVar = (self.varActivity())

                # sum = 0
                # sum2 = 0
                # sum3 = 0

                self.u = list(np.logical_and(u, uCap))
                self.u = list(map(int, self.u))

                self.u = list(np.logical_and(self.u, self.varActivity()))
                self.u = list(map(int, self.u))

                # d = list(np.add(self.m, np.matmul(self.u, self.c)))
                # if d[0] > self.k[0] - self.m[0]:
                #     msgBox = QMessageBox()
                #     msgBox.information(self, "Information", "Conflict")

                a = 0
                temp1 = 0
                for x in range(len(self.c)):
                    a += self.u[x] * self.c[x][0]
                    if a < 0:
                        temp1 = 1
                if abs(a) > self.m[0] and temp1 == 1:
                    print(a, self.m, self.m[0])
                    outArcs = list(self.item.placesDict.values())[0].outArcs
                    info = ""
                    for key, value in enumerate(outArcs.values()):
                        prefix = "T"
                        info += f"{prefix}{list(value[2])[0]} "

                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Solve conflict in " + info + "before continuation")
                    self.mNew = self.m
                    self.item.stop_simulationFun()
                    return

                if a > self.k[0] - self.m[0]:
                    inArcs = list(self.item.placesDict.values())[0].inArcs
                    print(inArcs, "AAA")
                    info = ""
                    for key, value in enumerate(inArcs.values()):
                        prefix = "T"
                        info += f"{prefix}{list(value[1])[0]} "

                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Solve conflict in " + info + "before continuation")
                    self.mNew = self.m
                    self.item.stop_simulationFun()
                    return
                temp1 = 0
                a = 0

                self.mNew = list(np.add(self.m, np.matmul(self.u, self.c)))


                for x in range(len(self.u)):
                    if self.u[x] == 1 and self.c[x][0] < 0:
                        for key, value in self.item.placesDict.items():
                            for key2, value2 in value.variables.items():
                                print(self.item.variableDict, "variableDict10")

                                self.item.variableDict.update({key2: value2})
                                print(self.item.variableDict, "variableDict11")

                        self.mainWindow.dock_variables.refresh_table()
                # if sum == len(self.c) and sum2 == len(self.c) and sum3 == len(self.c):
                #     s = 0
                #     for x in range(len(self.c)):
                #         s += self.c[x][0]
                #         print("XD")
                #     self.mNew = [self.m[0] + s]
                #     print("XDD", self.mNew)

                    #ustawianie zmiennych
                    # for key, value in self.item.placesDict.items():
                    #     for key2, value2 in value.variables.items():
                    #         self.item.variableDict.update({key2: value2})
                    #
                    # self.mainWindow.dock_variables.refresh_table()



        elif len(self.item.transitionsDict) == 1 and len(self.item.placesDict) > 1:
            if len(self.item.arcsDict) > 0:
                self.c = self.c[0]

                u = []
                uCap = []
                for x in range(len(self.c)):
                    if self.c[x] < 0:
                        if self.m[x] >= abs(self.c[x]):
                            u.append(1)
                        else:
                            u.append(0)
                    else:
                        u.append(1)

                    if self.c[x] > 0:
                        if self.k[x] - self.m[x] >= self.c[x]:
                            uCap.append(1)
                        else:
                            uCap.append(0)
                    else:
                        uCap.append(1)

                    # if self.c[x] == 0:
                    #     u.append(1)
                    #     uCap.append(1)

                sum = 0
                sum2 = 0
                uVar = (self.varActivity())

                for x in range(len(self.m)):
                    sum += u[x]
                    sum2 += uCap[x]

                if sum == len(self.m) and sum2 == len(self.m) and uVar[0] == 1:
                    self.mNew = list(np.add(self.m, self.c))

                    for key, value in self.item.placesDict.items():
                        for key2, value2 in value.variables.items():
                            print(self.item.variableDict, "variableDict12")

                            self.item.variableDict.update({key2: value2})
                            print(self.item.variableDict, "variableDict13")

                    self.mainWindow.dock_variables.refresh_table()




        #aktywnosc ze znakowania
        else:
            temp = []
            sum = 0

            if len(self.c) > 0:
                if len(self.c[0]) > 0:
                    temp = 0
                    for row in range(len(self.c)):
                        for col in range(len(self.c[0])):
                            if self.c[row][col] < 0:
                                if self.m[col] < abs(self.c[row][col]):
                                    temp = 1
                                    break
                                else:
                                    temp = 0
                        if temp == 1:
                            self.u.append(0)
                        else:
                            self.u.append(1)
                        temp = 0

                    self.u = list(np.logical_and(self.u, self.varActivity()))
                    self.u = list(map(int, self.u))

                    self.u = list(np.logical_and(self.u, self.capActivity()))
                    self.u = list(map(int, self.u))

                    a = 0
                    temp1 = 0
                    for y in range(len(self.c[0])):
                        for x in range(len(self.c)):
                            a += self.u[x] * self.c[x][y]
                            if a < 0:
                                temp1 = 1
                        if abs(a) > self.m[y] and temp1 == 1:
                            outArcs = list(self.item.placesDict.values())[y].outArcs
                            info = ""
                            for key, value in enumerate(outArcs.values()):
                                prefix = "T"
                                info += f"{prefix}{list(value[2])[0]} "

                            msgBox = QMessageBox()
                            msgBox.information(self, "Information", "Solve conflict in " + info + "before continuation")
                            self.mNew = self.m
                            self.item.stop_simulationFun()
                            return

                        if a > self.k[y] - self.m[y]:
                            inArcs = list(self.item.placesDict.values())[y].inArcs
                            info = ""
                            for key, value in enumerate(inArcs.values()):
                                prefix = "T"
                                info += f"{prefix}{list(value[1])[0]} "

                            msgBox = QMessageBox()
                            msgBox.information(self, "Information", "Solve conflict in " + info + "before continuation")
                            self.mNew = self.m
                            self.item.stop_simulationFun()
                            return

                        temp1 = 0
                        a = 0

                    self.mNew = list(np.add(self.m, np.matmul(self.u, self.c)))
                    for col in range(len(self.u)):
                        if self.u[col] == 1:
                            for row in range(len(self.c[col])):
                                if self.c[col][row] > 0:
                                    counter = 0
                                    for key, value in self.item.placesDict.items():
                                        if counter == col:
                                            for key2, value2 in value.variables.items():
                                                print(self.item.variableDict, "variableDict14")

                                                self.item.variableDict.update({key2: value2})
                                                print(self.item.variableDict, "variableDict15")

                                        counter += 1
                                    self.mainWindow.dock_variables.refresh_table()

    def tokenActivity(self):
        temp = []
        u = []
        # if len(self.c) == 1:
        #     self.c = self.c[0]

        for col in range(len(self.c[0])):
            for row in range(len(self.c)):
                if self.c[row][col] < 0:
                    sum += self.c[row][col]
            if sum < 0:
                temp.append(abs(sum))
            else:
                temp.append(999)

            sum = 0

        for col in range(len(self.c)):
            if self.m[col] >= temp[col]:
                u.append(1)
            else:
                u.append(0)

        return u


    #przepelnienie
    def capActivity(self):
        uCap = []
        temp1 = 0
        for row in range(len(self.c)):
            for col in range(len(self.c[0])):
                if self.c[row][col] > 0:
                    if self.k[col] - self.m[col] < self.c[row][col]:
                        temp1 = 1
                        break
                    else:
                        temp1 = 0
            if temp1 == 1:
                uCap.append(0)
            else:
                uCap.append(1)
            temp1 = 0

        return uCap

    #aktywnosc ze zmiennych
    def varActivity(self):
        varC = []
        for key, value in self.item.transitionsDict.items():
            if value.variables != "":
                print(self.item.variableDict, "variableDict16")

                a = parser(value.variables, self.item.variableDict)

                print(self.item.variableDict, "variableDict17")

                varC.append(int(a))
            else:
                varC.append(1)
        return varC


    def refresh(self):
        for col in range(len(self.places)):
            self.table_widget.setItem(0, col, QTableWidgetItem(str((self.places[col]).tokens)))



