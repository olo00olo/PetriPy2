from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRadialGradient, QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem, QStyle, QGraphicsTextItem

from Node import Node

import itertools

class Place(Node):
    # Type = QGraphicsItem.UserType + 1
    counter = 0
    def __init__(self, graphWidget):
        super().__init__(graphWidget)

        self.id = Place.counter
        Place.counter += 1

        self.labels()
        self.token()

        self.active = False

    def setId(self, id):
        self.id = id
        print(self.id)

    def setActivated(self, bool):
        self.active = bool
        print(self.active)

    def labels(self):
        text = str(self.id)
        text = "P" + text
        self.label = QGraphicsTextItem(text, self)
        self.label.setPos(-20, -25)

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        print(self.active, "Place")
        if option.state & QStyle.State_Sunken or self.active is True:

            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.blue)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)


