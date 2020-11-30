# Game object
import os
import random
from strategy import optStrat
from common import *

# GameSeries object takes in a player strategy and a number of games in the series, N, 
# then runs that strategy against N randomly generated games

deck = [i for i in range(2, 15)] * 4  # deck var
win = 2 # base amount a player gains from winning
loss = -3 # base amount a player loses from losing

# [gameNet dealerHand playerHand] gameNet returns the net loss/gain of the game by
# checking game end scenarios 
# returns 0 if the game is not ended, returns win if player won, returns loss if
# dealer won 
def gameNet(dealerHand, playerHand, playerStop):
    playerTotal = total(playerHand)
    dealerTotal = total(dealerHand)
    if playerTotal > 21:
        print("player lost")
        return loss # player busts
    elif dealerTotal > 21:
        print("player won")
        return win # dealer busts
    elif playerStop:
        if playerTotal > dealerTotal:
            print("player won")
            return win
        else:
            print("player lost")
            return loss
    return 0

# [addCard hand] adds a card to hand by popping a card off the shuffled deck
def addCard(hand):
    card = deck.pop()
    card = 10 if card == 12 or card == 13 or card == 14 else card
    hand.append(card)

# [deal] returns a dealt deck with two random cards
# NOTE: resets deck and hand, then shuffles cards 
def deal():
    hand = []
    for _ in range(2):
        addCard(hand)
    return hand      

# [shuffle] resets & shuffles deck hand
def shuffle():
    deck = [i for i in range(2, 15)]
    random.shuffle(deck)

# returns the net gain (or loss) from a game
def playGame(dealerHand, playerHand, playerStrat):
    playerStop = False # true if player chooses to stay
    multiplier = 1 # 2 if the player chooses to double down

    print("player's starting hand: " + str(playerHand))
    print("dealer's starting hand: " + str(dealerHand))

    # counter var to print turns
    i = 1

    # while loop to play through game until player chooses to stop
    while not playerStop:
        net = multiplier*gameNet(dealerHand, playerHand, playerStop)
        if net != 0: return net
        # using the beat the dealer optimal strat get a player choice
        playerChoice = optStrat.getMove(playerHand, dealerHand[0])
        print("player's choice turn " + str(i) + ": " + str(playerChoice))
        if playerChoice == 'H':
            # if player chooses to hit we add a card
            addCard(playerHand)
        elif playerChoice == 'P':
            # if player chooses to split we split the cards and play through with both
            playerHand1 = [playerHand[0]]
            addCard(playerHand1)
            playerHand2 = [playerHand[1]]
            addCard(playerHand2)
            return playGame(dealerHand, playerHand1, playerStrat) + playGame(dealerHand, playerHand2, playerStrat)
        elif playerChoice == 'D':
            # double down bet
            addCard(playerHand)
            multiplier = 2
        elif playerChoice == 'S':
            # if player chooses to stay, go through dealer playing and test win state
            playerStop = True
            while total(dealerHand) < 17:
                addCard(dealerHand)
            net = multiplier*gameNet(dealerHand, playerHand, playerStop)
            if net != 0: return net
        print("player's hand turn " + str(i) + ": " + str(playerHand))
        i += 1


def playSeries(playerStrat, numGames):
    """plays a series of games and returns the net loss of those games using the input strategy

    Args:
        playerStrat: strategy object to use to simulate player
        numGames: number of sequential games to play
    """
    seriesNet = 0
    for _ in range(0, numGames):
        # shuffle and deal
        shuffle()
        dealerHand = deal()
        playerHand = deal()
        #play game
        seriesNet += playGame(dealerHand, playerHand, playerStrat)
    return seriesNet
