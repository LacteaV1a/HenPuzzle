import sys
import random
import pygame


pygame.init()

IMAGE_FILE = "1.jpg" 
IMAGE_SIZE = (680, 920)
TILE_WIDTH = 226
TILE_HEIGHT = 184
SCREEN_WIDTH = pygame.display.Info().current_w
SCREEN_HEIGHT = pygame.display.Info().current_h
COLUMNS = 3
ROWS = 5
GAME_FIELD_WIDTH = round(SCREEN_WIDTH / 2 - IMAGE_SIZE[0] / 2)
GAME_FIELD_HEIGHT = round(SCREEN_HEIGHT / 2 - IMAGE_SIZE[1] / 2)

# bottom right corner contains no tile
EMPTY_TILE = (COLUMNS-1, ROWS-1)   


mainScreen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
display = pygame.Surface(IMAGE_SIZE)
pygame.display.set_caption("shift-puzzle")
myfont = pygame.font.SysFont('Roboco', 80)

BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
# horizontal and vertical borders for tiles
hor_border = pygame.Surface((TILE_WIDTH, 1))
hor_border.fill(BLACK)
ver_border = pygame.Surface((1, TILE_HEIGHT))
ver_border.fill(BLACK)

winningtext = myfont.render('You win!', 1, BLACK, (255, 255, 255))
textplace = winningtext.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))

# load the image and divide up in tiles
# putting borders on each tile also adds them to the full image
image = pygame.image.load(IMAGE_FILE).convert()
background_image = pygame.image.load("background.jpg").convert()
tiles = {}
for c in range(COLUMNS) :
    for r in range(ROWS) :
        tile = image.subsurface(
            c * TILE_WIDTH, r * TILE_HEIGHT, 
            TILE_WIDTH, TILE_HEIGHT)
        tiles[(c, r)] = tile#.convert()
        
        tile.blit(hor_border, (0, 0))
        tile.blit(hor_border, (0, TILE_HEIGHT - 1))
        tile.blit(ver_border, (0, 0))
        tile.blit(ver_border, (TILE_WIDTH - 1, 0))
            # make the corners a bit rounded
        tile.set_at((1, 1), BLACK)
        tile.set_at((1, TILE_HEIGHT - 2), BLACK)
        tile.set_at((TILE_WIDTH - 2, 1), BLACK)
        tile.set_at((TILE_WIDTH - 2, TILE_HEIGHT - 2), BLACK)
#tiles[EMPTY_TILE].fill(BLACK)

# keep track of which tile is in which position
state = {(col, row): (col, row) 
            for col in range(COLUMNS) for row in range(ROWS)}
sourceState = state.copy();
# keep track of the position of the empty tyle
(emptyc, emptyr) = EMPTY_TILE

# start game and display the completed puzzle

display.blit(image, (0, 0))
mainScreen.blit(background_image, (0, 0))
mainScreen.blit(display, (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT))
pygame.display.flip()

# swap a tile (c, r) with the neighbouring (emptyc, emptyr) tile
def shift(c, r):
    global emptyc, emptyr 
    display.blit(
        tiles[state[(c, r)]],
        (emptyc * TILE_WIDTH, emptyr * TILE_HEIGHT))
    
    display.blit(
        tiles[EMPTY_TILE],
        (c * TILE_WIDTH, r * TILE_HEIGHT))
    mainScreen.blit(display, (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT))
    state[(emptyc, emptyr)] = state[(c, r)]
    state[(c, r)] = EMPTY_TILE
    (emptyc, emptyr) = (c, r)
    pygame.display.flip()

#tile movement animation from c,r to c1, r1
def moveAnimationTiles(c, r, c1, r1, saved_image):
    #initialization of coordinates
    ax = c * TILE_WIDTH
    ay = r * TILE_HEIGHT
    bx = c1 * TILE_WIDTH
    by = r1 * TILE_HEIGHT
    #getting a list of steps
    speed = 3
    steps_number = max(abs(bx - ax), abs(by - ay))
    listSteps = range(0, steps_number, speed)
    
    try:
        stepx, stepy = (float(bx - ax) / steps_number, float(by - ay) / steps_number)
    except ZeroDivisionError:
        None
    else:
        #render loop
        for i in listSteps:
            if i == listSteps[-1]:
                i = steps_number
            print(str(i)) 
            display.blit(saved_image, (0, 0))
            pygame.draw.rect(display, BLACK, (ax, ay, TILE_WIDTH, TILE_HEIGHT))
            pygame.draw.rect(display, BLACK, (bx, by, TILE_WIDTH, TILE_HEIGHT))
            display.blit(tiles[state[(c, r)]], ((ax + stepx * i), (ay + stepy * i)))
            display.blit(tiles[state[(c1, r1)]], ((bx - stepx * i), (by - stepy * i)))
            mainScreen.blit(display, (GAME_FIELD_WIDTH, GAME_FIELD_HEIGHT))
            pygame.display.update()

        #changing the state of tiles    
        interimState = state[(c1, r1)]
        state[(c1, r1)] = state[(c, r)]
        state[(c, r)] = interimState 

        print(str(stepx) + "  " + str(stepy) + " " + str(steps_number))
        print(str(speed))
        if state == sourceState:
            mainScreen.blit(winningtext, textplace)
            pygame.display.update()         

def moveTiles(c, r, c1, r1):
    display.blit(
        tiles[state[(c, r)]],
        (c1*TILE_WIDTH, r1*TILE_HEIGHT))
    display.blit(
        tiles[state[(c1, r1)]],
        (c*TILE_WIDTH, r*TILE_HEIGHT))
    interimState = state[(c1, r1)]
    state[(c1, r1)] = state[(c, r)]
    state[(c, r)] = interimState       
    print(state)
    if state == sourceState:
        print('win')
    pygame.display.flip()


# shuffle the puzzle by making some random shift moves
def shuffle():
    global emptyc, emptyr
    # keep track of last shuffling direction to avoid "undo" shuffle moves
    last_r = 0 
    for i in range(75):
        # slow down shuffling for visual effect
        #pygame.time.delay(50)
        while True:
            # pick a random direction and make a shuffling move
            # if that is possible in that direction
            r = random.randint(1, 4)
            if (last_r + r == 5):
                # don't undo the last shuffling move
                continue
            if r == 1 and (emptyc > 0):
                shift(emptyc - 1, emptyr) # shift left
            elif r == 4 and (emptyc < COLUMNS - 1):
                shift(emptyc + 1, emptyr) # shift right
            elif r == 2 and (emptyr > 0):
                shift(emptyc, emptyr - 1) # shift up
            elif r == 3 and (emptyr < ROWS - 1):
                shift(emptyc, emptyr + 1) # shift down
            else:
                # the random shuffle move didn't fit in that direction  
                continue
            last_r=r
            break # a shuffling move was made


# process mouse clicks 
at_start = True
showing_solution = False
phaseClick = False
while True:
    event = pygame.event.wait()
    if event.type == pygame.QUIT:
        pygame.quit()
        sys.exit()

    if at_start:
        #shuffle after the first mouse click
        shuffle()
        at_start = False 

    if event.type == pygame.MOUSEBUTTONDOWN:
        if event.dict['button'] == 1:
            # mouse left button: ...
            mouse_pos = pygame.mouse.get_pos()
            c = (mouse_pos[0] - GAME_FIELD_WIDTH) // TILE_WIDTH
            r = (mouse_pos[1] - GAME_FIELD_HEIGHT) // TILE_HEIGHT
            if not phaseClick and 0 <= c <= COLUMNS - 1 and 0 <= r <= ROWS - 1:
                onePhase = {'c': c, 'r': r}
                print(onePhase)
                phaseClick = True
            elif phaseClick and 0 <= c <= COLUMNS - 1 and 0 <= r <= ROWS - 1:
                secondPhase = {'c1': c, 'r1': r}
                print(secondPhase)
                saveImage = display.copy()
                moveAnimationTiles(onePhase['c'], onePhase['r'], secondPhase['c1'], secondPhase['r1'], saveImage)              
                #moveTiles(onePhase['c'], onePhase['r'], secondPhase['c1'], secondPhase['r1'])
                phaseClick = False
            #if (    (abs(c-emptyc) == 1 and r == emptyr) or  
            #        (abs(r-emptyr) == 1 and c == emptyc)):
                #shift (c, r)
        elif event.dict['button'] == 3:
            # mouse right button: show solution image
            saved_image = display.copy()
            display.blit(image, (0, 0))
            pygame.display.flip()
            showing_solution = True
    elif showing_solution and (event.type == pygame.MOUSEBUTTONUP):
        # stop showing the solution
        display.blit(saved_image, (0, 0))
        pygame.display.flip()
        showing_solution = False
