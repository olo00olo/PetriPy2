import sys
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QPushButton

if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)

    newPlace = QPushButton("0")
    newPlace.clicked.connect(lambda: dock.show())
    newPlace.show()



    w = QtWidgets.QMainWindow()
    w.setCentralWidget(QtWidgets.QWidget())
    dock = QtWidgets.QDockWidget("Collapsible Demo")
    w.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)




    scroll = QtWidgets.QScrollArea()
    dock.setWidget(scroll)



    # print(dock.isActiveWindow(), dock.isHidden(), dock.isEnabled())
    #
    #
    # newPlace = QPushButton("0")
    # newPlace.clicked.connect(lambda: dock.show())
    # newPlace.show()

    # content = QtWidgets.QWidget()
    # scroll.setWidget(content)
    # vlay = QtWidgets.QVBoxLayout(content)
    # vlay.addStretch()

    # w.resize(640, 480)
    w.show()
    sys.exit(app.exec_())