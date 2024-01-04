import itertools
import math

from PyQt5.QtCore import QPointF, Qt, QLineF, QRectF, QSizeF
from PyQt5.QtGui import QPen, QPolygonF
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem


class Edge(QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QGraphicsItem.UserType + 2

    counter = 0

    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()

        self.id = Edge.counter
        Edge.counter += 1

        self.weightValue = 1
        self.weightInit()

        self.arrowSize = 6.0
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

        self.active = False



    def setActivated(self, bool):

        self.active = bool
        self.update()

    def weightInit(self):
        self.weightTextItem = QGraphicsTextItem(str(self.weightValue), self)


    def weight(self):
        self.weightValue = int(self.weightValue)

        self.weightTextItem.setPlainText(str(self.weightValue))
        # self.weightTextItem.setPos(0, -50)
        print("222")

    def setWeight(self, value):
        self.weightValue = value
        self.weight()
    def type(self):
        return Edge.Type

    def sourceNode(self):
        return self.source

    def setSourceNode(self, node):
        self.source = node
        self.adjust()

    def destNode(self):
        return self.dest

    def setDestNode(self, node):
        self.dest = node
        self.adjust()

    def findNearest(self):
        lenList = []
        lineList = []

        l = [QPointF(-2.5, 0), QPointF(2.5, 0), QPointF(0, -2.5), QPointF(0, 2.5)]

        for e in l:
            for i in l:
                line = QLineF(self.mapFromItem(self.source, e),
                                      self.mapFromItem(self.dest, i))
                lenList.append(line.length())
                lineList.append(line)

        m = min(lenList)
        for e in lineList:
            if m == e.length():
                return e



    def adjust(self):
        if not self.source or not self.dest:
            return

        # self.findNearest()
        line = self.findNearest()

        # line = QLineF(self.mapFromItem(self.source, 0, 0),
        #               self.mapFromItem(self.dest, 0, 0))
        length = line.length()



        self.prepareGeometryChange()

        if length > 20.0:
            edgeOffset = QPointF((line.dx() * 10) / length,
                                 (line.dy() * 10) / length)

            self.sourcePoint = line.p1() + edgeOffset
            self.destPoint = line.p2() - edgeOffset

        else:
            self.sourcePoint = line.p1()
            self.destPoint = line.p1()

        self.weightTextItem.setPos(line.center())

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()

        penWidth = 1.0
        extra = (penWidth + self.arrowSize) / 2.0

        return QRectF(self.sourcePoint,
                      QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                             self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra,
                                                                                               extra)

    # TODO: active edge highlight
    def paint(self, painter, option, widget):
        if not self.source or not self.dest:
            return

        # Draw the line itself.
        line = QLineF(self.sourcePoint, self.destPoint)

        if line.length() == 0.0:
            return

        painter.setPen(QPen(Qt.black, 1, Qt.SolidLine, Qt.RoundCap,
                            Qt.RoundJoin))
        painter.drawLine(line)

        # Draw the arrows if there's enough room.
        angle = math.acos(line.dx() / line.length())
        if line.dy() >= 0:
            angle = Edge.TwoPi - angle

        # sourceArrowP1 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi / 3) * self.arrowSize,
        #                                            math.cos(angle + Edge.Pi / 3) * self.arrowSize)
        # sourceArrowP2 = self.sourcePoint + QPointF(math.sin(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize,
        #                                            math.cos(angle + Edge.Pi - Edge.Pi / 3) * self.arrowSize);
        destArrowP1 = self.destPoint + QPointF(math.sin(angle - Edge.Pi / 3) * self.arrowSize,
                                               math.cos(angle - Edge.Pi / 3) * self.arrowSize)
        destArrowP2 = self.destPoint + QPointF(math.sin(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize,
                                               math.cos(angle - Edge.Pi + Edge.Pi / 3) * self.arrowSize)

        painter.setBrush(Qt.black)
        # painter.drawPolygon(QPolygonF([line.p1(), sourceArrowP1, sourceArrowP2]))
        painter.drawPolygon(QPolygonF([line.p2(), destArrowP1, destArrowP2]))