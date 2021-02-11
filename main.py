import json
import sys
from os import sep, path

DATA_DIR = path.dirname(path.realpath(sys.argv[0])) + sep + "data" + sep
K = 32


def getTransformedRating(rating):
    return 10**(rating/400)


def getExpectedScore(subjectTrans, opponentTrans):
    return subjectTrans/(subjectTrans + opponentTrans)


def getNewRating(rating, score, expectedScore):
    return round(rating + K*(score - expectedScore), 1)


def calculateNewElo(rating1, rating2, score1):
    transformedRating1 = getTransformedRating(rating1)
    transformedRating2 = getTransformedRating(rating2)

    expectedScore1 = getExpectedScore(
        transformedRating1, transformedRating2)
    expectedScore2 = 1 - expectedScore1

    newRating1 = getNewRating(rating1, score1, expectedScore1)
    newRating2 = getNewRating(rating2, 1 - score1, expectedScore2)

    return newRating1, newRating2


def updateElo(char1, char2, char1Score=1):
    with open(DATA_DIR + "characters.json", 'r+') as f:
        characterData = json.load(f)

        if char1 not in characterData:
            characterData[char1] = 0
        if char2 not in characterData:
            characterData[char2] = 0

        newRating1, newRating2 = calculateNewElo(
            characterData[char1], characterData[char2], char1Score)

        print("%s: %d" % (char1, newRating1))
        print("%s: %d" % (char2, newRating2))

        characterData[char1] = newRating1
        characterData[char2] = newRating2

        f.seek(0)
        json.dump(characterData, f, indent=2)
        f.truncate()


if __name__ == "__main__":
    while True:
        try:
            winner = input("\nWinner: ")
            if winner == "":
                drawer1 = input("1st character: ")
                drawer2 = input("2nd character: ")
                updateElo(drawer1, drawer2, 0.5)
            else:
                loser = input("Loser: ")
                updateElo(winner, loser, 1)
        except KeyError:
            print("The character provided does not exist.")
