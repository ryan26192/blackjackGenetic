import os
import random

deck = [i for i in range(2, 15)] * 4
playerStop = False

def total(hand):
    total = 0
    for card in hand:
        if card == 11:
            if total >= 11: total += 1
            else: total += 11
        else: total += card
    return total

class Strategy:
    hard = {
        5 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        6 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        7 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        8 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        10 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        11 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        12 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        13 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        14 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        15 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        16 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        17 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        18 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        19 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
    }
    soft = {
        2 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        3 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        4 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        5 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        6 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        7 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        8 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
    pair = {
        2 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        3 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        4 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        5 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        6 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        7 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        8 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        9 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        10 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H'],
        1 : ['H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H', 'H']
        }
    def isPair(self, hand):
        return all(x == hand[0] for x in hand)

    def getMove(self, playerHand, dealer):
        if 11 in playerHand:
            # soft hand
            nonAce = next(x for x in playerHand if x != 11)
            return self.soft[nonAce][dealer-2]
        elif self.isPair(playerHand):
            return self.pair[playerHand[0]][dealer-2]
        else:
            x = total(playerHand)
            return self.hard[x][dealer-2]

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
            print("no one wins lol")
            exit()



def deal():
    hand = []
    for i in range(2):
        random.shuffle(deck)
        card = deck.pop()
        card = 10 if card == 12 or card == 13 or card == 14 else card
        hand.append(card)
    return hand

def main():
    strat = Strategy()
    dealerHand = deal()
    playerHand = deal()
    print playerHand
    print dealerHand
    testWin(dealerHand, playerHand)
    playerChoice = strat.getMove(playerHand, dealerHand[0])
    print(playerChoice)

main()



# strat = Strategy()
# strat.getMove(11,2,11)