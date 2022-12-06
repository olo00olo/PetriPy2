import math

from PyQt5.QtCore import (QRectF, Qt, QPoint)
from PyQt5.QtGui import (QPainter)
from PyQt5.QtWidgets import (QApplication, QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QPushButton, QMessageBox)

from Edge import Edge
from NewArc import NewArc
from Node import Node
from Place import Place
from Transition import Transition


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
        self.addPlaceBtn.clicked.connect(self.setActiveButton)

        self.addTransitionBtn = QPushButton("add transition", self)
        self.addTransitionBtn.move(155, 5)
        self.addTransitionBtn.setCheckable(True)
        self.addTransitionBtn.clicked.connect(self.setActiveButton)

        self.addArcButton = QPushButton("add arc", self)
        self.addArcButton.move(305, 5)
        self.addArcButton.setCheckable(True)
        self.addArcButton.clicked.connect(self.setActiveButton)

        self.scale(1.8, 1.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("PetryPy")

        self.rightButtonPressed = False
        self.panStartX = None
        self.panStartY = None

        self.n = NewArc()

        self.places = []
        self.transitions = []
        self.arcs = []
        self.activeState = None

    def setActiveButton(self):
        self.n.reset()
        if self.sender() is self.addPlaceBtn and self.addPlaceBtn.isChecked():
            self.addTransitionBtn.setChecked(False)
            self.addArcButton.setChecked(False)
            self.activeState = 1
        elif self.sender() is self.addTransitionBtn and self.addTransitionBtn.isChecked():
            self.addPlaceBtn.setChecked(False)
            self.addArcButton.setChecked(False)
            self.activeState = 2
        elif self.addArcButton.isChecked():
            self.addPlaceBtn.setChecked(False)
            self.addTransitionBtn.setChecked(False)
            self.activeState = 3
        else:
            self.addPlaceBtn.setChecked(False)
            self.addTransitionBtn.setChecked(False)
            self.addArcButton.setChecked(False)
            self.activeState = 0

    def keyPressEvent(self, event):
        key = event.key()
        print(key)

    def mousePressEvent(self, event):
        items = self.items(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            print(items)
            #default state
            if self.activeState == 0:
                for item in items:
                    if isinstance(item, (Transition, Place)) and item.active is False:
                        item.active = True
                    elif isinstance(item, (Transition, Place)) and item.active is True:
                        item.active = False
            #add place
            if self.activeState == 1:
                newPlace = Place(self)
                newPlace.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newPlace)

            #add transition
            if self.activeState == 2:
                newTransition = Transition(self)
                newTransition.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newTransition)

            #add arc
            if self.activeState == 3:
                source, destination, error = self.n.setNode(items)
                if error is False:
                    print(source, destination)
                    if destination is not None:
                        self.scene.addItem(Edge(source, destination))
                        newArc = []
                        newArc.append(self.n.source)
                        newArc.append(self.n.destination)
                        self.arcs.append(newArc)
                        self.n.reset()
                else:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Can't connect same type nodes")


        elif event.button() == Qt.MouseButton.RightButton:
            self.rightButtonPressed = True
            self.panStartX = event.x()
            self.panStartY = event.y()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()

        elif event.button() == Qt.MouseButton.MiddleButton:
            self.centerOn(event.pos())

        if items and isinstance(items[0], QGraphicsItem):
            QGraphicsView.mousePressEvent(self, event)
            return

    def mouseMoveEvent(self, event):
        # self.setActiveButton()
        if self.rightButtonPressed:
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - (event.x() - self.panStartX))
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - (event.y() - self.panStartY))
            self.panStartX = event.x()
            self.panStartY = event.y()
            event.accept()
        items = self.items(event.pos())
        if items and isinstance(items[0], QGraphicsItem):
            QGraphicsView.mouseMoveEvent(self, event)
            return


    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.RightButton:
            self.rightButtonPressed = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        items = self.items(event.pos())
        if items and isinstance(items[0], QGraphicsItem):
            QGraphicsView.mouseReleaseEvent(self, event)
            return

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
