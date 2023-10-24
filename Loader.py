import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QMessageBox, QFileDialog

from Edge import Edge
from Place import Place
from Transition import Transition


def loader(graphWidget):
    places = {}
    transitions = {}

    filename = QFileDialog.getOpenFileName(graphWidget, 'Select file', '*.txt')
    path = filename[0]

    with open(path, 'r') as convert_file:
        try:
            Place.counter = 0
            Transition.counter = 0
            Edge.counter = 0

            graphWidget.scene.clear()

            net = json.load(convert_file)

            for key, place in net["places"].items():
                newPlace = Place(graphWidget)
                newPlace.setPos(place['pos'][0], place['pos'][1])
                graphWidget.scene.addItem(newPlace)
                places.update({place['id']: newPlace})
                graphWidget.placesDict.update({newPlace.id: newPlace})

            for key, transition in net["transitions"].items():
                newTransition = Transition(graphWidget)
                newTransition.setPos(transition['pos'][0], transition['pos'][1])
                graphWidget.scene.addItem(newTransition)
                transitions.update({transition['id']: newTransition})
                graphWidget.transitionsDict.update({newTransition.id: newTransition})

            for key, arc in net['arcs'].items():
                if next(iter(arc)) == 'P':
                    source = places[int(arc['P'])]
                    destination = transitions[int(arc['T'])]
                    newArc = Edge(source, destination)
                    graphWidget.scene.addItem(newArc)
                    graphWidget.scene.update()

                    arc = []
                    arc.append(newArc)
                    arc.append({source.id: source})
                    arc.append({destination.id: destination})
                    graphWidget.arcsDict.update({newArc.id: arc})
                    source.outArcs.update({newArc.id: arc})
                    destination.inArcs.update({newArc.id: arc})


                else:
                    source = transitions[int(arc['T'])]
                    destination = places[int(arc['P'])]
                    newArc = Edge(source, destination)
                    print(places[int(arc['T'])], places[int(arc['P'])])
                    graphWidget.scene.addItem(newArc)
                    graphWidget.scene.update()

                    arc = []
                    arc.append(newArc)
                    arc.append({source.id: source})
                    arc.append({destination.id: destination})
                    graphWidget.arcsDict.update({newArc.id: arc})
                    source.outArcs.update({newArc.id: arc})
                    destination.inArcs.update({newArc.id: arc})

        except JSONDecodeError:
            msgBox = QMessageBox()
            msgBox.information(graphWidget, "Information", "File empty")
            pass
