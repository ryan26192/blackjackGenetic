## Strategy file that holds a strategy class and
## initializes a the optimal strategy from beat the dealer
from common import *
import random

choices = ['H', 'S', 'D']
choicesPair = ['H', 'S', 'D', 'P']
# creates a strategy object with the three tables
class Strategy:
    def __init__(self, hard, soft, pair):
        self.hard = hard
        self.soft = soft
        self.pair = pair

    def isPair(self, hand):
        return all(x == hand[0] for x in hand)

    def getMove(self, playerHand, dealer):
        if self.isPair(playerHand):
            return self.pair[playerHand[0]][dealer-2]
        elif 11 in playerHand:
            # soft hand
            nonAce = next(x for x in playerHand if x != 11)
            return 'S' if nonAce == 10 else self.soft[nonAce][dealer-2]
        else:
            x = total(playerHand)
            return 'S' if x >= 21 else self.hard[x][dealer-2]


optHard = {
    5: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    6: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    7: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    8: ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
    9: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    10: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
    11: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'D'],
    12: ['H', 'H', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    13: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    14: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    15: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    16: ['S', 'S', 'S', 'S', 'S', 'H', 'H', 'H', 'H', 'H'],
    17: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    18: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    19: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    20: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
}
optSoft = {
    2: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    3: ['H', 'H', 'H', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    4: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    5: ['H', 'H', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    6: ['H', 'D', 'D', 'D', 'D', 'H', 'H', 'H', 'H', 'H'],
    7: ['D', 'D', 'D', 'D', 'D', 'S', 'S', 'H', 'H', 'H'],
    8: ['S', 'S', 'S', 'S', 'D', 'S', 'S', 'S', 'S', 'S'],
    9: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S']
}
optPair = {
    2: ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    3: ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    4: ['H', 'H', 'H', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
    5: ['D', 'D', 'D', 'D', 'D', 'D', 'D', 'D', 'H', 'H'],
    6: ['P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H', 'H'],
    7: ['P', 'P', 'P', 'P', 'P', 'P', 'H', 'H', 'H', 'H'],
    8: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
    9: ['P', 'P', 'P', 'P', 'P', 'S', 'P', 'P', 'S', 'S'],
    10: ['S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S', 'S'],
    11: ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P', 'P']
}

optStrat = Strategy(optHard, optSoft, optPair)

def generateRow(isPair):
    moves = choicesPair if isPair else choices
    return [random.choice(moves) for i in range(10)]

def generateTable(start, end, isPair=False):
    table = {}
    for i in range(start, end):
        table[i] = generateRow(isPair)
    return table

def randomStrat():
    #randomly generate hard, soft and pair dictionaries
    #return a new strat given that
    randomHard = generateTable(5, 21)
    # print("hard: " + str(randomHard))
    randomSoft = generateTable(2, 10)
    # print("soft: " + str(randomSoft))
    randomPair = generateTable(2, 12, isPair=True)
    # print("pair: " + str(randomPair))
    return Strategy(randomHard, randomSoft, randomPair)