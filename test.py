import sys
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class MyLine(QLine):
    def __init__(self):
        super().__init__()

    def paintEvent(self):
        b = QPoint(0, 0)
        e = QPoint(500, 500)
        print(self)
        painter = QPainter(self)
        pen = QPen(Qt.red, 3)
        painter.setPen(pen)
        line = QLine(b, e)
        painter.drawLine(line)
        # painter.drawRect(100, 15, 400, 200)
