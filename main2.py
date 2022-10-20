# coffee counter = 2
# hours spend = about 5
import sys

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QApplication, QPushButton, QMenu, QDockWidget, QMainWindow, QWidget, QScrollArea, QLabel, \
    QVBoxLayout, QTextEdit
from PyQt6.uic.properties import QtCore


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__(parent=None)
        self.button_map = []

        self.setCentralWidget(QWidget())
        self.dock = QDockWidget("Menu")
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, self.dock)
        scroll = QScrollArea()
        self.dock.setWidget(scroll)

        self.text = QLabel("Text")
        self.text.setDisabled(True)
        wid = QWidget()
        lay = QVBoxLayout(wid)
        lay.addWidget(self.text)
        self.dock.setWidget(wid)
        self.dock.setVisible(False)




        self.setWindowTitle("PetriPy")
        self.resize(600, 600)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)

        # self.addTransitionBtn = QPushButton("add transition", self)
        # self.addTransitionBtn.move(100, 5)
        # self.addTransitionBtn.setCheckable(True)


        self.changeLabelBtn = QPushButton("+1", self)
        self.changeLabelBtn.move(195, 5)
        self.changeLabelBtn.clicked.connect(self.change)





    def change(self):
        for place in self.button_map:
            if place.isChecked():
                place.setText(str(int(place.text())+1))

    def changeColorIfChecked(self, name):
        for place in self.button_map:
            if not place == name:
                place.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
                place.setChecked(False)

        if name.isChecked():
            self.text.setText(str(name))
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
            newPlace = QPushButton("0", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
            newPlace.setCheckable(True)
            newPlace.clicked.connect(lambda: self.changeColorIfChecked(newPlace))
            newPlace.show()

            self.button_map.append(newPlace)
            # print(self.button_map)

        # if self.addTransitionBtn.isChecked():
        #     newPlace = QPushButton("0", self)
        #     newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
        #     newPlace.setStyleSheet("border: 3px solid dodgerblue;")
        #     newPlace.setCheckable(True)
        #     newPlace.show()

if __name__ == "__main__":
    app = QApplication([])
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
