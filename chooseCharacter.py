import json
import secrets
import random
from os import sep, path
import sys

DATA_DIR = path.dirname(path.realpath(sys.argv[0])) + sep + "data" + sep

def randomiseCharacter():
    with open(DATA_DIR + "characters.json", 'r+') as f:
        rawData = json.load(f)
        charData = list(rawData.items())
        random.shuffle(charData)
        values = {v: k for k, v in charData}

        eloValues = list(values.keys())
        eloValues.sort()
        char1Idx = secrets.randbelow(len(values))

        char1Val = eloValues[char1Idx]
        char1 = values[char1Val]
        if char1Idx == len(values):
            char2 = values[eloValues[char1Idx - 1]]
        elif char1Idx == 0:
            char2 = values[eloValues[char1Idx + 1]]
        else:
            lower = eloValues[char1Idx - 1]
            higher = eloValues[char1Idx + 1]
            if (char1Val - lower) > (higher - char1Val):
                char2 = values[higher]
            else:
                char2 = values[lower]

        print(char1)
        print(char2)


if __name__ == "__main__":
    while True:
        randomiseCharacter()
        input("Press enter for the next characters")
