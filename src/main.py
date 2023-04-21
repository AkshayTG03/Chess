import chess as ch

if __name__ == '__main__':
    b = ch.board()
    # b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    # b.addPiece('Rook', 'W', (2, 1))
    # b.addPiece('Bishop', 'W', (2, 3))
    b.addPiece('knight', 'B', ch.getPosFromStdNotation('a4'))
    b.legalMoves(ch.getPosFromStdNotation('a4'))
