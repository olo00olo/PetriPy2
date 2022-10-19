import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton

def window():
    app = QApplication(sys.argv)
    window = QtWidgets.QWidget()
    window.setWindowTitle("PetriPy")

    button1 = QPushButton(window)
    button1.setText("Button1")
    button1.setCheckable(True)
    button1.move(64, 32)
    button1.setGeometry(200, 150, 200, 200)
    button1.setStyleSheet("border: 10px solid blue; border-radius: 100px")
    button1.clicked.connect(button1_clicked)


    button2 = QPushButton(window)
    button2.setText("Button2")
    button2.move(64, 128)
    button2.clicked.connect(button2_clicked)

    window.setGeometry(50, 50, 1000, 1000)
    window.show()
    sys.exit(app.exec_())


def button1_clicked():
    print("Button 1 clicked")



def button2_clicked():
    print("Button 2 clicked")
    newBtn = QPushButton()
    newBtn.setText("New button")
    newBtn.move(0, 0)
    newBtn.show()


if __name__ == '__main__':
    window()


