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

    def printBoard(self):
        print('\n'.join([' '.join([str(j) for j in i]) for i in self.pieces]), end='\n\n')

    # Self is not used
    def self_is_not_used(self):
        pass

    # Return Opposite Colour
    def oppositeColour(self, colour):
        self.self_is_not_used()
        if colour == 'W':
            return 'B'
        else:
            return 'W'

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
        if self.pieces[pos[0]][pos[1]] is None:
            self.pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    # Remove a piece of particular type and colour to the board
    def removePiece(self, pos):
        self.pieces[pos[0]][pos[1]] = None

    # Move piece, TODO promotion
    def movePiece(self, currPos, targetPos, pieces, tmp=0):
        # TODO temporary piece boards
        pieceType = self.pieces[currPos[0]][currPos[1]].name.lower()
        colour = self.pieces[currPos[0]][currPos[1]].colour
        if self.pieces[targetPos[0]][targetPos[1]] is None:
            self.addPiece(pieceType, colour, targetPos)
            self.removePiece(currPos)
        else:
            if tmp == 0:
                # TODO Add score
                pass
            else:
                self.removePiece(targetPos)
                self.addPiece(pieceType, colour, targetPos)
                self.removePiece(currPos)

    # Fen notation add pieces and set game
    def fen(self, notation):
        self.pieces.clear()
        fields = notation.split('/')
        endFields = fields[-1].split(' ')
        del fields[-1]
        fields += endFields
        for row in range(8):
            col = 0
            for s in fields[row]:
                print(s, end=' ')
                if str(s).isdigit():
                    for i in range(int(s)):
                        self.pieces[row][col] = None
                        col += 1
                else:
                    piece_dict = {'p': 'Bpawn', 'b': 'Bbishop', 'r': 'Brook', 'n': 'Bknight', 'q': 'Bqueen', 'k': 'Bking',
                                  'P': 'Wpawn', 'B': 'Wbishop', 'R': 'Wrook', 'N': 'Wknight', 'Q': 'Wqueen', 'K': 'Wking'}
                    self.addPiece(piece_dict[str(s)][1:], piece_dict[str(s)][0], (row, col))
                    col += 1
        self.printBoard()

    # Find all pawn moves
    def generatePawnMoves(self, pos, colour):
        moves = []
        r, c = pos
        if colour == 'W':
            moves.append([r - 1, c]) if self.pieces[r - 1][c] is None else None
            if pos[0] == 7:
                # Starting squre rule. Can move 2
                moves.append([r - 2, c]) if self.pieces[r - 2][c] is None else None
            else:
                # TODO enpassant
                oppositePositions = self.getPieces(self.oppositeColour('W'))
                moves.append([r - 1, c - 1]) if [r - 1, c - 1] in oppositePositions else None
                moves.append([r - 1, c + 1]) if [r - 1, c + 1] in oppositePositions else None
                pass
        else:
            moves.append([r + 1, c]) if self.pieces[r + 1][c] is None else self.self_is_not_used()
            if pos[0] == 1:
                # Starting squre rule. Can move 2
                moves.append([r + 2, c]) if self.pieces[r + 2][c] is None else self.self_is_not_used()
            else:
                # TODO enpassant
                oppositePositions = self.getPieces(self.oppositeColour('B'))
                moves.append([r + 1, c - 1]) if [r + 1, c - 1] in oppositePositions else None
                moves.append([r + 1, c + 1]) if [r + 1, c + 1] in oppositePositions else None
                pass

    # Find all horizontal and vertical(rook) moves possible from a given square
    def generateLinearMoves(self, pos, colour):
        moves = []
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
    def generateDiagonalMoves(self, pos, colour):
        moves = []
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
            pseudoLegalMoves.append(self.generatePawnMoves(pos,colour))
            # Code enpassant and first square double move
        elif selectedPiece.name == 'Rook':
            pseudoLegalMoves.append(self.generateLinearMoves(pos, colour))
            # Code castling
        elif selectedPiece.name == 'Bishop':
            pseudoLegalMoves.append(self.generateDiagonalMoves(pos, colour))
        elif selectedPiece.name == 'Knight':
            pass
        elif selectedPiece.name == 'Queen':
            pseudoLegalMoves.append(self.generateLinearMoves(pos, colour))
            pseudoLegalMoves.append(self.generateDiagonalMoves(pos, colour))
        elif selectedPiece.name == 'King':
            pass
        else:
            print("No piece selected!")
        return pseudoLegalMoves

    # Actual legal moves to check for checks
    def legalMoves(self, pos):
        pseudoLegalMoves = self.pseudoLegalMoves(pos)
        if pseudoLegalMoves is not None:
            for i in pseudoLegalMoves:
                tempBoard = self.pieces.copy()

                print(i)
        else:
            print("No legal moves")

    def __init__(self):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        # Initialize starting position
        self.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
        self.move = 0
        self.turn = 'White'
        self.possibleMoves = None


if __name__ == '__main__':
    b = board()
    print("\nTesting\n")
    b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR')
    # b.addPiece('Bishop', 'W', (3, 3))
    # b.addPiece('Rook', 'W', (2, 0))
    # b.legalMoves((2, 0))
    # b.fen('8/5k2/3p4/1p1Pp2p/pP2Pp1P/P4P1K/8/8')
