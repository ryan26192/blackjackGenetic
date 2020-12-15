# Main executable blackjack game
from strategy import randomStrat, optStrat, printClean
from gameSeries import playSeries
from localSearch import search

NUM_STRATEGIES = 3
NUM_GAMES_PER_STRATEGY = 100000
def main():
    strat = search()
    printClean(strat)
    print(strat.hard)
    print(strat.soft)
    print(strat.pair)

if __name__ == "__main__":
    main()