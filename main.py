# Main executable blackjack game
from strategy import randomStrat, optStrat
from gameSeries import playSeries

NUM_STRATEGIES = 3
NUM_GAMES_PER_STRATEGY = 100000
def main():
    for i in range(NUM_STRATEGIES):
        print(str(i)+ "| net loss from " + str(NUM_GAMES_PER_STRATEGY) +" games: " + str(playSeries(randomStrat(), NUM_GAMES_PER_STRATEGY)))


if __name__ == "__main__":
    main()