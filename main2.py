# coffee counter = 4
# redbull counter = 2
# hours spend = about 10

import sys

from PyQt5.QtCore import Qt, QLine, QPoint
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtWidgets import QApplication, QPushButton, QDockWidget, QMainWindow, QWidget, QScrollArea, QLabel, \
    QVBoxLayout

# from Arcs import ViewPort
from Arcs import Path
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

        # view = ViewPort(self)
        # self.setCentralWidget(view)

        self.setWindowTitle("PetriPy")
        self.resize(600, 600)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)
        self.addPlaceBtn.clicked.connect(lambda: self.uncheck(self.addPlaceBtn))

        self.addTransitionBtn = DragButton("add transition", self)
        self.addTransitionBtn.move(120, 5)
        self.addTransitionBtn.setCheckable(True)
        self.addTransitionBtn.clicked.connect(lambda: self.uncheck(self.addTransitionBtn))

        self.addArcsBtn = DragButton("add arcs", self)
        self.addArcsBtn.move(235, 5)
        self.addArcsBtn.setCheckable(True)
        self.addArcsBtn.clicked.connect(lambda: self.uncheck(self.addArcsBtn))

        self.line = QLine()
        self.path = Path()


    def drawLin(self):
        b = QPoint(0, 0)
        e = QPoint(500, 500)
        self.line = QLine(b, e)
        self.path = Path(b, e)
        self.update()

    def paintEvent(self,event):
        QMainWindow.paintEvent(self, event)
        if not self.line.isNull():
            print("XD")
            painter = QPainter(self)
            pen = QPen(Qt.red, 3)
            painter.setPen(pen)
            # painter.drawLine(self.line)
            # painter.drawRect(100, 15, 400, 200)




    def change(self, symbol):
        initValue = int(self.checkedPlace.text())
        if symbol == "+":
            value = str(initValue + 1)
        elif symbol == "-":
            if initValue > 0:
                value = str(initValue - 1)
            else:
                value = str(0)
        else:
            value = initValue

        self.checkedPlace.setText(value)
        self.value.setText(value)

    def changeColorIfChecked(self, name):
        print("XDDDDD")
        for place in self.button_map:
            if not place == name:
                place.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px; background-color: white;")
                place.setChecked(False)

        if name.isChecked():
            self.checkedPlace = name
            self.value.setText(str(name.text()))
            self.dock.setVisible(True)
            name.setStyleSheet(
                "border: 3px solid darkblue; border-radius: 25px; background-color: rgba(200, 255, 255, 255);")
            name.raise_()
        else:
            self.dock.setVisible(False)
            name.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px; background-color: white;")
            # name.lower()
        # print(name.isChecked())

    # def contextMenuEvent(self, event):
        # contextMenu = QMenu(self)
        # delete = contextMenu.addAction("Delete")
        # action = contextMenu.exec(self.mapToGlobal(event.pos()))

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.MouseButton.RightButton:
            print(QMouseEvent.pos().x(), QMouseEvent.pos().y())

        if self.addPlaceBtn.isChecked() and QMouseEvent.button() == Qt.MouseButton.LeftButton:
            newPlace = DragButton("0", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px; background-color: white")
            newPlace.setCheckable(True)
            newPlace.clicked.connect(lambda: self.changeColorIfChecked(newPlace))
            newPlace.show()

            self.button_map.append(newPlace)

        if self.addTransitionBtn.isChecked():
            newPlace = DragButton("", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 18, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue;")
            newPlace.setCheckable(True)
            newPlace.show()

        if self.addArcsBtn.isChecked():
            self.drawLin()

        # if self.addTransitionBtn.isChecked():
        #     newPlace = QPushButton("0", self)
        #     newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
        #     newPlace.setStyleSheet("border: 3px solid dodgerblue;")
        #     newPlace.setCheckable(True)
        #     newPlace.show()

    # def mouseMoveEvent(self, QMouseEvent):
    #     print(QMouseEvent.self.addPlaceButton)



    def uncheck(self, button):
        buttons = [self.addPlaceBtn, self.addTransitionBtn, self.addArcsBtn]
        for btn in buttons:
            if btn != button:
                btn.setChecked(False)

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()

    # view = ViewPort(window)
    # window.setCentralWidget(view)

    window.show()
    sys.exit(app.exec())
