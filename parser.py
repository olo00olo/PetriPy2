from pyparsing import Word, alphas, oneOf, infixNotation, opAssoc, Literal, ParseException

def parser(string, dict):
    if string == "":
        return 1
    input_string = string.replace("~", "not ")
    input_string = input_string.replace("OR", "or")
    input_string = input_string.replace("AND", "and")

    input_string = input_string.split()
    for w in range(len(input_string)):
        if input_string[w] not in ["or", "and", "not"]:
            input_string[w] = dict[input_string[w]]

    input_string = " ".join(str(x) for x in input_string)

    return eval(input_string)