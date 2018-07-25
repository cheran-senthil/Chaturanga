# Chaturanga

Chaturanga is a Chess API written in Python that supports both single-player and two-player games.

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
* Chess Engine using Depth Analysis and a Piece-Square Table
* [Lichess BOT](https://lichess.org/@/SultanKhan2)

As of now, the Chessboard supports input in a [UCI](https://www.shredderchess.com/chess-info/features/uci-universal-chess-interface.html) notation (eg. `e2e4`, `b7b8n`) to make a move.

## License

[MIT](LICENSE)
