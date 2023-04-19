class piece:
    def __init__(self, name, colour):
        self.name = name
        self.colour = colour

    def __str__(self):
        if self.colour == 'B':
            return f'Black-{self.name}'
        else:
            return f'White-{self.name}'


class pawn(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class bishop(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class knight(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class rook(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class queen(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class king(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1


class board:

    def addPiece(self, pieceType, colour, pos):
        self.pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    def removePiece(self, pieceType, colour, pos):
        self.pieces[pos[0]][pos[1]] = None

    def initializeBoard(self):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        print('\n'.join([' '.join([str(j) for j in i]) for i in self.pieces]), end='\n\n')
        # Add pieces to the starting position
        # Add black pawns
        for i in range(8):
            self.addPiece('Pawn', 'B', (1, i))
        # Add white pawns
        for i in range(8):
            self.addPiece('Pawn', 'W', (6, i))
        # Add black pieces
        self.addPiece('Rook', 'B', (0, 0))
        self.addPiece('Knight', 'B', (0, 1))
        self.addPiece('Bishop', 'B', (0, 2))
        self.addPiece('Queen', 'B', (0, 3))
        self.addPiece('King', 'B', (0, 4))
        self.addPiece('Bishop', 'B', (0, 5))
        self.addPiece('Knight', 'B', (0, 6))
        self.addPiece('Rook', 'B', (0, 7))
        # Add white pieces
        self.addPiece('Rook', 'W', (7, 0))
        self.addPiece('Knight', 'W', (7, 1))
        self.addPiece('Bishop', 'W', (7, 2))
        self.addPiece('Queen', 'W', (7, 3))
        self.addPiece('King', 'W', (7, 4))
        self.addPiece('Bishop', 'W', (7, 5))
        self.addPiece('Knight', 'W', (7, 6))
        self.addPiece('Rook', 'W', (7, 7))
        print('\n'.join([' '.join([str(j) for j in i]) for i in self.pieces]))

    def __init__(self):
        self.initializeBoard()
        self.pieces = None


if __name__ == '__main__':
    b = board()
