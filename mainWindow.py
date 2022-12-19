from PyQt5.QtCore import Qt, pyqtSlot
from PyQt5.QtWidgets import QMainWindow, QDockWidget, QApplication, QPushButton, QVBoxLayout, QLineEdit


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        from main import GraphWidget

        self.setGeometry(50, 50, 800, 800)

        self.xd = 1
        graphWidget = GraphWidget(self)
        self.setCentralWidget(graphWidget)

        self.dock = QDockWidget("menu")
        self.dock.setMinimumWidth(200)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)

        self.btn = QPushButton("123", self)
        self.btn.clicked.connect(self.addLine)

        self.line = QLineEdit()


        self.dock.setWidget(self.btn)
        self.dock.setWidget(self.line)


    def addLine(self):
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

