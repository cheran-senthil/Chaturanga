# Chaturanga

Chaturanga is a Chess API written in Python that supports two-player games.

## Installation

```
$ pip install Chaturanga
```

## Functionality

* Chessboard generation from a given valid FEN position
* Pretty print of the Chessboard using Unicode (optional, defaults to False)
* Generation of all legal moves for a given position. (including en-passant, castling, and promotion)
* Identifying potential draw situations (3-fold repitition, 100 plies) and checks.
* Identification of all game ending criteria (Checkmate, Stalemate, 5-fold repitition, 150 plies)
* Undoing a move
* Resetting the Chessboard

As of now, the Chessboard supports input in a (start, stop) format to make a move.

A Chess bot using depth analysis is under construction.
