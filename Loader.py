import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QMessageBox

from Place import Place


def loader(graphWidget):

    with open('output.json', 'r') as convert_file:
        try:
            graphWidget.scene.clear()

            net = json.load(convert_file)
            for key, place in net["places"].items():
                print(place)

        except JSONDecodeError:
            msgBox = QMessageBox()
            msgBox.information(graphWidget, "Information", "File empty")
            pass
    # newPlace = Place(graphWidget)
    # newPlace.setPos(50, 50)
    # graphWidget.scene.addItem(newPlace)
    #
    # graphWidget.scene.addItem(newPlace)
