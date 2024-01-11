from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRadialGradient, QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem, QStyle, QGraphicsTextItem, QFormLayout, QLineEdit

from Node import Node

import itertools

class Place(Node):
    # Type = QGraphicsItem.UserType + 1
    counter = 1

    def __init__(self, graphWidget):
        super().__init__(graphWidget)

        self.id = Place.counter
        Place.counter += 1

        self.tokens = 0
        self.capacityValue = 1
        self.variables = {}
        # self.variables = {"x": bool(1), "y": bool(0)}
        # self.variables = {"x": bool(1)}

        self.label = QGraphicsTextItem("", self)



        # self.tokens = (self.tokens)

        self.labels()

        self.tokensInit()
        # self.token()

        self.capacityInit()
        self.capacity()

        self.active = False

        self.variablesTextItems = []
        self.variablesPrint()





    def tokensInit(self):
        self.tokenTextItem = QGraphicsTextItem(str(self.tokens), self)
        self.tokenTextItem.hide()

    def capacityInit(self):
        self.capacityTextItem = QGraphicsTextItem(str(self.capacityValue), self)

        # self.capacityTextItem.setPos(-7, -5)
        self.fractionLine = QGraphicsTextItem(chr(95), self)

    def token(self):
        self.tokenTextItem.setPlainText(str(self.tokens))
        # if self.tokens == 1 and self.capacityValue == 1:


    def variablesPrint(self):
        print(self.variables)
        posOffset = 0

        for v in self.variablesTextItems:
            v.deleteLater()
        self.variablesTextItems = []

        for key, value in self.variables.items():
            self.var = QGraphicsTextItem(str(key) + ":", self)
            self.var.setPos(0, posOffset)
            self.variablesTextItems.append(self.var)

            self.varValue = QGraphicsTextItem(str(int(value)), self)
            self.varValue.setPos(12, posOffset)
            self.variablesTextItems.append(self.varValue)
            posOffset += 10




    def capacity(self):
        self.capacityValue = int(self.capacityValue)
        self.fractionLine.hide()
        self.capacityTextItem.hide()
        self.tokenTextItem.hide()
        self.capacityTextItem.setPos(-7, -11)

        if self.capacityValue == 1:
            self.tokenTextItem.show()
            self.tokenTextItem.setPos(-7, -11)

        elif self.capacityValue > 1:
            self.fractionLine.show()
            self.capacityTextItem.show()
            self.tokenTextItem.show()

            self.tokenTextItem.setPos(-7, -15)
            self.fractionLine.setPos(-7, -15)
            self.capacityTextItem.setPos(-7, -5)
            self.capacityTextItem.setPlainText(str(self.capacityValue))

    def setCapacity(self, value):
        self.capacityValue = value
        self.capacity()

    def setToken(self, value):
        self.tokens = value
        self.token()

    def addVariable(self, edit, variable):
        print(edit, variable, "VAR")

    def setId(self, id):
        self.id = id
        self.labels()
        # print(self.id)

    def setActivated(self, bool):
        self.active = bool
        self.update()

    def labels(self):
        text = str(self.id)
        text = "P" + text
        self.label.setPlainText(text)
        self.label.setPos(-20, -25)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        print(self, self.active, "Place")
        if option.state & QStyle.State_Sunken or self.active is True:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.blue)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)


