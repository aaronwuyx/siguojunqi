from Tkinter import *
from defines import *

class Board( Frame ):
    def __init__( self, parent = None, **config ):
        Frame.__init__( self, parent, config )
        self.pack( expand = YES, fill = BOTH )
        self.image = None
        self.back = Label( self )
        self.back.pack( side = TOP, fill = BOTH, expand = YES )
        self.Set_Background( '../resource/ugly1.gif' )
        self.front = Canvas( self )
        Button( self.back, text = 'button' ).pack()

    def Draw_Background( self, filename ):
        self.image = PhotoImage( file = filename )
        self.back.config( image = self.image )

    def Draw_Map( self, maps ):
        if maps is rule.Map:
            for pos in range( 0, maps.size ):
                self.Draw_Position( pos )
                self.Draw_Chess( pos, maps.GetValue( pos ) )

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
