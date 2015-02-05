import random
import string
import urllib2
import random
import string
import time

VOWELS = 'aeiou'
CONSONANTS = 'bcdfghjklmnpqrstvwxyz'
HAND_SIZE = 7

SCRABBLE_LETTER_VALUES = {
    'a': 1, 'b': 3, 'c': 3, 'd': 2, 'e': 1, 'f': 4, 'g': 2, 'h': 4, 'i': 1, 'j': 8, 'k': 5, 'l': 1, 'm': 3, 'n': 1, 'o': 1, 'p': 3, 'q': 10, 'r': 1, 's': 1, 't': 1, 'u': 1, 'v': 4, 'w': 4, 'x': 8, 'y': 4, 'z': 10
}

def loadWords():
    print "Loading word list from website..."
    word_site = "http://svnweb.freebsd.org/csrg/share/dict/words?view=co&content-type=text/plain"
    response = urllib2.urlopen(word_site)
    wordList = response.read().splitlines()
    for i in range(0, len(wordList)):
        wordList[i] = wordList[i].translate(string.maketrans('', ''), " .,/\|:;[]{}'`!@#$&*^%()-_+=")
        wordList[i] = wordList[i].lower()
        wordList[i] = wordList[i].strip()
    print "  ", len(wordList), "words loaded."
    return wordList


def getFrequencyDict(sequence):
    freq = {}
    for x in sequence:
        freq[x] = freq.get(x,0) + 1
    return freq

def getWordScore(word, n):
    length = len(word)
    points = 0
    for i in range(0, length):
        letter = word[i]
        point = SCRABBLE_LETTER_VALUES[letter]
        points = points + point
    points = points * length
    if (length >= n):
        points = points + 50
    return points

def displayHand(hand):
    for letter in hand.keys():
        for j in range(hand[letter]):
             print letter,
    print


def dealHand(n):
    hand={}
    numVowels = n / 3
    
    for i in range(numVowels):
        x = VOWELS[random.randrange(0,len(VOWELS))]
        hand[x] = hand.get(x, 0) + 1
        
    for i in range(numVowels, n):    
        x = CONSONANTS[random.randrange(0,len(CONSONANTS))]
        hand[x] = hand.get(x, 0) + 1
        
    return hand

def updateHand(hand, word):
    newHand = hand.copy()
    frequency = getFrequencyDict(word)
    for letter in frequency:
        has = newHand.get(letter, 0)
        needs = frequency[letter]
        new = has-needs
        if (new < 0):
            new = 0
        newHand[letter] = new
    return newHand

def isValidWord(word, hand, wordList):
    check = False;
    tHand = hand.copy()
    if (word in wordList):
        check = True
        for i in range(0, len(word)):
            letter = word[i]
            if (tHand.get(letter, 0) <= 0):
                check = False
            else:
                tHand[letter] = tHand[letter] - 1
    return check

def calculateHandlen(hand):
    count = 0
    for letter in hand:
        count = count + hand[letter]
    return count

def playHand(hand, wordList, n):
   score = 0
   while calculateHandlen(hand) > 0:
        displayHand(hand)
        word = raw_input("Enter word, or a \".\" to indicate that you are finished:")
        if (word == '.'):
            break;
        else:
            if (not isValidWord(word, hand, wordList)):
                print "Invalid word, please try again."
                print
            else:
                score = score + getWordScore(word, n)
                print "\"" + word + "\" earned " + str(getWordScore(word, n)) + " points. Total: " + str(score) + " points" 
                print
                hand = updateHand(hand, word)
   if (calculateHandlen(hand) > 0):
        print "Run out of letters. Total score: " + str(score) + " points."
   else:
        print "Goodbye! Total score: " + str(score) + " points. "

def getPossibleWords(hand, wordList):
    words = []
    letterCount = calculateHandlen(hand)
    for word in wordList:
        if (len(word) <= letterCount):
            if (isValidWord(word, hand, wordList)):
                words.append(word)
    return words

def compChooseWord(hand, wordList, n):
    letterCount = calculateHandlen(hand)
    choosenWord = None
    if (letterCount > 0):
        words = getPossibleWords(hand, wordList)
        if (len(words) > 0):
            last = 0
            for word in words:
                score = getWordScore(word, n)
                if (score > last):
                    last = last
                    choosenWord = word
    return choosenWord

def playHand(hand, wordList, n):
    score = 0
    while calculateHandlen(hand) > 0:
        displayHand(hand)
        word = raw_input("Enter word, or a \".\" to indicate that you are finished:")
        if (word == '.'):
            break;
        else:
            if (not isValidWord(word, hand, wordList)):
                print "Invalid word, please try again."
                print
            else:
                score = score + getWordScore(word, n)
                print "\"" + word + "\" earned " + str(getWordScore(word, n)) + " points. Total: " + str(score) + " points" 
                print
                hand = updateHand(hand, word)
    if (calculateHandlen(hand) > 0):
        print "Run out of letters. Total score: " + str(score) + " points."
    else:
        print "Goodbye! Total score: " + str(score) + " points. "

def getPossibleWords(hand, wordList):
    words = []
    letterCount = calculateHandlen(hand)
    for word in wordList:
        if (len(word) <= letterCount):
            if (isValidWord(word, hand, wordList)):
                words.append(word)
    return words

def compChooseWord(hand, wordList, n):
    letterCount = calculateHandlen(hand)
    choosenWord = None
    if (letterCount > 0):
        words = getPossibleWords(hand, wordList)
        if (len(words) > 0):
            last = 0
            for word in words:
                score = getWordScore(word, n)
                if (score > last):
                    last = score
                    choosenWord = word
    return choosenWord


def compPlayHand(hand, wordList, n):
    score = 0
    while calculateHandlen(hand) > 0:
        hmsg = "Current Hand: "
        for letter in hand.keys():
            for j in range(hand[letter]):
                 hmsg = hmsg + str(letter) + " "
        print hmsg
        word = compChooseWord(hand, wordList, n)
        if (word == None):
            break
        else:
            if (isValidWord(word, hand, wordList)):
                score = score + getWordScore(word, n)
                hand = updateHand(hand, word)
                print "\"" + word + "\" earned " + str(getWordScore(word, n)) + " points. Total: " + str(score) + " points" 
                print
    print "Total score: " + str(score) + " points."

def playGame(wordList):
    last = None
    validCommand = False
    while True:

        if (validCommand == False):
            option = raw_input("Enter n to deal a new hand, r to replay the last hand, or e to end game:")
            if (option == "n"):
                hand = dealHand(HAND_SIZE)
                last = hand
                validCommand = True
            elif (option == "r"):
                if (not(last == None)):
                    validCommand = True
                    hand = last
                else:
                    print "You have not played a hand yet. Please play a new hand first!"
            elif (option == "e"):
                break
            else:
                print "Invalid command."
        
        if (validCommand):
            option = raw_input("Enter u to have yourself play, c to have the computer play: ")
            if (option == "u"):
                playHand(hand, wordList, HAND_SIZE)
                validCommand = False
            elif (option == "c"):
                compPlayHand(hand, wordList, HAND_SIZE)
                validCommand = False
            elif (option == "e"):
                break
            else:
                print "Invalid command."
    return None

        
if __name__ == '__main__':
    wordList = loadWords()
    playGame(wordList)


