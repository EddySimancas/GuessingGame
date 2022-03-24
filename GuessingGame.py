"""
Eddy Sanchez Simancas
This is a number guessing game program
created on Mon Mar 21, 2021
"""
import random
from datetime import date
import numpy as np
import matplotlib.pyplot as plt

def setRange():
    upper_num = None

    while True:
        try:
            lower_num = int(input("Please enter a lower range value: "))
        except ValueError or BaseException:
            print("Invalid input. Please enter an integer\n")
        else:
            break
    while True:
        try:
            upper_num = int(input("Please enter a upper range value: "))
        except ValueError or BaseException:
            print("Invalid input. Please enter an integer\n")
            continue
        if upper_num <= lower_num:
            print(f"Invalid input. upper range must be bigger than {lower_num}\n")
        else:
            break

    return lower_num, upper_num

def setDifficulty():
    while True:
        print("choose a difficulty level. Options are easy (E), normal (N), hard (H):", end=' ')
        level = input().upper()
        if len(level) > 1:
            print("Please only enter a single character.")
            continue
        if len(level) == 1 and level not in ('E', 'N', 'H'):
            print("Please enter 'E', 'N', or 'H'")
            continue
        if len(level) == 1 and level in ('E', 'N', 'H'):
            break

    if level == "E":
        lives = 10
    elif level == "N":
        lives = 5
    else:
        lives = 1

    return lives

def getWonLostCount():
    rowList = []
    totalWins = 0
    totalLost = 0
    with open("gameData.txt", 'r') as f:
        fileLines = f.readlines()
    rowList.extend(fileLines)
    for i, t in enumerate(fileLines):
        rowList[i] = t.split(',')
    rowArray = np.array(rowList)
    dateList = rowArray[:, 0]
    winRateList = rowArray[:, 1]
    lostRateList = rowArray[:, 2]
    currentDate = str(date.today())
    for i, j in enumerate(dateList):
        if currentDate == j:
            totalWins = int(winRateList[i])
            totalLost = int(lostRateList[i])

    return totalWins, totalLost

def updateFile(newLine):
    myList = []

    with open("gameData.txt", 'r') as f:
        rowListFromFile = f.readlines()
    with open("gameData.txt", 'r') as f:
        fileData = f.read()

    myList.extend(rowListFromFile)

    for j, t in enumerate(rowListFromFile):
        myList[j] = t.split(',')

    myArray = np.array(myList)
    dateList = myArray[:, 0]

    index = -1
    for i, j in enumerate(dateList):
        if newLine[0] == j:
            index = i

    if index == -1:
        with open("gameData.txt", "a") as f:
            f.writelines(','.join(newLine))
            f.writelines('\n')
    else:
        lineToRemove = ','.join(myList[index])
        newLineInserting = ','.join(newLine)
        newFileData = fileData.replace(lineToRemove, newLineInserting + '\n')
        with open("gameData.txt", 'w') as f:
            f.write(newFileData)

def printWinLossRatio():
    rowList = []
    with open("gameData.txt", 'r') as f:
        fileData = f.readlines()
    rowList.extend(fileData)
    for i, j in enumerate(fileData):
        rowList[i] = j.split(',')
    rowArray = np.array(rowList)
    datesArray = rowArray[1:, 0]
    winRatioArray = rowArray[1:, 3]
    for i, j in enumerate(winRatioArray):
        winRatioArray[i] = float(str(j).strip())
    print('\ndatesArray: \n', datesArray)
    print('\nwinRatioA: \n', winRatioArray)
    plt.bar(datesArray, winRatioArray, label='Win Ratio Over Time')
    plt.xlabel('Dates (yr-mt-day)')
    plt.ylabel('Wins (%)')
    plt.legend()
    plt.show()

def main():
    currentDate = date.today()
    newRow = []
    while True:
        print("Welcome to the number guessing game\n")
        minNum, maxNum = setRange()
        randomNum = random.randint(minNum, maxNum)
        lives = setDifficulty()
        winCount, lostCount = getWonLostCount()
        while True:
            print(f"live's left: {lives}")
            if lives == 0:
                print(f"you lost. The correct answer was {randomNum}")
                lostCount += 1
                break

            while True:
                try:
                    answer = int(input("Enter your guess: "))
                except ValueError or BaseException:
                    print("Invalid input. Please enter an integer\n")
                else:
                    break

            if answer == randomNum:
                print("congrats, you won")
                winCount += 1
                break
            else:
                lives -= 1
                if answer < randomNum:
                    print(f"Incorrect. {answer} was too low.")
                if answer > randomNum:
                    print(f"Incorrect. {answer} was too high.")
        print("Would you like to play again? (y/n): ", end=' ')
        while True:
            reply = input().lower()
            if reply in ('y', 'yes', 'no', 'n'):
                break
            else:
                print("Please enter correct response.\n")
        if reply.lower() in ('n', 'no'):
            break
    newRow.append(str(currentDate))
    newRow.append(str(winCount))
    newRow.append(str(lostCount))
    newRow.append(str(round((winCount/(winCount + lostCount) * 100), 1)))
    updateFile(newRow)
    printWinLossRatio()
    print("\nThank you for playing.\n")

if __name__ == "__main__":
    main()
