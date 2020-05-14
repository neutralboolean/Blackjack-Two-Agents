from enum import Enum

class Suits(Enum):
    HEART = "♡(Hearts)"
    SPADE = "♠(Spade)"
    DIAMOND = "♢(Diamond)"
    CLUB = "♣(Club)"

class Ranks(Enum):
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5
    SIX = 6
    SEVEN = 7
    EIGHT = 8
    NINE = 9
    TEN = 10
    JACK = "J"
    QUEEN = "Q"
    KING = "K"
    ACE = "A"


class Card:
    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit

    def getScore(self):
        if self.rank in (Ranks.JACK, Ranks.QUEEN, Ranks.KING):
            return 10
        elif self.rank is Ranks.ACE:
            return 11
        else:
            return self.rank.value

    def getSuit(self):
        return self.suit

    def getRank(self):
        return self.rank

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            compare = self.rank is other.getRank()
            return compare and self.suit is other.getSuit()
        else:
            return False

    def __str__(self):
        return self.rank.value + " " + self.suit.value
