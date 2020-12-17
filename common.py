## common functions to share between strategy and main

## calculates total of a hand
def total(hand):
    highValue, lowValue = 0, 0
    ifAceWasUsedHigh = False # only one ace can be used as high
    for card in hand:
        if card == 11:
            if not ifAceWasUsedHigh:
                highValue += 11
                lowValue += 1
                ifAceWasUsedHigh = True
            else:
                highValue += 1
                lowValue += 1
        else:
            highValue += card
            lowValue += card
    if lowValue > 21: return lowValue
    if highValue > 21: return lowValue
    return highValue

def percentDifference(x, y):
    return (abs(x - y)/((abs(x) + abs(y))/2)) * 100
    