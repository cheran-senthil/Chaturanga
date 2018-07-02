from six import python_2_unicode_compatible

@python_2_unicode_compatible
class Chessboard:
    """"""
    FILES = 'abcdefgh'
    RANKS = '12345678'
    WHITE_PIECES = 'PNBRQK'
    BLACK_PIECES = 'pnbrqk'
    STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    PRETTY_SYMBOLS = {'K' : u'\u2654', 'Q' : u'\u2655', 'R' : u'\u2656',
                      'B' : u'\u2657', 'N' : u'\u2658', 'P' : u'\u2659',
                      'k' : u'\u265A', 'q' : u'\u265B', 'r' : u'\u265C',
                      'b' : u'\u265D', 'n' : u'\u265E', 'p' : u'\u265F' }

    def __init__(self, fen = STARTING_FEN, pretty_print = False):
        """Create a new Chessboard"""
        self.fen = fen
        self.pretty_print = pretty_print
        fields = self.fen.split(' ')
        self.piece_placement = fields[0]
        self.active_color = fields[1]
        self.castling_availability = fields[2]
        self.enpassant_target = fields[3]
        self.halfmove_clock = fields[4]
        self.fullmove_number = fields[5]
        self.board = ''
        rows = self.piece_placement.split('/')
        for row in rows:
            for square in row:
                if square in Chessboard.RANKS:
                    self.board += int(square) * ' '
                if (square in Chessboard.WHITE_PIECES) or (square in Chessboard.BLACK_PIECES):
                        self.board += square
            self.board += '\n'

    """
    def generate_legal_moves(self):

    def ply(self, move):
        legal_moves = self.generate_legal_moves()
        self.fen = legal_moves[1]
        fields = self.fen.split(' ')
        self.piece_placement = fields[0]
        self.active_color = fields[1]
        self.castling_availability = fields[2]
        self.enpassant_target = fields[3]
        self.halfmove_clock = fields[4]
        self.fullmove_number = fields[5]
        self.board = ''
        rows = self.piece_placement.split('/')
        for row in rows:
            for square in row:
                if square in RANKS:
                    self.board += int(square) * ' '
                if square.lower() in "rnbqkbnrp":
                        self.board += square
            self.board += '\n'
    """

    def reset(self):
        self.__init__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        if self.pretty_print:
            pretty_board = ''
            for square in self.board:
                if square in Chessboard.PRETTY_SYMBOLS:
                    pretty_board += Chessboard.PRETTY_SYMBOLS[square]
                else:
                    pretty_board += square
            return pretty_board
        return self.board
