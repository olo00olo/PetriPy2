from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit, QMenu, QWidget, \
    QHBoxLayout, QAction, QFormLayout, QLabel, QMessageBox

from Edge import Edge
from Place import Place
from Saver import saver
from Transition import Transition
from VariableWindow import TableWindow

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        # print(self)
        super(MainWindow, self).__init__(parent=parent)
        from main import GraphWidget
        self.linesArray = []
        self.setGeometry(50, 50, 800, 800)

        self.xd = 1
        graphWidget = GraphWidget(self)


        self.tableWindow = None
        self.activeItem = None
        graphWidget.activeElementChanged.connect(self.setActiveItem)



        # TODO: menu bar
        self.menuBar = self.menuBar()

        file_menu = self.menuBar.addMenu("&File")
        save_action = QAction("&Save", self)
        save_action.triggered.connect(lambda: graphWidget.saveNet())
        file_menu.addAction(save_action)

        load_action = QAction("&Open", self)
        load_action.triggered.connect(lambda: graphWidget.loadNet())
        file_menu.addAction(load_action)

        view_menu = self.menuBar.addMenu("&View")
        show_dock_action = QAction("&Show menu", self)
        show_dock_action.triggered.connect(lambda: self.dock.show())
        view_menu.addAction(show_dock_action)

        self.dock = QDockWidget("menu", self)
        self.dock.setMinimumWidth(250)
        # self.dock.setFloating(True)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.verticalLayout = QVBoxLayout()

        self.dockedWidget = QWidget(self)
        self.dockedWidget.setLayout(self.verticalLayout)

        self.dock.setWidget(self.dockedWidget)

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


        self.setCentralWidget(graphWidget)

        # self.dock.setVisible(False)
        # self.dock.hide()





    def placeEditor(self):
        if self.activeItem is not None and isinstance(self.activeItem, Place):
            # self.newLineBtn = QPushButton("+", self)
            # self.newLineBtn.clicked.connect(self.addLine)
            editVariablesBtn = QPushButton("Edit variables", self)
            editVariablesBtn.clicked.connect(self.openVariableTable)

            self.labell = QLabel()

            onlyInt = QIntValidator()
            onlyInt.setRange(1, 9)

            self.capacityLabel = QLabel()
            self.capacityLabel.setText("Capacity: ")
            self.capacityValue = QLineEdit()
            self.capacityValue.setText(str(self.activeItem.capacityValue))
            self.capacityValue.setValidator(onlyInt)
            self.capacityValue.editingFinished.connect(self.setPlaceCapacity)
            self.f1 = QFormLayout()
            self.f1.addRow(self.capacityLabel, self.capacityValue)

            self.tokenLabel = QLabel()
            self.tokenLabel.setText("Token: ")
            self.tokenValue = QLineEdit()
            self.tokenValue.setText(str(self.activeItem.tokens))
            self.tokenValue.setValidator(onlyInt)
            self.tokenValue.editingFinished.connect(self.setPlaceToken)
            self.f2 = QFormLayout()
            self.f2.addRow(self.tokenLabel, self.tokenValue)

            self.verticalLayout.addLayout(self.f2)
            self.verticalLayout.addLayout(self.f1)
            self.verticalLayout.addWidget(editVariablesBtn)
            # self.verticalLayout.addWidget(self.newLineBtn)
            self.verticalLayout.setAlignment(Qt.AlignTop)

        elif self.activeItem is not None and isinstance(self.activeItem, Edge):
            self.labell = QLabel()

            onlyInt = QIntValidator()
            onlyInt.setRange(1, 9)
            self.weightLabel = QLabel()
            self.weightLabel.setText("Weight: ")
            self.weightValue = QLineEdit()
            self.weightValue.setText(str(self.activeItem.weightValue))
            self.weightValue.setValidator(onlyInt)
            self.weightValue.editingFinished.connect(self.setArcWeight)

            self.f1 = QFormLayout()
            self.f1.addRow(self.weightLabel, self.weightValue)

            self.verticalLayout.addLayout(self.f1)
            self.verticalLayout.setAlignment(Qt.AlignTop)

            print("111")



        else:
            try:
                # for i in self.linesArray:
                #     self.removeLine(i[0], i[1], i[2])
                #     self.linesArray = []
                for i in reversed(range(self.verticalLayout.count())):
                    widget = self.verticalLayout.itemAt(i).widget()
                    if widget is not None:
                        widget.setParent(None)
                for i in reversed(range(self.f1.count())):
                    widget = self.f1.itemAt(i).widget()
                    if widget is not None:
                        widget.setParent(None)
                for i in reversed(range(self.f2.count())):
                    widget = self.f2.itemAt(i).widget()
                    if widget is not None:
                        widget.setParent(None)

                self.labell = QLabel("None item selected")
                self.verticalLayout.addWidget(self.labell)
            except:
                print("XD")

    def openVariableTable(self):
        if isinstance(self.activeItem, Place):
            if self.activeItem.capacityValue == 1:
                self.a = TableWindow(self.activeItem)
                # a.setGeometry(100, 100, 800, 600)
                self.a.show()
            else:
                msgBox = QMessageBox()
                msgBox.information(self, "Information", "Can't open variable editor if capacity is greater than 0")


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
        line.setParent(None)

    def setArcWeight(self):
        print(self.activeItem)
        self.activeItem.setWeight(self.weightValue.text())


    def setPlaceCapacity(self):
        # print(self.capacityValue.text())
        # print(self.capacityValue)
        if bool(self.activeItem.variables):
            msgBox = QMessageBox()
            msgBox.information(self, "Information", "Can't change capacity if any variable exist")
        else:
            self.activeItem.setCapacity(self.capacityValue.text())


    def setPlaceToken(self):
        # print(self.capacityValue.text())
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


