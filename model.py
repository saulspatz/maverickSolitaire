import random


ranks = (DEUCE, TREY, FOUR, FIVE, SIX, SEVEN, EIGHT, NINE, TEN, JACK,
         QUEEN, KING, ACE) = range(13)
suits = (CLUB, DIAMOND, HEART, SPADE) = range(4)
handValues = (BUST, LOWSTRAIGHT, STRAIGHT, FLUSH, FULL) = range(5)

# Each card is uniquely identified by an integer called it's "order."
# order = 4*rank + suit
# suit = order % 4
# rank = order // 4

# Hand is a list of cards, perhaps more or less than 5.
# If exactly 5, then it is a poker hand.

class Hand(list):
    def __init__(self):
        list.__init__(self)
        self.value = None

    def numRanks(self):
        return len(set([x // 4 for x in self]))

    def flush(self):
        if len(set([x % 4 for x in self])) != 1:
            return BUST
        s = self.straight()
        if not s:
            return FLUSH
        if s == LOWSTRAIGHT:
            return s

    def straight(self):
        if self.numRanks() != 5:
            return BUST
        ranks = [x // 4 for x in self]
        ranks.sort()
        if ranks[4] - ranks[0] == 4:
            return STRAIGHT
        elif ranks[4] == ACE and ranks[3] == FIVE:
            return LOWSTRAIGHT
        else:
            return BUST

    def full(self):
        ranks = [x // 4 for x in self]
        numRanks = len(set(ranks))
        hi = max([ranks.count(y) for y in ranks])
        if numRanks == 2 and hi == 3:
            return FULL
        else:
            return BUST

    def evaluate(self):
        if len(self) != 5:
            self.value = None
        else:
            answer = self.full()
            if not answer:
                answer = self.flush()
            if not answer:
                answer = self.straight()
            self.value =  answer

    def isPat(self):
        return self.value in (STRAIGHT, LOWSTRAIGHT, FLUSH, FULL)

    def setCards(self, cards):
        self[0:] = cards
        self.evaluate()
        self.sort()

    def isEmpty(self):
        return len(self) == 0

    def sort(self):
        list.sort(self)
        if self.value == LOWSTRAIGHT:
            self[0:] = [self[4]] + self[:4]

class Model(object):
    def __init__(self):
        self.hands = []
        for k in range(6):
            self.hands.append(Hand())

    def deal(self):
        self.clear()
        self.sample =  random.sample(range(52), 25)
        self.reset()
        return self.sample

    def clear(self):
        for h in self.hands:
            h.setCards([])
            h.value = None

    def isSolved(self):
        return all([h.isPat() or h.isEmpty() for h in self.hands])

    def setHand(self, hand, cards):
        self.hands[hand].setCards(cards)

    def removeCard(self, src, card):
        self.hands[src].remove(card)
        self.hands[src].evaluate()
        self.hands[src].sort()
        return card

    def addCard(self, dest, card):
        self.hands[dest].append(card)
        self.hands[dest].evaluate()
        self.hands[dest].sort()

    def getCards(self, hand):
        return self.hands[hand]

    def getHandWithCard(self, card):
        for hand in range(6):
            if card in self.hands[hand]:
                return hand

    def transferCards(self, solution):
        solution = [[4*card[0] + card[1] for card in hand]
                    for hand in solution]
        self.clear()
        for idx, hand in enumerate(solution):
            self.setHand(idx, hand)

    def patHands(self):
        return [k for k in range(6) if self.hands[k].isPat()]

    def reset(self):
        self.clear()
        for suit in range(5):
            self.setHand(suit, [c for c in self.sample if c % 4 == suit])
