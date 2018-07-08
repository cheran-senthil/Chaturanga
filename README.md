# Chaturanga

Chaturanga is a Chess API written in Python that supports two-player games.

As of now, the Chessboard supports input in a (start, stop) format to make a move.

Functionality includes:
* Chessboard generation from a given valid FEN position
* Pretty print of the chessboard using UNICODE (optional, defaults to False)
* Generation of all legal moves for a given position. (including en-passant, castling, and promotion)
* Identifying potential draw situations (3-fold repitition, 100 plies) and checks.
* Identification of all game ending criteria (Checkmate, Stalemate, 5-fold repitiyion, 150 plies)
* Undoing a move
* Resetting the Chessboard

A Chess bot using depth analysis is under construction.
