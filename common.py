## common functions to share between strategy and main

## calculates total of a hand
# NOTE: is this the proper way to calculate total given and ace
def total(hand):
    total = 0
    for card in hand:
        if card == 11:
            if total >= 11:
                total += 1
            else:
                total += 11
        else:
            total += card
    return total
