#coding = gbk
MAXPLAYER = 4
MAXPOSITION = 129

Term4 = [3, 4, 1, 2]
Term2 = [None, None]

class Position:
    def __init__( self, safe, move, x, y, link ):
        self.safe = safe
        self.move = move
        self.x = x
        self.y = y
        self.link = link

Pos4 = [
#0 .. 29
        Position( False, True, 6, 0, [1, 5] ), Position( False, False, 7, 0, [0, 2, 6] ), Position( False, True, 8, 0, [1, 3, 7] ),
        Position( False, False, 9, 0, [2, 4, 8] ), Position( False, True, 10, 0, [3, 9] ), Position( False, True, 6, 1, [0, 6, 10, 11] ),
        Position( False, True, 7, 1, [1, 5, 7, 11] ), Position( False, True, 8, 1, [2, 6, 8, 11, 12, 13] ), Position( False, True, 9, 1, [3, 7, 9, 13] ),
        Position( False, True, 10, 1, [4, 8, 13, 14] ), Position( False, True, 6, 2, [5, 11, 15] ), Position( True, True, 7, 2, [5, 6, 7, 10, 12, 15, 16, 17] ),
        Position( False, True, 8, 2, [7, 11, 13, 17] ), Position( True, True, 9, 2, [7, 8, 9, 12, 14, 17, 18, 19] ), Position( False, True, 10, 2, [9, 13, 19] ),
        Position( False, True, 6, 3, [10, 11, 16, 20, 21] ), Position( False, True, 7, 3, [11, 15, 17, 21] ), Position( True, True, 8, 3, [11, 12, 13, 16, 18, 21, 22, 23] ),
        Position( False, True, 9, 3, [13, 17, 19, 23] ), Position( False, True, 10, 3, [13, 14, 18, 23, 24] ), Position( False, True, 6, 4, [15, 21, 25] ),
        Position( True, True, 7, 4, [15, 16, 17, 20, 22, 25, 26, 27] ), Position( False, True, 8, 4, [17, 21, 23, 27] ), Position( True, True, 9, 4, [17, 18, 19, 22, 24, 27, 28, 29] ),
        Position( False, True, 10, 4, [19, 23, 29] ),
        Position( False, True, 6, 5, [20, 21, 26, 119, 127] ), Position( False, True, 7, 5, [21, 25, 27] ), Position( False, True, 8, 5, [21, 22, 23, 26, 28, 120] ),
        Position( False, True, 9, 5, [23, 27, 29] ), Position( False, True, 10, 5, [23, 24, 28, 55, 121] ),
#30 .. 59 x=16-y,y=x
        Position( False, True, 16, 6, [31, 35] ), Position( False, False, 16, 7, [30, 32, 36] ), Position( False, True, 16, 8, [31, 33, 37] ),
        Position( False, False, 16, 9, [32, 34, 38] ), Position( False, True, 16, 10, [33, 39] ), Position( False, True, 15, 6, [30, 36, 40, 41] ),
        Position( False, True, 15, 7, [31, 35, 37, 41] ), Position( False, True, 15, 8, [32, 36, 38, 41, 42, 43] ), Position( False, True, 15, 9, [33, 37, 39, 43] ),
        Position( False, True, 15, 10, [34, 38, 43, 44] ), Position( False, True, 14, 6, [35, 41, 45] ), Position( True, True, 14, 7, [35, 36, 37, 40, 42, 45, 46, 47] ),
        Position( False, True, 14, 8, [37, 41, 43, 47] ), Position( True, True, 14, 9, [37, 38, 39, 42, 44, 47, 48, 49] ), Position( False, True, 14, 10, [39, 43, 49] ),
        Position( False, True, 13, 6, [40, 41, 46, 50, 51] ), Position( False, True, 13, 7, [41, 45, 47, 51] ), Position( True, True, 13, 8, [41, 42, 43, 46, 48, 51, 52, 53] ),
        Position( False, True, 13, 9, [43, 47, 49, 53] ), Position( False, True, 13, 10, [43, 44, 48, 53, 54] ), Position( False, True, 12, 6, [45, 51, 55] ),
        Position( True, True, 12, 7, [45, 46, 47, 50, 52, 55, 56, 57] ), Position( False, True, 12, 8, [47, 51, 53, 57] ), Position( True, True, 12, 9, [47, 48, 49, 52, 54, 57, 58, 59] ),
        Position( False, True, 12, 10, [49, 53, 59] ),
        Position( False, True, 11, 6, [50, 51, 56, 29, 121] ), Position( False, True, 11, 7, [51, 55, 57] ), Position( False, True, 11, 8, [51, 52, 53, 56, 58, 122] ),
        Position( False, True, 11, 9, [53, 57, 59] ), Position( False, True, 11, 10, [53, 54, 58, 85, 123] ),
#60 .. 89 x=16-x y=16-y
        Position( False, True, 10, 16, [61, 65] ), Position( False, False, 9, 16, [60, 62, 66] ), Position( False, True, 8, 16, [61, 63, 67] ),
        Position( False, False, 7, 16, [62, 64, 68] ), Position( False, True, 6, 16, [63, 69] ), Position( False, True, 10, 15, [60, 66, 70, 71] ),
        Position( False, True, 9, 15, [61, 65, 67, 71] ), Position( False, True, 8, 15, [62, 66, 68, 71, 72, 73] ), Position( False, True, 7, 15, [63, 67, 69, 73] ),
        Position( False, True, 6, 15, [64, 68, 73, 74] ), Position( False, True, 10, 14, [65, 71, 75] ), Position( True, True, 9, 14, [65, 66, 67, 70, 72, 75, 76, 77] ),
        Position( False, True, 8, 14, [67, 71, 73, 77] ), Position( True, True, 7, 14, [67, 68, 69, 72, 74, 77, 78, 79] ), Position( False, True, 6, 14, [69, 73, 79] ),
        Position( False, True, 10, 13, [70, 71, 76, 80, 81] ), Position( False, True, 9, 13, [71, 75, 77, 81] ), Position( True, True, 8, 13, [71, 72, 73, 76, 78, 81, 82, 83] ),
        Position( False, True, 7, 13, [73, 77, 79, 83] ), Position( False, True, 6, 13, [73, 74, 78, 83, 84] ), Position( False, True, 10, 12, [75, 81, 85] ),
        Position( True, True, 9, 12, [75, 76, 77, 80, 82, 85, 86, 87] ), Position( False, True, 8, 12, [77, 81, 83, 87] ), Position( True, True, 7, 12, [77, 78, 79, 82, 84, 87, 88, 89] ),
        Position( False, True, 6, 12, [79, 83, 89] ),
        Position( False, True, 10, 11, [59, 80, 81, 86, 123] ), Position( False, True, 9, 11, [81, 85, 87] ), Position( False, True, 8, 11, [81, 82, 83, 86, 88, 124] ),
        Position( False, True, 7, 11, [83, 87, 89] ), Position( False, True, 6, 11, [83, 84, 88, 115, 125] ),
#90 .. 119 x=y y=16-x
        Position( False, True, 0, 10, [91, 95] ), Position( False, False, 0, 9, [90, 92, 96] ), Position( False, True, 0, 8, [91, 93, 97] ),
        Position( False, False, 0, 7, [92, 94, 98] ), Position( False, True, 0, 6, [93, 99] ), Position( False, True, 1, 10, [90, 96, 100, 101] ),
        Position( False, True, 1, 9, [91, 95, 97, 101] ), Position( False, True, 1, 8, [92, 96, 98, 101, 102, 103] ), Position( False, True, 1, 7, [93, 97, 99, 103] ),
        Position( False, True, 1, 6, [94, 98, 103, 104] ), Position( False, True, 2, 10, [95, 101, 105] ), Position( True, True, 2, 9, [95, 96, 97, 100, 102, 105, 106, 107] ),
        Position( False, True, 2, 8, [97, 101, 103, 107] ), Position( True, True, 2, 7, [97, 98, 99, 102, 104, 107, 108, 109] ), Position( False, True, 2, 6, [99, 103, 109] ),
        Position( False, True, 3, 10, [100, 101, 106, 110, 111] ), Position( False, True, 3, 9, [101, 105, 107, 111] ), Position( True, True, 3, 8, [101, 102, 103, 106, 108, 111, 112, 113] ),
        Position( False, True, 3, 7, [103, 107, 109, 113] ), Position( False, True, 3, 6, [103, 104, 108, 113, 114] ), Position( False, True, 4, 10, [105, 111, 115] ),
        Position( True, True, 4, 9, [105, 106, 107, 110, 112, 115, 116, 117] ), Position( False, True, 4, 8, [107, 111, 113, 117] ), Position( True, True, 4, 7, [107, 108, 109, 112, 114, 117, 118, 119] ),
        Position( False, True, 4, 6, [109, 113, 119] ),
        Position( False, True, 5, 10, [89, 110, 111, 116, 125] ), Position( False, True, 5, 9, [111, 115, 117] ), Position( False, True, 5, 8, [111, 112, 113, 116, 118, 126] ),
        Position( False, True, 5, 7, [113, 117, 119] ), Position( False, True, 5, 6, [25, 113, 114, 118, 127] ),
#120 .. 128
        Position( False, True, 8, 6, [27, 121, 127, 128] ), Position( False, True, 10, 6, [29, 55, 120, 122] ), Position( False, True, 10, 8, [57, 121, 123, 128] ),
        Position( False, True, 10, 10, [59, 85, 122, 124] ), Position( False, True, 8, 10, [87, 123, 125, 128] ), Position( False, True, 6, 10, [89, 115, 124, 126] ),
        Position( False, True, 6, 8, [117, 125, 127, 128] ), Position( False, True, 6, 6, [25, 119, 120, 126] ), Position( False, True, 8, 8, [120, 122, 124, 126] )]
#who can finish 60..119?
"""
position <-> value:
    0  1   2   3   4   5  6   7   8   9  10 11 12 13 14 15 16
                           Player 1's side
0                        00  01  02  03  04
1                        05  06  07  08  09
2                        10  11  12  13  14
3                        15  16  17  18  19
4                        20  21  22  23  24
5                        25  26  27  28  29
6  94 99 104 109 114 119 127    120     121 55 50 45 40 35 30
7  93 98 103 108 113 118                    56 51 46 41 36 31
8  92 97 102 107 112 117 126    128     122 57 52 47 42 37 32 Player 2's side
9  91 96 101 106 111 116                    58 53 48 43 38 33
10 90 95 100 105 110 115 125    124     123 59 54 49 44 39 34
11                       89  88  87  86  85
12                       84  83  82  81  80
13                       79  78  77  76  75
14                       74  73  72  71  70
15                       69  68  67  66  65
16                       64  63  62  61  60
"""

Railways = [[5, 6, 7, 8, 9], [9, 8, 7, 6, 5], [35, 36, 37, 38, 39], [39, 38, 37, 36, 35], [65, 66, 67, 68, 69], [69, 68, 67, 66, 65], [95, 96, 97, 98, 99], [99, 98, 97, 96, 95],
          [25, 26, 27, 28, 29], [29, 28, 27, 26, 25], [55, 56, 57, 58, 59], [59, 58, 57, 56, 55], [85, 86, 87, 88, 89], [89, 88, 87, 86, 85], [115, 116, 117, 118, 119], [119, 118, 117, 116, 115],
          [5, 10, 15, 20, 25, 127, 126, 125, 89, 84, 79, 74, 69], [69, 74, 79, 84, 89, 125, 126, 127, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 121, 122, 123, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 123, 122, 121, 29, 24, 19, 14, 9],
          [99, 104, 109, 114, 119, 127, 120, 121, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 121, 120, 127, 119, 114, 109, 104, 99],
          [95, 100, 105, 110, 115, 125, 124, 123, 59, 54, 49, 44, 39], [39, 44, 49, 54, 59, 123, 124, 125, 115, 110, 105, 100, 95],
          [5, 10, 15, 20, 25, 119, 114, 109, 104, 99], [99, 104, 109, 114, 119, 25, 20, 15, 10, 5],
          [9, 14, 19, 24, 29, 55, 50, 45, 40, 35], [35, 40, 45, 50, 55, 29, 24, 19, 14, 9],
          [39, 44, 49, 54, 59, 85, 80, 75, 70, 65], [65, 70, 75, 80, 85, 59, 54, 49, 44, 39],
          [69, 74, 79, 84, 89, 115, 110, 105, 100, 95], [95, 100, 105, 110, 115, 89, 84, 79, 74, 69],
          [117, 126, 128, 122, 57], [57, 122, 128, 126, 117],
          [27, 120, 128, 124, 87], [87, 124, 128, 120, 27]]

class ChessProp:
    def __init__( self, name, value, initnum, initrule = 0, move = True ):
        self.name = name
        self.value = value
        self.initnum = initnum
        self.initrule = 0
        self.move = move

InitChess = [ChessProp( 'SiLi', 40, 1 ), ChessProp( 'JuZh', 39, 1 ), ChessProp( 'ShZh', 38, 2 ), ChessProp( 'LvZh', 37, 2 ),
             ChessProp( 'TuZh', 36, 2 ), ChessProp( 'YiZh', 35, 2 ), ChessProp( 'LiZh', 34, 3 ), ChessProp( 'PaZh', 33, 3 ),
             ChessProp( 'GoBi', 32, 3 ), ChessProp( 'DiLe', 41, 3, 1, False ), ChessProp( 'ZhDa', 42, 2, 2 ), ChessProp( 'JuQi', 31, 1, 3, False )]
