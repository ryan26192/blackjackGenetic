from strategy import setStrat, printClean
from gameSeries import playSeriesPerf
from common import total, isPair

NUM_GAMES = 100000000

def optimize():
    perf = Performance() # performance object to learn and then optimize from
    playSeriesPerf(setStrat('S'), NUM_GAMES, perf)
    playSeriesPerf(setStrat('H'), NUM_GAMES, perf)
    playSeriesPerf(setStrat('D'), NUM_GAMES, perf)
    playSeriesPerf(setStrat('P'), NUM_GAMES, perf)

    print("HARD")
    #print(perf.hard)
    printTable(perf.hard)
    print("SOFT")
    #print(perf.soft)
    printTable(perf.soft)
    print("PAIR")
    #print(perf.pair) 
    printTable(perf.pair)
    print(perf.bestStrat())

def printTable(table):
    for key in table:
        print(str(key) + ": " + str(table[key]) +"\n")

def generatePerfTable(start, end, isPair=False):
        table = {}
        for i in range(start, end):
            if isPair:
                table[i] = [{
                    'S': [0] * 2, # [net, number of games] using stay
                    'H': [0] * 2, # [net, number of games] using hit
                    'D': [0] * 2, # [net, number of games] using double
                    'P': [0] * 2 # [net, number of games] using split
                } for i in range(10)] 
            else:    
                table[i] = [{
                    'S': [0] * 2, # [net, number of games] using stay
                    'H': [0] * 2, # [net, number of games] using hit
                    'D': [0] * 2 # [net, number of games] using double
                } for i in range(10)] 
        return table

class Performance:
    def __init__(self):
        self.hard = generatePerfTable(5, 21)
        self.soft = generatePerfTable(2, 10)
        self.pair = generatePerfTable(2, 12, isPair=True)

    def getCell(self, playerHand, dealer):
        #print("player: " + str(playerHand) + ", dealer: " + str(dealer))
        if isPair(playerHand):
            return self.pair[playerHand[0]][dealer-2]
        elif 11 in playerHand:
            # soft hand
            nonAce = next(x for x in playerHand if x != 11)
            return None if nonAce == 10 else self.soft[nonAce][dealer-2]
        else:
            x = total(playerHand)
            return None if x >= 21 else self.hard[x][dealer-2]

    def bestStrat(self):
        # create strat to edit
        strat = setStrat('S')
        # Set hard table
        for playerKey in strat.hard:
            row = strat.hard[playerKey]
            for dealerKey, _ in enumerate(row):
                cell = self.hard[playerKey][dealerKey]
                stayAvg = float('-inf') if cell['S'][1] == 0 else cell['S'][0] / cell['S'][1]
                hitAvg = float('-inf') if cell['H'][1] == 0 else cell['H'][0] / cell['H'][1]
                doubAvg = float('-inf') if cell['D'][1] == 0 else cell['D'][0] / cell['D'][1]
                if max(stayAvg, hitAvg, doubAvg) == stayAvg:
                    row[dealerKey] = 'S'
                elif max(stayAvg, hitAvg, doubAvg) == hitAvg:
                    row[dealerKey] = 'H'
                else:
                    row[dealerKey] = 'D'
        # Set soft table
        for playerKey in strat.soft:
            row = strat.soft[playerKey]
            for dealerKey, _ in enumerate(row):
                cell = self.soft[playerKey][dealerKey]
                stayAvg = float('-inf') if cell['S'][1] == 0 else cell['S'][0] / cell['S'][1]
                hitAvg = float('-inf') if cell['H'][1] == 0 else cell['H'][0] / cell['H'][1]
                doubAvg = float('-inf') if cell['D'][1] == 0 else cell['D'][0] / cell['D'][1]
                if max(stayAvg, hitAvg, doubAvg) == stayAvg:
                    row[dealerKey] = 'S'
                elif max(stayAvg, hitAvg, doubAvg) == hitAvg:
                    row[dealerKey] = 'H'
                else:
                    row[dealerKey] = 'D'
        # Set pair table
        for playerKey in strat.pair:
            row = strat.pair[playerKey]
            for dealerKey, _ in enumerate(row):
                cell = self.pair[playerKey][dealerKey]
                stayAvg = float('-inf') if cell['S'][1] == 0 else cell['S'][0] / cell['S'][1]
                hitAvg = float('-inf') if cell['H'][1] == 0 else cell['H'][0] / cell['H'][1]
                doubAvg = float('-inf') if cell['D'][1] == 0 else cell['D'][0] / cell['D'][1]
                pairAvg = float('-inf') if cell['P'][1] == 0 else cell['P'][0] / cell['P'][1]
                if max(stayAvg, hitAvg, doubAvg, pairAvg) == stayAvg:
                    row[dealerKey] = 'S'
                elif max(stayAvg, hitAvg, doubAvg, pairAvg) == hitAvg:
                    row[dealerKey] = 'H'
                elif max(stayAvg, hitAvg, doubAvg, pairAvg) == pairAvg:
                    row[dealerKey] = 'P'
                else:
                    row[dealerKey] = 'D'
        return strat

""" class CellPerformance:
    def __init__(self, split=False):
        self.stay = [0] * 2 # [net, number of games] using stay
        self.hit = [0] * 2 # [net, number of games] using hit
        self.double = [0] * 2 # [net, number of games] using double
        if split: 
            self.split = [0] * 2 # [net, number of games] using double
        else:
            self.split = None """

optimize()