from tkinter import *
import os
#import Image, ImageTk    # PIL
os.chdir('graphics')
cardHeight = 96
deltaX = 18
imageDict = {}   # hang on to images, or they may disappear!

unPatColor = '#b8b8b8'
patColor= '#d0ca1e'
resetCoords = (100, 540)
dealCoords = (700, 540)
showCoords = (700, 540)
textCoords = (400, 160)

suitStr = ('club', 'diamond', 'heart', 'spade')
rankStr = ('2', '3', '4', '5', '6', '7', '8','9', '10',
            'Jack', 'Queen', 'King','Ace')
class View(Canvas):
    def __init__(self, parent, win, height, width, bg, cursor):
        Canvas.__init__(self, win, height=height, width = width,
                        bg=bg, cursor=cursor, relief='flat', borderwidth=0)
        self.model = parent.model
        self.control = parent.control
        self.pack(side=TOP, expand = YES, fill = BOTH)
        self.loadImages()                              # load all card images
        self.draw()

    def draw(self):
        self.create_rectangle( 10,  20,  320, 120, width = 2,
                               outline = unPatColor, tags= ['rect0', 'rect'])
        self.create_rectangle(480,  20,  790, 120, width = 2,
                              outline = unPatColor, tags= ['rect1', 'rect'])
        self.create_rectangle( 10, 200,  320, 300, width = 2,
                               outline = unPatColor, tags= ['rect4', 'rect'])
        self.create_rectangle(480, 200,  790, 300, width = 2,
                              outline = unPatColor, tags= ['rect5', 'rect'])
        self.create_rectangle( 10, 380,  320, 480, width = 2,
                               outline = unPatColor, tags= ['rect2', 'rect'])
        self.create_rectangle(480, 380,  790, 480, width = 2,
                              outline = unPatColor, tags= ['rect3', 'rect'])

        self.create_text(400, 540, text ="Make Five Pat Poker Hands",
                         fill = unPatColor,font=("Times", "24", "bold"))
        self.create_text(*textCoords, text ="You Win!", fill = self.cget('bg'),
                         font=("Times", "24", "bold"), tag = 'winText')
        self.create_text(*textCoords, text ="No Solution", fill = self.cget('bg'),
                                 font=("Times", "24", "bold"), tag = 'noneText')
        self.create_image(-200, -200, image=imageDict['showMeButton'],
                          tag='showMeButton')
        self.create_image(-200, -200, image=imageDict['dealButton'],
                          tag='dealButton')
        self.create_image(-200, -200, image=imageDict['resetButton'],
                          tag = 'resetButton')
        self.enableDeal()
        control = self.control
        self.tag_bind('dealButton', '<ButtonRelease-1>', control.deal)
        self.tag_bind('showMeButton', '<ButtonRelease-1>', control.show)
        self.tag_bind('resetButton', '<ButtonRelease-1>', control.reset)

    def loadImages(self):

        for card in range(52):
            foto = PhotoImage(file =
                    suitStr[card % 4] + rankStr[card // 4] + '.gif')
            imageDict[card] = foto
            self.create_image(-200, -200, image = foto, anchor = NW,
                          tag = ['card', 'order%d' % card])
        imageDict['back'] = PhotoImage(file='blueBackVert.gif')
        imageDict['dealButton'] = PhotoImage(file='dealButton.gif')
        imageDict['showMeButton'] = PhotoImage(file='showMeButton.gif')
        imageDict['resetButton'] = PhotoImage(file='resetButton.gif')

    def displayHand(self, hand):
        model = self.model
        cards = model.getCards(hand)
        x0, y0, x1, y1 = self.bbox('rect%s' % hand)
        x0 += 1
        y0 += 1
        x1 -= 1
        y1 -= 1
        x = x0 + deltaX // 2
        y = y0 + (y1 - y0 - cardHeight) // 2
        for c in cards:
            tag = 'order%d' % c
            self.coords(tag, x, y)
            self.lift(tag)
            x += deltaX
        self.showPats(model.patHands())

    def displayHands(self):
        for hand in range(6):
            self.displayHand(hand)

    def celebrate(self):
        self.disableClicks()
        self.spreadHands()
        self.itemconfigure('rect', outline=unPatColor)
        self.lift('winText')
        self.itemconfigure('winText', fill = 'yellow')
        self.enableDeal()

    def spreadHands(self):
        # Spread the hands in celebration of a win

        for k in range(6):
            x0, y0, x1, y1 = self.bbox('rect%s' % k)
            x0 += 1
            y0 += 1
            x1 -= 1
            y1 -= 1
            x = x0 + deltaX
            y = y0 + (y1 - y0 - cardHeight) // 2

            hand = self.find_enclosed(x0, y0, x1, y1)

            for c in hand:
                self.coords(c, x, y)
                self.lift(c)
                x += 2*deltaX

    # The deal method sets up a "script" of 25 tuples,
    # one for each card in the deal.
    # The playScript method then plays them out at timed intervals

    # tuple format is: (dx, dy, itemID, card, timesRemaining)

    def deal(self):
        for card in self.find_withtag('card'):
            self.coords(card,-200,-200)
        self.itemconfigure('winText', fill = self.cget('bg'))
        self.itemconfigure('noneText', fill = self.cget('bg'))
        self.displayHands()
        self.enableClicks()
        self.enableShow()
        self.enableReset()
        self.disableDeal()

    #def deal(self, sample):
            ##self.delete('card')
            #for card in self.find_withtag('card'):
                #self.coords(card,-200,-200)
            #self.itemconfigure('winText', fill = self.cget('bg'))
            #self.itemconfigure('noneText', fill = self.cget('bg'))
            #self.disableReset()
            #for k in range(6):
                #self.itemconfigure('rect%d' % k, outline = unPatColor)
            #x0, y0 = 400, 300
            #west, east, north, south = 100, 700, 60, 430
            #goal = [ (west, north), (east, north), (west, south), (east, south) ]

            #script = []
            #for item in sample:
                #x1, y1 = goal[item % 4]
                #dx = ( x1 - x0 ) // deltaX
                #dy = ( y1 - y0 ) // deltaX
                #ident = self.create_image(x0, y0, image = imageDict['back'])
                #script.append( (dx, dy, ident, item, 8) )
            #self.playScript(script)

    #def playScript(self, script):
        #if not script:
            #self.showPats(self.model.patHands())
            #self.after(400, self.enableClicks)
        #else:
            #self.dealBack( script[0] )
            #self.after( 250, self.playScript, script[1:] )

    #def dealBack(self, script):

        ## play the animation script for dealing a card

        #dx, dy, item, card, n = script
        #if n == 0:
            #self.delete(item)
            #hand = card % 4
            #num = len(self.model.getCards(hand))
            #x0, y0, x1, y1 = self.bbox('rect%s' % hand)
            #x = x0 + 1 +  num*deltaX + deltaX // 2
            #y = y0 + (y1 - y0 - cardHeight) // 2
            #orderTag = 'order%d' % card
            #self.model.addCard(hand, card)
            #self.displayHand(hand)
        #else:
            #self.move(item, dx, dy)
        #self.after(25, self.dealBack, script[:-1]+(n-1,))

    def disableDeal(self):

        # move deal button off canvas

        self.coords('dealButton', -200, -200)

    def enableDeal(self):

        # move deal button back on canvas

        self.coords('dealButton', *dealCoords)

    def disableShow(self):

        # move show me button off canvas

        self.coords('showMeButton', -200, -200)

    def enableShow(self):

        # move show me button back on canvas

        self.coords('showMeButton', *showCoords)

    def enableReset(self):
        # move reset button back on canvas

        self.coords('resetButton', *resetCoords)

    def disableReset(self):
        # move reset button off canvas

        self.coords('resetButton', -200, -200)

    def noSolution(self):
        self.lift('noneText')
        self.itemconfigure('noneText', fill = 'red')

    def enableClicks(self):
        control = self.control
        self.tag_bind('card', '<Button-1>', control.onClick)
        self.tag_bind('card', '<ButtonRelease-1>', control.onRelease)
        self.tag_bind('card', '<B1-Motion>', control.onDrag)
        self.enableShow()
        self.enableReset()

    def disableClicks(self):
        self.disableShow()
        control = self.control
        self.tag_bind('card', '<Button-1>', control.dummyHandler)
        self.tag_bind('card', '<ButtonRelease-1>', control.dummyHandler)
        self.tag_bind('card', '<B1-Motion>', control.dummyHandler)

    def showPats(self, pats):
        for k in range(6):
            rect = 'rect'+str(k)
            if k in pats:
                self.itemconfigure(rect, outline = patColor)
            else:
                self.itemconfigure(rect, outline = unPatColor)

    def deleteImages(self):
        for image in imageDict.values():
            image.__del__()

    def reset(self):
        self.itemconfigure('winText', fill = self.cget('bg'))
        self.itemconfigure('noneText', fill = self.cget('bg'))
        self.displayHands()
        self.enableClicks()
        self.disableDeal()
        self.enableShow()

    def getDealCoords(self):
        return self.bbox('dealButton')

    def getShowCoords(self):
        return self.bbox('showMeButton')

    def getResetCoords(self):
        return self.bbox('resetButton')


