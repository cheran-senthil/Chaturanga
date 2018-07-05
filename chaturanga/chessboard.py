from six import python_2_unicode_compatible

def next_point(ref, points, axis, positive):

    # next point in same row
    if axis == 0:
        line = list(filter(lambda p: p[0] == ref[0], points))
        if positive:
            line = list(filter(lambda p: p[1] > ref[1], line))
            if line != []:
                return min(line, key=lambda p: p[1])[0]
        else:
            line = list(filter(lambda p: p[1] < ref[1], line))
            if line != []:
                return max(line, key=lambda p: p[1])[0]

    # next point in same column
    if axis == 1:
        line = list(filter(lambda p: p[1] == ref[1], points))
        if positive:
            line = list(filter(lambda p: p[0] > ref[0], line))
        else:
            line = list(filter(lambda p: p[0] < ref[0], line))

    # next point in same diagonal
    if axis == 2:
        line = list(filter(lambda p: p[0] + p[1] == ref[0] + ref[1], points))
        if positive:
            line = list(filter(lambda p: p[0] > ref[0], line))
        else:
            line = list(filter(lambda p: p[0] < ref[0], line))

    # next point in same anti-diagonal
    if axis == 3:
        line = list(filter(lambda p: p[0] - p[1] == ref[0] - ref[1], points))
        if positive:
            line = list(filter(lambda p: p[0] > ref[0], line))
        else:
            line = list(filter(lambda p: p[0] < ref[0], line))

    if line != []:
        if positive:
            return min(line, key=lambda p: p[0])[0]
        else:
            return max(line, key=lambda p: p[0])[0]

    return None

def is_check(board, active_color):
    pieces = board.keys()

    # swap color if black
    if active_color == 'b':
        pass

    enemy_knights = []
    enemy_pawns = []
    for square, piece in board.items:
        if piece == 'K':
            king = square
        if piece == 'k':
            enemy_king = square
        if piece == 'n':
            knights.append(square)
        if piece == 'p':
            pawns.append(square)

    # check for attack by enemy king
    if (king[0] - enemy_king[0])**2 + (king[1] - enemy_king[1])**2 < 3:
        return True

    # check for attack by enemy knights
    for knight in enemy_knights:
        if (king[0] - knight[0])**2 + (king[1] - knight[1])**2 == 13:
            return True

    # check for attack by enemy pawns
    for pawn in enemy_pawns:
        if (king[0] - pawn[0] == 1) and (abs(king[1] - pawn[1]) == 1):
            return True

    # check for attack by enemy bishops, rooks, and queens
    for axis in range(4):
        for positive in [True, False]:
            p = next_point(king, pieces, axis, positive)
            if axis in [0, 1]:
                if board[p] in 'qr':
                    return True
            if axis in [2, 3]:
                if board[p] in 'qb':
                    return True

    return False

@python_2_unicode_compatible
class Chessboard:
    """"""
    WHITE_PIECES = 'KQRBNP'
    BLACK_PIECES = 'kqrbnp'
    PIECES = WHITE_PIECES + BLACK_PIECES
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
        self.board = {}
        rows = self.piece_placement.split('/')
        for row_num, row in enumerate(rows):
            col_num = 0
            for square in row:
                if square in '12345678':
                    col_num += int(square)
                if square in Chessboard.PIECES:
                    self.board[(row_num, col_num)] = square
                    col_num += 1

    def move(self, ply):
        all_moves = self.generate_moves()
        if ply in all_moves:
            # change fen
            pass
        else:
            print('Invalid Move!')

    def generate_moves(self):
        return None

    def reset(self):
        self.__init__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        board = [[' ']*8 for _ in range(8)]
        for p in self.board:
            if self.pretty_print:
                board[p[0]][p[1]] = Chessboard.PRETTY_SYMBOLS[self.board[p]]
            else:
                board[p[0]][p[1]] = self.board[p]
        return '\n'.join(map(''.join, board))
