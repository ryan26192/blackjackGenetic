import random
from common import total
from deck import Deck

# def replaceCard(hand, deck):
#     card = deck.pop()
#     card = 10 if card == 12 or card == 13 or card == 13 else card
#     hand[1] = card

def calculateFitnessScore(playerStrat, numHandsToPlay):
    playerChips = 0
    deck = Deck()
    bet = 5
    payoff = 1.5 * bet

    for i in range(numHandsToPlay):
        # init hands 
        dealerHand = []
        playerHand = []
        # deal hands
        # addCard(dealerHand, deck)
        dealerHand.append(deck.dealCard())
        dealerHand.append(deck.dealCard())
        playerHand.append(deck.dealCard())
        playerHand.append(deck.dealCard())
        # add hand to playerHand
        playerHands = []
        playerHands.append(playerHand)

        # tracking bets per hand
        betAmountperHand = []
        betAmountperHand.append(bet)
        playerChips -= bet

        # checking for immediate blackjack
        if total(playerHand) == 21:
            if total(dealerHand) != 21:
                playerChips += betAmountperHand[0]
            else:
                playerChips += payoff
            betAmountperHand[0] = 0
            continue
        
        # if dealer has blackjack go to next hand
        if total(dealerHand) == 21: continue

        for i in range(len(playerHands)):
            playerHand = playerHands[i]
            gameState = 0 # 0 -> playerTurn, 1 -> dealer, 2 -> playerbusted, 3 -> dealerBusted
            while(gameState == 0):

                if total(playerHand) == 21:
                    if len(playerHand) == 2: # blackjack
                        blackjackPayoff = payoff * betAmountperHand[i] / bet
                        playerChips += blackjackPayoff
                        betAmountperHand[i] = 0
                    gameState = 1
                    break

                choice = playerStrat.getMove(playerHand, dealerHand[0])
                
                # you can only double down with two cards
                if choice == 'D' and len(playerHand) > 2: choice = 'H'
                
                if choice == 'H': # hit
                    # addCard(playerHand, deck)
                    playerHand.append(deck.dealCard())
                    if total(playerHand) == 21:
                        gameState = 1
                    elif total(playerHand) > 21:
                        betAmountperHand[i] = 0
                        gameState = 2
                elif choice == 'S': # stay
                    gameState = 1
                elif choice == 'D': # double down
                    playerChips -= bet
                    betAmountperHand[i] += bet

                    # addCard(playerHand, deck)
                    playerHand.append(deck.dealCard())
                    if total(playerHand) > 21: 
                        betAmountperHand[i] = 0
                        gameState = 2
                    else: gameState = 1
                elif choice == 'P': # split
                    newHand = []
                    newHand.append(playerHand[1])
                    playerHand[1] = deck.dealCard()
                    # replaceCard(playerHand, deck)
                    playerHands.append(newHand)

                    playerChips -= bet
                    betAmountperHand.append(bet)
    
        playerHandsAvailable = sum(betAmountperHand) > 0
        if playerHandsAvailable:
            gameState = 1

            while total(dealerHand) < 17:
                # addCard(dealerHand, deck)
                dealerHand.append(deck.dealCard())
                if total(dealerHand) > 21:
                    for i in range(len(playerHands)):
                        playerChips += betAmountperHand[i] * 2
                    gameState = 3
                    break
            if gameState != 3:
                dealerHandValue = total(dealerHand)
                for i in range(len(playerHands)):
                    playerHandValue = total(playerHands[i])

                    if playerHandValue == dealerHandValue:
                        playerChips += betAmountperHand[i]
                    elif playerHandValue > dealerHandValue:
                        playerChips += betAmountperHand[i] * 2
    playerStrat.setFitness(playerChips)
    return playerChips



                

