# Main executable blackjack game
from strategy import randomStrat, optStrat
from gameSeries import playSeries
import random

NUM_STRATEGIES = 2
NUM_GAMES_PER_STRATEGY = 100000
TOURNAMENT_SIZE = 2
def tournamentSelect(tournamentSize, strategySet):
    tourneyEntrants = random.sample(strategySet, k=tournamentSize)
    parent = max(tourneyEntrants, key = lambda strat: strat.fitness)
    return parent

def main():
    strategySet = set()
    for i in range(NUM_STRATEGIES):
        strat = randomStrat()
        strategyFitness = playSeries(strat, NUM_GAMES_PER_STRATEGY)
        strategySet.add(strat)
        print(str(i)+ "| net loss from " + str(NUM_GAMES_PER_STRATEGY) +" games: " + str(strategyFitness))
    ## Tournament Selection
    parentSet = set()
    for i in range(round(NUM_STRATEGIES/2)):
        parentSet.add(tournamentSelect(TOURNAMENT_SIZE, strategySet))
    print(' '.join(map(str, parentSet)))  

main()