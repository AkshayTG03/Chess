import chess as ch
import pygame

def drawBG(win):
    """Draw the board by first setting the entire board to a colour and then placing the opposite colour alternatively."""
    win.fill(blackBgClr)
    for row in range(rows):
        for col in range(row%2, rows, 2):
            pygame.draw.rect(win, whiteBgClr, (row*squareSize, col*squareSize, squareSize,squareSize))

def drawPieces(win, pieces):
    for r in range(rows):
        for c in range(cols):
            piece = pieces[r][c]
            if piece is None:
                continue
            else:
                img = pygame.transform.scale(pygame.image.load("images/"+ str(piece)+".png"), (squareSize,squareSize))
                win.blit(img, pygame.Rect(c*squareSize, r*squareSize, squareSize, squareSize))
def main():
    clock = pygame.time.Clock()
    run = True
    selectedPiece = None
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
                print(str(p[r][c]))
        drawBG(WIN)
        drawPieces(WIN, p)
        pygame.display.update()
    pygame.quit()

if __name__ == '__main__':
    #Constants
    width = 800
    height = 800
    rows = cols = 8
    squareSize = width / cols
    blackBgClr = (209, 139, 71)
    whiteBgClr = (255, 206, 158)
    possibleMoveClr = (59, 191, 19)
    blackPieceClr = (20, 20, 20)
    whitePieceClr = (245, 245, 245)
    FPS = 30
    #Init
    b = ch.board('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    p = b.pieces
    #p = b.fen('rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1')
    '''b.addPiece(p, 'queen', 'W', ch.getPosFromStdNotation('b2'))
    b.addPiece(p, 'king', 'W', ch.getPosFromStdNotation('a1'))
    b.addPiece(p, 'queen', 'B', ch.getPosFromStdNotation('h8'))
    b.legalMoves(p, ch.getPosFromStdNotation('b2'))
    print(str([[str(j) for j in i] for i in p]).split("-"))
    '''

    #Pychame render
    WIN = pygame.display.set_mode((width, height))
    pygame.display.set_caption('Chess by Akshay')
    main()