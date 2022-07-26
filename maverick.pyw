from tkinter import *
from model import Model
from control import Control
from view import View

# Maverick solitarire, using MVC pattern.

class Maverick(object):
    def __init__(self, win, height = 780, width = 820, cursor = 'hand2',
                 bg = '#166316'):
        self.win = win
        self.win.title('Maverick Solitaire')
        self.model = Model()
        self.control = Control(self, win)
        self.view = View(self, win, height = height, width = width,
                         bg = bg, cursor=cursor)
        self.control.view = self.view
    def destroy(self):
        self.view.deleteImages()
        self.win.destroy()

def main():
    root = Tk()
    root.resizable(False, False)
    mav = Maverick(root)
    root.protocol("WM_DELETE_WINDOW", mav.destroy)
    root.mainloop()

if __name__ == "__main__":
    main()