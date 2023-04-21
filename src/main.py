import chess as ch

if __name__ == '__main__':
    '''
    b = board()
    print("\nTesting\n")
    # b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    # b.addPiece('Bishop', 'W', (3, 3))
    # b.addPiece('Rook', 'W', (2, 0))
    # b.legalMoves((2, 0))
    # b.fen('8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8')
    '''
    b = ch.board()
    # b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    b.addPiece('Rook', 'W', (2, 1))
    b.addPiece('Bishop', 'W', (2, 3))
    b.printBoard()
    b.legalMoves((1, 0))
