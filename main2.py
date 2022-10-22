# coffee counter = 3
# redbull counter = 2
# hours spend = about 10

import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QPushButton, QMenu, QDockWidget, QMainWindow, QWidget, QScrollArea, QLabel, \
    QVBoxLayout

from Arcs import ViewPort
from DragButton import DragButton


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.button_map = []
        self.checkedPlace = None
        # print(self.windowFlags())

        self.setCentralWidget(QWidget())
        self.dock = QDockWidget("Menu")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        scroll = QScrollArea()
        self.dock.setWidget(scroll)

        self.text = QLabel("Value= ")
        self.text.setDisabled(True)
        self.value = QLabel("")
        self.value.setDisabled(True)
        self.deleteBtn = QPushButton("Delete place", self)
        self.deleteBtn.clicked.connect(lambda: self.checkedPlace.hide())
        self.addValue = QPushButton("+1", self)
        self.addValue.clicked.connect(lambda: self.change("+"))
        self.subValue = QPushButton("-1", self)
        self.subValue.clicked.connect(lambda: self.change("-"))
        wid = QWidget()
        lay = QVBoxLayout(wid)
        lay.addWidget(self.text)
        lay.addWidget(self.value)
        lay.addWidget(self.addValue)
        lay.addWidget(self.subValue)
        lay.addWidget(self.deleteBtn)
        self.dock.setWidget(wid)
        self.dock.setVisible(False)

        view = ViewPort(self)
        self.setCentralWidget(view)

        self.setWindowTitle("PetriPy")
        self.resize(600, 600)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)
        # self.addPlaceBtn.dragMoveEvent(True)

        # self.addTransitionBtn = QPushButton("add transition", self)
        # self.addTransitionBtn.move(100, 5)
        # self.addTransitionBtn.setCheckable(True)
        #
        #
        # self.changeLabelBtn = QPushButton("+1", self)
        # self.changeLabelBtn.move(195, 5)
        # self.changeLabelBtn.clicked.connect(self.change)

    def change(self, symbol):
        initValue = int(self.checkedPlace.text())
        if symbol == "+":
            value = str(initValue + 1)
        elif symbol == "-":
            if initValue > 0:
                value = str(initValue - 1)
            else:
                value = str(0)

        self.checkedPlace.setText(value)
        self.value.setText(value)

    def changeColorIfChecked(self, name):
        for place in self.button_map:
            if not place == name:
                place.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
                place.setChecked(False)

        if name.isChecked():
            self.checkedPlace = name
            self.value.setText(str(name.text()))
            self.dock.setVisible(True)
            name.setStyleSheet("border: 3px solid darkblue; border-radius: 25px")
        else:
            self.dock.setVisible(False)
            name.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
        # print(name.isChecked())

    def contextMenuEvent(self, event):
        contextMenu = QMenu(self)
        delete = contextMenu.addAction("Delete")
        action = contextMenu.exec(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.RightButton:
            print(QMouseEvent.pos().x(), QMouseEvent.pos().y())

        if self.addPlaceBtn.isChecked() and QMouseEvent.button() == Qt.MouseButton.LeftButton:
            # newPlace = QPushButton("0", self)
            newPlace = DragButton("0", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
            newPlace.setCheckable(True)
            newPlace.clicked.connect(lambda: self.changeColorIfChecked(newPlace))
            newPlace.show()

            self.button_map.append(newPlace)
            # print(self.button_map)

        # if self.checkedPlace is not None:
        #     self.checkedPlace.move(10, 10)

        # if self.addTransitionBtn.isChecked():
        #     newPlace = QPushButton("0", self)
        #     newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
        #     newPlace.setStyleSheet("border: 3px solid dodgerblue;")
        #     newPlace.setCheckable(True)
        #     newPlace.show()

    # def mouseMoveEvent(self, QMouseEvent):
    #     print(QMouseEvent.self.addPlaceButton)


if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    # view = ViewPort(window)
    # window.setCentralWidget(view)

    window.show()
    sys.exit(app.exec())
