# Solve a deal of Maverick Solitaire#
#         ********* ACE IS HIGH ************
#

# Result is indicated by global variable solution.
# Either it contains the five pats hands, or it is
# set to False.  The original value is None, the
# thread has exited if solution is not None.

import threading
from itertools import combinations, product

from model import DEUCE, TREY, FOUR, FIVE, SIX, SEVEN
from model import EIGHT, NINE, TEN, JACK, QUEEN, KING, ACE
from model import CLUB, DIAMOND, HEART, SPADE

class Solver(threading.Thread):
    def __init__(self, deal):
        global killThread
        killThread = False
        threading.Thread.__init__(self)
        self.deal = [(c // 4, c % 4) for c in deal]

    def findPatHands(self):

        # patHands is a list of all possible pathands.

        # Find all possible pat hands.
        # First, the flushes (including straight flushes)

        deal = self.deal
        patHands = []
        clubs =    [card for card in deal if card[1] == CLUB]
        diamonds = [card for card in deal if card[1] == DIAMOND]
        hearts =   [card for card in deal if card[1] == HEART]
        spades =   [card for card in deal if card[1] == SPADE]

        for suit in (clubs, diamonds, hearts, spades):
            patHands += list(combinations(suit, 5))

        ranks = [[card for card in deal if card[0] == rank]
                  for rank in range(13)]

        # Get the straights

        for rank in range(JACK):
            theRanks = ranks[rank:rank+5]
            if all(theRanks):
                patHands += product(*theRanks)

        # Now the low straights

        theRanks = [ranks[ACE]] + ranks[DEUCE:SIX]
        if all(theRanks):
            patHands += product(*theRanks)

        # Full houses

        ranks = [card[0] for card in deal]
        pairs = [rank for rank in range(13) if ranks.count(rank) == 2]
        trips = [rank for rank in range(13) if ranks.count(rank) == 3]
        fours = [rank for rank in range(13) if ranks.count(rank) == 4]

        ranks = [tuple([card for card in deal if card[0] == rank])
                 for rank in range(13)]

        for t in trips:
            T = ranks[t]
            for p in pairs:
                P = ranks[p]
                patHands += [T + P]

        for f in fours:
            F = ranks[f]
            for p in pairs:
                P = ranks[p]
                patHands += [P + s for s in combinations(F, 3)]

        for f in fours:
            F = ranks[f]
            for t in trips:
                T = ranks[t]
                patHands += [s1 + s2 for s1 in combinations(F, 3)
                             for s2 in combinations(T, 2)]
                patHands += [T +  s2 for s2 in combinations(F, 2)]

        for t1 in trips:
            T1 = ranks[t1]
            for t2 in trips:
                T2 = ranks[t2]
                if t1 != t2:
                    patHands += [T1 + p for p in combinations(T2, 2)]

        for f1 in fours:
            F1 = ranks[f1]
            for f2 in fours:
                F2 = ranks[f2]
                if f1 != f2:
                    patHands += [t + p for t in combinations(F1, 3)
                                 for p in combinations(F2, 2)]

        self.patHands = patHands

    def run(self):

        global solution
        solution = None

        self.findPatHands()

        # At this point, we have found all the possible pat hands.
        # We find all pat hands containing each individual card, and
        # sort the deck so that cards occurring in the fewest pat
        # hands come first

        pats = {}
        deal = self.deal
        for card in deal:
            pats[card] = [set(pat) for pat in self.patHands if card in pat]

        deal.sort(key = lambda c: len(pats[c]))

        # Try to find 5 pairwise disjoint pat hands.
        # We search for hands containing the rarest cards first

        for hand0 in pats[deal[0]]:
            if killThread: return
            card1 = [card for card in deal if card not in hand0][0]
            for hand1 in pats[card1]:
                if killThread:
                    return
                if any([c in hand1 for c in hand0]):
                    continue
                used1 = hand0.union(hand1)
                card2 = [card for card in deal if card not in used1][0]
                for hand2 in pats[card2]:
                    if killThread:
                        return
                    if any([c in hand2 for c in used1]):
                        continue
                    used2 = used1.union(hand2)
                    card3 = [card for card in deal if card not in used2][0]
                    for hand3 in pats[card3]:
                        if killThread:
                            return
                        if any([c in hand3 for c in used2]):
                            continue
                        used3 = used2.union(hand3)
                        card4 = [card for card in deal if card not in used3][0]
                        for hand4 in pats[card4]:
                            if killThread:
                                return
                            if all([card not in used3 for card in hand4]):
                                solution =  [hand0, hand1, hand2, hand3, hand4]
                                return
        solution =  False
