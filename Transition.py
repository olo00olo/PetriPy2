import itertools

from PyQt5.QtCore import Qt, QRectF
from PyQt5.QtGui import QPainterPath, QRadialGradient, QColor, QBrush, QPen, QFont
from PyQt5.QtWidgets import QGraphicsItem, QStyle, QGraphicsTextItem

from Node import Node


class Transition(Node):
    Type = QGraphicsItem.UserType + 1

    counter = 1

    def __init__(self, graphWidget):
        super().__init__(graphWidget)

        self.id = Transition.counter
        Transition.counter += 1

        self.font = QFont()
        self.font.setPointSize(12)


        self.label = QGraphicsTextItem("text", self)
        self.label.setFont(self.font)


        self.labels()

        self.active = False

        self.variables = ""
        self.variablesTextItem = QGraphicsTextItem("", self)


    def setId(self, id):
        self.id = id
        self.labels()

    def labels(self):
        text = str(self.id)
        text = "T" + text
        self.label.setPlainText(text)
        self.label.setPos(-30, -36)

    def shape(self):
        path = QPainterPath()
        path.addRect(-10, -10, 20, 30)
        return path

    def setActivated(self, bool):
        self.active = bool
        self.update()

    def setVariables(self, s):
        self.variables = s
        self.variablesTextItem.setPlainText(s)
    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.drawRect(-10, -10, 20, 30)

        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken or self.active:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.red)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawRect(QRectF(-7.5, -15, 15, 30))