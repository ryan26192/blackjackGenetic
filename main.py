# Main executable blackjack game
from strategy import randomStrat, optStrat, printClean
from gameSeries import playSeries, playGame
from localSearch import search

NUM_GAMES_PER_STRATEGY = 100000
def main():
    printClean(search())


if __name__ == "__main__":
    main()