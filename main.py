import math

from PyQt5.QtCore import (QLineF, QPointF, QRectF, QSizeF, Qt)
from PyQt5.QtGui import (QBrush, QColor, QPainter,
                         QPainterPath, QPen, QPolygonF, QRadialGradient)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QStyle, QPushButton, QGraphicsTextItem)


class Edge(QGraphicsItem):
    Pi = math.pi
    TwoPi = 2.0 * Pi

    Type = QGraphicsItem.UserType + 2

    def __init__(self, sourceNode, destNode):
        super(Edge, self).__init__()

        self.arrowSize = 10.0
        self.sourcePoint = QPointF()
        self.destPoint = QPointF()

        self.setAcceptedMouseButtons(Qt.NoButton)
        self.source = sourceNode
        self.dest = destNode
        self.source.addEdge(self)
        self.dest.addEdge(self)
        self.adjust()

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

    def adjust(self):
        if not self.source or not self.dest:
            return

        line = QLineF(self.mapFromItem(self.source, 0, 0),
                      self.mapFromItem(self.dest, 0, 0))
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

    def boundingRect(self):
        if not self.source or not self.dest:
            return QRectF()

        penWidth = 1.0
        extra = (penWidth + self.arrowSize) / 2.0

        return QRectF(self.sourcePoint,
                      QSizeF(self.destPoint.x() - self.sourcePoint.x(),
                             self.destPoint.y() - self.sourcePoint.y())).normalized().adjusted(-extra, -extra, extra,
                                                                                               extra)

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


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget):
        super(Node, self).__init__()

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QPointF()

        self.label = None
        self.tokens = None

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

    # TODO: scaling and moving
    def labels(self):
        self.label = QGraphicsTextItem("P1", self)
        self.label.setPos(-20, -25)

    def token(self):
        self.tokens = QGraphicsTextItem("0", self)
        self.tokens.setPos(-7, -11)

    @staticmethod
    def type(self):
        return Node.Type

    def addEdge(self, edge):
        self.edgeList.append(edge)
        edge.adjust()

    def edges(self):
        return self.edgeList

    def advance(self):
        if self.newPos == self.pos():
            return False

        self.setPos(self.newPos)
        return True

    def boundingRect(self):
        adjust = 2.0
        return QRectF(-10 - adjust, -10 - adjust, 23 + adjust, 23 + adjust)

    # def shape(self):
    #     path = QPainterPath()
    #     path.addEllipse(-10, -10, 20, 20)
    #     return path
    #
    # def paint(self, painter, option, widget):
    #     painter.setPen(Qt.NoPen)
    #     painter.drawEllipse(-7, -7, 20, 20)
    #     gradient = QRadialGradient(-3, -3, 10)
    #     if option.state & QStyle.State_Sunken:
    #         gradient.setCenter(3, 3)
    #         gradient.setFocalPoint(3, 3)
    #         gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
    #     else:
    #         gradient.setColorAt(0, Qt.yellow)
    #
    #     painter.setBrush(QBrush(gradient))
    #     painter.setPen(QPen(Qt.black, 0))
    #     painter.drawEllipse(-10, -10, 20, 20)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for edge in self.edgeList:
                edge.adjust()

        return super(Node, self).itemChange(change, value)

    def mousePressEvent(self, event):
        self.update()
        super(Node, self).mousePressEvent(event)

    def mouseReleaseEvent(self, event):
        self.update()
        super(Node, self).mouseReleaseEvent(event)


class Place(Node):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget):
        super().__init__(graphWidget)
        self.labels()
        self.token()

    def shape(self):
        path = QPainterPath()
        path.addEllipse(-10, -10, 20, 20)
        return path

    def paint(self, painter, option, widget):
        painter.setPen(Qt.NoPen)
        painter.drawEllipse(-7, -7, 20, 20)

        gradient = QRadialGradient(-3, -3, 10)
        if option.state & QStyle.State_Sunken:
            gradient.setCenter(3, 3)
            gradient.setFocalPoint(3, 3)
            gradient.setColorAt(0, QColor(Qt.darkYellow).lighter(120))
        else:
            gradient.setColorAt(0, Qt.red)

        painter.setBrush(QBrush(gradient))
        painter.setPen(QPen(Qt.black, 0))
        painter.drawEllipse(-10, -10, 20, 20)


class GraphWidget(QGraphicsView):
    def __init__(self):
        super(GraphWidget, self).__init__()

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 600, 600)

        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)

        node1 = Place(self)
        self.scene.addItem(node1)
        node1.setPos(0, 0)

        node2 = Place(self)
        self.scene.addItem(node2)
        node2.setPos(50, 50)

        self.scene.addItem(Edge(node1, node2))

        self.scale(1.8, 1.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("Elastic Nodes")

        self.rightButtonPressed = False
        self.panStartX = None
        self.panStartY = None

    def keyPressEvent(self, event):
        key = event.key()
        print(key)

    def mousePressEvent(self, event):
        items = self.items(event.pos())
        if items and isinstance(items[0], QGraphicsItem):
            QGraphicsView.mousePressEvent(self, event)
            return

        if event.button() == Qt.MouseButton.LeftButton:
            if self.addPlaceBtn.isChecked():
                newPlace = Node(self)
                newPlace.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newPlace)

    #
    #     elif event.button() == Qt.MouseButton.RightButton:
    #         self.rightButtonPressed = True
    #         self.panStartX = event.x()
    #         self.panStartY = event.y()
    #         self.setCursor(Qt.ClosedHandCursor);
    #         event.accept()
    #
    #     elif event.button() == Qt.MouseButton.MiddleButton:
    #         self.centerOn(event.pos())
    #
    # def mouseMoveEvent(self, event):
    #     items = self.items(event.pos())
    #     if items and isinstance(items[0], QGraphicsItem):
    #         QGraphicsView.mouseMoveEvent(self, event)
    #         return
    #     if self.rightButtonPressed:
    #         self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self.panStartX))
    #         self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self.panStartY))
    #         self.panStartX = event.x()
    #         self.panStartY = event.y()
    #         event.accept()
    #
    #
    # def mouseReleaseEvent(self, event):
    #     items = self.items(event.pos())
    #     if items and isinstance(items[0], QGraphicsItem):
    #         QGraphicsView.mouseReleaseEvent(self, event)
    #         return
    #     if event.button() == Qt.MouseButton.RightButton:
    #         self.rightButtonPressed = False
    #         self.setCursor(Qt.ArrowCursor)
    #         event.accept()

    def wheelEvent(self, event):
        self.scaleView(math.pow(2.0, -event.angleDelta().y() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    widget = GraphWidget()
    widget.show()

    sys.exit(app.exec_())
