    # coding: utf-8
#
# A simple snake game with

VERSION = "0.1"

try:
    import sys
    import os
    import time
    import itertools
    import random

    from configuration import (WINDOW_SIZE, HEAD_IMG, IMAGE_FOLDER,
                               TAIL_IMG, BODY_STRAIGHT_IMG, MAP_SIZE,
                               CASE_SIZE, TURN_IMG, GAME_OVER, FRUITS_IMG)
    import pygame
    from pygame.locals import *
except ImportError as err:
    print("Impossible de charger le module. %s" % (err))
    sys.exit(2)

pygame.init()
screen = pygame.display.set_mode(WINDOW_SIZE)


def load_png(image):
    """ Charge une image à partir d'un fichier
    Param:
        image -> str -> chemin vers une image
    Return:
        pygame.Surface -> Objet de l'image
    """
    fullname = os.path.join(IMAGE_FOLDER, image)
    try:
        image = pygame.image.load(fullname)
        if image.get_alpha() is None:
            image = image.convert()
        else:
            image = image.convert_alpha()
    except pygame.error as message:
        print("Impossible to load image: ", message)
        sys.exit(2)
    return image

game_over = load_png(GAME_OVER)

class Snake():
    """Classe permettant la gestion du serpent à afficher"""

    def __init__(self, initial_size=3):
        """Initialisation of the class
        param:
            initial_size -> int -> the lenght of the snake at the begining
        """
        self.images = {"head": load_png(HEAD_IMG),
                       "body_straight": load_png(BODY_STRAIGHT_IMG),
                       "tail": load_png(TAIL_IMG),
                       "body_turn": load_png(TURN_IMG)}
        self.initial_size = initial_size
        self.coordonnees = [[int(MAP_SIZE[0] / 2), int(MAP_SIZE[1] / 2)]
                            for i in range(initial_size)]
        self.surface = pygame.surface.Surface(WINDOW_SIZE)
        self.surface.set_colorkey((0, 0, 0))
        self.directions = [0 for i in range(initial_size)]

    def update(self):
        """Update the surface of the snake"""
        self.surface.fill((0, 0, 0))
        # head
        self.surface.blit(pygame.transform.rotate(self.images["head"],
                                                  -90 * self.directions[0]),
                          (CASE_SIZE[0] * self.coordonnees[0][0],
                           CASE_SIZE[1] * self.coordonnees[0][1]))
        # body
        size_x, size_y = CASE_SIZE

        for i in range(len(self.coordonnees[1:-1])):
            x, y = self.coordonnees[i + 1]
            direction = self.directions[i + 1]
            direction_prec = self.directions[i]
            if direction == direction_prec:  # straight
                self.surface.blit(pygame.transform.rotate(
                    self.images["body_straight"],
                    -90 * direction),
                                  (size_x * x, size_y * y))
            # turn right>top or botom>left
            if (direction == 0 and direction_prec == 1) or \
               (direction == 3 and direction_prec == 2):
                self.surface.blit(pygame.transform.rotate(
                    self.images["body_turn"],
                    0),
                                  (size_x * x, size_y * y))
            # turn left>top or botom>right
            if (direction == 0 and direction_prec == 3) or \
               (direction == 1 and direction_prec == 2):
                self.surface.blit(pygame.transform.rotate(
                    self.images["body_turn"],
                    -90),
                                  (size_x * x, size_y * y))
            # turn left>botom or top>right
            if (direction == 2 and direction_prec == 3) or \
               (direction == 1 and direction_prec == 0):
                self.surface.blit(pygame.transform.rotate(
                    self.images["body_turn"],
                    180),
                                  (size_x * x, size_y * y))
            # turn top>left or right>botom
            if (direction == 3 and direction_prec == 0) or \
               (direction == 2 and direction_prec == 1):
                self.surface.blit(pygame.transform.rotate(
                    self.images["body_turn"],
                    90),
                                  (size_x * x, size_y * y))
        # Tail
        self.surface.blit(pygame.transform.rotate(self.images["tail"],
                                                  -90 * self.directions[-2]),
                          (size_x * self.coordonnees[-1][0],
                           size_y * self.coordonnees[-1][1]))

    def deplacer(self, direction=0):
        """Move the snake
        0 = top
        1 = right
        2 = bottom
        3 = left"""
        # forbiden about-face
        if self.directions[0] != direction:
            if self.directions[0] + direction == 2:
                direction = self.directions[0]
            elif self.directions[0] + direction == 4:
                direction = self.directions[0]
            elif direction not in (0, 1, 2, 3):
                direction = self.directions[0]

        # insert new direction
        self.directions.insert(0, direction)
        self.directions = self.directions[:-1]
        # insert new coordonnees
        if direction == 0:
            nouvelle_coordonnee = (self.coordonnees[0][0],
                                   self.coordonnees[0][1] - 1)
            self.coordonnees.insert(0, nouvelle_coordonnee)
            self.coordonnees = self.coordonnees[:-1]
        elif direction == 1:
            nouvelle_coordonnee = (self.coordonnees[0][0] + 1,
                                   self.coordonnees[0][1])
            self.coordonnees.insert(0, nouvelle_coordonnee)
            self.coordonnees = self.coordonnees[:-1]
        elif direction == 2:
            nouvelle_coordonnee = (self.coordonnees[0][0],
                                   self.coordonnees[0][1] + 1)
            self.coordonnees.insert(0, nouvelle_coordonnee)
            self.coordonnees = self.coordonnees[:-1]
        elif direction == 3:
            nouvelle_coordonnee = (self.coordonnees[0][0] - 1,
                                   self.coordonnees[0][1])
            self.coordonnees.insert(0, nouvelle_coordonnee)
            self.coordonnees = self.coordonnees[:-1]

    def grow(self):
        """Grow the snake"""
        self.directions.append(self.directions[-1])
        self.coordonnees.append(self.coordonnees[-1])

    def collision(self):
        for coord in self.coordonnees[1:]:
            if coord == self.coordonnees[0]:
                return True
        if self.coordonnees[0][0] < 0 or \
           self.coordonnees[0][1] < 0 or \
           self.coordonnees[0][0] > MAP_SIZE[0] or \
           self.coordonnees[0][1] > MAP_SIZE[1]:
            return True
        return False


class Fruits():
    """Class for fruits"""

    def __init__(self):
        self.fruits_coords = []
        self.fruits_image = []
        self.images = [load_png(image) for image in FRUITS_IMG]
        self.surface = pygame.surface.Surface(WINDOW_SIZE)
        self.surface.fill((0, 0, 0))
        self.surface.set_colorkey((0, 0, 0))

    def add_fruit(self):
        """Add a fruit on the map"""
        condition = True
        ligne, case = (0, 0)
        while (ligne, case) in self.fruits_coords or condition:
            ligne = random.randint(0, MAP_SIZE[0]-1)
            case = random.randint(0, MAP_SIZE[1]-1)
            condition = False
        self.fruits_coords.append((ligne, case))
        self.fruits_image.append(random.choice(self.images))
        self.update()

    def collision(self, x, y):
        """test if ther is a colision between coordinates, y and x, and a fruit on map"""
        for i in range(len(self.fruits_coords)):
            if self.fruits_coords[i] == (x, y):
                del self.fruits_coords[i]
                del self.fruits_image[i]
                return True
            
    def update(self):
        self.surface.fill((0, 0, 0))
        for i in range(len(self.fruits_coords)):
            self.surface.blit(self.fruits_image[i],
                              (self.fruits_coords[i][0]*CASE_SIZE[0],
                               self.fruits_coords[i][1]*CASE_SIZE[1]))
    


class Game():
    """ Main class for the game """

    def __init__(self, difficult):
        """initialisation of the game"""
        self.snake = Snake(initial_size=6)
        self.fruits = Fruits()
        self.points = 0
        self.font = pygame.font.SysFont("monospace", 24)
        self.speed = 1
        self.difficult = difficult

    def run(self):
        """run the game"""
        
        pygame.display.set_caption('Znake')
        pygame.mouse.set_visible(0)
        temps_prec = 0
        clock = pygame.time.Clock()
        move = False
        black = pygame.surface.Surface(WINDOW_SIZE)
        self.fruits.add_fruit()
        self.fruits.add_fruit()
        self.fruits.add_fruit()
        self.fruits.add_fruit()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    return
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    if event.key == K_UP:
                        self.snake.deplacer(0)
                        move = True
                    elif event.key == K_RIGHT:
                        self.snake.deplacer(1)
                        move = True
                    elif event.key == K_DOWN:
                        self.snake.deplacer(2)
                        move = True
                    elif event.key == K_LEFT:
                        self.snake.deplacer(3)
                        move = True
            if not move:
                self.snake.deplacer(-1)
            if self.fruits.collision(*self.snake.coordonnees[0]):
                self.points += 10
                self.snake.grow()
                self.fruits.add_fruit()
                self.speed += 0.1*self.difficult
            self.points += 1
            move = False
            self.snake.update()
            screen.blit(black, (0, 0))
            score_display = self.font.render(str(self.points), 1, (0,0,255))
            screen.blit(score_display, (0, 0))
            screen.blit(self.fruits.surface, (0, 0))
            screen.blit(self.snake.surface, (0, 0))
            if self.snake.collision():
                screen.blit(game_over, (0, 0))
                pygame.display.flip()
                return
            pygame.display.flip()
            clock.tick(self.speed)

if __name__ == '__main__':
    game = Game(difficult = 5)
    game.run()
