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


# noinspection PyUnresolvedReferences
class board:

    # Get a particular piece on board
    def getPiece(self, pieceType, colour):
        position = None
        for i in range(8):
            for j in range(8):
                if self.pieces[i][i] is not None:
                    if self.pieces[i][j].colour == colour and self.pieces[i][j].name == pieceType.lower():
                        position = [i, j]
                        break
        return position

    # Get all positions of pieces of a particular colour
    def getPieces(self, colour):
        positions = []
        for i in range(8):
            for j in range(8):
                if self.pieces[i][j] is not None:
                    if self.pieces[i][j].colour == colour:
                        positions.append([i, j])
        return positions

    # Add a piece of particular type and colour to the board
    def addPiece(self, pieceType, colour, pos):
        self.pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    # Remove a piece of particular type and colour to the board
    def removePiece(self, pos):
        self.pieces[pos[0]][pos[1]] = None

    # Find all horizontal and vertical(rook) moves possible from a given square
    def generateLinearMoves(self, pos):
        moves = []
        colour = self.pieces[pos[0]][pos[1]].colour
        r, c = pos
        # Left
        while c - 1 >= 0:
            if self.pieces[r][c - 1] is None:
                moves.append([r, c - 1])
                c -= 1
            elif self.pieces[r][c - 1].colour != colour:
                moves.append([r, c - 1])
                c -= 1
                break
            else:
                break
        r, c = pos
        # Bottom
        while r + 1 <= 7:
            if self.pieces[r + 1][c] is None:
                moves.append([r + 1, c])
                r += 1
            elif self.pieces[r + 1][c].colour != colour:
                moves.append([r + 1, c])
                r += 1
                break
            else:
                break
        r, c = pos
        # Right
        while c + 1 <= 7:
            if self.pieces[r][c + 1] is None:
                moves.append([r, c + 1])
                c += 1
            elif self.pieces[r][c + 1].colour != colour:
                moves.append([r, c + 1])
                c += 1
                break
            else:
                break
        r, c = pos
        # Top
        while r - 1 >= 0:
            if self.pieces[r - 1][c] is None:
                moves.append([r - 1, c])
                r -= 1
            elif self.pieces[r - 1][c].colour != colour:
                moves.append([r - 1, c])
                r -= 1
                break
            else:
                break
        return moves

    # Find all possible diagonal(bishop) moves possible from a given square taking into consideration enemy and
    # allied pieces
    def generateDiagonalMoves(self, pos):
        moves = []
        colour = self.pieces[pos[0]][pos[1]].colour
        r, c = pos
        # Top left
        while r - 1 >= 0 and c - 1 >= 0:
            if self.pieces[r - 1][c - 1] is None:
                moves.append([r - 1, c - 1])
                r -= 1
                c -= 1
            elif self.pieces[r - 1][c - 1].colour != colour:
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
            elif self.pieces[r - 1][c + 1].colour != colour:
                moves.append([r - 1, c + 1])
                break
            else:
                break
        r, c = pos
        # Bottom Left
        while r + 1 <= 7 and c - 1 >= 0:
            if self.pieces[r + 1][c - 1] is None:
                moves.append([r + 1, c - 1])
                r += 1
                c -= 1
            elif self.pieces[r + 1][c - 1].colour != colour:
                moves.append([r + 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Bottom right
        while r + 1 <= 7 and c + 1 <= 7:
            if self.pieces[r + 1][c + 1] is None:
                moves.append([r + 1, c + 1])
                r += 1
                c += 1
            elif self.pieces[r + 1][c + 1].colour != colour:
                moves.append([r + 1, c + 1])
                break
            else:
                break
        return moves

    def pseudoLegalMoves(self, pos):
        selectedPiece = self.pieces[pos[0]][pos[1]]
        if selectedPiece is None:
            return None
        colour = selectedPiece.colour
        pseudoLegalMoves = []
        if selectedPiece.name == 'Pawn':
            print('Pawn is here')
            # Code enpassant and first square double move
        elif selectedPiece.name == 'Rook':
            print('Rook is here', pos)
            pseudoLegalMoves.append(self.generateLinearMoves(pos))
            # Code castling
        elif selectedPiece.name == 'Bishop':
            print('Bishop is here:', pos)
            pseudoLegalMoves.append(self.generateDiagonalMoves(pos))
        elif selectedPiece.name == 'Knight':
            print('Knight is here')
        elif selectedPiece.name == 'Queen':
            print('Queen is here')
            pseudoLegalMoves.append(self.generateLinearMoves(pos))
            pseudoLegalMoves.append(self.generateDiagonalMoves(pos))
        elif selectedPiece.name == 'King':
            print('King is here')
        else:
            print("No piece selected!")
        return pseudoLegalMoves

    # Actual legal moves to check for checks
    def legalMoves(self, pos):
        pseudoLegalMoves = self.pseudoLegalMoves(pos)
        if pseudoLegalMoves is not None:
            for i in pseudoLegalMoves:
                print(i)
        else:
            print("No legal moves")

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
    b.addPiece('Rook', 'W', (2, 0))
    b.legalMoves((2, 0))
