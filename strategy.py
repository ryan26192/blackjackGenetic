## Strategy file that holds a strategy class and
## initializes a the optimal strategy from beat the dealer
from common import total
import random
import json
from marshmallow import Schema, fields

choices = ['H', 'S', 'D']
choicesPair = ['H', 'S', 'D', 'P']
# creates a strategy object with the three tables
class Strategy:
    def __init__(self, hard, soft, pair, name='Random', fitness=0, numGenerations=0):
        self.hard = hard
        self.soft = soft
        self.pair = pair
        self.fitness = fitness
        self.name = name
        self.numGenerations = numGenerations

    def isPair(self, hand):
        if len(hand) > 2: return False
        return hand[0] == hand[1]
        
    def hasSoftAce(self, hand):
        numAces = hand.count(11)
        if numAces == 0: return False

        total = 11 + sum(x for x in hand if x != 11) + (numAces - 1)
        return total <= 21

    def getMove(self, playerHand, dealer, pairAllowed = True):
        if total(playerHand) >= 21: return 'S'

        if self.isPair(playerHand):
            return self.pair[playerHand[0]][dealer-2]
        if self.hasSoftAce(playerHand):
            # ensures having a soft ace
            numAces = playerHand.count(11)
            nonAceSum = sum(x for x in playerHand if x != 11) + (numAces - 1)
            return self.soft[nonAceSum][dealer-2]
        return self.hard[total(playerHand)][dealer-2]

    def setFitness(self, fitness):
        self.fitness = fitness

    def incrGen(self):
        self.numGenerations += 1
    
    def __eq__(self, strategy):
        if not isinstance(strategy, Strategy):
            return False
        return self.hard == strategy.hard and self.soft == strategy.soft and self.pair == strategy.pair
        
    def __str__(self):
        hardStr = ''
        for i in range(5,21): hardStr += str(i) + ': ' + str(self.hard[i]) + '\n'
        softStr = ''
        for i in range(2,10): softStr += str(i) + ': ' + str(self.soft[i]) + '\n'
        pairStr = ''
        for i in range(2,12): pairStr += str(i) + ': ' + str(self.pair[i]) + '\n'
        return "Strategy with Fitness: " + str(self.fitness) + \
               "\nCame from: " + self.name + \
               "\nHard Strat: \n" + hardStr + \
               "\nSoft Strat: \n" + softStr + \
               "\nPair Strat: \n" + pairStr + "\n\n"

class ObjectSchema(Schema):
    fitness = fields.Str()
    numGenerations = fields.Str()
    name = fields.Str()
    hard = fields.Dict()
    soft = fields.Dict()
    pair = fields.Dict()

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

def generateRowCrossOver(p1, p2, isPair):
    return [random.choice([p1[i],p2[i]]) for i in range(10)]

def generateTable(start, end, isPair=False):
    table = {}
    for i in range(start, end):
        table[i] = generateRow(isPair)
    return table

def generateTableCrossOver(start, end, p1, p2, isPair=False):
    table = {}
    for i in range(start, end):
        table[i] = generateRowCrossOver(p1[i], p2[i], isPair)
    return table
    
def randomStrat():
    #randomly generate hard, soft and pair dictionaries
    #return a new strat given that
    randomHard = generateTable(5, 21)
    randomSoft = generateTable(2, 10)
    randomPair = generateTable(2, 12, isPair=True)
    return Strategy(randomHard, randomSoft, randomPair)

## takes two parents and crossovers them to create a child
def crossOver(parent1, parent2):
    # p1Fitness = parent1.fitness + worstFitness
    # p2Fitness = parent2.fitness + worstFitness
    # choice = random.choices([0,1], weights=(p1Fitness / p2Fitness, 1), k = 1)
    crossHard = generateTableCrossOver(5,21, parent1.hard, parent2.hard)
    crossSoft = generateTableCrossOver(2,10, parent1.soft, parent2.soft)
    crossPair = generateTableCrossOver(2, 12, parent1.pair, parent2.pair)
    return Strategy(crossHard, crossSoft, crossPair, 'crossOver')

# fixes dictionary to be right format for a strategy
def fixDict(dict):
    return {int(k): v for k, v in dict.items()}

## converts a dict to a strategy
def convertToStrategy(s):
    strat = Strategy(
        fixDict(s['hard']),
        fixDict(s['soft']), 
        fixDict(s['pair']),
        name=s['name'],
        fitness=float(s['fitness']),
        numGenerations=int(s['numGenerations']))
    return strat

## Returns a list of strategies from a JSON
def getStrategiesFromGeneration(gen):
    f = open('generations/gen'+str(gen)+'.json',)
    data = json.load(f)['strategies']
    return [convertToStrategy(jsonStrat) for jsonStrat in data]

def bestStrategyFromNormalGeneration(gen):
    f = open('generations/gen'+str(gen)+'.json',)
    data = json.load(f)['best']
    return convertToStrategy(data)
def bestStrategyFromLowParamGeneration():
    f = open('generations100-10000/gen'+str(664)+'.json',)
    data = json.load(f)['best']
    return convertToStrategy(data)
def streakFromGeneration(gen):
    f = open('generations/gen'+str(gen)+'.json')
    data = json.load(f)['bestStratStreak']
    return int(data)
def testStrategy():
    f = open('testStrategyGeneration.json')
    data = json.load(f)['best']
    return convertToStrategy(data)