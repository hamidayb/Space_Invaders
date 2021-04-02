# Required Libraries imported
import pygame as py
from pygame import mixer
import random

# initialize pygame fonts
py.font.init()

# Set the game window
width = 750
height = 750
window = py.display.set_mode((width, height))
py.display.set_caption("SPACE INVADERS")

# Load background music
mixer.init()
mixer.music.load("bg_sound.mp3")
mixer.music.set_volume(0.7)

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

def main(level):
    # start background music
    mixer.music.play(-1)

    # initializing variables
    run_game = True
    frames_per_second = 60
    score = 0

    # Setting font family to 'comicsans' and font size to 50px
    label_font = py.font.SysFont("comicsans",35)
    popup_font = py.font.SysFont("comicsans", 60)

    # array of asteroids displayed on screen
    asteroids = []

    if level == "Easy":
        asteroids_wave_size = 50
        asteroid_move_value = 1
    if level == "Medium":
        asteroids_wave_size = 70
        asteroid_move_value = 2
    if level == "Hard":
        asteroids_wave_size = 90
        asteroid_move_value = 3

    # spaceship moving speed
    spaceship_move_value = 10

    # SpaceShip object with 300 x value and 650 y value
    spaceship = SpcaeShip(300, 650)

    time_clock = py.time.Clock()

    hit_fire_asteroid = False
    timer = 0   # timer to quit game after hit
    win = False

    # For each iteration of while loop we want to refresh the window
    def redraw_window():
        # set background image
        window.blit(BG, (0, 0))

        orange_color = (252, 186, 3)
        # displaying level with White(255,255,255) color
        level_label = label_font.render("Level:  {}".format(level), 1, orange_color)
        # displaying score with red(0,0,255) color
        score_label = label_font.render("Score:  {}".format(score), 1, orange_color)

        # calculate left padding of score label
        score_left_padding = width - score_label.get_width() - 10

        # position level
        window.blit(level_label, (10, 10))
        # position score
        window.blit(score_label, (score_left_padding, 10))

        # display asteroids on window
        for asteroid in asteroids:
            asteroid.draw(window)

        # display spaceship on game window
        spaceship.draw(window)

        # if spaceship hit fire_asteroid
        if hit_fire_asteroid:
            # display
            hit_label = popup_font.render("You Lose: {}".format(score), 1, orange_color)
            window.blit(hit_label, (width/2 - hit_label.get_width()/2, 350))

        # winning Score
        if win:
            # display
            win_label = popup_font.render("You Win: {}".format(score), 1, orange_color)
            window.blit(win_label, (width / 2 - win_label.get_width() / 2, 350))


        py.display.update()

    # Loop until the user quits the game
    while run_game:
        # run the game at 60 frames per second
        time_clock.tick(frames_per_second)

        #call redraw_window function
        redraw_window()

        # After collision end the game after 3s
        if hit_fire_asteroid or win:
            timer += 1
            # exit the game if timer equals 3
            if timer > frames_per_second * 5:
                quit()

        # checks asteroids array lengtht
        if len(asteroids) == 0:
            # loop upto the asteroids_wave_size
            for i in range(asteroids_wave_size):
                # x value of asteroid
                x_value = random.randrange(50, width-100)

                # y value of asteroid
                # it is negative because asteroid is to created off the screen
                if level == "Easy":
                    y_value = random.randrange(-2500, -100)
                if level == "Medium":
                    y_value = random.randrange(-3500, -100)
                if level == "Hard":
                    y_value = random.randrange(-4500, -100)
                # random asteroid type
                random_asteroid = random.choice([FIRE_ROCK, WHITE_ROCK])

                # Asteroids object created
                asteroid = Asteroids(x_value, y_value, random_asteroid)

                # add asteroid to the asteroids array
                asteroids.append(asteroid)



        # Loop through events that occurs
        for event in py.event.get():
            # Quit the game
            if event.type == py.QUIT:
                quit()


        # move the spaceship when arrow keys are pressed
        key = py.key.get_pressed()

        # If hit_fire_asteroid is true then player shouldn't be able to move spaceship
        if (not hit_fire_asteroid) and (not win):
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
            if (not hit_fire_asteroid) and (not win):
                # move asteroid down
                asteroid.move(asteroid_move_value)

            # spaceship hits fire_asteroid
            if asteroid.collision(spaceship) and (asteroid.get_type() is FIRE_ROCK):
                # play collision sound
                collision_sound = mixer.Sound("crash.wav")
                collision_sound.play()

                hit_fire_asteroid = True
                asteroids.remove(asteroid)

            # spaceship hits white_asteroid
            if asteroid.collision(spaceship) and (asteroid.get_type() is WHITE_ROCK):
                # play eat sound
                eat_sound = mixer.Sound("eat.wav")
                eat_sound.play()

                score += 5 # increase score by 5
                asteroids.remove(asteroid) # hide that asteroid
                # set win to True score exceeds winning score 50
                if(score >= 50):
                    win = True

# Main Menu
def menu():
    # Font to be used for main menu
    menu_font = py.font.SysFont("comicsans", 50)
    level_font = py.font.SysFont("comicsans", 40)
    # variable to handle game quit or run
    run_game = True
    while run_game:
        # rgb value of orange
        orange_color = (252, 186, 3)
        white_color = (255, 255, 255)
        # Label to be shown before game start and after game ends
        menu_label = menu_font.render("Main Menu", 1, orange_color)
        easy_level = level_font.render("Press 1 for EASY Level", 1, white_color)
        medium_level = level_font.render("Press 2 for MEDIUM Level", 1, white_color)
        hard_level = level_font.render("Press 3 for HARD Level", 1, white_color)

        # place label on the window
        x_value = width/2 - menu_label.get_width()/2 # center position
        y_value = 150
        window.blit(menu_label, (x_value, y_value)) # position Menu Label
        window.blit(easy_level, (x_value - 70, y_value + 100)) # position Easy Label
        window.blit(medium_level, (x_value - 70, y_value + 150)) # position Medium Label
        window.blit(hard_level, (x_value - 70, y_value + 200)) # position Hard Label

        py.display.update()

        # check for events and loop through them
        for event in py.event.get():
            # Quit game
            if event.type == py.QUIT:
                run_game = False
        keys = py.key.get_pressed()
        if keys[py.K_1]:
            main("Easy")
        if keys[py.K_2]:
            main("Medium")
        if keys[py.K_3]:
            main("Hard")

    py.quit()

menu()