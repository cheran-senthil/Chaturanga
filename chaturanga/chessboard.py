"""Chessboard class and its helper functions"""

from six import python_2_unicode_compatible

def next_point(ref, points, axis, positive):
    """next_point in points w.r.t. ref on given axis and direction"""
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
    """Horizontal mirror image of board with inverted colors"""
    flipped_board = dict()
    for square, piece in board.items():
        flipped_board[(7 - square[0], square[1])] = piece.swapcase()
    return flipped_board


def is_check(board):
    """True if White in Check, False otherwise"""
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
                if (axis in [0, 1]) and (board[square] in 'qr'):
                    return True
                if (axis in [2, 3]) and (board[square] in 'qb'):
                    return True

    return False

def get_moves(board, castling_availability, enpassant_square):
    """List of all moves for white for the given position"""

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
            if (finish in board) and (board[finish] in enemy_pieces):
                moves.append((start, finish))
            finish = (start[0] - 1, start[1] - 1)
            if (finish in board) and (board[finish] in enemy_pieces):
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

def new_b(board, enpassant_target, start, finish, promotion_piece):
    """Update board"""
    files = 'abcdefgh'
    piece = board[start]

    # remove captured pawn for enpassant
    if piece in 'Pp':
        if files[finish[1]] == enpassant_target[0]:
            if finish[0] == 2:
                board.pop((finish[0] + 1, finish[1]))
            if finish[0] == 5:
                board.pop((finish[0] - 1, finish[1]))

    # move rook for castling
    if piece in 'Kk':
        rook_finish = (start[0], (start[1] + finish[1])//2)
        if start[1] - finish[1] == 2:
            rook_start = (start[0], 0)
            board[rook_finish] = board.pop(rook_start)
        if start[1] - finish[1] == -2:
            rook_start = (start[0], 7)
            board[rook_finish] = board.pop(rook_start)

    # update piece position
    board[finish] = board.pop(start)

    # replace last rank pawn with promotion piece
    if piece in 'Pp':
        if finish[0] in [0, 7]:
            board[finish] = promotion_piece

    return board

def new_pp(board):
    """Update piece_placement"""
    nboard = [[' ']*8 for _ in range(8)]
    for square in board:
        nboard[square[0]][square[1]] = board[square]

    piece_placement = ''

    for row_num in range(8):
        count = 0
        for col_num in range(8):
            square = nboard[row_num][col_num]
            if square == ' ':
                count += 1
            else:
                if count != 0:
                    piece_placement += str(count)
                piece_placement += square
                count = 0
        if count != 0:
            piece_placement += str(count)
        piece_placement += '/'

    return piece_placement[:-1]

def new_ca(castling_availability, active_color, piece, start):
    """Update castling_availability"""
    if active_color == 'w':
        if piece == 'K':
            castling_availability.replace('K', '')
            castling_availability.replace('Q', '')
        if piece == 'R':
            if start == (7, 7):
                castling_availability.replace('K', '')
            if start == (7, 0):
                castling_availability.replace('Q', '')
        return castling_availability

    if piece == 'k':
        castling_availability.replace('k', '')
        castling_availability.replace('q', '')
    if piece == 'r':
        if start == (0, 7):
            castling_availability.replace('k', '')
        if start == (1, 0):
            castling_availability.replace('q', '')

    if castling_availability == '':
        castling_availability = '-'

    return castling_availability

def new_et(piece, start, finish):
    """Update enpassant_target"""
    files = 'abcdefgh'

    if piece in 'Pp':
        if abs(start[0] - finish[0]) == 2:
            row = 8 - (start[0] + finish[0])//2
            col = start[1]
            enpassant_target = files[col] + str(row)
    else:
        enpassant_target = '-'

    return enpassant_target

def new_hc(board, halfmove_clock, piece, finish):
    """
    Update halfmove_clock
    """
    if (finish not in board) and (piece not in 'Pp'):
        halfmove_clock += 1
    else:
        halfmove_clock = 0
    return halfmove_clock

@python_2_unicode_compatible
class Chessboard:
    """
    Chessboard class that supports 2 player games.
    """
    PIECES = 'KQRBNPkqrbnp'
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
        self.pretty_print = pretty_print

        self.fen = fen

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

        self.fen_stack = [self.fen]

        three_move_fen = ' '.join(fields[:4])
        self.move_stack = {three_move_fen: 1}

    def move(self, ply):
        """Move a piece"""
        moves = self.get_legal_moves()

        start = ply[0]
        finish = ply[1]

        if self.active_color == 'w':
            promotion_piece = 'Q'
        else:
            promotion_piece = 'q'

        if (start, finish) in moves:

            piece = self.board[start]

            self.halfmove_clock = new_hc(self.board, self.halfmove_clock,
                                         piece, finish)

            self.board = new_b(self.board, self.enpassant_target,
                               start, finish, promotion_piece)

            self.castling_availability = new_ca(self.castling_availability,
                                                self.active_color,
                                                piece, start)

            self.enpassant_target = new_et(piece, start, finish)
            self.piece_placement = new_pp(self.board)

            if self.active_color == 'w':
                self.active_color = 'b'
            else:
                self.active_color = 'w'
                self.fullmove_number += 1

            three_move_fen = ' '.join([self.piece_placement,
                                       self.active_color,
                                       self.castling_availability,
                                       self.enpassant_target])

            self.fen = ' '.join([three_move_fen,
                                 str(self.halfmove_clock),
                                 str(self.fullmove_number)])

            self.fen_stack.append(self.fen)

            game_status = self.game_status()
            if game_status != '':
                print(game_status)

            if three_move_fen in self.move_stack:
                self.move_stack[three_move_fen] += 1
                if self.move_stack[three_move_fen] == 3:
                    if (game_status == '') or (game_status == 'Check'):
                        print('Claim Draw?')
                if self.move_stack[three_move_fen] == 5:
                    if game_status != 'Draw!':
                        print('Draw!')
            else:
                self.move_stack[three_move_fen] = 1

        else:
            print('Invalid Move!')

    def get_legal_moves(self):
        """Generate Legal Moves"""
        board = dict(self.board)
        castling_availability = self.castling_availability
        enpassant_square = Chessboard.ENPASSANT_MAP[self.enpassant_target[0]]

        if self.active_color == 'b':
            board = flip(board)
            castling_availability = castling_availability.swapcase()

        all_moves = get_moves(board, castling_availability, enpassant_square)

        valid_moves = []
        for move in all_moves:
            nboard = dict(board)

            # remove captured pawn for enpassant
            if (nboard[move[0]] == 'P') and (enpassant_square != None):
                if move[1] == enpassant_square:
                    nboard.pop((move[1][0] + 1, move[1][1]))

            # update piece position
            nboard[move[1]] = nboard.pop(move[0])

            if not is_check(nboard):
                valid_moves.append(move)

        if self.active_color == 'b':
            nmoves = []
            for move in valid_moves:
                start = (7 - move[0][0], move[0][1])
                finish = (7 - move[1][0], move[1][1])
                nmoves.append((start, finish))
            return nmoves

        return valid_moves

    def game_status(self):
        """Current Game Status"""
        board = dict(self.board)
        moves = self.get_legal_moves()
        if self.active_color == 'b':
            board = flip(board)

        if moves == []:
            if is_check(board):
                return 'Checkmate!'
            return 'Stalemate!'

        if self.halfmove_clock == 100:
            return 'Claim Draw?'
        if self.halfmove_clock == 150:
            return 'Draw!'

        if is_check(board):
            return 'Check!'

        return ''

    def undo(self):
        """Undo a move"""
        self.fen = self.fen_stack.pop()
        self.__init__(fen=self.fen)

    def reset(self):
        """Reset the Chessboard"""
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
