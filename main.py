import json
import sys
from os import sep, path
from git import Repo
from git import Git

DATA_DIR = path.dirname(path.realpath(sys.argv[0])) + sep + "data" + sep
K = 32
EDITION = "-5e"
FILENAME = f"characters{EDITION}.json"


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
    with open(DATA_DIR + FILENAME, 'r+') as f:
        characterData = json.load(f)

        if char1 not in characterData:
            characterData[char1] = 0
        if char2 not in characterData:
            characterData[char2] = 0

        oldRating1, oldRating2 = characterData[char1], characterData[char2]
        newRating1, newRating2 = calculateNewElo(
            oldRating1, oldRating2, char1Score)

        print("%s: %.1f --> %.1f" % (char1, oldRating1, newRating1))
        print("%s:  %.1f --> %.1f" % (char2, oldRating2, newRating2))

        characterData[char1] = newRating1
        characterData[char2] = newRating2

        f.seek(0)
        sortedData = {k: v for k, v in sorted(characterData.items(), key=lambda item: item[1])}
        json.dump(sortedData, f, indent=2)
        f.truncate()

        verb = "defeated"
        if char1Score == 0.5:
            verb = "drew with"
        commitMsg = "%s %s %s" % (char1, verb, char2)
        with Git().custom_environment(GIT_SSH_COMMAND="ssh -i %s" % path.expanduser("~/.ssh/id_rsa")):
            repo = Repo(path.dirname(path.realpath(sys.argv[0])) + sep + ".git")
            repo.index.add([DATA_DIR + FILENAME])
            repo.index.commit(commitMsg)

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
