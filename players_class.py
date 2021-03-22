import pygame
import math
from pygame.locals import *
from settings import *
from dice import *

class Players:
    def __init__(self, game, pos, color):
        self.game = game

        self.grid_pos = pos
        self.color = color

        self.pix_pos = self.get_pix_pos(self.grid_pos)

        self.player_img1 = pygame.image.load('players//player1-right.png')
        self.player_img2 = pygame.image.load('players//player2-left.png')
        self.player_img3 = pygame.image.load('players//player3-left.png')
        self.player_img4 = pygame.image.load('players//player4-right.png')

        self.direction = None

        self.able_to_move = True

    def draw(self):
        if self.color == red:
            self.direction = vec(1, 0)
            self.game.screen.blit(self.player_img1, (self.pix_pos.x, self.pix_pos.y))

        elif self.color == green:
            self.direction = vec(-1, 0)
            self.game.screen.blit(self.player_img2, (self.pix_pos.x, self.pix_pos.y))

        elif self.color == blue:
            self.direction = vec(-1, 0)
            self.game.screen.blit(self.player_img3, (self.pix_pos.x, self.pix_pos.y))

        elif self.color == yellow:
            self.direction = vec(1, 0)
            self.game.screen.blit(self.player_img4, (self.pix_pos.x, self.pix_pos.y))

    # inside our game maze we have different positions of grid and of pixels

    def get_pix_pos(self, grid_pos):
        self.grid_pos = grid_pos
        if self.color == red:
            return vec((self.grid_pos.x + self.game.cell_width), (self.grid_pos.y + self.game.cell_height))
        elif self.color == green:
            return vec((self.grid_pos.x - self.game.cell_width), (self.grid_pos.y + self.game.cell_height))
        elif self.color == blue:
            return vec((self.grid_pos.x - self.game.cell_width), (self.grid_pos.y - self.game.cell_height))
        elif self.color == yellow:
            return vec((self.grid_pos.x + self.game.cell_width), (self.grid_pos.y - self.game.cell_height))

    def update(self):
        self.able_to_move = self.can_move()

        if self.able_to_move:
            if self.direction == vec(1, 0):
                self.pix_pos[0] += self.game.cell_width

            if self.direction == vec(-1, 0):
                self.pix_pos[0] -= self.game.cell_width

            if self.direction == vec(0, 1):
                self.pix_pos[1] += self.game.cell_height

            if self.direction == vec(0, -1):
                self.pix_pos[1] -= self.game.cell_height

        #this is for coordinating grid pos with pix pos
        self.grid_pos[0] = (self.pix_pos[0] + self.game.cell_width//2)//self.game.cell_width
        self.grid_pos[1] = (self.pix_pos[1] + self.game.cell_height // 2) // self.game.cell_height

    def move(self, direction):
        self.direction = direction
        self.update()

    #check if it is hitting a wall
    def can_move(self):
        for wall in self.game.walls:
            if (vec(self.grid_pos) + self.direction) == wall:
                self.game.count -= 1
                return False
        return True

    def reset_player(self):
        if self.color == red:
            self.pix_pos = self.get_pix_pos(vec(1, 1))
            self.player_img1 = pygame.image.load('players//player1-right.png')
            self.draw()
        if self.color == green:
            self.pix_pos = self.get_pix_pos(vec(540, 1))
            self.player_img2 = pygame.image.load('players//player2-left.png')
            self.draw()
        if self.color == blue:
            self.pix_pos = self.get_pix_pos(vec(540, 600))
            self.player_img3 = pygame.image.load('players//player3-left.png')
            self.draw()
        if self.color == yellow:
            self.pix_pos = self.get_pix_pos(vec(1, 600))
            self.player_img4 = pygame.image.load('players//player4-right.png')
            self.draw()
