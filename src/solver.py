
import os, random

def loadWords():
    filePath = os.path.dirname(os.path.realpath(__file__)) + "//words.txt"
    words = []
    f = open(filePath,"r")
    for word in f:
        words.append(word.strip())
    return words

def guessWord(banList):
    words = loadWords()
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

def startingWord():
    words = loadWords()
    ind = random.randint(0,len(words))
    return words[ind]


if __name__ == "__main__":
    banList = ['s','t','m','a','n','d','y','f','c']

    known = ['','o','r','','e']

    impossibleCharacters = [
        [],
        ['e'],
        ['o'],
        [],
        []
        ]

    solutions1 = guessWord(banList)
    
    solutions2 = knownCharacters(solutions1,known)  

    solutions3 = possibleChars(solutions2,impossibleCharacters)
    print(solutions3)
