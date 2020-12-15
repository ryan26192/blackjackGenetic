# Main executable blackjack game
from strategy import randomStrat, optStrat
from gameSeries import playSeries, playGame

NUM_GAMES_PER_STRATEGY = 100000
def main():
    playSeries(optStrat, NUM_GAMES_PER_STRATEGY)


if __name__ == "__main__":
    main()