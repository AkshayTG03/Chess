import chess as ch
import pygame

def evaluatePosition(board, pieces):
    pass
def gameStateCheck(board:ch.board, pieces) -> int:
    """Returns an integer corresponding to game state. 0->Can Continue 1->Checkmate 2->Stalemate 3->Draw.
    Draw condition to be implemented"""
    end = 0
    possibleMoves = board.allPossibleMoves(pieces, board.turn)
    canMove = False
    for values in possibleMoves.values():
        if values:
            canMove = True
            break
    if not canMove:
        if board.checkForcheck(pieces, board.turn):
            #king is in check
            end = 1
            print("Checkmate!", board.fullColour(board.oppositeColour(board.turn)),  "Wins!")
        else:
            #stalemate
            end = 2
            print("Stalemate!")
    return end

def drawBG(win):
    """Draw the board by first setting the entire board to a colour and then placing the opposite colour
     alternatively.
    """
    win.fill(blackBgClr)
    for row in range(rows):
        for col in range(row%2, rows, 2):
            pygame.draw.rect(win, whiteBgClr, (row*squareSize, col*squareSize, squareSize, squareSize))

def drawPieces(win, pieces):
    for r in range(rows):
        for c in range(cols):
            piece = pieces[r][c]
            if piece is None:
                continue
            else:
                img = pygame.transform.scale(pygame.image.load("images/"+ str(piece)+".png"),
                                             (scaleSize*squareSize,scaleSize*squareSize))
                win.blit(img, pygame.Rect(squareSize*(c + (1-scaleSize)/2), squareSize*(r + (1-scaleSize)/2),
                                          squareSize, squareSize))

def drawPossibleMoves(win, legalMoves):
    if legalMoves is not None:
        for i in legalMoves:
            pygame.draw.circle(win, possibleMoveClr, (squareSize*(i[1]+0.5),squareSize*(i[0]+0.5)), squareSize/5.5)

def main():
    clock = pygame.time.Clock()
    run = True
    selectedPiece = []
    legalMoves = None
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            #Quit
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                loc = pygame.mouse.get_pos()
                c = int(loc[0]//squareSize)
                r = int(loc[1]//squareSize)
                if selectedPiece == [r, c]:
                    selectedPiece = []
                else:
                    if selectedPiece:
                        if b.legalMoves(p, selectedPiece) is not None:
                            if [r, c] in b.legalMoves(p, selectedPiece):
                                b.movePiece(p, selectedPiece, [r, c])
                                gameStateCheck(b, p)
                                selectedPiece = []
                            else:
                                selectedPiece = [r, c]
                        else:
                            selectedPiece = [r, c]
                    else:
                        selectedPiece = [r, c]
                legalMoves = b.legalMoves(p, selectedPiece)
        drawBG(WIN)
        drawPieces(WIN, p)
        drawPossibleMoves(WIN, legalMoves)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    #Constants
    width = 800
    height = 800
    rows = cols = 8
    scaleSize= 0.8
    squareSize = width / cols
    blackBgClr = (209, 139, 71)
    whiteBgClr = (255, 206, 158)
    #blackBgClr = (20,20,20)
    #whiteBgClr = (245,245,245)
    possibleMoveClr = (59, 191, 19)
    FPS = 30
    #Init
    b = ch.board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    p = b.pieces
    b.generateFen(p)
    #p = b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    #for checking enpassant 8/p7/8/1P6/8/8/6k1/R3K3 b - - 0 1
    '''
    b.addPiece(p, 'queen', 'W', ch.getPosFromStdNotation('b2'))
    b.addPiece(p, 'king', 'W', ch.getPosFromStdNotation('a1'))
    b.addPiece(p, 'queen', 'B', ch.getPosFromStdNotation('h8'))
    b.legalMoves(p, ch.getPosFromStdNotation('b2'))
    print(str([[str(j) for j in i] for i in p]).split("-"))
    '''

    #Pychame render
    WIN = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chess by Akshay')
    pygame.display.update()
    main()