import json

from Place import Place


def saver(places, transitions, arcs):
    i = 1
    placesDict = {}
    transitionsDict = {}
    arcsDict = {}

    all = {"places": {}, "transitions": {}, "arcs": {}}

    for placeId, placeRef in places.items():
        placesDict.update({"id": placeId})
        placesDict.update({"pos": [round(placeRef.x(), 2), round(placeRef.y(), 2)]})
        all["places"].update({i: placesDict})
        placesDict = {}
        i += 1

    i = 1
    for transitionId, transitionRef in transitions.items():
        transitionsDict.update({"id": transitionId})
        transitionsDict.update({"pos": [round(transitionRef.x(), 2), round(transitionRef.y(), 2)]})
        all["transitions"].update({i: transitionsDict})
        transitionsDict = {}
        i += 1

    i = 1
    for arcId, arcRef in arcs.items():
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

        all["arcs"].update({i: arcsDict})
        arcsDict = {}
        i += 1

    with open('output.json', 'w') as convert_file:
        convert_file.write(json.dumps(all))