from PyQt5.QtCore import Qt, pyqtSlot, QSize
from PyQt5.QtGui import QIntValidator, QIcon
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit, QMenu, QWidget, \
    QHBoxLayout, QAction, QFormLayout, QLabel, QMessageBox, QToolBar, QSizePolicy

from Edge import Edge
from Place import Place
from Saver import saver
from Transition import Transition
from VariableWindow import TableWindow
from TransitionVariables import TransitionVariables
# from VariablesDock import VariablesDock
from VariableDock2 import VariablesDock



class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        from main import GraphWidget
        self.linesArray = []
        self.setGeometry(50, 50, 800, 800)

        self.xd = 1
        self.graphWidget = GraphWidget(self)


        self.activeItem = None
        self.tableWindow = None
        self.graphWidget.activeElementChanged.connect(self.setActiveItem)

        self.setWindowTitle("PetryPy")

        self.setWindowIcon(QIcon('./icons/mainIcon.png'))

        # TODO: menu bar
        self.menuBar = self.menuBar()

        file_menu = self.menuBar.addMenu("&File")
        save_action = QAction("&Save", self)
        save_action.triggered.connect(lambda: self.graphWidget.saveNet())
        file_menu.addAction(save_action)

        load_action = QAction("&Open", self)
        load_action.triggered.connect(lambda: self.loadNet())
        file_menu.addAction(load_action)

        view_menu = self.menuBar.addMenu("&View")
        show_dock_action = QAction("&Show menu", self)
        show_dock_action.triggered.connect(lambda: self.dock.show())
        view_menu.addAction(show_dock_action)

        show_matrix = QAction("&Show matrix", self)
        show_matrix.triggered.connect(lambda: self.graphWidget.showMatrix())
        view_menu.addAction(show_matrix)

        show_variables = QAction("&Show variables", self)
        show_variables.triggered.connect(lambda: self.dock_variables.show())
        view_menu.addAction(show_variables)

        edit_menu = self.menuBar.addMenu("&Edit")
        undo_action = QAction("&Undo", self)
        undo_action.triggered.connect(lambda: self.graphWidget.undo())
        edit_menu.addAction(undo_action)

        redo_action = QAction("&Redo", self)
        redo_action.triggered.connect(lambda: self.graphWidget.redo())
        edit_menu.addAction(redo_action)



        self.dock = QDockWidget("menu", self)
        self.dock.setMinimumWidth(250)
        # self.dock.setFloating(True)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.verticalLayout = QVBoxLayout()

        self.dockedWidget = QWidget(self)
        self.dockedWidget.setLayout(self.verticalLayout)

        self.dock.setWidget(self.dockedWidget)

        #
        # self.dock_variables = QDockWidget("variables", self)
        # self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_variables)


        self.dock_variables = VariablesDock(self, self.graphWidget)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock_variables)







        self.menuItem = None
        # self.labell = QLabel(str(self.menuItem))
        self.labell = QLabel("None item selected")
        self.verticalLayout.addWidget(self.labell)



        #
        # self.horizontalLayout = QHBoxLayout()
        #
        # self.removeLineBtn = QPushButton("-", self)
        #
        # edit = QLineEdit(self)
        # self.linesArray.append(edit)
        # self.horizontalLayout.addWidget(edit)
        # self.horizontalLayout.addWidget(self.removeLineBtn)
        # self.removeLineBtn.clicked.connect(lambda: self.removeLine(self.horizontalLayout))
        # self.verticalLayout.addLayout(self.horizontalLayout)


        self.setCentralWidget(self.graphWidget)

        self.f1 = QFormLayout()
        self.f2 = QFormLayout()

        # self.dock.setVisible(False)
        # self.dock.hide()

        # toolbar = QToolBar(self)
        # toolbar.setFixedHeight(50)
        # # toolbar.setFixedWidth(100)
        # toolbar.setMovable(False)
        # spacer = QWidget(self)
        # spacer.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        # toolbar.addWidget(spacer)
        # self.addToolBar(toolbar)
        #
        # akcja1 = QAction('Akcja 1', self)
        # ikon1 = QIcon("./icons/circle.png")
        # ikon1.actualSize(QSize(50,50))
        # akcja1.setIcon(ikon1)
        # # akcja1.triggered.connect(self.akcja1_triggered)
        # toolbar.addAction(akcja1)


        # remove_button.setIcon(QIcon("./icons/bin.png"))


    def loadNet(self):
        self.graphWidget.loadNet()
        self.dock_variables.loadValue()




    def placeEditor(self):
        if self.activeItem is not None and isinstance(self.activeItem, Place):
            editVariablesBtn = QPushButton("Edit variables", self)
            editVariablesBtn.clicked.connect(self.openVariableTable)

            self.labell = QLabel()
            # self.verticalLayout.addWidget(self.labell)

            onlyInt = QIntValidator()
            onlyInt.setRange(0, 9)

            self.capacityLabel = QLabel()
            self.capacityLabel.setText("Capacity: ")
            self.capacityValue = QLineEdit(self)
            self.capacityValue.setText(str(self.activeItem.capacityValue))
            self.capacityValue.setValidator(onlyInt)
            self.capacityValue.editingFinished.connect(self.setPlaceCapacity)

            self.f1.addRow(self.capacityLabel, self.capacityValue)

            self.tokenLabel = QLabel()
            self.tokenLabel.setText("Token: ")
            self.tokenValue = QLineEdit(self)
            self.tokenValue.setText(str(self.activeItem.tokens))
            self.tokenValue.setValidator(onlyInt)
            self.tokenValue.editingFinished.connect(self.setPlaceToken)

            self.f2.addRow(self.tokenLabel, self.tokenValue)
            # self.verticalLayout.addWidget(self.labell)
            self.verticalLayout.addLayout(self.f2)
            self.verticalLayout.addLayout(self.f1)

            self.verticalLayout.addWidget(editVariablesBtn)
            self.verticalLayout.setAlignment(Qt.AlignTop)


        elif self.activeItem is not None and isinstance(self.activeItem, Transition):
            print("XDDD")
            self.labell = QLabel()

            editVariablesBtn = QPushButton("Edit variables", self)
            editVariablesBtn.clicked.connect(self.openTransitionVariables)

            self.verticalLayout.addWidget(editVariablesBtn)
            self.verticalLayout.setAlignment(Qt.AlignTop)

        elif self.activeItem is not None and isinstance(self.activeItem, Edge):
            self.labell = QLabel()

            onlyInt = QIntValidator()
            onlyInt.setRange(1, 9)
            self.weightLabel = QLabel()
            self.weightLabel.setText("Weight: ")
            self.weightValue = QLineEdit(self)
            self.weightValue.setText(str(self.activeItem.weightValue))
            self.weightValue.setValidator(onlyInt)
            self.weightValue.editingFinished.connect(self.setArcWeight)

            self.f1 = QFormLayout()
            self.f1.addRow(self.weightLabel, self.weightValue)

            self.verticalLayout.addLayout(self.f1)
            self.verticalLayout.setAlignment(Qt.AlignTop)





        else:
            for i in reversed(range(self.verticalLayout.count())):
                widget = self.verticalLayout.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            for i in reversed(range(self.f1.count())):
                widget = self.f1.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()
            for i in reversed(range(self.f2.count())):
                widget = self.f2.itemAt(i).widget()
                if widget is not None:
                    widget.deleteLater()

            self.labell.setText("None item selected")
            self.verticalLayout.addWidget(self.labell)

    def openVariableTable(self):
        if isinstance(self.activeItem, Place):
            if self.activeItem.capacityValue == 1:
                self.a = TableWindow(self.activeItem, self.graphWidget, self)
                self.a.setGeometry(100, 100, 325, 300)
                self.a.setFixedSize(325, 300)
                self.a.setWindowModality(Qt.ApplicationModal)
                self.a.show()

            else:
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Can't open variable editor if capacity is greater than 0")

    def openTransitionVariables(self):
        if isinstance(self.activeItem, Transition):

            self.transitionVariablesWindow = TransitionVariables(self.activeItem, self.graphWidget, self)
            self.transitionVariablesWindow.setWindowModality(Qt.ApplicationModal)
            self.transitionVariablesWindow.setGeometry(100, 100, 325, 300)
            self.transitionVariablesWindow.setFixedSize(325, 300)
            self.transitionVariablesWindow.show()


    def addLine(self):
        # variableWindow = TableWindow()
        # variableWindow.show()
        horizontalLayout = QHBoxLayout()
        removeLineBtn = QPushButton("-", self)
        edit = QLineEdit(self)
        edit.textChanged.connect(lambda: self.activeItem.addVariable(edit, edit.text()))
        self.linesArray.append([horizontalLayout, edit, removeLineBtn])
        horizontalLayout.addWidget(edit)
        horizontalLayout.addWidget(removeLineBtn)
        removeLineBtn.clicked.connect(lambda: self.removeLine(horizontalLayout, edit, removeLineBtn))
        self.verticalLayout.addLayout(horizontalLayout)

    def removeLine(self, line, edit, btn):
        edit.deleteLater()
        btn.deleteLater()
        # line.setParent(None)
        line.deleteLater()

    def setArcWeight(self):
        self.activeItem.setWeight(self.weightValue.text())


    def setPlaceCapacity(self):
        if bool(self.activeItem.variables):
            msgBox = QMessageBox()
            msgBox.information(self, "Information", "Can't change capacity if any variable exist")
        else:
            self.activeItem.setCapacity(self.capacityValue.text())


    def setPlaceToken(self):
        if int(self.tokenValue.text()) > self.activeItem.capacityValue:
            msgBox = QMessageBox()
            msgBox.information(self, "Information", "Token value can't be greater than capacity")
        else:
            self.activeItem.setToken(self.tokenValue.text())

    def setActiveItem(self, a):
        if a is not None and isinstance(a, Place):
            self.activeItem = a
            self.labell.setText("P" + str(a.id))
        elif a is not None and isinstance(a, Transition):
            self.activeItem = a
            self.labell.setText("T" + str(a.id))
        elif a is not None and isinstance(a, Edge):
            self.activeItem = a
            self.labell.setText("A" + str(a.id))
        else:
            self.activeItem = None
            self.labell.setText("None item selected")
        self.placeEditor()


    @pyqtSlot(object)
    def onJob(self, a):
        self.aaa = "XD"
        self.labell.setText("XD")
        self.changeItemLabel()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # widget = GraphWidget()
    GUI = MainWindow()
    # widget = GraphWidget(GUI)


    GUI.show()
    # widget.show()


    sys.exit(app.exec_())


