import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QMessageBox

from Edge import Edge
from Place import Place
from Transition import Transition


def loader(graphWidget):
    places = {}
    transitions = {}
    with open('output.json', 'r') as convert_file:
        try:
            graphWidget.scene.clear()

            net = json.load(convert_file)

            for key, place in net["places"].items():
                newPlace = Place(graphWidget)
                newPlace.setPos(place['pos'][0], place['pos'][1])
                graphWidget.scene.addItem(newPlace)
                places.update({place['id']: newPlace})

            for key, transition in net["transitions"].items():
                newTransition = Transition(graphWidget)
                newTransition.setPos(transition['pos'][0], transition['pos'][1])
                graphWidget.scene.addItem(newTransition)
                transitions.update({transition['id']: newTransition})

            for key, arc in net['arcs'].items():
                if next(iter(arc)) == 'P':
                    newArc = Edge(places[int(arc['P'])], transitions[int(arc['T'])])
                    graphWidget.scene.addItem(newArc)
                    graphWidget.scene.update()
                else:
                    newArc = Edge(transitions[int(arc['T'])], places[int(arc['P'])])
                    print(places[int(arc['T'])], places[int(arc['P'])])
                    graphWidget.scene.addItem(newArc)
                    graphWidget.scene.update()

        except JSONDecodeError:
            msgBox = QMessageBox()
            msgBox.information(graphWidget, "Information", "File empty")
            pass
