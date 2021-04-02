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

# set background image size to game resolution
BG = py.transform.scale(BG, (width, height))

class SpcaeShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.spaceship_img = SPACESHIP
        # create mask of spaceship_img
        # mask tells where the pixels are and where are not
        # so that when we have a collision we can know about that
        self.mask = py.mask.from_surface(self.spaceship_img)

    # for displaying spacship on game window
    def draw(self, window):
        window.blit(self.spaceship_img, (self.x, self.y))

    # get spaceship width
    def get_width(self):
        return  self.spaceship_img.get_width()

    # get spaceship height
    def get_height(self):
        return  self.spaceship_img.get_height()

# Asteroid Class
class Asteroids:
    def __init__(self, x, y, asteroid):
        self.x = x
        self.y = y
        self.asteroid_img = asteroid
        self.mask = py.mask.from_surface(self.asteroid_img)

    # move asteroids on the window
    def move(self, value):
        self.y += value

    # for displaying asteroid on game window
    def draw(self, window):
        window.blit(self.asteroid_img, (self.x, self.y))

    def get_type(self):
        return self.asteroid_img

    # get asteroid width
    def get_width(self):
        return  self.asteroid_img.get_width()

    # get asteroid height
    def get_height(self):
        return  self.asteroid_img.get_height()

    def collision(self, spaceship):
        return collide(self, spaceship)

# checks whether spaceship and asteroid collides or not
def collide(object1, object2):
    x_offset = object2.x - object1.x
    y_offset = object2.y - object1.y
    return object1.mask.overlap(object2.mask, (x_offset, y_offset)) != None
def main():
    run_game = True
    frames_per_second = 60
    # initializing game level and score variables
    level = "High"
    score = 0
    # Setting font family to 'comicsans' and font size to 50px
    label_font = py.font.SysFont("comicsans",35)
    popup_font = py.font.SysFont("comicsans", 60)

    # array of asteroids displayed on screen
    asteroids = []

    if level == "Easy":
        asteroids_wave_size = 40
        asteroid_move_value = 1
    if level == "Medium":
        asteroids_wave_size = 40
        asteroid_move_value = 2
    if level == "High":
        asteroids_wave_size = 40
        asteroid_move_value = 3

    # for setting the pixels when arrow keys are pressed to move the spaceship
    spaceship_move_value = 20

    spaceship = SpcaeShip(300, 650)

    time_clock = py.time.Clock()

    hit_fire_asteroid = False
    timer = 0   # timer to quit game after hit

    # For each iteration of while loop we want to refresh the window
    def redraw_window():
        window.blit(BG, (0, 0))

        orange_color = (252, 186, 3)
        # displaying level with White(255,255,255) color
        level_label = label_font.render("Level:  {}".format(level), 1, orange_color)
        # displaying score with red(0,0,255) color
        score_label = label_font.render("Score:  {}".format(score), 1, orange_color)

        # calculate left padding of score label
        score_left_padding = width - score_label.get_width() - 10

        # position level and score
        window.blit(level_label, (10, 10))
        window.blit(score_label, (score_left_padding, 10))

        # display asteroids on window
        for asteroid in asteroids:
            asteroid.draw(window)

        # display spaceship on game window
        spaceship.draw(window)

        if hit_fire_asteroid:
            hit_label = popup_font.render("You Lost!", 1, (255,255,255))
            window.blit(hit_label, (width/2 - hit_label.get_width()/2, 350))
            end_time = time.process_time()

        py.display.update()

    # Loop until the user quits the game
    while run_game:
        # run the game at 60 frames per second
        time_clock.tick(frames_per_second)

        #call redraw_window
        redraw_window()

        if hit_fire_asteroid:
            timer += 1
            if timer > frames_per_second * 3:
                run_game = False

        if len(asteroids) == 0:
            for i in range(asteroids_wave_size):
                asteroid = Asteroids(random.randrange(50, width-100), random.randrange(-2500, -100), random.choice([FIRE_ROCK, WHITE_ROCK]))
                asteroids.append(asteroid)
            asteroids_wave_size = 0

        # Loop through the 60 frames per second & check for events
        for event in py.event.get():
            if event.type == py.QUIT:
                run_game = False

        # move the spaceship when arrow keys are pressed
        key = py.key.get_pressed()

        # If hit_fire_asteroid is true then player shouldn't be able to move spaceship
        if not hit_fire_asteroid:
            # if 'a' is pressed move left
            if(key[py.K_a]) and (spaceship.x - spaceship_move_value > 0):
                spaceship.x -= spaceship_move_value
            # if 'd' is pressed move right
            if (key[py.K_d]) and (spaceship.x + spaceship_move_value + spaceship.get_width() < width): # right
                spaceship.x += spaceship_move_value
            # if 'w' is pressed move up
            if (key[py.K_w]) and (spaceship.y - spaceship_move_value > 0): # up
                spaceship.y -= spaceship_move_value
            # if 's' is pressed move down
            if (key[py.K_s]) and (spaceship.y + spaceship_move_value + spaceship.get_height() + 15 < height):  # down
                spaceship.y += spaceship_move_value

        # move asteroids downward
        for asteroid in asteroids[:]:

            # pause movement of asteroids if asteroid spaceship hit asteroid
            if not hit_fire_asteroid:
                # move asteroid down
                asteroid.move(asteroid_move_value)

            # spaceship hits fire_asteroid
            if asteroid.collision(spaceship) and (asteroid.get_type() is FIRE_ROCK):
                hit_fire_asteroid = True

            # spaceship hits white_asteroid
            if asteroid.collision(spaceship) and (asteroid.get_type() is WHITE_ROCK):
                score += 1 # increase score by 1
                asteroids.remove(asteroid) # hide that asteroid

main()