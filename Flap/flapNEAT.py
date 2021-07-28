import pygame, sys, random, os, neat, pickle


def main(genomes, config):
    def drawFloor():
        screen.blit(floor, (floor_x, 900))
        screen.blit(floor, (floor_x + 1024, 900))
        if floor_x == -1024:
            return 0
        else:
            return floor_x

    def createPipe(pipes):
        i = 0
        while i < len(pipes):
            if abs(pipes[i].centerx - 700) < 500:
                return []
            i += 2
        y = random.randint(350, 850)
        newtop = topPipe.get_rect(midbottom=(700, y - 300))
        newbottom = bottomPipe.get_rect(midtop=(700, y))
        disty.append(y - 150)
        return newtop, newbottom

    def movePipes(pipes):
        for pipe in pipes:
            pipe.centerx -= 5
            if pipe.bottom > 1024:
                screen.blit(bottomPipe, pipe)
            else:
                screen.blit(topPipe, pipe)
        return pipes

    def checkColl(pipes):
        for bird in birds:
            for pipe in pipes:
                if bird[0].colliderect(pipe):
                    ge[birds.index(bird)].fitness -= (
                        (bird[0].centerx - pipe.centerx - 60) ** 2
                        + (bird[0].centery - disty[pipes.index(pipe) // 2]) ** 2
                    ) / 75 ** 2
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    break
                elif bird[0].top < -100 or bird[0].bottom > 900:
                    ge[birds.index(bird)].fitness = 0
                    nets.pop(birds.index(bird))
                    ge.pop(birds.index(bird))
                    birds.pop(birds.index(bird))
                    break

    def rotateBirb(bird, movement):
        return pygame.transform.rotozoom(bird, -movement * 2, 1)

    def scoreDisplay():
        scoreSur = gameFont.render(str(score), True, (255, 255, 255))
        scoreRect = scoreSur.get_rect(center=(288, 100))
        screen.blit(scoreSur, scoreRect)

    def getPipeInd(pipes):
        i = 0
        while i < len(pipes) and pipes[i].centerx + 60 < 0:
            i += 2
        return i

    birds = []
    nets = []
    ge = []

    # Game Vars
    gravity = 1
    score = 0
    floor_x = 0

    pygame.init()
    screen = pygame.display.set_mode((576, 1024))
    clock = pygame.time.Clock()

    gameFont = pygame.font.Font("assets/04B_19.TTF", 40)

    bg_s = pygame.image.load("assets/bg.png").convert()
    floor = pygame.image.load("assets/floor.png").convert()
    birb = pygame.image.load("assets/birb.png").convert_alpha()

    running = True

    bottomPipe = pygame.image.load("assets/bottomP.png").convert_alpha()
    topPipe = pygame.transform.flip(bottomPipe, False, True)
    dy = random.randint(350, 850)
    fp = topPipe.get_rect(midbottom=(700, dy - 300))
    bp = bottomPipe.get_rect(midtop=(700, dy))
    pipeList = []
    pipeList.extend([fp, bp])
    disty = [dy - 150]

    SPAWNPIPE = pygame.USEREVENT
    pygame.time.set_timer(SPAWNPIPE, 2400)

    # neat
    for _, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        birds.append([birb.get_rect(center=(100, 512)), 0])
        g.fitness = 0
        ge.append(g)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == SPAWNPIPE:
                pipeList.extend(createPipe(pipeList))
                pygame.event.clear()

        # manage memory and score
        if len(pipeList) > 6:
            pipeList.pop(0)
            pipeList.pop(1)
            disty.pop(0)
            for g in ge:
                g.fitness += 5

        # Draw Background
        screen.blit(bg_s, (0, 0))
        pipeList = movePipes(pipeList)

        # Draw Floor
        floor_x -= 1
        floor_x = drawFloor()

        ind = getPipeInd(pipeList)
        for x, bird in enumerate(birds):
            ge[x].fitness += 0.1
            output = nets[x].activate(
                (
                    bird[0].centery,
                    abs(bird[0].centery - pipeList[ind].bottom),
                    abs(bird[0].centery - pipeList[ind + 1].height),
                    #                    pipeList[ind].centerx,
                    #                    bird[1],
                )
            )
            if output[0] > 0.5:
                bird[1] = -18

        # draw bird
        for bird in birds:
            bird[1] += gravity
            birby = rotateBirb(birb, bird[1])
            bird[0].centery += bird[1]
            if birds.index(bird) < 10:
                screen.blit(birby, bird[0])

        checkColl(pipeList)

        if len(birds) < 1:
            running = False
            pipeList.clear
            pygame.event.clear()
        pygame.display.update()
        clock.tick(60)


def run(config_path):
    config = neat.config.Config(
        neat.DefaultGenome,
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_path,
    )

    p = neat.Population(config)

    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)

    winner = p.run(main)

    with open("winner.pkl", "wb") as output:
        pickle.dump(winner, output, 1)


if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    run(config_path)
