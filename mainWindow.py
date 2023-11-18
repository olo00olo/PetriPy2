from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit, QMenu, QWidget, \
    QHBoxLayout, QAction, QFormLayout, QLabel

from Saver import saver
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
        if self.activeItem is not None:
            self.newLineBtn = QPushButton("+", self)
            self.newLineBtn.clicked.connect(self.addLine)
            editVariablesBtn = QPushButton("Edit variables", self)
            editVariablesBtn.clicked.connect(self.openVariableTable)
            self.verticalLayout.addWidget(editVariablesBtn)
            self.verticalLayout.addWidget(self.newLineBtn)
            self.verticalLayout.setAlignment(Qt.AlignTop)
            self.labell = QLabel()
        else:
            for i in self.linesArray:
                self.removeLine(i[0], i[1], i[2])
                self.linesArray = []
            for i in reversed(range(self.verticalLayout.count())):
                self.verticalLayout.itemAt(i).widget().setParent(None)

            self.labell = QLabel("None item selected")
            self.verticalLayout.addWidget(self.labell)
            print("n")

    def openVariableTable(self):
        self.a = TableWindow(self.activeItem)
        # a.setGeometry(100, 100, 800, 600)
        self.a.show()

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


    def setActiveItem(self, a):
        if a is not None:
            self.activeItem = a
            self.labell.setText("P" + str(a.id))
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


