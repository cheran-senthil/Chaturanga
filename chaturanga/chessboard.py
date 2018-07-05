from six import python_2_unicode_compatible

def is_check(pieces, active_color):
    if active_color == 'b':
        pieces = map((swapcase(piece[0]), piece[1], piece[2]), pieces)
    piece_dict = dict()
    for piece in pieces:
        if piece[0] in piece_dict:
            piece_dict[piece[0]].append((piece[1], piece[2]))
        else:
            piece_dict[piece[0]] = [(piece[1], piece[2])]
    king = piece_dict['K'][0]

    # check for attack by knight
    knights = piece_dict['n']
    for knight in knights:
        if (king[0] - knight[0])**2 + (king[1] - knight[1])**2 == 13:
            return True

    # check for attack by pawn
    pawns = piece_dict['p']
    for pawn in pawns:
        if (king[0] - pawn[0] == 1) and ((king[1] - pawn[1] == 1) or (king[1] - pawn[1] == -1)):
            return True

    # check if nearest piece in same row is enemy rook or queen
    row = list(filter(lambda piece: (piece[1] == king[0]) and (piece[2] < king[1]), pieces))
    if row != []:
        if max(row, key=lambda x: x[2])[0] in 'rq':
            return True
    row = list(filter(lambda piece: (piece[1] == king[0]) and (piece[2] > king[1]), pieces))
    if row != []:
        if min(row, key=lambda x: x[2])[0] in 'rq':
            return True

    # check if nearest piece in same column is enemy rook or queen
    col = list(filter(lambda piece: (piece[2] == king[1]) and (piece[1] < king[0]), pieces))
    if col != []:
        if max(col, key=lambda x: x[1])[0] in 'rq':
            return True
    col = list(filter(lambda piece: (piece[2] == king[1]) and (piece[1] > king[0]), pieces))
    if col != []:
        if min(col, key=lambda x: x[1])[0] in 'rq':
            return True

    # check if nearest piece in diagonal is enemy bishop or queen
    dia = list(filter(lambda piece: (piece[1] + piece[2] == king[0] + king[1]) and (piece[1] < king[0]), pieces))
    if dia != []:
        if max(dia, key=lambda x: x[1])[0] in 'bq':
            return True
    dia = list(filter(lambda piece: (piece[1] + piece[2] == king[0] + king[1]) and (piece[1] > king[0]), pieces))
    if dia != []:
        if min(dia, key=lambda x: x[1])[0] in 'bq':
            return True

    # check if nearest piece in anti-diagonal is enemy bishop or queen
    dia = list(filter(lambda piece: (piece[1] - piece[2] == king[0] - king[1]) and (piece[1] < king[0]), pieces))
    if dia != []:
        if max(dia, key=lambda x: x[1])[0] in 'bq':
            return True
    dia = list(filter(lambda piece: (piece[1] - piece[2] == king[0] - king[1]) and (piece[1] > king[0]), pieces))
    if dia != []:
        if min(dia, key=lambda x: x[1])[0] in 'bq':
            return True

    return False

@python_2_unicode_compatible
class Chessboard:
    """"""
    PIECES = 'PNBRQKpnbrqk'
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
        self.pieces = []
        rows = self.piece_placement.split('/')
        for row_num, row in enumerate(rows):
            col_num = 0
            for square in row:
                if square in '12345678':
                    col_num += int(square)
                if square in Chessboard.PIECES:
                    self.pieces.append((square, row_num, col_num))
                    col_num += 1

    """
    def generate_legal_moves(self):
        if self.active_color == 'w':

        if self.active_color == 'b':
    """

    def reset(self):
        self.__init__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        pieces = self.pieces
        if self.pretty_print:
            pieces = [(Chessboard.PRETTY_SYMBOLS[piece[0]], piece[1], piece[2]) for piece in pieces]
        board = [[' ']*8 for _ in range(8)]
        for piece in pieces:
            board[piece[1]][piece[2]] = piece[0]
        return '\n'.join(map(''.join, board))
