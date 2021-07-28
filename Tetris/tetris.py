from collections import deque
import random
import pygame
import copy
from pieces import I, O, T, L, J, S, Z

# Colors
black = (0, 0, 0)
white = (255, 255, 255)
blue = (255, 0, 0)


# Window Size
winX = 576
winY = 1024


# Grid Vars
blocksize = 35
gap = 2
grid = [10, 20]
startx = (winX - (grid[0] * (blocksize + gap) - gap)) / 5
starty = (winY - (grid[1] * (blocksize + gap) - gap)) / 3


def tetris():
    global SCREEN, CLOCK, pieceBag, nextPiece
    pygame.init()

    # Game Vars
    SCREEN = pygame.display.set_mode((winX, winY))
    CLOCK = pygame.time.Clock()
    running = True

    gameGrid = []
    for x in range(grid[1]):
        newlist = []
        for y in range(grid[0]):
            newlist.append(0)
        gameGrid.append(newlist)

    SCREEN.fill(black)
    pieceBag = deque()
    pieceBag.extend(random.sample(range(7), 7))
    currentPiece = getNextPiece()
    nextPiece = getNextPiece()
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                running = False
            if event.type == pygame.KEYDOWN and currentPiece.getActive():
                if event.key == pygame.K_LEFT and intersection(currentPiece, gameGrid, -1):
                    currentPiece.moveSide(-1)
                    gameGrid = handleSide(currentPiece, gameGrid, -1)
                if event.key == pygame.K_RIGHT and intersection(currentPiece, gameGrid, 1):
                    currentPiece.moveSide(1)
                    gameGrid = handleSide(currentPiece, gameGrid, 1)
                if event.key == pygame.K_x and rotationCheck(currentPiece, gameGrid, 1):
                    currentPiece.rotation(1)
                    gameGrid = handleRotations(currentPiece, gameGrid, 1)
                if event.key == pygame.K_z and rotationCheck(currentPiece, gameGrid, -1):
                    currentPiece.rotation(-1)
                    gameGrid = handleRotations(currentPiece, gameGrid, -1)
                if event.key == pygame.K_RETURN:
                    running = True
                    gameGrid = []
                    for x in range(grid[1]):
                        newlist = []
                        for y in range(grid[0]):
                            newlist.append(0)
                        gameGrid.append(newlist)
                    SCREEN.fill(black)
                    pieceBag = deque()
                    pieceBag.extend(random.sample(range(7), 7))
                    currentPiece = getNextPiece()

        gameGrid = renderBlock(currentPiece, gameGrid)
        drawGrid(gameGrid)
        drawSidePanel()
        if checkUnder(currentPiece, gameGrid):
            currentPiece.moveDown()

        if not currentPiece.getActive():
            gameGrid = freeze(gameGrid)
            currentPiece = nextPiece
            nextPiece = getNextPiece()

        CLOCK.tick(5)
        pygame.display.update()


def drawGrid(gameGrid):
    for y, list in enumerate(gameGrid):
        for x, nums in enumerate(list):
            rect = pygame.Rect(
                startx + x * (blocksize + gap),
                starty + y * (blocksize + gap),
                blocksize,
                blocksize,
            )
            if nums == 1:
                pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            else:
                pygame.draw.rect(SCREEN, white, rect)


def drawSidePanel():
    np = copy.deepcopy(nextPiece.pieceMatrix())
    for row in np:
        while len(row) < 4:
            row.append(0)
    for y, list in enumerate(np):
        for x, nums in enumerate(list):
            rect = pygame.Rect(
                startx * 11 + x * (20 + 1),
                starty + y * (20 + 1),
                20,
                20,
            )
            if nums == 1:
                pygame.draw.rect(SCREEN, (0, 0, 255), rect)
            else:
                pygame.draw.rect(SCREEN, (0, 0, 0), rect)


def renderBlock(aPiece, board):
    position = aPiece.getPosition()
    piece = aPiece.pieceMatrix()
    stopper = aPiece.yLenInd(0)
    y = 0
    while y < len(piece) and aPiece.getActive():
        x = 0
        while x < len(piece[y]):
            # Add case were y == 0 or bottom blocks will be removed.
            if position[1] == 0 and piece[y][x] != 0:
                board[position[1] + y][position[0] + x] = piece[y][x]
            elif stopper + position[1] <= grid[1] and piece[y][x] != 0:
                if y == 0 or piece[y - 1][x] == 0:
                    board[position[1] + y - 1][position[0] + x] = 0
                    board[position[1] + y][position[0] + x] = piece[y][x]
                else:
                    board[position[1] + y][position[0] + x] = piece[y][x]
            elif position[1] + stopper > grid[1]:
                if piece[y][x] != 0:
                    board[position[1] + y - 1][position[0] + x] = piece[y][x]
                    aPiece.activeOff()
            x += 1
        y += 1
    return board


def handleSide(aPiece, board, dx):
    position = aPiece.getPosition()
    piece = aPiece.pieceMatrix()
    y = 0
    if dx == -1:
        while y < len(piece):
            x = 0
            while x < len(piece[y]):
                if piece[y][x] != 0:
                    if x == len(piece[y]) - 1 or piece[y][x + 1] == 0:
                        board[position[1] + y - 1][position[0] + x + 1] = 0
                x += 1
            y += 1
    if dx == 1:
        while y < len(piece):
            x = 0
            while x < len(piece[y]):
                if piece[y][x] != 0:
                    if x == 0 or piece[y][x - 1] == 0:
                        board[position[1] + y - 1][position[0] + x - 1] = 0
                x += 1
            y += 1
    return board


def sideCheck(aPiece, dx):
    end = aPiece.xLenInd(0)
    xpos = aPiece.getPosition()[0]
    start = aPiece.getStart(0)
    if dx == -1:
        if start + xpos + dx - 1 < 0:
            return False
    else:
        if xpos + end + dx > grid[0]:
            return False
    return True


def intersection(aPiece, board, dx):
    piece = aPiece.pieceMatrix()
    position = aPiece.getPosition()
    end = aPiece.xLenInd(0)
    if sideCheck(aPiece, dx):
        y = 0
        if dx == -1:
            while y < len(piece):
                x = 0
                while x < len(piece[y]):
                    if piece[y][x] != 0:
                        if x == 0 or piece[y][x - 1] == 0:
                            if position[1] + y > 19:
                                break
                            if board[position[1] + y - 1][position[0] + x - 1] != 0:
                                return False
                    x += 1
                y += 1
            return True
        else:
            while y < len(piece):
                x = 0
                while x < len(piece[y]):
                    if piece[y][x] != 0:
                        if x == end - 1 or piece[y][x + 1] == 0:
                            if position[1] + y > 19:
                                break
                            if board[position[1] + y - 1][position[0] + x + 1] != 0:
                                return False
                    x += 1
                y += 1
            return True
    else:
        return False


def checkUnder(aPiece, board):
    piece = aPiece.pieceMatrix()
    position = aPiece.getPosition()
    y = 0
    bot = len(piece[y]) - 1
    while y < len(piece):
        x = 0
        while x < len(piece[y]):
            if piece[y][x] != 0 and (y == bot or piece[y + 1][x] == 0):
                if (
                    position[1] + y + 1 < grid[1]
                    and board[position[1] + y + 1][position[0] + x] != 0
                ):
                    aPiece.activeOff()
                    return False
            x += 1
        y += 1
    return True


def freeze(board):
    y = 0
    while y < len(board):
        x = 0
        cleared = True
        while x < len(board[y]) and cleared:
            if board[y][x] == 0:
                cleared = False
            x += 1
        if cleared:
            i = 0
            while i < y:
                board[y - i] = board[y - i - 1]
                i += 1
            board.pop(0)
            list = []
            for x in board[3]:
                list.append(0)
            board.insert(0, list)
            y -= 1
        y += 1
    return board


def handleRotations(aPiece, board, dir):
    position = aPiece.getPosition()
    oldLoc = aPiece.rotationImg(-dir)
    y = 0
    while y < len(oldLoc):
        x = 0
        while x < len(oldLoc[y]):
            if oldLoc[y][x] != 0:
                board[position[1] + y - 1][position[0] + x] = 0
            x += 1
        y += 1
    return board


def rotationCheck(aPiece, board, dir):
    position = aPiece.getPosition()
    loc = aPiece.pieceMatrix()
    i = 0
    while i < len(loc):
        j = 0
        while j < len(loc[i]):
            if loc[i][j] != 0:
                board[position[1] + i - 1][position[0] + j] = 0
            j += 1
        i += 1
    futLoc = aPiece.rotationImg(dir)
    endx = aPiece.xLenInd(dir)
    endy = aPiece.yLenInd(dir)
    startx = aPiece.getStart(dir)
    y = 0
    while y < len(futLoc):
        x = 0
        while x < len(futLoc[y]):
            if futLoc[y][x] != 0:
                if (
                    endy + y + position[1] > grid[1]
                    or position[0] + startx + x - 1 < 0
                    or position[0] + x + endx > grid[0]
                    or board[position[1] + y][position[0] + x] != 0
                ):
                    return False
            x += 1
        y += 1
    return True


def getNextPiece():
    if len(pieceBag) < 7:
        pieceBag.extend(random.sample(range(7), 7))
    ind = pieceBag.popleft()
    return getPiece(ind)


def getPiece(ind):
    if ind == 0:
        return I()
    elif ind == 1:
        return O()
    elif ind == 2:
        return T()
    elif ind == 3:
        return L()
    elif ind == 4:
        return J()
    elif ind == 5:
        return S()
    else:
        return Z()


tetris()
