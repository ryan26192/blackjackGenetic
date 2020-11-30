# Main executable blackjack game
import os
import random
from strategy import optStrat
from common import *
from gameSeries import playSeries

def main():
    print("net loss from 10 games: " + playSeries(optStrat, 10))