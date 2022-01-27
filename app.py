
import os, random
from string import ascii_lowercase
from collections import Counter
import collections

def loadWords():
    filePath = os.path.dirname(os.path.realpath(__file__)) + "//words.txt"
    words = []
    f = open(filePath,"r")
    for word in f:
        words.append(word.strip())
    return words

def guessWord(words,banList):
    acceptableWords = []
    for word in words:
        passed = True
        for letter in word:
            if letter in banList:
                passed = False
        if passed == True:
            acceptableWords.append(word)
    return acceptableWords

def knownCharactersInWord(word,known):
    passed = False
    for i in range(0,5):
        if known[i] == '':
            continue
        elif word[i] == known[i]:
            passed = True
        else:
            passed = False
            return False
    if passed:
        return True

def knownCharacters(words, known):
    acceptableWords = []
    for word in words:
        if knownCharactersInWord(word,known):
            acceptableWords.append(word)
        else:
            continue
    return acceptableWords

def possibleChars(words,knownPossibilites):
    flatPossibilities = [item for sublist in knownPossibilites for item in sublist]
    acceptableWords = []
    for word in words:
        possibility = True
        for i in range(0,5):
            if word[i] in knownPossibilites[i]:
                possibility = False
        for j in flatPossibilities:
            if j not in word:
                possibility = False
        if possibility:
            acceptableWords.append(word)
    return acceptableWords

def characterProbability(words):
    countDict = {}
    probDict = {}
    letterSum = 0
    for c in ascii_lowercase:
        count = sum(map(lambda x : 1 if c in x else 0, words))
        letterSum += count
        countDict[c] = count
    for c in countDict:
        probDict[c] = countDict[c]/letterSum
    return probDict

def characterProbabilityByPosition(words):
    positionList = {}
    for i in range(0,5):
        probDict = {}
        countDict = {}
        listOfChars = []
        letterSum = 0
        for word in words:
            listOfChars.append(word[i])
        
        for c in ascii_lowercase:
            count = listOfChars.count(c)
            countDict[c] = count
            letterSum += count
        
        for c in countDict:
            probDict[c] = countDict[c]/letterSum
        
        positionList[i]=probDict
    print(positionList)
    return positionList

def sortWordsByLetterScore(words):
    probList = characterProbabilityByPosition(words)
    scoredDict = {}
    for word in words:
        score = 1
        for i in range(0,4):
            value = probList[i][word[i]]
            if value != 0:
                score *= value
        scoredDict[word] = score
    sorted_dict = collections.OrderedDict(sorted(scoredDict.items(), key=lambda kv: kv[1],reverse=True))
    sorted_words = []
    for key in sorted_dict.keys():
        sorted_words.append(key)
    printNum = min(5,len(sorted_words))
    print("There are {} solutions, with the top {} being {}".format(len(sorted_words),printNum,sorted_words[0:printNum]))
    if printNum == 5:
        removeWordsWithDupLetters(sorted_words)
    return sorted_words

def sortWordsByScore(words):
    probDict = characterProbability(words)
    scoredDict = {}
    for word in words:
        score = 1
        for c in word:
            score *= probDict[c]
        scoredDict[word] = score
    sorted_dict = collections.OrderedDict(sorted(scoredDict.items(), key=lambda kv: kv[1],reverse=True))
    sorted_words = []
    for key in sorted_dict.keys():
        sorted_words.append(key)
    printNum = min(5,len(sorted_words))
    print("There are {} solutions, with the top {} being {}".format(len(sorted_words),printNum,sorted_words[0:printNum]))
    if printNum == 5:
        removeWordsWithDupLetters(sorted_words)
    return sorted_words

def removeWordsWithDupLetters(words):
    removedDups = []
    for word in words:
        repeatingLetters = False
        for c in word:
            if word.count(c) > 1:
                repeatingLetters = True
        if not repeatingLetters:
            removedDups.append(word)
    printNum = min(5,len(removedDups))
    print("There are {} solutions with no repeating letters, with the top {} being {}".format(len(removedDups),printNum,removedDups[0:printNum]))
    return removedDups

def commandLineApp():
    banList = []
    known = ['','','','','']
    impossibleCharacters = [
        [],
        [],
        [],
        [],
        []
        ]  

    optionList = loadWords()
    sortWordsByLetterScore(optionList)

    while True:
        success = input("Was the guess successful? (Y/n) ")
        if success in ["Y","y",""]:
            quit()

        greenLetters = input("Please type any green characters, separated with a comma: ")
        if greenLetters != "":
            greenLettersList = greenLetters.split(",")
            for i in range(0,5):
                if greenLettersList[i] != '':
#                    print(greenLettersList[i])
                    known[i] = greenLettersList[i]

        yellowLetters = input("Please type any yellow characters, separated by a comma: ")
        if yellowLetters != "":
            yellowCharsList = yellowLetters.split(",")
            for i in range(0,5):
                if yellowCharsList[i] == '':
                    continue
                impossibleCharacters[i].append(yellowCharsList[i])

        banChars = input("Please list the grey characters seperated by a comma: ")
        if banChars != "":
            banCharsListInput = banChars.split(",")
            for i in range(0,len(banCharsListInput)):
                if banCharsListInput[i] in known or banCharsListInput[i] in impossibleCharacters:
                    continue
                else:
                    banList.append(banCharsListInput[i])

        solutions1 = guessWord(optionList,banList)

        if known[0] == '' and known[1] == '' and known[2] == '' and known[3] == '' and known[4] == '':
            optionList = possibleChars(solutions1, impossibleCharacters)
        else:
            solutions2 = knownCharacters(solutions1,known) 
            optionList = possibleChars(solutions2,impossibleCharacters)

        sortWordsByLetterScore(optionList)

def manualSolver():
    banList = []

    known = ['','','','','']

    impossibleCharacters = [
        [],
        [],
        [],
        [],
        []
        ]
    
    print("First guess.")
    if len(banList) == 0:
        sortWordsByScore(loadWords())

    solutions1 = guessWord(banList)
    print("After first filter, grey letters.") 
    sortWordsByScore(solutions1)
    
    if known[0] == '' and known[1] == '' and known[2] == '' and known[3] == '' and known[4] == '':
        solutions3 = possibleChars(solutions1, impossibleCharacters)
    else:
        solutions2 = knownCharacters(solutions1,known) 
        print("After second filter, green letters") 
        sortWordsByScore(solutions2)
        solutions3 = possibleChars(solutions2,impossibleCharacters)
    
    print("After third filter, yellow letters")
    sortWordsByScore(solutions3)


if __name__ == "__main__":
    commandLineApp()
