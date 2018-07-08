# Chaturanga

Chaturanga is a Chess API written in Python that supports two-player games.

As of now, the Chessboard supports input in a (start, stop) format to make a move.

Functionality includes:
 Markup : * Chessboard generation from a given valid FEN position
          * Pretty print of the chessboard using UNICODE (optional, defaults to False)
          * Generation of all legal moves for a given position. (including en-passant, castling, and promotion)
          * Identification of all game ending criteria (Checkmate, Stalemate, 5-fold repitiyion, 150 plies)
          * Identifying potential draw situations (3-fold repitiyion, 100 plies) and checks.
          * Undoing a move
          * Resetting the Chessboard

A Chess bot using depth analysis is under construction.
