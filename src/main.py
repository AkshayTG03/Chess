class pawn:
    def __init__(self, name):
        self.name = name


class piece:
    def __init__(self, name, colour, points):
        self.name = name
        self.colour = colour
        self.Points = points

    def __str__(self):
        return f'{self.colour}, {self.name}'


class board:
    def addPiece(self, pieceType):
        pass

    @staticmethod
    def initializeBoard():
        pieces = [None for i in range(8)]
        print(board)
        pass

    def __init__(self):
        self.initializeBoard()


if __name__ == '__main__':
    b = board()

