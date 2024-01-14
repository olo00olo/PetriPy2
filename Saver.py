import json

from PyQt5.QtWidgets import QFileDialog

from Place import Place


def saver(graphWidget, mode):

    i = 1
    placesDict = {}
    transitionsDict = {}
    arcsDict = {}
    all = {"places": {}, "transitions": {}, "arcs": {}}

    print(placesDict)
    for placeId, placeRef in graphWidget.placesDict.items():
        placesDict.update({"id": placeId})
        placesDict.update({"pos": [round(placeRef.x(), 2), round(placeRef.y(), 2)]})
        placesDict.update({"tokens": int(placeRef.tokens)})
        placesDict.update({"capacity": int(placeRef.capacityValue)})
        placesDict.update({"variables": placeRef.variables})
        all["places"].update({i: placesDict})
        placesDict = {}
        i += 1

    i = 1
    for transitionId, transitionRef in graphWidget.transitionsDict.items():
        transitionsDict.update({"id": transitionId})
        transitionsDict.update({"pos": [round(transitionRef.x(), 2), round(transitionRef.y(), 2)]})
        transitionsDict.update({"var": transitionRef.variables})
        all["transitions"].update({i: transitionsDict})
        transitionsDict = {}
        i += 1

    i = 1
    for arcId, arcRef in graphWidget.arcsDict.items():
        for key, value in arcRef[1].items():
            if isinstance(value, Place):
                arcsDict.update({"P": key})
            else:
                arcsDict.update({"T": key})

        for key, value in arcRef[2].items():
            if isinstance(value, Place):
                arcsDict.update({"P": key})
            else:
                arcsDict.update({"T": key})
        arcsDict.update({"weight": arcRef[0].weightValue})
        arcsDict.update({"id": arcRef[0].id})

        all["arcs"].update({i: arcsDict})
        arcsDict = {}
        i += 1

    if mode == "file":
        filename = QFileDialog.getSaveFileName(graphWidget, 'Select file', '*.json')
        path = filename[0]

        try:
            with open(path, 'w') as convert_file:
                convert_file.write(json.dumps(all))
        except:
            print("Couldn't open file")
    else:
        return json.dumps(all)
