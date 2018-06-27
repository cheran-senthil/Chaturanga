from six import python_2_unicode_compatible

@python_2_unicode_compatible
class Chessboard:
    """"""
    STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    PRETTY_SYMBOLS = {'K' : u'\u2654', 'Q' : u'\u2655', 'R' : u'\u2656',
                      'B' : u'\u2657', 'N' : u'\u2658', 'P' : u'\u2659',
                      'k' : u'\u265A', 'q' : u'\u265B', 'r' : u'\u265C',
                      'b' : u'\u265D', 'n' : u'\u265E', 'p' : u'\u265F' }

    def __init__(self, fen = STARTING_FEN, ascii = False):
        """Create a new Chessboard"""
        self.fen = fen
        self.ascii = ascii
        fields = self.fen.split(' ')
        self.piece_placement = fields[0]
        self.active_color = fields[1]
        self.castling_availability = fields[2]
        self.enpassant_target = fields[3]
        self.halfmove_clock = fields[4]
        self.fullmove_number = fields[5]


    def __repr__(self):
        return self.__str__()

    def __str__(self):
        board = ''
        rows = self.piece_placement.split('/')
        for row in rows:
            for square in row:
                if square in "12345678":
                    board += int(square) * ' '
                if square.lower() in "rnbqkbnrp":
                    if self.ascii:
                        board += square
                    else:
                        board += Chessboard.PRETTY_SYMBOLS[square]
            board += '\n'

        return board
