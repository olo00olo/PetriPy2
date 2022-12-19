import json


def saver(places, transitions, arcs):
    i = 1
    placeDict = {}
    all = {"places": {}, "transitions": {}, "arcs": {}}

    for placeId, placeRef in places.items():
        placeDict.update({"id": placeId})
        placeDict.update({"pos": [round(placeRef.x(), 2), round(placeRef.y(), 2)]})
        all["places"].update({i: placeDict})
        placeDict = {}
        print(all)
        i += 1

    # all = json.dump(all)
    with open('output.json', 'w') as convert_file:
        convert_file.write(json.dumps(all))