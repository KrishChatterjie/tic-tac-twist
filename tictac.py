import random
import pygame
from pygame.locals import *

# Constants
SCR_WIDTH = 800
SCR_HEIGHT = 600

# Colours
teal = (0, 128, 128)
matte_red = (204, 35, 35)
grey= (200, 200, 200)

# Initialisation
pygame.init()
rulefont = pygame.font.SysFont("montserrat", 40)
winfont = pygame.font.SysFont("montserrat", 80)

# Screen
screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))

# Title & Icon
pygame.display.set_caption("Tic Tac Toe")
icon = pygame.image.load("tictac-icon.png").convert()
pygame.display.set_icon(icon)


class Box:
    def __init__(self):
        self.surface = pygame.Surface((250,250))
        self.surface.fill((0, 0, 0))

class Cross:
    def __init__(self):
        self.cross_surface = pygame.transform.scale(pygame.image.load("cross1.png").convert(), (67,67))

        
class Circle:
    def __init__(self):
        self.circle_surface = pygame.transform.scale(pygame.image.load("circle1.png").convert(), (67,67))


grid = [[None, None, None],
        [None, None, None],
        [None, None, None]]

player = 1

box = Box()
box_dim = (box.surface.get_width(), box.surface.get_height())


def check_winner():
    global grid
    
    for row in range(3):
        if grid[row][0] != None and grid[row][0] == grid[row][1] and grid[row][1] == grid[row][2]:
                return player_switch()
    
    for col in range(3):
        if grid[0][col] != None and grid[0][col] == grid[1][col] and grid[1][col] == grid[2][col]:
                return player_switch()
    
    if grid[0][0] != None and grid[0][0] == grid[1][1] and grid[1][1] == grid[2][2]:
        return player_switch()
    if grid[0][2] != None and grid[0][2] == grid[1][1] and grid[1][1] == grid[2][0]:
        return player_switch()

    return 0


def check_finish():
    global grid

    for row in grid:
        for val in row:
            if val == None:
                return False
    return True


def draw():
    global grid

    for row in range(3):
        for col in range(3):

            if row == 0:
                x = 0
            elif row == 1:
                x = 83
            else:
                x = 167
            
            if col == 0:
                y = 0
            elif col == 1:
                y = 83
            else:
                y = 167
            
            
            if grid[row][col] == 'x':
                box.surface.blit(Cross().cross_surface, (x+5, y+5))
            elif grid[row][col] == 'o':
                box.surface.blit(Circle().circle_surface, (x+5, y+5))


def player_switch():
    global player

    if player == 1:
        return 2
    else:
        return 1


def place(row, col):
    global player
    
    if grid[row-1][col-1] != None:
        return

    if player == 1:
        grid[row-1][col-1] = 'x'
        player = player_switch()
    
    else:
        grid[row-1][col-1] = 'o'
        player = player_switch()
    
    

def click():
    # Coordinates
    x, y = pygame.mouse.get_pos()

    x -= (SCR_WIDTH - box_dim[0])//2
    y -= (SCR_HEIGHT - box_dim[1])//2

    # Checking if cheeky user clicked on the line
    if x in range(77, 83) or x in range(162, 167):
        return
    if y in range(77, 83) or y in range(162, 167):
        return

    # Checking which box was pressed
    if x < 0:
        return
    elif x < 77:
        r = 1
    elif x < 162:
        r = 2
    elif x < 250:
        r = 3
    else:
        return
    
    if y < 0:
        return
    elif y < 77:
        c = 1
    elif y < 162:
        c = 2
    elif y < 250:
        c = 3
    else:
        return
    
    place(r,c)

running = True

while running:

    screen.fill(teal)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                print("Trying to escape?")
        elif event.type == MOUSEBUTTONDOWN and winner == 0:
            click()

    # Displaying the grid
    screen.blit(box.surface, ((SCR_WIDTH - box_dim[0])//2, (SCR_HEIGHT - box_dim[1])//2))
    pygame.draw.line(box.surface, grey, (80, 5), (80, 245), 5)
    pygame.draw.line(box.surface, grey, (165, 5), (165, 245), 5)
    pygame.draw.line(box.surface, grey, (5, 80), (245, 80), 5)
    pygame.draw.line(box.surface, grey, (5, 165), (245, 165), 5)

    # Displaying the rules
    msg1 = "If the game ends in a draw, Player 1 gets a point." 
    msg2 = "If either player wins, Player 2 gets a point."
    m1_w, m1_h = rulefont.size(msg1)
    m2_w, m2_h = rulefont.size(msg2)
    rules1 = rulefont.render(msg1, 1, (0,0,0))
    rules2 = rulefont.render(msg2, 1, (0,0,0))
    screen.blit(rules1, ((SCR_WIDTH - m1_w)//2, (SCR_HEIGHT - box_dim[1])//2 - 100))
    screen.blit(rules2, ((SCR_WIDTH - m2_w)//2, (SCR_HEIGHT - box_dim[1]+m1_h)//2 - 75))

    draw()
    winner = check_winner()
    
    # NORMAL RULES
    # if winner != 0:
    #     if winner == 1:
    #         label = winfont.render("X wins!", 1, (0,0,0))
    #     else:
    #         label = winfont.render("O wins!", 1, (0,0,0))
    #     screen.blit(label, ((SCR_WIDTH - box_dim[0])//2 + 25, (SCR_HEIGHT - box_dim[1])//2 + 300))

    if winner != 0:
        label = winfont.render("Player 2 Wins!", 1, (0,0,0))
        label_w, label_h = winfont.size("Player 2 Wins!")
        screen.blit(label, ((SCR_WIDTH - label_w)//2, (SCR_HEIGHT - box_dim[1])//2 + 300))
    
    if check_finish() and winner == 0:
        label = winfont.render("Player 1 Wins!", 1, (0,0,0))
        label_w, label_h = winfont.size("Player 1 Wins!")
        screen.blit(label, ((SCR_WIDTH - label_w)//2, (SCR_HEIGHT - box_dim[1])//2 + 300))


    pygame.display.flip()

print("Fin.")
