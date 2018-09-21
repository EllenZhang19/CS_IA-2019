'''
Created by Ellen Zhang
'''

import random
import pygame
from pygame.locals import *
from sys import exit

# --- constants --- (UPPER_CASE names)

SCREEN_WIDTH = 400         # resolution of the windows
SCREEN_HEIGHT = 600


# --- classes --- (CamelCase names)

class Car(pygame.sprite.Sprite):

    def __init__(self, image, dx):
        pygame.sprite.Sprite.__init__(self)

        self.car_img1 = pygame.image.load('resources/car1.png')
        self.car_img2 = pygame.image.load('resources/car2.png')

        # self.image is the current image to be drawn
        # switch betweeen image 1 and image 2 before drawing
        self.image = self.car_img1
        self.rect = self.image.get_rect()
        self.rect.y = 500
        self.rect.x = dx

        self.moving_left = False
        self.moving_right = False
        self.is_hit = False

    def update(self):
        # always update position and rect together
        # puts position of car on center of rect
        if self.moving_left:
            self.rect.x -= 8
        if self.moving_right:
            self.rect.x += 8


    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False


    def draw(self, image, screen):
        screen.blit(image, self.rect)


class Star(pygame.sprite.Sprite):
    def __init__(self, initial_x):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('resources/star.png')
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = 0

        self.v = random.randint(0,5)
        self.a = (random.randint(2, 10))/10

    def update(self):
        self.rect.y += self.v
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        self.accelerated()

    def accelerated(self):
        self.v += self.a

class Stone(pygame.sprite.Sprite):
    def __init__(self, initial_x):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('resources/stone.png')
        self.rect = self.image.get_rect()
        self.rect.x = initial_x
        self.rect.y = 0

        self.v = 1
        self.a = 0.8

    def update(self):
        self.rect.y += self.v
        if self.rect.y > SCREEN_HEIGHT:
            self.kill()
        self.accelerated()

    def accelerated(self):
        self.v += self.a



# --- fuctions --- (lower_case names)

    # empty

# --- main --- (lower_case names)\


# - init -


# initiate the game
pygame.init()                                                    # initiate pygame
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))  # initiate screen
pygame.display.set_caption('Get the Coin')                         # initiate caption

pygame.font.init()                                               # initiate font
myfont = pygame.font.SysFont('Comic Sans MS', 30)

# - objects -

background = pygame.image.load('resources/bg.png')   # load the bg image
gameover = pygame.image.load('resources/gameover.png') # new

car = Car('resources/car1.jpg', 183)   # create a car, middle = 183, left = 83, right = 283
rect = car.image.get_rect()


#create a sprite group that contains just sars
star_group = pygame.sprite.Group()
star_group_catch = pygame.sprite.Group()

stone_group = pygame.sprite.Group()
stone_group_catch = pygame.sprite.Group()

# create button
#button = pygame.Rect(150, 520, 100, 50)

# - main loop -

goal_star = 0
ticks = 0
clock = pygame.time.Clock()


while True:

    # - events -
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            pygame.QUIT
            exit()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                pygame.QUIT
                exit()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos     # gets mouse position

            # checks if mouse position is over the button

            if button.collidepoint(mouse_pos):
                # prints current location of mouse
                print(mouse_pos)
                goal_star = 0
                continue

                # restart game

        # - objects event handle -
        car.handle_event(event)

    # - updates -
    car.update()
    if car.rect.x < 52:
        car.rect.x = 52
    elif car.rect.x > 312:
        car.rect.x = 312

    # generate stars
    if ticks % 100 == 0:
        star = Star(random.randint(65, 304))
        star_group.add(star)

    if ticks % 30 == 0:
        stone = Stone(random.randint(65, 304))
        stone_group.add(stone)
        
    # update stars
    star_group.update()
    stone_group.update()

    # determine collision with star
    star_group_catch.add(pygame.sprite.spritecollide(car, star_group, True))
    goal_star = len(star_group_catch)
    for star_catch in star_group_catch:
        star_catch.image = None

    # determine collision with stones
    stone_group_catch.add(pygame.sprite.spritecollide(car, stone_group, True))
    for stone_catch in stone_group_catch:
        stone_catch.image = None
    if len(stone_group_catch) > 0:
        car.is_hit = True


    # -  draw -
    screen.blit(background ,(0,0))
    if car.is_hit:
        car.image = pygame.image.load('resources/car_crush.png')
        textsurface1 = myfont.render('You get a score of ' + str(goal_star*10), False, (0, 0, 0))
        textsurface2 = myfont.render('Press ESC to exit', False, (0, 0, 0))
        textsurface3 = myfont.render('Press the button to restart', False, (0,0,0))
        screen.blit(gameover, (0, 0))
        screen.blit(textsurface1,(100,50))
        screen.blit(textsurface2,(120,450))
        #screen.blit(textsurface3,(70,480))
        #pygame.draw.rect(screen, [255, 0, 0], button)  # draw button
    else:
        if ticks % 50 < 25:
            car.draw(car.car_img1, screen)
        else:
            car.draw(car.car_img2, screen)
        ticks += 1

    # draw stars
    star_group.draw(screen)
    stone_group.draw(screen)

    # update the pygame display
    pygame.display.update()

    # - FPS -
    clock.tick(60)


while True:
    pygame.display.update()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
