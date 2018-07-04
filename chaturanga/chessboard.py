from six import python_2_unicode_compatible

def is_check(board, color):
    if color == 'w':
        for row_id, row in enumerate(board):
            if 'K' in row:
                col_id = row.index('K')
                break
        print(row_id, col_id, row)
    if color == 'b':
        for row_id, row in enumerate(board):
            if 'k' in row:
                col_id = row.index('k')
                break
        print(row_id, col_id)

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
        self.board = []
        rows = self.piece_placement.split('/')
        for row in rows:
            board_row = ''
            for square in row:
                if square in Chessboard.RANKS:
                    board_row += int(square) * ' '
                if (square in Chessboard.WHITE_PIECES) or (square in Chessboard.BLACK_PIECES):
                    board_row += square
            self.board.append(board_row)

    """
    def is_check(board, color):
        if color == 'w':
            for row_id, row in enumerate(board):
                if 'K' in row:
                    col_id = row.index('K')
                    break

        if color == 'b':
            for row_id, row in enumerate(board):
                if 'k' in row:
                    col_id = row.index('k')
                    break

    def generate_legal_moves(self):
        if self.active_color == 'w':

        if self.active_color == 'b':


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
        self.board = []
        rows = self.piece_placement.split('/')
        for row in rows:
            board_row = ''
            for square in row:
                if square in Chessboard.RANKS:
                    board_row += int(square) * ' '
                if (square in Chessboard.WHITE_PIECES) or (square in Chessboard.BLACK_PIECES):
                    board_row += square
            self.board.append(board_row)
    """

    def reset(self):
        self.__init__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        board = "\n".join(self.board)
        if self.pretty_print:
            pretty_board = u''
            for square in board:
                if square in Chessboard.PRETTY_SYMBOLS:
                    pretty_board += Chessboard.PRETTY_SYMBOLS[square]
                else:
                    pretty_board += square
            board = pretty_board
        return board
