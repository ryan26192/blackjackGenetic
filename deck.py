import random

# new Deck class that never becomes empty, 
# and resets whenever it gets low
class Deck:
    currentCard = 0
    cards = []
    numDecks = 4

    def __init__(self):
        self.createRandomDeck()

    def shuffle(self):
        random.shuffle(self.cards)
        self.currentCard = 0

    def createRandomDeck(self):
        self.cards = [i for i in range(2, 15)] * 4
        self.shuffle()

    def dealCard(self):
        self.shuffleIfNeeded()
        card = self.cards[self.currentCard]
        card = 10 if card == 12 or card == 13 or card == 14 else card
        self.currentCard += 1
        return card
    
    def shuffleIfNeeded(self):
        if self.cardsRemaining() < 20:
            self.shuffle()
    
    def cardsRemaining(self):
        return len(self.cards) - self.currentCard