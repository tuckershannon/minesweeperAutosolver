# Minesweeper with Autosolve by Tucker Shannon 2020

import random


class MapLocation:
    def __init__(self, x, y):
        self.isMine = False
        self.isDiscovered = False
        self.neighbors = []
        self.nextToNMines = 0
        self.flagged = False
        self.x = x
        self.y = y


class Minesweeper:
    def __init__(self, sizeOfField, nMines):
        self.sizeOfField = sizeOfField
        self.nMines = nMines
        self.minefield = {}
        self.setupMinefield()
        self.placeMines()
        self.assignNumbers()
        self.noExplodedMines = True
        self.gameCompleted = False

    def getKey(self, x, y):
        return "x" + str(x) + "y" + str(y)

    def getLocation(self, x, y):
        key = self.getKey(x, y)
        return self.minefield[key]

    def setupMinefield(self):
        for x in range(0, self.sizeOfField):
            for y in range(0, self.sizeOfField):
                key = self.getKey(x, y)
                self.minefield[key] = MapLocation(x, y)
        return self.minefield

    def placeMines(self):
        for n in range(0, self.nMines):
            while True:
                x = random.randrange(0, self.sizeOfField)
                y = random.randrange(0, self.sizeOfField)
                possibleLocation = self.getLocation(x, y)
                if not possibleLocation.isMine:
                    possibleLocation.isMine = True
                    break

    def assignNeighbors(self):
        possibleDirs = [[1, -1], [1, 0], [1, 1], [0, -1], [0, 1], [-1, -1], [-1, 0], [-1, 1]]
        for location in self.minefield.values():
            for direction in possibleDirs:
                neighborX = location.x + direction[0]
                neighborY = location.y + direction[1]
                if 0 <= neighborX < self.sizeOfField and 0 <= neighborY < self.sizeOfField:
                    location.neighbors.append(self.getLocation(neighborX, neighborY))

    def assignNumbers(self):
        self.assignNeighbors()
        for location in self.minefield.values():
            for neighbor in location.neighbors:
                if neighbor.isMine:
                    location.nextToNMines += 1

    def printMineField(self):
        for x in range(0, self.sizeOfField):
            rowString = ""
            for y in range(0, self.sizeOfField):
                location = self.getLocation(x, y)
                if location.isDiscovered:
                    if location.isMine:
                        rowString += "X  "
                    else:
                        if location.nextToNMines == 0:
                            rowString += "   "
                        else:
                            rowString += str(location.nextToNMines) + "  "
                elif location.flagged:
                    rowString += "!  "
                else:
                    rowString += "?  "
            print(rowString)
        print()

    def printMineFieldWithCords(self):
        rowLabel = "   "
        for x in range(0, self.sizeOfField):
            rowLabel += str(x + 1) + "  "
        print(rowLabel)
        for x in range(0, self.sizeOfField):
            rowString = str(x + 1) + "  "
            for y in range(0, self.sizeOfField):
                location = self.getLocation(x, y)
                if location.isDiscovered:
                    if location.isMine:
                        rowString += "X  "
                    else:
                        if location.nextToNMines == 0:
                            rowString += "   "
                        else:
                            rowString += str(location.nextToNMines) + "  "
                elif location.flagged:
                    rowString += "!  "
                else:
                    rowString += "?  "
            print(rowString)
        print()

    def discoverNewLocations(self):
        for location in self.minefield.values():
            nFlaggedBombs = 0
            for neighbor in location.neighbors:
                if neighbor.flagged:
                    nFlaggedBombs += 1
            if nFlaggedBombs == location.nextToNMines:
                for neighbor in location.neighbors:
                    if not neighbor.flagged:
                        self.selectLocation(neighbor.x, neighbor.y)
                        # self.printMineField()
                        # time.sleep(0.2)

    def flagMines(self):
        for location in self.minefield.values():
            if location.isDiscovered:
                listOfUnknownNeighbors = []
                for neighbor in location.neighbors:
                    if not neighbor.isDiscovered:
                        listOfUnknownNeighbors.append(neighbor)
                if len(listOfUnknownNeighbors) == location.nextToNMines:
                    for newFlaggedLocation in listOfUnknownNeighbors:
                        newFlaggedLocation.flagged = True
                        # self.printMineField()
                        # time.sleep(0.2)

    def selectLocation(self, x, y):
        location = self.getLocation(x, y)
        location.isDiscovered = True
        if location.isMine:
            self.mineExploded()
        if location.nextToNMines == 0:
            for neighbor in location.neighbors:
                if not neighbor.isDiscovered:
                    self.selectLocation(neighbor.x, neighbor.y)

    def checkIfCompleted(self):
        isCompleted = True
        for location in self.minefield.values():
            if not location.isMine and not location.isDiscovered:
                isCompleted = False
        self.gameCompleted = isCompleted

    def mineExploded(self):
        self.noExplodedMines = False
        print("You landed on a mine! BOOM")
        self.endGame()

    def askUserForLocation(self):
        self.printMineFieldWithCords()
        while True:
            x = int(input(("Pick Row between 1 and " + (str(self.sizeOfField)) + ": "))) - 1
            y = int(input(("Pick Col between 1 and " + (str(self.sizeOfField)) + ": "))) - 1
            if 0 <= x < self.sizeOfField and 0 <= y < self.sizeOfField:
                break
            print("Must be between 1 and " + str(self.sizeOfField))
        self.selectLocation(x, y)

    def endGame(self):
        self.printMineField()
        if self.noExplodedMines:
            print("Congratulations! You completed without exploding anything!")
        else:
            print("Sorry, better luck next time.")
            self.gameCompleted = True

    def firstPick(self):
        self.printMineFieldWithCords()
        x = int(input(("Pick Starting Row between 1 and " + (str(self.sizeOfField)) + ": "))) - 1
        y = int(input(("Pick Starting Col between 1 and " + (str(self.sizeOfField)) + ": "))) - 1
        while True:
            location = self.getLocation(x, y)
            if location.nextToNMines == 0 and not location.isMine:
                self.selectLocation(x, y)
                break
            self.minefield = {}
            self.setupMinefield()
            self.placeMines()
            self.assignNumbers()

    def autoPickStartPoint(self):
        while True:
            randomX = random.randrange(0, self.sizeOfField)
            randomY = random.randrange(0, self.sizeOfField)
            startPoint = self.getLocation(randomX, randomY)
            if startPoint.nextToNMines == 0 and not startPoint.isMine:
                self.selectLocation(randomX, randomY)
                break

    def autoSolveMaze(self):
        self.autoPickStartPoint()
        while not self.gameCompleted:
            self.flagMines()
            self.discoverNewLocations()
            self.checkIfCompleted()
        self.endGame()

    def userSolveMaze(self):
        self.firstPick()
        while not self.gameCompleted:
            self.askUserForLocation()

    def startGame(self):
        answer = input("Would you like to auto-solve this map? Y/N: ")
        if answer == "Y" or answer == "y":
            self.autoSolveMaze()
        else:
            self.userSolveMaze()


def main():
    mapSize = 9
    nMines = 9
    minesweeper = Minesweeper(mapSize, nMines)
    minesweeper.startGame()


if __name__ == "__main__":
    main()
