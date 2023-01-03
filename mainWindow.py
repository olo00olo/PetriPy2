from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit, QMenu, QWidget, \
    QHBoxLayout, QAction

from Saver import saver


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        from main import GraphWidget

        self.setGeometry(50, 50, 800, 800)

        self.xd = 1
        graphWidget = GraphWidget(self)
        self.setCentralWidget(graphWidget)

        # TODO: menu bar
        self.menuBar = self.menuBar()

        file_menu = self.menuBar.addMenu("&File")
        save_action = QAction("&Save", self)
        save_action.triggered.connect(lambda: saver(graphWidget.placesDict, graphWidget.transitionsDict, graphWidget.arcsDict))
        file_menu.addAction(save_action)

        load_action = QAction("&Open", self)
        load_action.triggered.connect(lambda: graphWidget.loadNet())
        file_menu.addAction(load_action)


        self.dock = QDockWidget("menu", self)
        self.dock.setMinimumWidth(200)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.layout = QVBoxLayout()

        self.dockedWidget = QWidget(self)
        self.dockedWidget.setLayout(self.layout)

        self.dock.setWidget(self.dockedWidget)



        self.btn = QPushButton("-", self)
        # self.btn.clicked.connect(self.addLine)

        self.line = QLineEdit()

        self.lineBtn = QWidget(self)
        self.lineBtnLayout = QHBoxLayout(self.lineBtn)
        self.lineBtnLayout.addWidget(self.btn)
        self.lineBtnLayout.addWidget(self.line)


        self.newLineBtn = QPushButton("+", self)
        self.newLineBtn.clicked.connect(self.addLine)

        self.layout.addWidget(self.lineBtn)
        self.layout.addWidget(self.newLineBtn)

        self.layout.addStretch()



    def addLine(self):
        self.lineBtnLayout.addWidget(self.btn)
        self.lineBtnLayout.addWidget(self.line)

        self.layout.addWidget(self.lineBtn)
        print("XD")

    @pyqtSlot(int)
    def onJob(self, a):
        print(a)


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)

    # widget = GraphWidget()
    GUI = MainWindow()
    # widget = GraphWidget(GUI)


    GUI.show()
    # widget.show()


    sys.exit(app.exec_())


