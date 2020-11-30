# Main executable blackjack game
import os
import random
from strategy import optStrat
from gameSeries import playSeries

def main():
    print("net loss from 10 games: " + str(playSeries(optStrat, 10)))

main()