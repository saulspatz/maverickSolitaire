import solver

class Control(object):
    def __init__(self, parent, win):
        self.model = parent.model

    def onClick(self, event):
        view, model = self.view, self.model
        # find_closest returns singleton tuple
        ident= view.find_closest(event.x, event.y)[0]
        tags = [tag for tag in view.gettags(ident)]
        otag = [t for t in tags if t.startswith('order')]
        if not otag:
            return
        tag = otag[0]
        #view.lift(tag)
        view.addtag_withtag('floating', tag)
        x0, y0, x1, y1 = view.bbox('floating')

        self.oldHand = model.getHandWithCard(int(tag[5:]))
        self.mouseX = event.x            # for dragging
        self.mouseY = event.y

        self.floater = model.removeCard(self.oldHand, int(tag[5:]))
        view.displayHand(self.oldHand)
        view.lift(tag)

    def onRelease(self, event):
        # If the floating card is not dropped in a rectangle,
        # just put it back where it came from.  Otherwise:
        # Is the floating card in a new hand?
        # If not, only one hand needs to be rearranged.
        # If so, two hands must be rearranged, and the model notified,
        # and we have to check whether the user has solved the puzzle.

        view, model = self.view, self.model
        card = view.find_withtag('floating')     # find the selected card
        view.dtag('floating', 'floating')
        try:
            (w, n, e, s) = view.bbox(card)
        except TypeError:
            # Not clear why we ever get this error, but it happens.
            return

        # Move the card if it overlaps precisely one rectangle.
        # It overlaps if it doesn't lie wholly above, wholly below,
        # or wholly to the right or left of the rectangle.

        overlaps = []
        for r in range(6):
            tag = "rect%d" % r
            x1, y1, x2, y2 = view.bbox(tag)

            if not ( n > y2 or s < y1 or w > x2 or e < x1):
                    overlaps.append(r)

        if len(overlaps) != 1:

            # floating card was not dropped in a rectangle;
            # return to original hand

            newHand = self.oldHand
        else:
            newHand  = overlaps[0]
            view.enableShow()

        model.addCard(newHand, self.floater)
        del(self.floater)
        view.displayHand(newHand)
        if model.isSolved():
            solver.killThread = True
            view.celebrate()

    def onDrag(self, event):
        dx = event.x - self.mouseX
        dy = event.y - self.mouseY
        self.mouseX = event.x
        self.mouseY = event.y
        self.view.move('floating', dx, dy)

    def deal(self, event):
        view = self.view
        x1, y1, x2, y2 = view.getDealCoords()
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            view.disableDeal()
            # The sample comes back as a list of cards
            sample = self.model.deal()
            view.deal()
            self.solver = solver.Solver(sample)
            self.solver.start()

    def show(self, event):
        view, model = self.view, self.model
        x1, y1, x2, y2 = view.getShowCoords()
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            if solver.solution == None:
                self.solver.join()
            if not solver.solution:
                view.noSolution()
            else:
                model.transferCards(solver.solution)
                view.displayHands()
            view.disableClicks()
            view.enableDeal()

    def reset(self, event):
        view, model = self.view, self.model
        x1, y1, x2, y2 = view.getResetCoords()
        if x1 <= event.x <= x2 and y1 <= event.y <= y2:
            model.reset()
            view.reset()

    def dummyHandler(self, event):
        pass
