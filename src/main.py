class piece:
    def __init__(self, name, colour, points):
        self.name = name
        self.colour = colour
        self.Points = points

    def __str__(self):
        return f'{self.colour}, {self.name}'


class pawn(piece):
    def __init__(self, name, colour, points):
        super().__init__(name, colour, points)


class board:
    def addPiece(self, pieceType, colour, pos):
        pass

    @staticmethod
    def initializeBoard():
        pieces = [[None for _ in range(8)] for _ in range(8)]
        print(pieces)
        pass

    def __init__(self):
        self.initializeBoard()


if __name__ == '__main__':
    b = board()
