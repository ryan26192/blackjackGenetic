import random
from common import total
from deck import Deck

def dealCards(playerHand, dealerHand, deck):
    dealerHand.append(deck.dealCard())
    dealerHand.append(deck.dealCard())
    playerHand.append(deck.dealCard())
    playerHand.append(deck.dealCard())

def playSeries(playerStrat, numHandsToPlay):
    fitness = 0
    deck = Deck()
    bet = 5
    payoff = 1.5 * bet

    for i in range(numHandsToPlay):
        # init hands 
        dealerHand = []
        playerHand = []
        # deal hands
        dealCards(playerHand, dealerHand, deck)
        # add hand to playerHand
        playerHands = []
        playerHands.append(playerHand)

        # tracking bets per hand
        betAmountperHand = []
        betAmountperHand.append(bet)
        fitness -= bet

        # checking for immediate blackjack
        if total(playerHand) == 21:
            if total(dealerHand) != 21:
                fitness += betAmountperHand[0]
            else:
                fitness += payoff
            betAmountperHand[0] = 0
            continue
        
        # if dealer has blackjack go to next hand
        if total(dealerHand) == 21: continue

        # play through all of hands
        for i in range(len(playerHands)):
            playerHand = playerHands[i]
            gameState = 0 # 0 -> playerTurn, 1 -> dealer, 2 -> playerbusted, 3 -> dealerBusted
            while(gameState == 0):
                if total(playerHand) == 21:
                    if len(playerHand) == 2: # blackjack
                        blackjackPayoff = payoff * betAmountperHand[i] / bet
                        fitness += blackjackPayoff
                        betAmountperHand[i] = 0
                    gameState = 1
                    break
                # player choice through strategy
                choice = playerStrat.getMove(playerHand, dealerHand[0])
                
                # you can only double down with two cards
                if choice == 'D' and len(playerHand) > 2: choice = 'H'
                
                if choice == 'H': # hit
                    playerHand.append(deck.dealCard())
                    if total(playerHand) == 21:
                        #player gets blackjack so it's dealer's turn
                        gameState = 1
                    elif total(playerHand) > 21:
                        # player busted and loses bet, goes to playerBusted
                        betAmountperHand[i] = 0
                        gameState = 2
                elif choice == 'S': gameState = 1 # stay, so dealer's turn
                elif choice == 'D': # double down
                    fitness -= bet # bet's again
                    betAmountperHand[i] += bet
                    playerHand.append(deck.dealCard()) # add new card
                    if total(playerHand) > 21: 
                        # player busted
                        betAmountperHand[i] = 0
                        gameState = 2
                    else: gameState = 1 # player didn't bust, dealer's turn
                elif choice == 'P': # split
                    # add a new hand to playerHands and bets again
                    newHand = []
                    newHand.append(playerHand[1])
                    playerHand[1] = deck.dealCard()
                    playerHands.append(newHand)
                    fitness -= bet
                    betAmountperHand.append(bet)
    
        playerHandsAvailable = sum(betAmountperHand) > 0
        if playerHandsAvailable:
            # there is still player hands that didn't bust
            gameState = 1 # we are now at the dealer's turn
            while total(dealerHand) < 17: 
                # dealer hit's until they hit 17
                dealerHand.append(deck.dealCard())
                if total(dealerHand) > 21:
                    # dealer has busted so now player wins 2 * bet
                    for i in range(len(playerHands)):
                        fitness += betAmountperHand[i] * 2
                    gameState = 3 
                    break
            if gameState != 3:
                # dealer stayed so now we check for ties or wins
                dealerHandValue = total(dealerHand)
                for i in range(len(playerHands)):
                    # for each hand check for tie or win, loss was already counted
                    playerHandValue = total(playerHands[i])
                    if playerHandValue == dealerHandValue:
                        fitness += betAmountperHand[i]
                    elif playerHandValue > dealerHandValue:
                        fitness += betAmountperHand[i] * 2
    playerStrat.setFitness(fitness)
    return fitness



                

