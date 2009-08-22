from Tkinter import *
from defines import *

class Board( Frame ):
    def __init__( self, parent = None, **config ):
        Frame.__init__( self, parent, config )
        self.pack( expand = YES, fill = BOTH )
        self.Draw_Background()
        Button( self.back, text = 'button' ).pack()
    def Draw_Background( self ):
        self.image = PhotoImage( file = 'ugly1.gif' )
#        self.wid = self.image.width()
#        self.hei = self.image.height()
        self.back = Label( self, image = self.image )
        self.back.pack( side = TOP, fill = BOTH, expand = YES )
    def Draw_Map( self, maps ):
        for pos in Pos4:
            self.drawposition( pos )
        return
    def Draw_Position( self, position, highlight = False ):
        print position
        #draw a rectangle at x y?
        return
    def Draw_Chess( self, somedata ):
        return
    def run( self ):
        self.mainloop()

if __name__ == '__main__':
    b = Board()
#    b.Draw_Map( rule.Map() )
    b.run()
