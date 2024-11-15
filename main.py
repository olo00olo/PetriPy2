import math

from PyQt5.QtCore import (QRectF, Qt, pyqtSignal, pyqtSlot, QSize)
from PyQt5.QtGui import (QPainter, QKeySequence, QIcon)
from PyQt5.QtWidgets import (QGraphicsItem, QGraphicsScene,
                             QGraphicsView, QPushButton, QMessageBox, QMenu, QAction, QShortcut)

from Edge import Edge
from Loader import loader
from Matrix import Matrix
from NewArc import NewArc
from Place import Place
from Saver import saver
from Simulator import Simulator
from Transition import Transition


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
        self.parent = parent
        self.scene = QGraphicsScene(self)
        self.scene.setItemIndexMethod(QGraphicsScene.NoIndex)
        self.scene.setSceneRect(-200, -200, 800, 800)

        self.setScene(self.scene)
        self.setCacheMode(QGraphicsView.CacheBackground)
        # self.setViewportUpdateMode(QGraphicsView.BoundingRectViewportUpdate)
        self.setRenderHint(QPainter.Antialiasing)
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorViewCenter)

        self.addPlaceBtn = QPushButton(self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)
        self.addPlaceBtn.clicked.connect(self.setActiveButton)
        self.addPlaceBtn.setIcon(QIcon("./icons/circle.png"))
        self.addPlaceBtn.setFixedSize(50, 50)
        self.addPlaceBtn.setIconSize(QSize(40, 40))


        self.addTransitionBtn = QPushButton("", self)
        self.addTransitionBtn.move(55, 5)
        self.addTransitionBtn.setCheckable(True)
        self.addTransitionBtn.clicked.connect(self.setActiveButton)
        self.addTransitionBtn.setIcon(QIcon("./icons/rectangle.png"))
        self.addTransitionBtn.setFixedSize(50, 50)
        self.addTransitionBtn.setIconSize(QSize(40, 40))


        self.addArcButton = QPushButton("", self)
        self.addArcButton.move(105, 5)
        self.addArcButton.setCheckable(True)
        self.addArcButton.clicked.connect(self.setActiveButton)
        self.addArcButton.setIcon(QIcon("./icons/arc.png"))
        self.addArcButton.setFixedSize(50, 50)
        self.addArcButton.setIconSize(QSize(40, 40))

        # self.saveNetButton = QPushButton("save net", self)
        # self.saveNetButton.move(455, 5)
        # self.saveNetButton.clicked.connect(lambda: saver(self, "file"))


        self.start_simulation_button = QPushButton("", self)
        self.start_simulation_button.move(205, 5)
        self.start_simulation_button.setCheckable(True)
        self.start_simulation_button.clicked.connect(self.start_simulationFun)
        self.start_simulation_button.setIcon(QIcon("./icons/play.png"))
        self.start_simulation_button.setFixedSize(50, 50)
        self.start_simulation_button.setIconSize(QSize(40, 40))


        self.step_button = QPushButton("", self)
        self.step_button.move(255, 5)
        self.step_button.setCheckable(False)
        self.step_button.clicked.connect(self.step_forward)
        self.step_button.setIcon(QIcon("./icons/step.png"))
        self.step_button.setFixedSize(50, 50)
        self.step_button.setIconSize(QSize(40, 40))

        self.stop_simulation = QPushButton("", self)
        self.stop_simulation.move(355, 5)
        self.stop_simulation.setCheckable(False)
        self.stop_simulation.clicked.connect(self.stop_simulationFun)
        self.stop_simulation.setIcon(QIcon("./icons/stop.png"))
        self.stop_simulation.setFixedSize(50, 50)
        self.stop_simulation.setIconSize(QSize(40, 40))
        self.stop_simulation.setEnabled(False)

        self.pause_simulation = QPushButton("", self)
        self.pause_simulation.move(305, 5)
        self.pause_simulation.setCheckable(False)
        self.pause_simulation.clicked.connect(self.pause_simulationFun)
        self.pause_simulation.setIcon(QIcon("./icons/pause.png"))
        self.pause_simulation.setFixedSize(50, 50)
        self.pause_simulation.setIconSize(QSize(40, 40))
        self.pause_simulation.setEnabled(False)









        undoShortcut = QShortcut(QKeySequence('Ctrl+Z'), self)
        undoShortcut.activated.connect(self.undo)

        redoShortcut = QShortcut(QKeySequence('Ctrl+Y'), self)
        redoShortcut.activated.connect(self.redo)

        self.undoHeap = ['{"places": {}, "transitions": {}, "arcs": {}, "var": {}']
        self.redoHeap = []

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

        self.matrix = Matrix(self, self.parent)
        self.simulator = Simulator(self)

        # loader(self, "file")

        self.variableDict = {}
        self.simulator.trigger.connect(self.timerFun)

        self.beforeSimNet = None


    def setActiveButton(self):
        self.n.reset()
        if self.activeElement is not None:
            self.activeElement.setActivated(False)
            self.activeElement = None
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
        saver(self, "file")

    def loadNet(self):
        self.undoHeap = ['{"places": {}, "transitions": {}, "arcs": {}, "var": {}']
        self.redoHeap = []

        loader(self, 'file')

        self.undoHeap.append(saver(self, "heap"))
        self.redoHeap = []



    def undo(self):
        if not self.stop_simulation.isEnabled():
            if len(self.undoHeap) > 1:
                self.redoHeap.append(self.undoHeap[-1])
                self.undoHeap.pop(-1)
                loader(self, self.undoHeap[-1])

    def redo(self):
        if not self.stop_simulation.isEnabled():
            if self.redoHeap:
                self.undoHeap.append(self.redoHeap[-1])
                loader(self, self.redoHeap[-1])
                self.redoHeap.pop(-1)

    # def keyPressEvent(self, event):
    # print(self.activeElement.active)
    # self.activeElement.active = False
    # self.activeElement.update()
    # self.start()

    # for element in self.activeElements:
    #     print(element)
    #     element.active = False
    #     element.setActivated(False)
    # key = event.key()

    def showMatrix(self):
        self.matrix.combo()
        self.matrix.show()

    def step_forward(self):
        if self.beforeSimNet is None:
            self.beforeSimNet = saver(self, "heap")
        self.stop_simulation.setEnabled(True)

        self.matrix.combo()
        mNew = self.matrix.mNew

        if mNew:
            counter = 0
            for key, value in self.placesDict.items():
                value.setToken(mNew[counter])
                counter += 1

        # self.matrix.show()
        self.matrix.refresh()
    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Q:
            # self.a = Matrix(self)
            pass
            # a.setGeometry(100, 100, 800, 600)

        if event.key() == Qt.Key_Space:
            pass
            print(self.undoHeap)
            # self.step_forward()

        # #start sim
        # if event.key() == Qt.Key_W:
        #     self.simulator.start_simulation()
        #
        # #stop sim
        # if event.key() == Qt.Key_S:
        #     self.simulator.stop_simulation()

        #faster
        if event.key() == Qt.Key_D:
            self.simulator.change_speed(decrement=100)

        #slower
        if event.key() == Qt.Key_A:
            self.simulator.change_speed(decrement=-100)

    #     if event.key() == Qt.Key_E:
    #         self.showVariables()
    #
    #
    #
    # def showVariables(self):
    #     self.initVariables.updateVariables()
    #     self.initVariables.show()

    def start_simulationFun(self):
        self.start_simulation_button.setChecked(True)
        self.simulator.start_simulation()

        self.step_button.setEnabled(False)
        self.addArcButton.setEnabled(False)
        self.addPlaceBtn.setEnabled(False)
        self.addTransitionBtn.setEnabled(False)
        self.start_simulation_button.setEnabled(False)
        self.stop_simulation.setEnabled(True)
        self.pause_simulation.setEnabled(True)


        if self.beforeSimNet is None:
            self.beforeSimNet = saver(self, "heap")

    def pause_simulationFun(self):
        self.step_button.setEnabled(True)
        self.start_simulation_button.setEnabled(True)
        self.stop_simulation.setEnabled(True)
        self.pause_simulation.setEnabled(False)

        self.simulator.stop_simulation()



    def stop_simulationFun(self):
        self.start_simulation_button.setChecked(False)
        self.simulator.stop_simulation()

        self.step_button.setEnabled(True)
        self.addArcButton.setEnabled(True)
        self.addPlaceBtn.setEnabled(True)
        self.addTransitionBtn.setEnabled(True)
        self.stop_simulation.setEnabled(False)
        self.start_simulation_button.setEnabled(True)
        self.pause_simulation.setEnabled(False)



        loader(self, self.beforeSimNet)
        self.beforeSimNet = None
        self.parent.dock_variables.loadValue()

    @pyqtSlot()
    def timerFun(self):

        self.step_forward()

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

        self.undoHeap.append(saver(self, "heap"))
        self.redoHeap = []

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
                        self.activeElementChanged.emit(item)

                    elif isinstance(item, (Transition, Place)) and item.active is True:
                        item.setActivated(False)
                        self.activeElement = None
                        self.activeElementChanged.emit(None)

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


                # print(self.undoHeap)
                self.undoHeap.append(saver(self, "heap"))
                self.redoHeap = []
                # print(self.undoHeap)

            # add transition
            if self.activeState == 2:
                newTransition = Transition(self)
                newTransition.setPos(self.mapToScene(event.pos()))
                self.scene.addItem(newTransition)
                self.transitions.append(newTransition)
                self.transitionsDict.update({newTransition.id: newTransition})

                self.undoHeap.append(saver(self, "heap"))
                self.redoHeap = []


            # add arc
            if self.activeState == 3:
                source, destination, error = self.n.setNode(items)
                for key, value in self.arcsDict.items():
                    if list(value[1].values())[0] is source and list(value[2].values())[0] is destination:
                        error = 2
                        break
                    if list(value[1].values())[0] is destination and list(value[2].values())[0] is source:
                        error = 3
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

                        self.undoHeap.append(saver(self, "heap"))
                        self.redoHeap = []

                elif error == 1:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Can't connect same type nodes")

                elif error == 2:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "This arc already exist")

                elif error == 3:
                    self.n.reset()
                    msgBox = QMessageBox()
                    msgBox.information(self, "Information", "Can't add reversed arc")

        elif event.button() == Qt.MouseButton.RightButton:
            for item in items:
                if isinstance(item, (Transition, Place, Edge)):
                    # print(item.id, item.variables)
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

#TODO:
#zmiejszyc czcionke
#przyciski zmieniajace czas/wybor czasu
#rysowanie lukow
#przyklad
#ten blad
#w ktyorym miejscu konflikt
#stan sieci sprzed symulacji
#zmienna nie dziala
#brak mozliwosc zmiany polozenia w trakcie symulacji
#nieaktywne undo/redo w menu podczas symulacji