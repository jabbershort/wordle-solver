
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

def characterProbability():
    words = loadWords()
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

def sortWordsByScore(words,probDict):
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
    printNum = min(10,len(sorted_words))
    print("There are {} solutions, with the top {} being {}".format(len(sorted_words),printNum,sorted_words[0:printNum]))
    return sorted_words

if __name__ == "__main__":
    charProb = characterProbability()
    print("First guess.")
    sortWordsByScore(loadWords(), charProb)
    banList = ['s','t','m','a','n','d','y','f','c']

    known = ['','o','','','e']

    impossibleCharacters = [
        [],
        ['e'],
        ['o'],
        [],
        []
        ]

    solutions1 = guessWord(banList)
    print("After first filter, grey letters.") 
    sortWordsByScore(solutions1, charProb)
    

    solutions2 = knownCharacters(solutions1,known) 
    print("After second filter, green letters") 
    sortWordsByScore(solutions2, charProb)


    solutions3 = possibleChars(solutions2,impossibleCharacters)
    print("After third filter, yellow letters")
    sortWordsByScore(solutions3, charProb)

