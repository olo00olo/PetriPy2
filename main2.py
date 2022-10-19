import sys

from PyQt6.QtWidgets import QApplication, QDialog, QPushButton


class Window(QDialog):
    def __init__(self):
        super(Window, self).__init__(parent=None)

        self.button_map = []

        self.setWindowTitle("PetriPy")
        self.resize(600, 600)

        self.addPlaceBtn = QPushButton("add place", self)
        self.addPlaceBtn.move(5, 5)
        self.addPlaceBtn.setCheckable(True)

        self.addTransitionBtn = QPushButton("add transition", self)
        self.addTransitionBtn.move(100, 5)
        self.addTransitionBtn.setCheckable(True)


        self.changeLabelBtn = QPushButton("+1", self)
        self.changeLabelBtn.move(195, 5)
        self.changeLabelBtn.clicked.connect(self.change)

    def change(self):
        for place in self.button_map:
            if place.isChecked():
                a = str(int(place.text())+1)
                print(a)
                place.setText(a)

    def changeColorIfChecked(self, name):
        for place in self.button_map:
            if not place == name:
                place.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
                place.setChecked(False)

        if name.isChecked():
            name.setStyleSheet("border: 3px solid darkblue; border-radius: 25px")
        else:
            name.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
        print(name.isChecked())

    def mousePressEvent(self, QMouseEvent):
        if self.addPlaceBtn.isChecked():
            newPlace = QPushButton("0", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue; border-radius: 25px")
            newPlace.setCheckable(True)
            newPlace.clicked.connect(lambda: self.changeColorIfChecked(newPlace))
            newPlace.show()

            self.button_map.append(newPlace)
            # print(self.button_map)

        if self.addTransitionBtn.isChecked():
            newPlace = QPushButton("0", self)
            newPlace.setGeometry(QMouseEvent.pos().x() - 25, QMouseEvent.pos().y() - 25, 50, 50)
            newPlace.setStyleSheet("border: 3px solid dodgerblue;")
            newPlace.setCheckable(True)
            newPlace.show()

if __name__ == "__main__":
    app = QApplication([])
    window = Window()
    window.show()
    sys.exit(app.exec())
