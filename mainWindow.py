from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit, QMenu, QWidget, \
    QHBoxLayout, QAction, QFormLayout, QLabel

from Saver import saver


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        print(self)
        super(MainWindow, self).__init__(parent=parent)
        from main import GraphWidget
        self.linesArray = []
        self.setGeometry(50, 50, 800, 800)

        self.xd = 1
        graphWidget = GraphWidget(self)
        self.setCentralWidget(graphWidget)


        graphWidget.activeElementChanged.connect(self.changeMenuLabel)


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
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.verticalLayout = QVBoxLayout()

        self.dockedWidget = QWidget(self)
        self.dockedWidget.setLayout(self.verticalLayout)

        self.dock.setWidget(self.dockedWidget)

        self.menuItem = None
        # self.labell = QLabel(str(self.menuItem))
        self.labell = QLabel("nic")
        self.verticalLayout.addWidget(self.labell)

        self.newLineBtn = QPushButton("+", self)
        self.newLineBtn.clicked.connect(self.addLine)
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
        self.verticalLayout.addWidget(self.newLineBtn)
        self.verticalLayout.setAlignment(Qt.AlignTop)




    def addLine(self):
        print(self.labell.text())
        horizontalLayout = QHBoxLayout()
        removeLineBtn = QPushButton("-", self)
        edit = QLineEdit(self)
        self.linesArray.append(edit)
        horizontalLayout.addWidget(edit)
        horizontalLayout.addWidget(removeLineBtn)
        removeLineBtn.clicked.connect(lambda: self.removeLine(horizontalLayout, edit, removeLineBtn))
        self.verticalLayout.addLayout(horizontalLayout)

    def removeLine(self, line, edit, btn):
        edit.deleteLater()
        btn.deleteLater()
        line.setParent(None)
        print(self.labell.text())
        # self.labell.setText("XD")

    def changeItemLabel(self):
        self.aaa = "XD"
        self.labell.setText("XD")
        print("XDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD", self.labell.text())
        QApplication.processEvents()
        self.labell.update()
        self.labell.repaint()

    def changeMenuLabel(self, a):
        print(a)
        self.labell.setText(a)


    @pyqtSlot(object)
    def onJob(self, a):
        self.aaa = "XD"
        self.labell.setText("XD")
        self.changeItemLabel()

        # self.menuItem = str(a)
        # self.label.setText(str(a))
        # self.label.repaint()
        # self.verticalLayout.update()
        # self.update()
        # print(a, "onJob")
        # print(self.label.text(), "label")
        # QApplication.processEvents()

    def printSth(self):
        print(self, "sth")

if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # widget = GraphWidget()
    GUI = MainWindow()
    # widget = GraphWidget(GUI)


    GUI.show()
    # widget.show()


    sys.exit(app.exec_())


