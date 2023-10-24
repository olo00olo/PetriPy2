from PyQt5.QtCore import QPointF, QRectF, Qt
from PyQt5.QtWidgets import QGraphicsItem, QGraphicsTextItem


class Node(QGraphicsItem):
    Type = QGraphicsItem.UserType + 1

    def __init__(self, graphWidget):
        super(Node, self).__init__()

        self.graph = graphWidget
        self.edgeList = []
        self.newPos = QPointF()

        self.label = None
        # self.tokens = None

        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)
        self.setZValue(1)

        # self.active = False
        self.inArcs = {}
        self.outArcs = {}

    # def token(self):
    #     self.tokens = QGraphicsTextItem("0", self)
    #     self.tokens.setPos(-7, -11)

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