# Required Libraries imported
import pygame as py
import time
import random

# initialize pygame fonts
py.font.init()

# Set the game window
width = 750
height = 750
window = py.display.set_mode((width, height))
py.display.set_caption("SPACE INVADERS")

# Load Player SpaceShip
SPACESHIP = py.image.load("spaceship.png")

# Load Asteroid Images
WHITE_ROCK = py.image.load("white_rock.png")
FIRE_ROCK = py.image.load("fire_rock.png")

# load background image
BG = py.image.load("space.jpg")

# Change SPACESHIP size
SPACESHIP = py.transform.scale(SPACESHIP, (80, 80))

# Change ASTEROID size
WHITE_ROCK = py.transform.scale(WHITE_ROCK, (80, 80))
FIRE_ROCK = py.transform.scale(FIRE_ROCK, (120, 120))

class SpcaeShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spaceship_img = None

    # spaceship
    def draw(self, window):
        window.blit(self.spaceship_img, (self.x, self.y))

class Player(SpcaeShip):
    def __init__(self, x, y):
        super().__init__(x,y)
        self.spaceship_img = SPACESHIP
        # create mask of spaceship_img
        # mask tells where the pixels are and where are not
        # so that when we have a collision we can know about that
        self.mask = py.mask.from_surface(self.spaceship_img)

def main():
    run_game = True
    frames_per_second = 60
    # initializing game level and score variables
    level = "Easy"
    score = 0
    # Setting font family to 'comicsans' and font size to 50px
    label_font = py.font.SysFont("comicsans",35)

    # for setting the pixels when arrow keys are pressed to move the spaceship
    spaceship_move_pixel = 20

    spaceship = Player(300, 650)

    time_clock = py.time.Clock()
    # For each iteration of while loop we want to refresh the window
    def redraw_window():
        # displaying level with White(255,255,255) color
        level_label = label_font.render("Level:  {}".format(level), 1, (255,255,255))
        # displaying score with red(0,0,255) color
        score_label = label_font.render("Score:  {}".format(score), 1, (255,255,255))

        # calculate left padding of score label
        score_left_padding = width - score_label.get_width() - 10

        # position level and score
        window.blit(level_label, (10, 10))
        window.blit(score_label, (score_left_padding, 10))

        spaceship.draw(window)

        py.display.update()

    # Loop until the user quits the game
    while run_game:
        # run the game at 60 frames per second
        time_clock.tick(frames_per_second)
        redraw_window()

        # Loop through the 60 frames per second & check for events
        for event in py.event.get():
            if event.type == py.QUIT:
                run_game = False

            # move the spaceship when arrow keys are pressed
            key = py.key.get_pressed()
            if(key[py.K_a]) and spaceship.x - spaceship_move_pixel > 0: # left
                spaceship.x -= spaceship_move_pixel
            if (key[py.K_d]) and spaceship.x + spaceship_move_pixel + 50 < width: # right
                spaceship.x += spaceship_move_pixel
            if (key[py.K_w]) and spaceship.y - spaceship_move_pixel > 0: # up
                spaceship.y -= spaceship_move_pixel
            if (key[py.K_s]) and spaceship.y + spaceship_move_pixel + 50 > height: # down
                spaceship.y += spaceship_move_pixel


main()