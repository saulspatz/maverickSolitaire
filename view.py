from tkinter import *
from tkinter import simpledialog
from tkinter import messagebox
from tip import CanvasTooltip
import os

os.chdir('graphics')
cardHeight = 115
deltaX = 21
imageDict = {}   # hang on to images, or they may disappear!

unPatColor = '#b8b8b8'
patColor = '#d0ca1e'
resetCoords = (100, 690)
dealCoords = (700, 690)
showCoords = (700, 690)
textCoords = (400, 190)
settingsCoords = (400, 690)

suitStr = ('spade', 'heart', 'diamond', 'club')
rankStr = ('2', '3', '4', '5', '6', '7', '8', '9', '10',
           'Jack', 'Queen', 'King', 'Ace')


class View(Canvas):
    def __init__(self, parent, win, height, width, bg, cursor):
        Canvas.__init__(self, win, height=height, width=width,
                        bg=bg, cursor=cursor, relief='flat', borderwidth=0)
        self.model = parent.model
        self.control = parent.control
        self.pack(side=TOP, expand=YES, fill=BOTH)
        self.loadImages()                              # load all card images
        self.draw()

    def draw(self):
        self.create_rectangle(10,  20,  350, 145, width=2,
                              outline=unPatColor, tags=['rect0', 'rect'])
        self.create_rectangle(490,  20,  830, 145, width=2,
                              outline=unPatColor, tags=['rect1', 'rect'])
        self.create_rectangle(10, 225,  350, 350, width=2,
                              outline=unPatColor, tags=['rect4', 'rect'])
        self.create_rectangle(490, 225,  830, 350, width=2,
                              outline=unPatColor, tags=['rect5', 'rect'])
        self.create_rectangle(10, 430,  350, 555, width=2,
                              outline=unPatColor, tags=['rect2', 'rect'])
        self.create_rectangle(490, 430,  830, 555, width=2,
                              outline=unPatColor, tags=['rect3', 'rect'])

        self.create_text(400, 620, text="Make Five Pat Poker Hands",
                         fill=unPatColor, font=("Times", "24", "bold"))
        self.create_text(*textCoords, text="You Win!", fill=self.cget('bg'),
                         font=("Times", "24", "bold"), tag='winText')
        self.create_text(*textCoords, text="No Solution", fill=self.cget('bg'),
                         font=("Times", "24", "bold"), tag='noneText')
        self.create_image(-200, -200, image=imageDict['showMeButton'],
                          tag='showMeButton')
        self.create_image(-200, -200, image=imageDict['dealButton'],
                          tag='dealButton')
        self.create_image(-200, -200, image=imageDict['resetButton'],
                          tag='resetButton')
        self.create_image(-200, -200, image=imageDict['settingsButton'],
                          tag='settingsButton')
        self.create_image(-200, -200, image=imageDict['infoButton'],
                          tag='infoButton')
        self.enableDeal()
        control = self.control
        self.tag_bind('dealButton', '<ButtonRelease-1>', control.deal)
        self.tag_bind('showMeButton', '<ButtonRelease-1>', control.show)
        self.tag_bind('resetButton', '<ButtonRelease-1>', control.reset)
        self.tag_bind('settingsButton', '<ButtonRelease-1>', self.settings)
        self.distributionTip = CanvasTooltip(self, 'settingsButton', text='Random Deal')
        self.dealTip = CanvasTooltip(self, 'infoButton', text='')

    def loadImages(self):

        for card in range(52):
            foto = PhotoImage(file=suitStr[card %
                              4] + rankStr[card // 4] + '.png')
            imageDict[card] = foto
            self.create_image(-200, -200, image=foto, anchor=NW,
                              tag=['card', 'order%d' % card])
        imageDict['back'] = PhotoImage(file='blueBack.png')
        imageDict['dealButton'] = PhotoImage(file='dealButton.png')
        imageDict['showMeButton'] = PhotoImage(file='showMeButton.png')
        imageDict['resetButton'] = PhotoImage(file='resetButton.png')
        imageDict['settingsButton'] = PhotoImage(file='gear.png')
        imageDict['infoButton'] = PhotoImage(file='info.png')

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
        self.itemconfigure('winText', fill='yellow')
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
            self.coords(card, -200, -200)
        self.itemconfigure('winText', fill=self.cget('bg'))
        self.itemconfigure('noneText', fill=self.cget('bg'))
        model = self.model       
        lens = [len(h) for h in model.hands[:4]]
        tip = f'{lens[0]}-{lens[1]}-{lens[2]}-{lens[3]}'

        self.dealTip.configure(text=tip)
        self.displayHands()
        self.enableClicks()
        # self.enableShow()
        
        self.enableReset()
        self.disableDeal()

    # def deal(self, sample):
        # self.delete('card')
        # for card in self.find_withtag('card'):
        # self.coords(card,-200,-200)
        #self.itemconfigure('winText', fill = self.cget('bg'))
        #self.itemconfigure('noneText', fill = self.cget('bg'))
        # self.disableReset()
        # for k in range(6):
        #self.itemconfigure('rect%d' % k, outline = unPatColor)
        #x0, y0 = 400, 300
        #west, east, north, south = 100, 700, 60, 430
        #goal = [ (west, north), (east, north), (west, south), (east, south) ]

        #script = []
        # for item in sample:
        #x1, y1 = goal[item % 4]
        #dx = ( x1 - x0 ) // deltaX
        #dy = ( y1 - y0 ) // deltaX
        #ident = self.create_image(x0, y0, image = imageDict['back'])
        #script.append( (dx, dy, ident, item, 8) )
        # self.playScript(script)

    # def playScript(self, script):
        # if not script:
        # self.showPats(self.model.patHands())
        #self.after(400, self.enableClicks)
        # else:
        #self.dealBack( script[0] )
        #self.after( 250, self.playScript, script[1:] )

    # def dealBack(self, script):

        # play the animation script for dealing a card

        #dx, dy, item, card, n = script
        # if n == 0:
        # self.delete(item)
        #hand = card % 4
        #num = len(self.model.getCards(hand))
        #x0, y0, x1, y1 = self.bbox('rect%s' % hand)
        #x = x0 + 1 +  num*deltaX + deltaX // 2
        #y = y0 + (y1 - y0 - cardHeight) // 2
        #orderTag = 'order%d' % card
        #self.model.addCard(hand, card)
        # self.displayHand(hand)
        # else:
        #self.move(item, dx, dy)
        #self.after(25, self.dealBack, script[:-1]+(n-1,))

    def disableDeal(self):

        # move deal button and settings button off canvas
        # move the info button on

        self.coords('dealButton', -200, -200)
        self.coords('settingsButton', -200, -200)
        self.coords('infoButton', *settingsCoords)

    def enableDeal(self):

        # move deal button and settings buttons back on canvas
        # move the info button off

        self.coords('dealButton', *dealCoords)
        self.coords('settingsButton', *settingsCoords)
        self.coords('infoButton', -200, -200)

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
        self.itemconfigure('noneText', fill='red')

    def enableClicks(self):
        control = self.control
        self.tag_bind('card', '<Button-1>', control.onClick)
        self.tag_bind('card', '<ButtonRelease-1>', control.onRelease)
        self.tag_bind('card', '<B1-Motion>', control.onDrag)
        # self.enableShow()
        # self.enableReset()

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
                self.itemconfigure(rect, outline=patColor)
            else:
                self.itemconfigure(rect, outline=unPatColor)

    def deleteImages(self):
        for image in imageDict.values():
            image.__del__()

    def reset(self):
        self.itemconfigure('winText', fill=self.cget('bg'))
        self.itemconfigure('noneText', fill=self.cget('bg'))
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

    def settings(self, event):
        model = self.model
        dist = simpledialog.askstring("Distribution", 
               "S H D C or blank for random")
        if dist == None:  # user pressed cancel
            return 
        if dist == '':
            model.distribution = None
            tip = 'Random Deal'
        else:
            s = dist.translate({ord(','):ord(' ')}).split()
            if not all(x.isdigit() for x in s):
                messagebox.showerror("No Change", 
                                    f'Could nor parse {s}')
                return
            i = [int(x) for x in s]
            if sum(i) != 25:
                messagebox.showerror("No Change", 
                                    f'Distribution has {sum(i)} cards')
                return
            if any( 0 > j > 13):
                messagebox.showerror("No Change", 
                                    f'Suit length not between 0 and 13')

            i += (4-len(i)) * [0]
            model.distribution = i
            tip = f'{i[0]}-{i[1]}-{i[2]}-{i[3]} Deals'
            self.distributionTip.configure(text=tip)

        
            

        


