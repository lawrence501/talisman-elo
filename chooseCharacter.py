import json
import secrets
from os import sep, path
import sys

DATA_DIR = path.dirname(path.realpath(sys.argv[0])) + sep + "data" + sep
SAME_CHARACTER_CHANCE = 0
EDITION = "-5e"

def randomiseCharacter():
    with open(DATA_DIR + f"characters{EDITION}.json", 'r+') as f:
        rawData = json.load(f)
        chars = sorted(list(rawData.items()),
                       key=lambda k: rawData[k[0]])
        numChars = len(chars)

        char1Idx = secrets.randbelow(numChars)
        char1, char1Val = chars[char1Idx]
        sameCharRoll = secrets.randbelow(100)
        if sameCharRoll < SAME_CHARACTER_CHANCE:
            char2 = char1
        elif char1Idx == numChars - 1:
            char2 = chars[char1Idx - 1][0]
        elif char1Idx == 0:
            char2 = chars[1][0]
        else:
            lower, lowerVal = chars[char1Idx - 1]
            higher, higherVal = chars[char1Idx + 1]
            lowDiff = (char1Val - lowerVal)
            highDiff = (higherVal - char1Val)
            if lowDiff == highDiff:
                char2 = secrets.choice([lower, higher])
            elif lowDiff > highDiff:
                char2 = higher
            else:
                char2 = lower
        print("Player 1: {} ({})".format(char1, char1Val))
        print("Player 2: {} ({})".format(char2, rawData[char2]))


if __name__ == "__main__":
    while True:
        randomiseCharacter()
        input("Press enter for the next characters")
