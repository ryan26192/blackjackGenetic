# Main executable blackjack game
import os
import random
from strategy import optStrat
from common import *

deck = [i for i in range(2, 15)] * 4  # deck global var
playerStop = False  # bool that is true when player's choice is S

# [testWin dealerHand playerHand] tests win scenarios and exits the game if
# one is met


def testWin(dealerHand, playerHand):
    playerTotal = total(playerHand)
    dealerTotal = total(dealerHand)
    if playerTotal > 21:
        print("player lost cause you busted")
        exit()
    elif dealerTotal > 21:
        print("player wins as dealer busted")
        exit()
    elif playerStop:
        if playerTotal > dealerTotal:
            print("player wins as you stopped with a higher value than dealer")
            exit()
        else:
            print("no one wins lol as dealer's total was higher than player")
            exit()
# [addCard hand] adds a card to hand by popping a card off the shuffled deck
# NOTE: cards are shuffled whenever addCard is called


def addCard(hand):
    random.shuffle(deck)
    card = deck.pop()
    card = 10 if card == 12 or card == 13 or card == 14 else card
    hand.append(card)
# [deal] returns a dealt deck with two random cards


def deal():
    hand = []
    for i in range(2):
        addCard(hand)
    return hand

# [main] main executable function


def main():
    global playerStop  # sets use of global var playerStop

    # deal hands to dealer and player
    dealerHand = deal()
    playerHand = deal()

    print "player's starting hand: " + str(playerHand)
    print "dealer's starting hand: " + str(dealerHand)

    # counter var to print turns
    i = 1

    # while loop to play through game until player chooses to stop
    while not playerStop:
        testWin(dealerHand, playerHand)  # at each turn we check win scenarios
        # using the beat the dealer optimal strat get a player choice
        playerChoice = optStrat.getMove(playerHand, dealerHand[0])
        print("player's choice turn " + str(i) + ": " + str(playerChoice))
        if playerChoice == 'H':
            # if player chooses to hit we add a card
            addCard(playerHand)
        elif playerChoice == 'P':
            # if player chooses to split we split the cards and play through with both
            # NOTE: don't know how this works tbh
            playerHand1 = [playerHand[0]]
            addCard(playerHand1)
            playerHand2 = [playerHand[1]]
            addCard(playerHand2)
            print("pairs are wack")
            exit()
            # splitGame(playerHand1, playerHand2, dealerHand)
        elif playerChoice == 'D':
            # double down bet
            # NOTE: not reall sure how this works tbh
            addCard(playerHand)
            print("double downs are wack")
            exit()
        elif playerChoice == 'S':
            # if player chooses to stay, go through dealer playing and test win state
            playerStop = True
            while total(dealerHand) < 17:
                addCard(dealerHand)
            testWin(dealerHand, playerHand)
        print "player's hand turn " + str(i) + ": " + str(playerHand)
        i += 1


main()
