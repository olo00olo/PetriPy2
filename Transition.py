import itertools

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainterPath, QRadialGradient, QColor, QBrush, QPen
from PyQt5.QtWidgets import QGraphicsItem, QStyle, QGraphicsTextItem

from Node import Node


class Transition(Node):
    Type = QGraphicsItem.UserType + 1
    newid = itertools.count(1)

    def __init__(self, graphWidget):
        super().__init__(graphWidget)

        self.id = next(self.newid)

        self.labels()
        self.token()

        self.active = False

    def labels(self):
        text = str(self.id)
        text = "T" + text
        self.label = QGraphicsTextItem(text, self)
        self.label.setPos(-20, -25)

    def shape(self):
        path = QPainterPath()
        path.addRect(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.drawRect(-7, -7, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken or self.active:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.red)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawRect(-10, -10, 10, 20)