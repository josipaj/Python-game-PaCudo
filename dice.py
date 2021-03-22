import pygame
import random
from game import *
from settings import *

class Dice:
    def __init__(self, game, screen):
        self.game = game
        self.dice_pos = pygame.Rect(WIDTH-90, HEIGHT//2-90, 80, 80)

        self.current_playing = None
        self.dice_num = 1

        self.roll_time = 500  # ms
        self.roll_start = 0
        self.roll = False                                               #used from the main update loop to check whether to animate dice
        self.double_roll = False
        self.completed_roll = False

    def draw_dice(self):
        self.dice_numbers(self.dice_num)
        #pygame.draw.rect(self.game.background, white, self.dice_pos, 0)

    # display a static dice

    def show_static_dice(self, current_playing):
        self.completed_roll = False
        self.current_playing = current_playing

    # begins the dice roll
    def start_roll(self):
        self.roll = True
        self.roll_start = pygame.time.get_ticks()

                                                        # get_ticks - daje vrime u milisekundama
    def roll_animation(self, current_playing):
        self.current_playing = current_playing
        time_since_roll = pygame.time.get_ticks() - self.roll_start

        if time_since_roll < self.roll_time:
            rand = random.randrange(1, 7)                                     # 1 to 6
            self.dice_num = rand
        else:
            if self.dice_num == 6:
                self.double_roll = True
            elif self.double_roll is True:
                self.double_roll = False
            self.roll = False
            self.completed_roll = True
            self.current_playing = None
            return

    def dice_numbers(self, num):
        pygame.draw.rect(self.game.background, self.game.def_players[self.game.current_playing], self.dice_pos, 0)
        set_x = [[40], [20, 60], [20, 40, 60], [20, 60, 20, 60], [20, 60, 20, 60, 40], [20, 60, 20, 60, 20, 60]]
        set_y = [[40], [20, 60], [20, 40, 60], [20, 20, 60, 60], [20, 20, 60, 60, 40], [20, 20, 60, 60, 40, 40]]
        for i in range(num):
            pos_x = self.dice_pos[0] + set_x[num-1][i]
            pos_y = self.dice_pos[1] + set_y[num-1][i]
            pygame.draw.circle(self.game.background, black, (pos_x, pos_y), 8)
