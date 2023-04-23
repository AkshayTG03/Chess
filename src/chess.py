import copy


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
    return column + row


# noinspection PyUnresolvedReferences
class board:

    # Print the board
    def printBoard(self, pieces):
        self.self_is_not_used()
        print('\n'.join([' '.join([str(j) for j in i]) for i in pieces]), end='\n\n')

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
    def getPiece(self, pieces, pieceType, colour):
        self.self_is_not_used()
        position = []
        for i in range(8):
            for j in range(8):
                if pieces[i][j] is not None:
                    if pieces[i][j].colour == colour and pieces[i][j].name.lower() == pieceType:
                        position = [i, j]
                        break
        return position

    # Get all positions of pieces of a particular colour
    def getPieces(self, pieces, colour):
        self.self_is_not_used()
        positions = []
        for i in range(8):
            for j in range(8):
                if pieces[i][j] is not None:
                    if pieces[i][j].colour == colour:
                        positions.append([i, j])
        return positions

    # Add a piece of particular type and colour to the board
    def addPiece(self, pieces, pieceType, colour, pos):
        self.self_is_not_used()
        if pieces[pos[0]][pos[1]] is None:
            pieces[pos[0]][pos[1]] = globals()[pieceType.lower()](pieceType.capitalize(), colour)

    # Remove a piece of particular type and colour to the board
    def removePiece(self, pieces, pos):
        self.self_is_not_used()
        pieces[pos[0]][pos[1]] = None

    # Move piece, TODO promotion
    def movePiece(self, pieces, currPos, targetPos):
        pieceType = pieces[currPos[0]][currPos[1]].name.lower()
        colour = pieces[currPos[0]][currPos[1]].colour
        if pieces[targetPos[0]][targetPos[1]] is None:
            self.addPiece(pieces, pieceType, colour, targetPos)
            self.removePiece(pieces, currPos)
        else:
            # TODO add score
            self.removePiece(pieces, targetPos)
            self.addPiece(pieces, pieceType, colour, targetPos)
            self.removePiece(pieces, currPos)

    # Fen notation add pieces and set game
    def fen(self, notation):
        pieces = [[None for _ in range(8)] for _ in range(8)]
        fields = notation.split('/')
        fields += fields.pop().split(' ')
        for row in range(8):
            col = 0
            for s in fields[row]:
                if str(s).isdigit():
                    for i in range(int(s)):
                        pieces[row][col] = None
                        col += 1
                else:
                    piece_dict = {'p': 'Bpawn', 'b': 'Bbishop', 'r': 'Brook', 'n': 'Bknight', 'q': 'Bqueen',
                                  'k': 'Bking', 'P': 'Wpawn', 'B': 'Wbishop', 'R': 'Wrook', 'N': 'Wknight',
                                  'Q': 'Wqueen', 'K': 'Wking'}
                    self.addPiece(pieces, piece_dict[str(s)][1:], piece_dict[str(s)][0], (row, col))
                    col += 1
        self.turn = fields[8].upper()
        # fields[9] is castling
        # fields[10] is enpassant
        # fields[11] is draw moves (half moves)
        self.move = int(fields[12])
        return pieces

    # Find all pawn moves
    def generatePawnMoves(self, pieces, pos, colour):
        moves = []
        r, c = pos
        if colour == 'W':
            moves.append([r - 1, c]) if pieces[r - 1][c] is None else None
            if pos[0] == 6:
                # Starting squre rule. Can move 2
                moves.append([r - 2, c]) if pieces[r - 2][c] is None and pieces[r - 1][c] is None else None
            # TODO enpassant
            oppositePositions = self.getPieces(pieces, self.oppositeColour('W'))
            moves.append([r - 1, c - 1]) if [r - 1, c - 1] in oppositePositions else None
            moves.append([r - 1, c + 1]) if [r - 1, c + 1] in oppositePositions else None
        else:
            moves.append([r + 1, c]) if pieces[r + 1][c] is None else self.self_is_not_used()
            if pos[0] == 1:
                # Starting squre rule. Can move 2
                moves.append([r + 2, c]) if pieces[r + 2][c] is None and pieces[r + 1][c] is None else None
            # TODO enpassant
            oppositePositions = self.getPieces(pieces, self.oppositeColour('B'))
            moves.append([r + 1, c - 1]) if [r + 1, c - 1] in oppositePositions else None
            moves.append([r + 1, c + 1]) if [r + 1, c + 1] in oppositePositions else None
        return moves

    # Find all horizontal and vertical(rook) moves possible from a given square
    def generateLinearMoves(self, pieces, pos, colour):
        self.self_is_not_used()
        moves = []
        r, c = pos
        # Left
        while c - 1 >= 0:
            if pieces[r][c - 1] is None:
                moves.append([r, c - 1])
                c -= 1
            elif pieces[r][c - 1].colour != colour:
                moves.append([r, c - 1])
                c -= 1
                break
            else:
                break
        r, c = pos
        # Bottom
        while r + 1 <= 7:
            if pieces[r + 1][c] is None:
                moves.append([r + 1, c])
                r += 1
            elif pieces[r + 1][c].colour != colour:
                moves.append([r + 1, c])
                r += 1
                break
            else:
                break
        r, c = pos
        # Right
        while c + 1 <= 7:
            if pieces[r][c + 1] is None:
                moves.append([r, c + 1])
                c += 1
            elif pieces[r][c + 1].colour != colour:
                moves.append([r, c + 1])
                c += 1
                break
            else:
                break
        r, c = pos
        # Top
        while r - 1 >= 0:
            if pieces[r - 1][c] is None:
                moves.append([r - 1, c])
                r -= 1
            elif pieces[r - 1][c].colour != colour:
                moves.append([r - 1, c])
                r -= 1
                break
            else:
                break
        return moves

    # Find all possible diagonal(bishop) moves possible from a given square taking into consideration enemy and
    # allied pieces
    def generateDiagonalMoves(self, pieces, pos, colour):
        self.self_is_not_used()
        moves = []
        r, c = pos
        # Top left
        while r - 1 >= 0 and c - 1 >= 0:
            if pieces[r - 1][c - 1] is None:
                moves.append([r - 1, c - 1])
                r -= 1
                c -= 1
            elif pieces[r - 1][c - 1].colour != colour:
                moves.append([r - 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Top Right
        while r - 1 >= 0 and c + 1 <= 7:
            if pieces[r - 1][c + 1] is None:
                moves.append([r - 1, c + 1])
                r -= 1
                c += 1
            elif pieces[r - 1][c + 1].colour != colour:
                moves.append([r - 1, c + 1])
                break
            else:
                break
        r, c = pos
        # Bottom Left
        while r + 1 <= 7 and c - 1 >= 0:
            if pieces[r + 1][c - 1] is None:
                moves.append([r + 1, c - 1])
                r += 1
                c -= 1
            elif pieces[r + 1][c - 1].colour != colour:
                moves.append([r + 1, c - 1])
                break
            else:
                break
        r, c = pos
        # Bottom right
        while r + 1 <= 7 and c + 1 <= 7:
            if pieces[r + 1][c + 1] is None:
                moves.append([r + 1, c + 1])
                r += 1
                c += 1
            elif pieces[r + 1][c + 1].colour != colour:
                moves.append([r + 1, c + 1])
                break
            else:
                break
        return moves

    # Check if the colour can check the opposite colour
    def checkForcheck(self, pieces, colour):
        check = False
        oppPieces = self.getPieces(pieces, colour)
        kingPos = self.getPiece(pieces, 'king', self.oppositeColour(colour))
        print("King Pos:", kingPos)
        for p in oppPieces:
            pseudoLegalMoves = self.pseudoLegalMoves(pieces, p)
            if kingPos in pseudoLegalMoves:
                check = True
                break
        return check

    def pseudoLegalMoves(self, pieces, pos):
        selectedPiece = pieces[pos[0]][pos[1]]
        if selectedPiece is None:
            return None
        colour = selectedPiece.colour
        pseudoLegalMoves = []
        if selectedPiece.name == 'Pawn':
            pseudoLegalMoves = self.generatePawnMoves(pieces, pos, colour)
            # Code enpassant
        elif selectedPiece.name == 'Rook':
            pseudoLegalMoves = self.generateLinearMoves(pieces, pos, colour)
            # Code castling
        elif selectedPiece.name == 'Bishop':
            pseudoLegalMoves = self.generateDiagonalMoves(pieces, pos, colour)
        elif selectedPiece.name == 'Knight':
            r, c = pos
            rm = [-2, -1, 1, 2, 2, 1, -1, -2]
            cm = [1, 2, 2, 1, -1, -2, -2, -1]
            for i in range(8):
                pseudoLegalMoves.append([r + rm[i], c + cm[i]] if [r + rm[i], c + cm[i]]
                                        not in self.getPieces(pieces, colour)
                                        and (r + rm[i] in range(0, 8))
                                        and (c + cm[i] in range(0, 8))
                                        else None)
        elif selectedPiece.name == 'Queen':
            pseudoLegalMoves = self.generateLinearMoves(pieces, pos, colour)
            pseudoLegalMoves += self.generateDiagonalMoves(pieces, pos, colour)
        elif selectedPiece.name == 'King':
            r, c = pos
            rm = [-1, -1, 0, 1, 1, 1, 0, -1]
            cm = [0, 1, 1, 1, 0, -1, -1, -1]
            for i in range(8):
                pseudoLegalMoves.append([r + rm[i], c + cm[i]] if [r + rm[i], c + cm[i]]
                                        not in self.getPieces(pieces, colour)
                                        and (r + rm[i] in range(0, 8))
                                        and (c + cm[i] in range(0, 8))
                                        else None)
        else:
            print("No piece selected!")
        return pseudoLegalMoves

    # Actual legal moves to check for checks
    def legalMoves(self, pieces, pos):
        legalMoves = []
        pseudoLegalMoves = self.pseudoLegalMoves(pieces, pos)
        colour = pieces[pos[0]][pos[1]].colour
        if pseudoLegalMoves:
            while None in pseudoLegalMoves:
                pseudoLegalMoves.remove(None)
            for i in pseudoLegalMoves:
                # print(getStdNotationFromPos(i), end='\n')
                # Make a temporary board and try every pseudo legal move and see if the opposite pieces can check king.
                # then remove said pseudo legal move if check. Basically pinning a piece.
                tempBoard = copy.deepcopy(self.pieces)
                self.movePiece(tempBoard, pos, i)
                if not self.checkForcheck(tempBoard, self.oppositeColour(colour)):
                    legalMoves.append(i)
                else:
                    pass
            [print(getStdNotationFromPos(i), end=' ') for i in legalMoves]
        else:
            print("No legal moves")

    def __init__(self):
        self.pieces = [[None for _ in range(8)] for _ in range(8)]
        # Initialize starting position
        # self.pieces = self.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 0')
        self.move = 0
        self.turn = 'W'
