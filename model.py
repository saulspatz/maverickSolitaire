from random import sample


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
    def __init__(self, s=None):
        list.__init__(self)
        self.value = None
        if s: self.setCards(s)

    def numRanks(self):
        return len(set([x // 4 for x in self]))

    def flush(self):
        # We consider a straight flush as a straight to get the sorting right

        haveFlush = True if len(set([x % 4 for x in self])) == 1 else False
        if value := self.straight() != BUST:
            return value
        return FLUSH if haveFlush else BUST

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
        self.distribution = None

    def deal(self):
        self.clear()
        dist = self.distribution
        ranks = range(13)
        if not dist:
            self.sample =  sample(range(52), 25)
        else:
            self.sample =  [4*c for c in sample(ranks, dist[0])]
            self.sample +=  [4*c+1 for c in sample(ranks, dist[1])]
            self.sample +=  [4*c+2 for c in sample(ranks, dist[2])]
            self.sample +=  [4*c+3 for c in sample(ranks, dist[3])]
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

        # Arrange the hands so that, to the extent possible,
        # flushes are in their original position
        hands = [Hand(s) for s in solution]
        flushes =[h for h in hands if h.flush()]
        others =[h for h in hands if h not in flushes]
        place = [0,1,2,3]
        for flush in flushes:
            suit = flush[0]%4
            if not self.hands[place[suit]]:
                self.setHand(place[suit], flush)
            else:
                others.append(flush)
        available = [i for i in range(6) if not self.hands[i]]
        for hand, index in zip(others, available):
            self.setHand(index, hand)

        
        

    def patHands(self):
        return [k for k in range(6) if self.hands[k].isPat()]

    def reset(self):
        self.clear()
        for suit in range(4):
            self.setHand(suit, [c for c in self.sample if c % 4 == suit])
