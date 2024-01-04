import json
import math
import PyQt5

from PyQt5.QtCore import (QRectF, Qt, pyqtSignal)
from PyQt5.QtGui import (QPainter)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QPushButton, QMessageBox, QMenu, QAction, QDialog)

from Edge import Edge
from Loader import loader
from Matrix import Matrix
from NewArc import NewArc
from Place import Place
from Transition import Transition
from mainWindow import MainWindow
from Saver import saver


class GraphWidget(QGraphicsView):
    # def __init__(self):
    #     super(GraphWidget, self).__init__()
    signal = pyqtSignal(object)
    activeElementChanged = pyqtSignal(object)

    # mainWindow = MainWindow()

    def __init__(self, parent=None):
        QGraphicsView.__init__(self, parent=parent)

        # self.mainWindow = MainWindow(self)
        # self.activeElementChanged.connect(self.mainWindow.changeMenuLabel)

        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 800, 800)

        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)
        self.addPlaceBtn.clicked.connect(self.setActiveButton)
        # self.addPlaceBtn.setShortcut("Ctrl+Z")

        self.addTransitionBtn = QPushButton("add transition", self)
        self.addTransitionBtn.move(155, 5)
        self.addTransitionBtn.setCheckable(True)
        self.addTransitionBtn.clicked.connect(self.setActiveButton)

        self.addArcButton = QPushButton("add arc", self)
        self.addArcButton.move(305, 5)
        self.addArcButton.setCheckable(True)
        self.addArcButton.clicked.connect(self.setActiveButton)

        self.saveNetButton = QPushButton("save net", self)
        self.saveNetButton.move(455, 5)
        self.saveNetButton.clicked.connect(lambda: saver(self))

        self.scale(1.8, 1.8)
        self.setMinimumSize(400, 400)
        self.setWindowTitle("PetryPy")

        self.rightButtonPressed = False
        self.panStartX = None
        self.panStartY = None

        self.n = NewArc()

        self.placesDict = {}
        self.transitionsDict = {}
        self.arcsDict = {}

        self.places = []
        self.transitions = []
        self.arcs = []
        self.activeState = 0
        self.activeElements = []
        self.activeElement = None

    def setActiveButton(self):
        self.n.reset()
        # self.deactivateAllElements()
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

    # def deactivateAllElements(self):
    #     print(self.activeElements, "XD")
    #     # self.activeElements[0].active = False
    #     for element in self.activeElements:
    #         print(element.active)
    #         element.active = False
    #         # self.activeElements.remove(element)

    def saveNet(self):
        saver(self)

    def loadNet(self):
        loader(self)


    # def keyPressEvent(self, event):
        # print(self.activeElement.active)
        # self.activeElement.active = False
        # self.activeElement.update()
        # print("XD")
        # self.start()

        # for element in self.activeElements:
        #     print(element)
        #     element.active = False
        #     element.setActivated(False)
        # key = event.key()

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            self.a = Matrix(self)
            # a.setGeometry(100, 100, 800, 600)
            self.a.show()
        # event.accept()

    def deleteItem(self, item):
        self.scene.removeItem(item)

        if isinstance(item, Place):
            self.placesDict.pop(item.id)
        elif isinstance(item, Transition):
            self.transitionsDict.pop(item.id)

        if isinstance(item, (Place, Transition)):
            for arcId, arcArr in item.inArcs.items():
                self.arcsDict.pop(arcId)
                self.scene.removeItem(arcArr[0])
                (next(iter(arcArr[1].values()))).outArcs.pop(arcId)

            for arcId, arcArr in item.outArcs.items():
                self.arcsDict.pop(arcId)
                self.scene.removeItem(arcArr[0])
                (next(iter(arcArr[2].values()))).inArcs.pop(arcId)

        elif isinstance(item, Edge):
            (next(iter(self.arcsDict[item.id][1].values()))).outArcs.pop(item.id)
            (next(iter(self.arcsDict[item.id][2].values()))).inArcs.pop(item.id)
            self.arcsDict.pop(item.id)



    # def start(self, obj):
    #
    #     o = MainWindow()
    #     self.signal.connect(o.onJob)
    #     print(obj, "XD")
    #     self.signal.emit(obj)

    def mousePressEvent(self, event):
        items = self.items(event.pos())

        if event.button() == Qt.MouseButton.LeftButton:
            # default state
            if self.activeState == 0:
                itemClicked = 0

                for item in items:
                    if isinstance(item, (Transition, Place, Edge)) and item.active is False:
                        if self.activeElement is not None and item is not self.activeElement:
                            self.activeElement.setActivated(False)
                            self.activeElementChanged.emit(None)
                        self.activeElement = item
                        item.setActivated(True)
                        # self.activeElements.append(item)
                        self.activeElementChanged.emit(item)
                    elif isinstance(item, (Transition, Place)) and item.active is True:
                        item.setActivated(False)
                        # self.activeElement.active = False
                        self.activeElement = None
                        self.activeElementChanged.emit(None)


                        # self.activeElements.remove(item)

                    itemClicked = 1

                if itemClicked == 0:
                    if self.activeElement != None:
                        self.activeElement.setActivated(False)
                        self.activeElement = None
                        self.activeElementChanged.emit(None)


            # add place
            if self.activeState == 1:
                newPlace = Place(self)
                newPlace.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newPlace)
                self.places.append(newPlace)
                self.placesDict.update({newPlace.id: newPlace})
                # print(self.placesDict)

            # add transition
            if self.activeState == 2:
                newTransition = Transition(self)
                newTransition.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newTransition)
                self.transitions.append(newTransition)
                self.transitionsDict.update({newTransition.id: newTransition})

            # add arc
            if self.activeState == 3:
                source, destination, error = self.n.setNode(items)
                for key, value in self.arcsDict.items():
                    if list(value[1].values())[0] is source and list(value[2].values())[0] is destination:
                        error = 2
                        break
                    # elif list(value[1].values())[0] is destination and list(value[2].values())[0] is source:
                    #     error = 2
                    #     break

                if error == 0:
                    if destination is not None:
                        ne = Edge(source, destination)

                        self.scene.addItem(ne)
                        newArc = []
                        newArc.append(ne)
                        newArc.append({self.n.source.id: self.n.source})
                        newArc.append({self.n.destination.id: self.n.destination})
                        self.n.source.outArcs.update({ne.id: newArc})
                        self.n.destination.inArcs.update({ne.id: newArc})
                        self.arcsDict.update({ne.id: newArc})
                        self.arcs.append(newArc)
                        self.n.reset()

                elif error == 1:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Can't connect same type nodes")

                elif error == 2:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "This arc already exists")

        elif event.button() == Qt.MouseButton.RightButton:
            for item in items:
                if isinstance(item, (Transition, Place, Edge)):
                    print(item.id, item.variables)

                    menu = QMenu(self)
                    deleteItem = QAction('Delete', self)
                    deleteItem.triggered.connect(lambda: self.deleteItem(item))
                    menu.addAction(deleteItem)
                    # print(self.mapToScene(event.pos()))
                    menu.popup((self.mapToGlobal(event.pos())))

            # self.rightButtonPressed = True
            self.panStartX = event.x()
            self.panStartY = event.y()
            # self.setCursor(Qt.ClosedHandCursor)
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
        self.scaleView(math.pow(2.0, + event.angleDelta().y() / 240.0))

    def scaleView(self, scaleFactor):
        factor = self.transform().scale(scaleFactor, scaleFactor).mapRect(QRectF(0, 0, 1, 1)).width()

        if factor < 0.07 or factor > 100:
            return

        self.scale(scaleFactor, scaleFactor)
