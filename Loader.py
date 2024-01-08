import json
from json import JSONDecodeError

from PyQt5.QtWidgets import QMessageBox, QFileDialog

from Edge import Edge
from Place import Place
from Transition import Transition


def loader(graphWidget, mode):

    places = {}
    transitions = {}

    if mode == "file":
        # filename = QFileDialog.getOpenFileName(graphWidget, 'Select file', '*.json')
        # path = filename[0]

        path = r'C:\Users\olo00\PycharmProjects\PetriPy2\test.json'

        maxArcId = 0

        convert_file = open(path, 'r')
        print(convert_file)
        # with open(path, 'r') as convert_file:

    else:
        convert_file = mode

    try:
        Place.counter = 0
        Transition.counter = 0
        Edge.counter = 0

        graphWidget.scene.clear()

        print("XD")
        net = json.loads(convert_file)
        print("2222")

        for key, place in net["places"].items():
            print("3")
            newPlace = Place(graphWidget)
            newPlace.setPos(place['pos'][0], place['pos'][1])
            newPlace.setId(place['id'])
            newPlace.setToken(place['tokens'])
            newPlace.setCapacity(place['capacity'])
            newPlace.variables = place['variables']

            graphWidget.scene.addItem(newPlace)
            places.update({place['id']: newPlace})
            graphWidget.placesDict.update({newPlace.id: newPlace})
            print(graphWidget.placesDict)

            Place.counter = newPlace.id + 1


        for key, transition in net["transitions"].items():
            newTransition = Transition(graphWidget)
            newTransition.setPos(transition['pos'][0], transition['pos'][1])

            newTransition.setId(transition['id'])

            graphWidget.scene.addItem(newTransition)
            transitions.update({transition['id']: newTransition})
            graphWidget.transitionsDict.update({newTransition.id: newTransition})

            Transition.counter = newTransition.id + 1

        for key, value in net['arcs'].items():
            if next(iter(value)) == 'P':
                source = places[int(value['P'])]
                # print(source.id, "source")
                destination = transitions[int(value['T'])]
                newArc = Edge(source, destination)

                newArc.setId(value["id"])
                newArc.setWeight(value["weight"])

                graphWidget.scene.addItem(newArc)
                graphWidget.scene.update()

                arc = []
                arc.append(newArc)
                arc.append({source.id: source})
                arc.append({destination.id: destination})
                graphWidget.arcsDict.update({value["id"]: arc})
                source.outArcs.update({value["id"]: arc})
                destination.inArcs.update({value["id"]: arc})

                if value["id"] > maxArcId:
                    maxArcId = value["id"]
                    Edge.counter = newArc.id + 1



            else:
                source = transitions[int(value['T'])]
                destination = places[int(value['P'])]
                newArc = Edge(source, destination)
                # print(places[int(arc['T'])], places[int(arc['P'])])

                newArc.setId(value["id"])
                newArc.setWeight(value["weight"])

                graphWidget.scene.addItem(newArc)
                graphWidget.scene.update()

                arc = []
                arc.append(newArc)
                arc.append({source.id: source})
                arc.append({destination.id: destination})
                graphWidget.arcsDict.update({value["id"]: arc})
                source.outArcs.update({value["id"]: arc})
                destination.inArcs.update({value["id"]: arc})

                if value["id"] > maxArcId:
                    maxArcId = value["id"]
                    Edge.counter = newArc.id + 1

    except JSONDecodeError:
        msgBox = QMessageBox()
        msgBox.information(graphWidget, "Information", "Not proper file")
        pass
