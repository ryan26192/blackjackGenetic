# Game object
import os
import random
from common import total

# GameSeries object takes in a player strategy and a number of games in the series, N, 
# then runs that strategy against N randomly generated games

deck = [] # deck var
win = 5 # base amount a player gains from winning, bet is 2 dollars
loss = -7.50 # base amount a player loses from losing, bet is 2 dollars
# [gameNet dealerHand playerHand] gameNet returns the net loss/gain of the game by
# checking game end scenarios 
# returns 0 if the game is not ended, returns win if player won, returns loss if
# dealer won 
def gameNet(dealerHand, playerHand, playerStop):
    playerTotal = total(playerHand)
    dealerTotal = total(dealerHand)
    if playerTotal > 21:
        #print("player lost")
        return loss # player busts
    elif dealerTotal > 21:
        #print("player won")
        return win # dealer busts
    elif playerStop:
        if playerTotal > dealerTotal:
            #print("player won")
            return win
        else:
            #print("player lost")
            return loss
    return 0

# [addCard hand] adds a card to hand by popping a card off the shuffled deck
def addCard(hand):
    global deck
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
    global deck
    deck = [i for i in range(2, 15)] * 4
    random.shuffle(deck)

def playGamePair(playerHand1, playerHand2, dealerHand, playerStrat):
    global deck
    playerStop1, playerStop2 = False, False
    playerBust1, playerBust2 = False, False # True means that the player busted for that hand
    multiplier1, multiplier2 = 1, 1
    pairNet = 0
    #print('playerHand1: ' + str(playerHand1))
    #print('playerHand2: ' + str(playerHand2))
    i = 1
    while not playerStop1:
        net = multiplier1*gameNet(dealerHand, playerHand1, playerStop1)
        if net != 0: 
            playerBust1 = True
            pairNet += net
            break
        # get a choice from the playerStrat (pairAllowed = False)
        playerChoice = playerStrat.getMove(playerHand1, dealerHand[0], False)
        if playerChoice == 'H':
            addCard(playerHand1)
        elif playerChoice == 'D':
            addCard(playerHand1)
            multiplier1 = 2
            playerStop1=True
        elif playerChoice == 'S':
            playerStop1 = True
        #print("player 1's hand turn " + str(i) + ": " + str(playerHand1))
        i += 1
    i=0
    while not playerStop2:
        net = multiplier2*gameNet(dealerHand, playerHand2, playerStop2)
        if net != 0: 
            playerBust2 = True
            pairNet += net
            break
        # get a choice from the playerStrat (pairAllowed = False)
        playerChoice = playerStrat.getMove(playerHand2, dealerHand[0], False)
        if playerChoice == 'H':
            addCard(playerHand2)
        elif playerChoice == 'D':
            addCard(playerHand2)
            multiplier2 = 2
            playerStop2=True
        elif playerChoice == 'S':
            playerStop2 = True
        #print("player 2's hand turn " + str(i) + ": " + str(playerHand2))
        i += 1
    
    # if both player hands have busted, return
    if playerBust1 and playerBust2:
        return pairNet
    # play through dealers hand if player hasn't lost both hands
    while total(dealerHand) < 17:
        addCard(dealerHand)
    # give reward based on which player's hands have not yet busted
    if not playerBust1:
        pairNet += multiplier1*gameNet(dealerHand, playerHand1, playerStop1)
    if not playerBust2:
        pairNet += multiplier2*gameNet(dealerHand, playerHand2, playerStop2)
    return net


# returns the net gain (or loss) from a game
def playGame(dealerHand, playerHand, playerStrat):
    global deck
    playerStop = False # true if player chooses to stay
    multiplier = 1 # 2 if the player chooses to double down
    #print("player's starting hand: " + str(playerHand))
    #print("dealer's starting hand: " + str(dealerHand))

    # counter var to print turns
    i = 1

    # while loop to play through game until player chooses to stop
    while not playerStop:
        net = multiplier*gameNet(dealerHand, playerHand, playerStop)
        if net != 0: return net
        # get a choice from the playerStrat
        playerChoice = playerStrat.getMove(playerHand, dealerHand[0])
        # print("player's choice turn " + str(i) + ": " + str(playerChoice))
        if playerChoice == 'H':
            addCard(playerHand)
        elif playerChoice == 'P':
            # if player chooses to split we split the cards and play through with both
            # print('split has happened')
            playerHand1 = [playerHand[0]]
            addCard(playerHand1)
            playerHand2 = [playerHand[1]]
            addCard(playerHand2)
            return playGamePair(playerHand1, playerHand2, dealerHand, playerStrat)
        elif playerChoice == 'D':
            # double down bet
            addCard(playerHand)
            multiplier = 2
            playerStop=True
        elif playerChoice == 'S':
            playerStop = True   
        #print("player's hand turn " + str(i) + ": " + str(playerHand))
        i += 1

    # play through dealers hand if player hasn't lost yet
    while total(dealerHand) < 17:
        addCard(dealerHand)
    net = multiplier*gameNet(dealerHand, playerHand, playerStop)
    return net

def playSeries(playerStrat, numGames):
    global deck
    """plays a series of games and returns the net loss of those games using the input strategy

    Args:
        playerStrat: strategy object to use to simulate player
        numGames: number of sequential games to play
    """
    seriesNet = 0
    for _ in range(0, numGames):
        #print('new game')
        # shuffle and deal
        shuffle()
        dealerHand = deal()
        playerHand = deal()
        #play game
        seriesNet += playGame(dealerHand, playerHand, playerStrat)
    playerStrat.setFitness(seriesNet)
    return seriesNet
