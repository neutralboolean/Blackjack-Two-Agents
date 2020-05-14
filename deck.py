from card import Card, Suits, Ranks
from random import shuffle

class Deck:
    def __init__(self):
        self.cards = list()
        self.discard = list()

        for suit in Suits:
            for rank in Ranks:
                self.cards.append(Card(rank, suit))

        self.reshuffle()
        self.cardsCount = len(self.cards)

    def draw(self):
        drawn = self.cards.pop()
        self.discard.append(drawn)
        return drawn;

    def getNumberOfCardsTotal(self):
        return self.cardsCount

    def getNumberOfCardsLeft(self):
        return len(self.cards)

    def restartDeck(self):
        """
        Puts all the cards back in the deck and reshuffles them.
        """
        self.cards.extend(self.discard)
        self.reshuffle()
        self.discard.clear()

    def copyDeck(self):
        newDeck = Deck()
        copy = list(self.cards)
        newDeck.cards = copy
        return newDeck

    def reshuffle(self):
        shuffle(self.cards)
