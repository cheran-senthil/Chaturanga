from six import python_2_unicode_compatible

def next_point(ref, points, axis, positive):

    # next point in same row
    if axis == 0:
        line = list(filter(lambda p: p[0] == ref[0], points))
        if positive:
            line = list(filter(lambda p: p[1] > ref[1], line))
            if line != []:
                return min(line, key=lambda p: p[1])
        else:
            line = list(filter(lambda p: p[1] < ref[1], line))
            if line != []:
                return max(line, key=lambda p: p[1])

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
            return min(line, key=lambda p: p[0])
        return max(line, key=lambda p: p[0])

    return None

def flip(board):
    flipped_board = dict()
    for square, piece in board.items():
        flipped_board[(7 - square[0], square[1])] = piece.swapcase()
    return flipped_board


def is_check(board):

    pieces = board.keys()

    enemy_knights = []
    enemy_pawns = []

    for square, piece in board.items():
        if piece == 'K':
            king = square
        if piece == 'k':
            enemy_king = square
        if piece == 'n':
            enemy_knights.append(square)
        if piece == 'p':
            enemy_pawns.append(square)

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
            square = next_point(king, pieces, axis, positive)
            if square != None:
                if axis in [0, 1]:
                    if board[square] in 'qr':
                        return True
                if axis in [2, 3]:
                    if board[square] in 'qb':
                        return True

    return False

def get_moves(board, castling_availability, enpassant_square):

    enemy_pieces = 'pnbrqk'
    knight_moves = [(-1, 2), (-1, -2), (2, 1), (2, -1),
                    (-2, 1), (-2, -1), (1, 2), (1, -2)]
    king_moves = [(1, 0), (1, -1), (-1, 0), (-1, -1),
                  (0, 1), (0, -1), (-1, 1), (1, 1)]

    moves = []

    for start, piece in board.items():
        if piece == 'P':
            # check square(s) ahead
            finish = (start[0] - 1, start[1])
            if finish not in board:
                moves.append((start, finish))
                # check if pawn on starting square
                if start in {(6, col_num) for col_num in range(8)}:
                    finish = (start[0] - 2, start[1])
                    if finish not in board:
                        moves.append((start, finish))
            # check diagonal squares
            finish = (start[0] - 1, start[1] + 1)
            if finish in board:
                if board[finish] in enemy_pieces:
                    moves.append((start, finish))
            finish = (start[0] - 1, start[1] - 1)
            if finish in board:
                if board[finish] in enemy_pieces:
                    moves.append((start, finish))
            # check enpassant_target
            if enpassant_square != None:
                finish = enpassant_square
                if start[0] - finish[0] == 1:
                    if abs(start[1] - finish[1]) == 1:
                        moves.append((start, finish))

        if piece == 'N':
            for knight_move in knight_moves:
                finish = tuple(map(sum, zip(start, knight_move)))
                if (-1 < finish[0] < 8) and (-1 < finish[1] < 8):
                    if finish not in board:
                        moves.append((start, finish))
                    elif board[finish] in enemy_pieces:
                        moves.append((start, finish))

        if piece == 'B':
            pass

        if piece == 'R':
            pass

        if piece == 'Q':
            pass

        if piece == 'K':
            for king_move in king_moves:
                finish = tuple(map(sum, zip(start, king_move)))
                if (-1 < finish[0] < 8) and (-1 < finish[1] < 8):
                    if finish not in board:
                        moves.append((start, finish))
                        # check castling
                        if 'K' in castling_availability:
                            if next_point(start, board, 0, True) == (7, 7):
                                if board[(7, 7)] == 'R':
                                    moves.append((start, (7, 6)))
                        if 'Q' in castling_availability:
                            if next_point(start, board, 0, False) == (7, 0):
                                if board[(7, 0)] == 'R':
                                    moves.append((start, (7, 2)))
                    elif board[finish] in enemy_pieces:
                        moves.append((start, finish))

    return moves

@python_2_unicode_compatible
class Chessboard:
    """"""
    WHITE_PIECES = 'KQRBNP'
    BLACK_PIECES = 'kqrbnp'
    PIECES = WHITE_PIECES + BLACK_PIECES
    FILES = 'abcdefgh'
    STARTING_FEN = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
    ENPASSANT_MAP = {'a': (2, 0), 'b': (2, 1), 'c': (2, 2),
                     'd': (2, 3), 'e': (2, 4), 'f': (2, 5),
                     'g': (2, 6), 'h': (2, 7), '-': None}
    PRETTY_SYMBOLS = {'K' : u'\u2654', 'Q' : u'\u2655', 'R' : u'\u2656',
                      'B' : u'\u2657', 'N' : u'\u2658', 'P' : u'\u2659',
                      'k' : u'\u265A', 'q' : u'\u265B', 'r' : u'\u265C',
                      'b' : u'\u265D', 'n' : u'\u265E', 'p' : u'\u265F'}

    def __init__(self, fen=STARTING_FEN, pretty_print=False):
        """Create a new Chessboard"""
        self.fen = fen
        self.pretty_print = pretty_print
        fields = self.fen.split(' ')
        self.piece_placement = fields[0]
        self.active_color = fields[1]
        self.castling_availability = fields[2]
        self.enpassant_target = fields[3]
        self.halfmove_clock = int(fields[4])
        self.fullmove_number = int(fields[5])
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
        moves = self.get_legal_moves()

        # change ply to start, end form (and promotion piece)

        if ply in moves:
            piece = self.board[ply[0]]

            # remove captured pawn for enpassant
            if piece in 'Pp':
                if Chessboard.FILES[ply[1][1]] == self.enpassant_target[0]:
                    if ply[1][0] == 2:
                        self.board.pop((ply[1][0] + 1, ply[1][1]))
                    if ply[1][0] == 5:
                        self.board.pop((ply[1][0] - 1, ply[1][1]))

            # move rook for castling
            if piece in 'Kk':
                finish = (ply[0][0], (ply[0][1] + ply[1][1])//2)
                if ply[0][1] - ply[1][1] == 2:
                    start = (ply[0][0], 0)
                    self.board[finish] = self.board.pop(start)
                if ply[0][1] - ply[1][1] == -2:
                    start = (ply[0][0], 7)
                    self.board[finish] = self.board.pop(start)

            self.board[ply[1]] = self.board.pop(ply[0])

            if piece in 'Pp':
                if ply[1][0] in [0, 7]:
                    self.board[ply[1]] = 'Q' # remove auto-promote

            if self.active_color == 'w':
                self.active_color = 'b'
                if piece == 'K':
                    self.castling_availability.replace('K', '')
                    self.castling_availability.replace('Q', '')
                if piece == 'R':
                    if ply[0] == (7, 7):
                        self.castling_availability.replace('K', '')
                    if ply[0] == (7, 0):
                        self.castling_availability.replace('Q', '')

            elif self.active_color == 'b':
                self.active_color = 'w'
                if piece == 'k':
                    self.castling_availability.replace('k', '')
                    self.castling_availability.replace('q', '')
                if piece == 'r':
                    if ply[0] == (0, 7):
                        self.castling_availability.replace('k', '')
                    if ply[0] == (1, 0):
                        self.castling_availability.replace('q', '')
                self.fullmove_number += 1

            if self.castling_availability == '':
                self.castling_availability = '-'

            if piece in 'Pp':
                if abs(ply[0][0] - ply[1][0]) == 2:
                    row = 8 - (ply[0][0] + ply[1][0])//2
                    col = ply[0][1]
                    self.enpassant_target = Chessboard.FILES[col] + str(row)
            else:
                self.enpassant_target = '-'

            if (ply[1] not in self.board) and (piece not in 'Pp'):
                self.halfmove_clock += 1
            else:
                self.halfmove_clock = 0

            self.piece_placement = ''

            board = [[' ']*8 for _ in range(8)]
            for square in self.board:
                board[square[0]][square[1]] = self.board[square]

            for row_num in range(8):
                count = 0
                for col_num in range(8):
                    square = board[row_num][col_num]
                    if square == ' ':
                        count += 1
                    else:
                        if count != 0:
                            self.piece_placement += str(count)
                        self.piece_placement += square
                        count = 0
                if count != 0:
                    self.piece_placement += str(count)
                self.piece_placement += '/'

            self.piece_placement = self.piece_placement[:-1]

            self.fen = ' '.join([self.piece_placement,
                                 self.active_color,
                                 self.castling_availability,
                                 self.enpassant_target,
                                 str(self.halfmove_clock),
                                 str(self.fullmove_number)])

        else:
            print('Invalid Move!')

    def get_legal_moves(self):

        nboard = dict(self.board)
        castling_availability = self.castling_availability
        enpassant_square = Chessboard.ENPASSANT_MAP[self.enpassant_target[0]]

        if self.active_color == 'b':
            nboard = flip(nboard)
            castling_availability = castling_availability.swapcase()

        all_moves = get_moves(nboard, castling_availability, enpassant_square)

        valid_moves = []
        for move in all_moves:
            board = dict(nboard)
            if (board[move[0]] == 'P') and (enpassant_square != None):
                if move[1] == enpassant_square:
                    board.pop((move[1][0] + 1, move[1][1]))
            board[move[1]] = board.pop(move[0])
            if not is_check(board):
                valid_moves.append(move)

        if self.active_color == 'b':
            nmoves = []
            for move in valid_moves:
                start = (7 - move[0][0], move[0][1])
                finish = (7 - move[1][0], move[1][1])
                nmoves.append((start, finish))
            return nmoves

        return valid_moves

    def reset(self):
        self.__init__()

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        board = [[' ']*8 for _ in range(8)]
        for i in self.board:
            if self.pretty_print:
                board[i[0]][i[1]] = Chessboard.PRETTY_SYMBOLS[self.board[i]]
            else:
                board[i[0]][i[1]] = self.board[i]
        return '\n'.join(map(''.join, board))
