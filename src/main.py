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
        self.points = 3


class knight(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 3


class rook(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 5


class queen(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 9


class king(piece):
    def __init__(self, name, colour):
        super().__init__(name, colour)
        self.points = 1000


class board:
    def getPieces(self, colour):
        positions = []
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] is not None:
                    if self.pieces[i][j].colour == colour:
                        positions.append([i, j])
        return positions

    def addPiece(self, pieceType, colour, pos):
        self.pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    def removePiece(self, pos):
        self.pieces[pos[0]][pos[1]] = None

    def generateDiagonalMoves(self, pos):
        moves = []
        row, column = pos
        r, c = pos
        # Top left
        while r - 1 >= 0 and c - 1 >= 0:
            if self.pieces[r - 1][c - 1] is None:
                moves.append([r - 1, c - 1])
                r -= 1
                c -= 1
            elif self.pieces[r - 1][c - 1].colour != self.pieces[row][column].colour:
                moves.append([r - 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Top Right
        while r - 1 >= 0 and c + 1 <= 7:
            if self.pieces[r - 1][c + 1] is None:
                moves.append([r - 1, c + 1])
                r -= 1
                c += 1
            elif self.pieces[r - 1][c + 1].colour != self.pieces[row][column].colour:
                moves.append([r - 1, c + 1])
                break
            else:
                break
        r, c = pos
        # Bottom Left
        while r + 1 <= 7 and c - 1 >= 0:
            print(r + 1, c - 1)
            if self.pieces[r + 1][c - 1] is None:
                print("None")
                moves.append([r + 1, c - 1])
                r += 1
                c -= 1
            elif self.pieces[r + 1][c - 1].colour != self.pieces[row][column].colour:
                print("Enemy Piece")
                moves.append([r + 1, c - 1])
                break
            else:
                print("Allied Piece")
                break
        r, c = pos
        # Bottom right
        while r + 1 <= 7 and c + 1 <= 7:
            if self.pieces[r + 1][c + 1] is None:
                moves.append([r + 1, c + 1])
                r += 1
                c += 1
            elif self.pieces[r + 1][c + 1].colour != self.pieces[row][column].colour:
                moves.append([r + 1, c + 1])
                break
            else:
                break
        return moves

    def pseudoLegalMoves(self, pos):
        selectedPiece = self.pieces[pos[0]][pos[1]]
        colour = selectedPiece.colour
        pseudoLegalMoves = []
        if selectedPiece.name == 'Pawn':
            print('Pawn is here')
        elif selectedPiece.name == 'Rook':
            print('Rook is here')
        elif selectedPiece.name == 'Bishop':
            print('Bishop is here:', pos)
            print(self.generateDiagonalMoves(pos))
        elif selectedPiece.name == 'Knight':
            print('Knight is here')
        elif selectedPiece.name == 'Queen':
            print('Queen is here')
        elif selectedPiece.name == 'King':
            print('King is here')
        else:
            print("No piece selected!")
            return pseudoLegalMoves

    def initializeBoard(self):
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
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        self.initializeBoard()
        self.move = 0
        self.turn = 'White'
        self.possibleMoves = None


if __name__ == '__main__':
    b = board()
    print("\nTesting\n")
    b.addPiece('Bishop', 'W', (3, 3))
    b.pseudoLegalMoves((3, 3))
    print(b.getPieces('B'))
