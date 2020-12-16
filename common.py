## common functions to share between strategy and main

## calculates total of a hand
def total(hand):
    total = 0
    hand.sort()
    for card in hand:
        if card == 11:
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total

def isPair(hand):
        if len(hand) == 2 and hand[0] == hand[1]: 
            return True
        else:
            return False
