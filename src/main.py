import chess as ch

if __name__ == '__main__':
    b = ch.board()
    p = b.pieces
    # b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    b.addPiece(p, 'queen', 'W', ch.getPosFromStdNotation('b2'))
    b.addPiece(p, 'king', 'W', ch.getPosFromStdNotation('a1'))
    b.addPiece(p, 'queen', 'B', ch.getPosFromStdNotation('h8'))
    b.legalMoves(p, ch.getPosFromStdNotation('b2'))
