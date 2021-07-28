import pygame, sys, random

def main():

    def drawFloor():
        screen.blit(floor, (floor_x, 900))
        screen.blit(floor, (floor_x + 1024, 900))
        if floor_x == -1024:
            return 0
        else:
            return floor_x


    def createPipe():
        y = random.randint(350, 850)
        newtop = topPipe.get_rect(midbottom=(700, y - 300))
        newbottom = bottomPipe.get_rect(midtop=(700, y))
        return newtop, newbottom


    def movePipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
            if pipe.bottom > 1024:
                screen.blit(bottomPipe, pipe)
            else:
                screen.blit(topPipe, pipe)
        return pipes

    def drawPipes(pipes):
        for pipe in pipes:
            if pipe.bottom > 1024:
                screen.blit(bottomPipe, pipe)
            else:
                screen.blit(topPipe, pipe)


    def checkColl(pipes):
        for pipe in pipes:
            if birbRect.colliderect(pipe):
                return True
        if birbRect.top < -100 or birbRect.bottom > 900:
            return True


    def rotateBirb(bird):
        return pygame.transform.rotozoom(bird, -birdMovement * 2, 1)


    def scoreDisplay():
        scoreSur = gameFont.render(str(score), True, (255, 255, 255))
        scoreRect = scoreSur.get_rect(center = (288, 100))
        screen.blit(scoreSur, scoreRect)




    # Game Vars
    gravity = 1
    birdMovement = 0
    pipe_x = 0
    score = 0

    pygame.init()
    screen = pygame.display.set_mode((576, 1024))
    clock = pygame.time.Clock()

    gameFont = pygame.font.Font("assets/04B_19.TTF", 40)

    bg_s = pygame.image.load("assets/bg.png").convert()
    floor = pygame.image.load("assets/floor.png").convert()
    birb = pygame.image.load("assets/birb.png").convert_alpha()
    birbRect = birb.get_rect(center = (100, 512))

    bottomPipe = pygame.image.load("assets/bottomP.png").convert_alpha()
    topPipe = pygame.transform.flip(bottomPipe, False, True)

    fp = topPipe.get_rect(midbottom = (-10, - 10))
    pipeList = [fp,fp,fp,fp,fp,fp]


    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 2400)

    gg = False
    floor_x = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not gg:
                    birdMovement = -18
                if event.key == pygame.K_RETURN:
                    gg = False
                    pipeList.clear()
                    pipeList = [fp,fp,fp,fp,fp,fp]
                    birbRect.center = (100, 512)
                    birdMovement = 0
                    score = 0

            if event.type == SPAWNPIPE:
                pipeList.extend(createPipe())

        if not gg:
            #manage memory and score
            if len(pipeList) > 8:
                pipeList.pop(0)
                pipeList.pop(1)
                score += 1
            
            #Draw Background
            screen.blit(bg_s, (0, 0))
            pipeList = movePipes(pipeList)

            #Draw Floor
            floor_x -= 1
            floor_x = drawFloor()

            #draw bird
            birdMovement += gravity
            birby = rotateBirb(birb)
            birbRect.centery += birdMovement
            screen.blit(birby, birbRect)

            scoreDisplay()
            gg = checkColl(pipeList)

        if gg:
            #Draw Background
            screen.blit(bg_s, (0, 0))

            drawPipes(pipeList)

            #Draw Floor
            floor_x = drawFloor()

            #draw bird
            if birbRect.centery < 850:
                birdMovement += gravity * 1.5
                birby = rotateBirb(birb)
                birbRect.centery += birdMovement
            screen.blit(birby, birbRect)

            scoreDisplay()

        pygame.display.update()
        clock.tick(60)

main()