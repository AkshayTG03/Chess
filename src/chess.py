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


# Convert given standard notation postion like a1 to Pos used by code (0,0)
def getPosFromStdNotation(std):
    column = ord(std[0]) - 97
    row = 8 - int(std[1])
    return [row, column]


# Convert given standard notation postion like a1 to Pos used by code (0,0)
def getStdNotationFromPos(pos):
    column = chr(pos[1] + 97)
    row = str(8 - pos[0])
    return column+row


# noinspection PyUnresolvedReferences
class board:

    # Print the board
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
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        fields = notation.split('/')
        fields += fields.pop().split(' ')
        for row in range(8):
            col = 0
            for s in fields[row]:
                if str(s).isdigit():
                    for i in range(int(s)):
                        self.pieces[row][col] = None
                        col += 1
                else:
                    piece_dict = {'p': 'Bpawn', 'b': 'Bbishop', 'r': 'Brook', 'n': 'Bknight', 'q': 'Bqueen',
                                  'k': 'Bking',
                                  'P': 'Wpawn', 'B': 'Wbishop', 'R': 'Wrook', 'N': 'Wknight', 'Q': 'Wqueen',
                                  'K': 'Wking'}
                    self.addPiece(piece_dict[str(s)][1:], piece_dict[str(s)][0], (row, col))
                    col += 1
        self.turn = fields[8].upper()
        # fields[9] is castling
        # fields[10] is enpassant
        # fields[11] is draw moves (half moves)
        self.move = int(fields[12])

    # Find all pawn moves
    def generatePawnMoves(self, pos, colour):
        moves = []
        r, c = pos
        if colour == 'W':
            moves.append([r - 1, c]) if self.pieces[r - 1][c] is None else None
            if pos[0] == 6:
                # Starting squre rule. Can move 2
                moves.append([r - 2, c]) if self.pieces[r - 2][c] is None and self.pieces[r - 1][c] is None else None
            # TODO enpassant
            oppositePositions = self.getPieces(self.oppositeColour('W'))
            moves.append([r - 1, c - 1]) if [r - 1, c - 1] in oppositePositions else None
            moves.append([r - 1, c + 1]) if [r - 1, c + 1] in oppositePositions else None
        else:
            moves.append([r + 1, c]) if self.pieces[r + 1][c] is None else self.self_is_not_used()
            if pos[0] == 1:
                # Starting squre rule. Can move 2
                moves.append([r + 2, c]) if self.pieces[r + 2][c] is None and self.pieces[r + 1][c] is None else None
            # TODO enpassant
            oppositePositions = self.getPieces(self.oppositeColour('B'))
            moves.append([r + 1, c - 1]) if [r + 1, c - 1] in oppositePositions else None
            moves.append([r + 1, c + 1]) if [r + 1, c + 1] in oppositePositions else None
        return moves

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
            pseudoLegalMoves = self.generatePawnMoves(pos, colour)
            # Code enpassant
        elif selectedPiece.name == 'Rook':
            pseudoLegalMoves = self.generateLinearMoves(pos, colour)
            # Code castling
        elif selectedPiece.name == 'Bishop':
            pseudoLegalMoves = self.generateDiagonalMoves(pos, colour)
        elif selectedPiece.name == 'Knight':
            print("Knight is here:", pos)
            r, c = pos
            rm = [-2, -1, 1, 2, 2, 1, -1, -2]
            cm = [1, 2, 2, 1, -1, -2, -2, -1]
            for i in range(8):
                pseudoLegalMoves.append([r+rm[i], c+cm[i]] if [r+rm[i], c+cm[i]]
                                        not in self.getPieces(colour)
                                        and (r+rm[i] in range(0, 8))
                                        and (c+cm[i] in range(0, 8))
                                        else None)
        elif selectedPiece.name == 'Queen':
            pseudoLegalMoves = self.generateLinearMoves(pos, colour)
            pseudoLegalMoves += self.generateDiagonalMoves(pos, colour)
        elif selectedPiece.name == 'King':
            pass
        else:
            print("No piece selected!")
        return pseudoLegalMoves

    # Actual legal moves to check for checks
    def legalMoves(self, pos):
        pseudoLegalMoves = self.pseudoLegalMoves(pos)
        if pseudoLegalMoves:
            for i in pseudoLegalMoves:
                while None in pseudoLegalMoves:
                    pseudoLegalMoves.remove(None)
                print(getStdNotationFromPos(i), end='\n')
        else:
            print("No legal moves")

    def __init__(self):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        # Initialize starting position
        self.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0')
        self.move = 0
        self.turn = 'W'
        self.possibleMoves = None
