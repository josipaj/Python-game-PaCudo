import pygame, math
from pygame.locals import *
# ova druga linija da nemoramo pisat non stop pygame. nesto nego se to podrazumijeva, ali ne kod svega nego samo kod odredenih konstanti
from settings import *
from dice import *
from players_class import *

# initialize the pygame
pygame.init()

class Game:
    def __init__(self):

        # create the screen
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        self.running = True
        self.state = 'start'

        # varijable za grid napravit
        self.cell_width = WIDTH // 28
        self.cell_height = HEIGHT // 30

        #pocetni polozaji igraca
        self.START_PLAYER1_POS = vec(1, 1)  # ovo u zagradama su ka pikseli
        self.START_PLAYER2_POS = vec(WIDTH - self.cell_width, 1)
        self.START_PLAYER3_POS = vec(WIDTH - self.cell_width, HEIGHT - self.cell_height)
        self.START_PLAYER4_POS = vec(1, HEIGHT - self.cell_height)

        self.num_of_play = 1

        self.player1 = Players(self, self.START_PLAYER1_POS, red)
        self.player2 = Players(self, self.START_PLAYER2_POS, green)
        self.player3 = Players(self, self.START_PLAYER3_POS, blue)
        self.player4 = Players(self, self.START_PLAYER4_POS, yellow)

        self.winning_pos_red = None
        self.winning_pos_green = None
        self.winning_pos_blue = None
        self.winning_pos_yellow = None
        self.grid_pos_red = None
        self.grid_pos_green = None
        self.grid_pos_blue = None
        self.grid_pos_yellow = None


        #grid pos za odredivanje ovih pobjednickih pozicija
        #self.grid_pos = None

        #varijable bas za igru
        self.current_playing = 0
        self.move_unit = False
        self.is_moving = False


        #brojac koji broji koliko pozicija je prosa igrac
        self.count = 0

        self.def_players = []

        self.dice = Dice(self, self.screen)

        self.walls = []
        self.area = []

        self.clock = pygame.time.Clock()  # vidicemo kad ce mi ovo trebati

        # naslov i ikona
        pygame.display.set_caption("PacUdo")
        icon = pygame.image.load('icon.png')
        pygame.display.set_icon(icon)

        self.load()

    def run(self):
        while self.running:
            if self.state == 'start':
                self.start_menu()

            elif self.state == 'select':
                self.select_draw()
                self.select_events()
            elif self.state == 'playing':
                self.playing_events()
                self.playing_draw(self.num_of_play)
                self.playing_update()

                self.throw_dice()

                self.dice.draw_dice()

            elif self.state == 'rules':
                self.rules_events()
                self.rules_draw()
            else:
                self.running = False

        pygame.quit()

################################## BASIC FUNCTIONS ################################
    def draw_text(self, text, screen, position, text_size, color, font_name, centered=False):
        font = pygame.font.SysFont(font_name, text_size)
        text1 = font.render(text, True, color)

        # true ode u render funkciji znaci da tekst ima glatke rubove
        size = text1.get_size()
        if centered:
            position[0] = position[0] - size[0] / 2
            position[1] = position[1] - size[1] / 2
            # triba oduzimat taman pola da bude tekst tocno na sredini, da toga nema bilo bi na sredini samo prvo slovo
        screen.blit(text1, position)

    def load(self):
        self.background = pygame.image.load('maze.png')
        self.background = pygame.transform.scale(self.background, (WIDTH, HEIGHT))

        # otvaranje walls.txt i stvaranje liste za zidove s koordinatama za zidove
        # svaka linija je y_id-prva je 0, druga je 1 itd..

        with open("walls.txt", 'r') as file:
            for y_id, line in enumerate(file):
                for x_id, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x_id, y_id))
                    elif char == "0":
                        self.area.append(vec(x_id, y_id))

        #print(self.walls)

        #crtamo grid radi odredivanja pozicija i usporedbe sa zidon

    def draw_grid(self):
        for x in range(WIDTH // self.cell_width):
            pygame.draw.line(self.background, grey, (x * self.cell_width, 0), (x * self.cell_width, HEIGHT))
        for x in range(HEIGHT // self.cell_height):
            pygame.draw.line(self.background, grey, (0, x * self.cell_height), (WIDTH, x * self.cell_height))

        # napravit prema listi self.walls tamo di je zid da ga oboja u bilo da
        # nan je lakse vidit jel nan radi otvaranje i citanje znakova

        #for area in self.area:
         #   pygame.draw.rect(self.background, white,
         #                    (area.x * self.cell_width, area.y * self.cell_height,
         #                     self.cell_width, self.cell_height))

    ############################ START MENU FUNCTIONS #############################
    def start_menu(self):
        self.screen.fill(black)
        self.draw_text('PacUdo', self.screen, [title[0], title[1]],
                      GAME_NAME_SIZE, yellow, START_FONT, centered=True)
        self.draw_text('Start game', self.screen, [text1pos[0], text1pos[1]],
                       START_TEXT_SIZE, yellow, START_FONT, centered=True)
        self.draw_text('Rules', self.screen, [text2pos[0], text2pos[1]],
                       START_TEXT_SIZE, yellow, START_FONT, centered=True)

        rect1 = pygame.Rect(text1pos[0]-text1pos[0]//3, text1pos[1] - START_TEXT_SIZE / 2, 180, 50)
        rect2 = pygame.Rect(text2pos[0] - 2 * START_TEXT_SIZE + 15, text2pos[1] - START_TEXT_SIZE / 2, 130, 40)
        pygame.draw.rect(self.screen, black, rect1, 1)
        pygame.draw.rect(self.screen, black, rect2, 1)

        mouse_x, mouse_y = pygame.mouse.get_pos()

        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if rect1.collidepoint((mouse_x, mouse_y)):
            if click:
                self.state = 'select'

        if rect2.collidepoint((mouse_x, mouse_y)):
            if click:
                self.state = 'rules'

        pygame.display.update()

 ############################## SELECT FUNCTIONS ##########################
    def select_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = 'start'
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

    def select_draw(self):

        self.screen.fill(black)
        self.draw_text("Select number of players:", self.screen, [WIDTH//2, 100], START_TEXT_SIZE, yellow, START_FONT, centered=True)

        self.draw_text("2", self.screen, [WIDTH//2, 200], START_TEXT_SIZE, yellow, START_FONT, centered=True)
        self.draw_text("3", self.screen, [WIDTH // 2, 270], START_TEXT_SIZE, yellow, START_FONT, centered=True)
        self.draw_text("4", self.screen, [WIDTH // 2, 340], START_TEXT_SIZE, yellow, START_FONT, centered=True)

        rect1 = pygame.Rect(WIDTH//2-START_TEXT_SIZE//2, 200-20, START_TEXT_SIZE, START_TEXT_SIZE)
        rect2 = pygame.Rect(WIDTH // 2-START_TEXT_SIZE//2, 270-20, START_TEXT_SIZE, START_TEXT_SIZE)
        rect3 = pygame.Rect(WIDTH // 2-START_TEXT_SIZE//2, 340-20, START_TEXT_SIZE, START_TEXT_SIZE)

        pygame.draw.rect(self.screen, black, rect1, 1)
        pygame.draw.rect(self.screen, black, rect2, 1)
        pygame.draw.rect(self.screen, black, rect3, 1)

        mouse_x, mouse_y = pygame.mouse.get_pos()
        click = False
        for event in pygame.event.get():
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
        if click:
            if rect1.collidepoint((mouse_x, mouse_y)):
                self.num_of_play = 2

            if rect2.collidepoint((mouse_x, mouse_y)):
                self.num_of_play = 3

            if rect3.collidepoint((mouse_x, mouse_y)):
                self.num_of_play = 4

        if self.num_of_play > 1:
            self.state = 'playing'

        pygame.display.update()

    ############################ PLAYING FUNCTIONS #############################
    def playing_events(self):
        for event in pygame.event.get():
            click = False
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.running = False

            #ova funckija mi reagira na klik na kocku
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True
                    self.dice_mouse_clicked(pygame.mouse.get_pos(), click)
                    #print("klik na kocku")

            #distance1 = math.sqrt((math.pow(self.player1.pix_pos[0] - self.winning_pos_red[0], 2)) + (math.pow(self.player1.pix_pos[1] - self.winning_pos_red[1], 2)))
            #distance2 = math.sqrt((math.pow(self.player2.pix_pos[0] - self.winning_pos_green[0], 2)) + (math.pow(self.player2.pix_pos[1] - self.winning_pos_green[1], 2)))
            #distance3 = math.sqrt((math.pow(self.player3.pix_pos[0] - self.winning_pos_blue[0], 2)) + (math.pow(self.player3.pix_pos[1] - self.winning_pos_blue[1], 2)))
            #distance4 = math.sqrt((math.pow(self.player4.pix_pos[0] - self.winning_pos_yellow[0], 2)) + (math.pow(self.player4.pix_pos[1] - self.winning_pos_yellow[1], 2)))

            #print(distance1)#, distance2, distance3, distance4)
            distance1 = False
            distance2 = False
            distance3 = False
            distance4 = False

            if self.player1.grid_pos[0]+1 == self.grid_pos_red[0] and self.player1.grid_pos[1]+1 == self.grid_pos_red[1]:
                distance1 = True
            if self.player2.grid_pos[0]+1 == self.grid_pos_green[0] and self.player2.grid_pos[1]+1 == self.grid_pos_green[1]:
                distance2 = True
            if self.player3.grid_pos[0]+1 == self.grid_pos_blue[0] and self.player3.grid_pos[1]+1 == self.grid_pos_blue[1]:
                distance3 = True
            if self.player4.grid_pos[0]+1 == self.grid_pos_yellow[0] and self.player4.grid_pos[1]+1 == self.grid_pos_yellow[1]:
                distance4 = True

            if len(self.def_players):
                if not distance1 and not distance2 and not distance3 and not distance4:
                    if self.dice.completed_roll:
################################ red ############################
                        if self.def_players[self.current_playing] == red:
                            if self.count < self.dice.dice_num:
                                if event.type == KEYDOWN:
                                    if event.key == K_RIGHT:
                                        self.count += 1
                                        self.player1.player_img1 = pygame.image.load('players//player1-right.png')
                                        self.player1.move(vec(1, 0))

                                    if event.key == K_LEFT:
                                        self.count += 1
                                        self.player1.player_img1 = pygame.image.load('players//player1-left.png')
                                        self.player1.move(vec(-1, 0))

                                    if event.key == K_UP:
                                        self.count += 1
                                        self.player1.player_img1 = pygame.image.load('players//player1-up.png')
                                        self.player1.move(vec(0, -1))

                                    if event.key == K_DOWN:
                                        self.count += 1
                                        self.player1.player_img1 = pygame.image.load('players//player1-down.png')
                                        self.player1.move(vec(0, 1))

                                self.check_collision(self.player1, self.player2, self.player3, self.player4)

                            elif self.dice.double_roll:
                                self.dice.completed_roll = False
                                self.count = 0

                            else:
                                self.next_player()


#################################### green ###########################

                        if self.def_players[self.current_playing] == green:
                            if self.count < self.dice.dice_num:
                                if event.type == KEYDOWN:
                                    if event.key == K_RIGHT:
                                        self.count += 1
                                        self.player2.player_img2 = pygame.image.load('players//player2-right.png')
                                        self.player2.move(vec(1, 0))

                                    # print(self.count)
                                    if event.key == K_LEFT:
                                        self.count += 1
                                        self.player2.player_img2 = pygame.image.load('players//player2-left.png')
                                        self.player2.move(vec(-1, 0))

                                    if event.key == K_UP:
                                        self.count += 1
                                        self.player2.player_img2 = pygame.image.load('players//player2-up.png')
                                        self.player2.move(vec(0, -1))

                                    if event.key == K_DOWN:
                                        self.count += 1
                                        self.player2.player_img2 = pygame.image.load('players//player2-down.png')
                                        self.player2.move(vec(0, 1))

                                self.check_collision(self.player2, self.player1, self.player3, self.player4)

                            elif self.dice.double_roll:
                                self.dice.completed_roll = False
                                self.count = 0

                            else:
                                self.next_player()


####################################### blue ###############################

                        if self.def_players[self.current_playing] == blue:
                            if self.count < self.dice.dice_num:
                                if event.type == KEYDOWN:
                                    if event.key == K_RIGHT:
                                        self.count += 1
                                        self.player3.player_img3 = pygame.image.load('players//player3-right.png')
                                        self.player3.move(vec(1, 0))

                                    # print(self.count)
                                    if event.key == K_LEFT:
                                        self.count += 1
                                        self.player3.player_img3 = pygame.image.load('players//player3-left.png')
                                        self.player3.move(vec(-1, 0))

                                    if event.key == K_UP:
                                        self.count += 1
                                        self.player3.player_img3 = pygame.image.load('players//player3-up.png')
                                        self.player3.move(vec(0, -1))

                                    if event.key == K_DOWN:
                                        self.count += 1
                                        self.player3.player_img3 = pygame.image.load('players//player3-down.png')
                                        self.player3.move(vec(0, 1))

                                self.check_collision(self.player3, self.player1, self.player2, self.player4)

                            elif self.dice.double_roll:
                                self.dice.completed_roll = False
                                self.count = 0

                            else:
                                self.next_player()

############################yellow ##################################

                        if self.def_players[self.current_playing] == yellow:
                            if self.count < self.dice.dice_num:
                                if event.type == KEYDOWN:
                                    if event.key == K_RIGHT:
                                        self.count += 1
                                        self.player4.player_img4 = pygame.image.load('players//player4-right.png')
                                        self.player4.move(vec(1, 0))

                                    # print(self.count)
                                    if event.key == K_LEFT:
                                        self.count += 1
                                        self.player4.player_img4 = pygame.image.load('players//player4-left.png')
                                        self.player4.move(vec(-1, 0))

                                    if event.key == K_UP:
                                        self.count += 1
                                        self.player4.player_img4 = pygame.image.load('players//player4-up.png')
                                        self.player4.move(vec(0, -1))

                                    if event.key == K_DOWN:
                                        self.count += 1
                                        self.player4.player_img4 = pygame.image.load('players//player4-down.png')
                                        self.player4.move(vec(0, 1))

                                self.check_collision(self.player4, self.player1, self.player2, self.player3)

                            elif self.dice.double_roll:
                                self.dice.completed_roll = False
                                self.count = 0

                            else:
                                self.next_player()
                else:
                    self.draw_text("Game Over! The winner is this color!",
                                   self.background, [WIDTH // 2, HEIGHT // 2], 30,
                                   self.def_players[self.current_playing],
                                   START_FONT, centered=True)

    def playing_draw(self, num_of_play):
        # kod ove funckcije se sve ka non stop crta
        # jer se ka non stop radi ovaj display update
        self.screen.fill(black)

        self.screen.blit(self.background, (0, 0))

        #preko onog zida u sredini crtan crni pravokutnik da se ne vide njegovi
        # plavi zidovi, a u walls.txt prominila iz 1 u 0 da ga ne gleda ko zid
        pygame.draw.rect(self.background, black, (WIDTH//2+2*self.cell_width, HEIGHT//2+self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2+3*self.cell_width, HEIGHT//2-self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2+3*self.cell_width, HEIGHT//2-5*self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2+2*self.cell_width, HEIGHT//2-7*self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2-3*self.cell_width, HEIGHT//2-7*self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2-4*self.cell_width, HEIGHT//2-5*self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2-4*self.cell_width, HEIGHT//2-self.cell_height//2, self.cell_width, self.cell_height),0)
        pygame.draw.rect(self.background, black, (WIDTH//2-3*self.cell_width, HEIGHT//2+self.cell_height//2, self.cell_width, self.cell_height),0)

        #self.draw_grid()
        self.draw_area()

        #pozicije igraca za pobjedu u pox_posu
        self.winning_pos_red = (WIDTH//2-3*self.cell_width//2, HEIGHT//2-self.cell_height)
        self.winning_pos_green = (WIDTH//2+self.cell_width//2, HEIGHT//2-self.cell_height)
        self.winning_pos_blue = (WIDTH//2+3*self.cell_width//2, HEIGHT//2-self.cell_height)
        self.winning_pos_yellow = (WIDTH//2-self.cell_width//2, HEIGHT//2-self.cell_height)

        self.grid_pos_red = ((self.winning_pos_red[0] + self.cell_width//2)//self.cell_width, (self.winning_pos_red[1] + self.cell_height // 2) // self.cell_height)
        self.grid_pos_green = ((self.winning_pos_green[0] + self.cell_width//2)//self.cell_width, (self.winning_pos_green[1] + self.cell_height // 2) // self.cell_height)
        self.grid_pos_blue = ((self.winning_pos_blue[0] + self.cell_width//2)//self.cell_width, (self.winning_pos_blue[1] + self.cell_height // 2) // self.cell_height)
        self.grid_pos_yellow = ((self.winning_pos_yellow[0] + self.cell_width//2)//self.cell_width, (self.winning_pos_yellow[1] + self.cell_height // 2) // self.cell_height)

        #sredisnja mjesta, tj cilj igraca
        pygame.draw.circle(self.background, red, self.winning_pos_red, 10, 0)
        pygame.draw.circle(self.background, green, self.winning_pos_green, 10, 0)
        pygame.draw.circle(self.background, yellow, self.winning_pos_yellow, 10, 0)
        pygame.draw.circle(self.background, blue, self.winning_pos_blue, 10, 0)



        if num_of_play > 1:
            num = num_of_play

            if num == 2:
                self.player1.draw()
                self.player2.draw()
                self.def_players = [self.player1.color, self.player2.color]

            if num == 3:
                self.player1.draw()
                self.player2.draw()
                self.player3.draw()
                self.def_players = [self.player1.color, self.player2.color, self.player3.color]

            if num == 4:
                self.player1.draw()
                self.player2.draw()
                self.player3.draw()
                self.player4.draw()
                self.def_players = [self.player1.color, self.player2.color, self.player3.color, self.player4.color]

        pygame.display.update()

    def draw_area(self):
        for area in self.area:
            pygame.draw.circle(self.background, white,
                               (int(area.x * self.cell_width) + self.cell_width // 2,
                                int(area.y * self.cell_height) + self.cell_height // 2), 7)

    def playing_update(self):
        None

    # da provjeri jel prisa priko njega
    def check_collision(self, playing, other1, other2, other3):
        if (playing.grid_pos[0] == other1.grid_pos[0]) and (playing.grid_pos[1] == other1.grid_pos[1]):
            other1.reset_player()
        if (playing.grid_pos[0] == other2.grid_pos[0]) and (playing.grid_pos[1] == other2.grid_pos[1]):
            other2.reset_player()
        if (playing.grid_pos[0] == other3.grid_pos[0]) and (playing.grid_pos[1] == other3.grid_pos[1]):
            other3.reset_player()

    # za iduceg igraca
    def next_player(self):
        self.move_unit = False
        if self.current_playing == len(self.def_players) - 1:
            self.current_playing = 0
        else:
            self.current_playing += 1
        self.dice.completed_roll = False
        self.dice.double_roll = False
        self.count = 0

    # show static or roll dice
    def throw_dice(self):
        current_team = self.def_players[self.current_playing]
        if not self.dice.completed_roll and not self.dice.roll:  # if not rolling or have rolled
            self.dice.show_static_dice(current_team)
        elif self.dice.roll:
            self.dice.roll_animation(current_team)

    def dice_mouse_clicked(self, mouse_pos, clicked):
        if not self.dice.completed_roll and not self.dice.roll:
            if self.dice.dice_pos.collidepoint(mouse_pos):
                if clicked:
                    self.dice.start_roll()

    ############################ RULES FUNCTIONS #############################
    def rules_events(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.running = False
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    self.state = 'start'


    def rules_draw(self):
        self.screen.fill(black)
        self.draw_text('GAME RULES', self.screen, [title[0], title[1]],
                       START_TEXT_SIZE, yellow, START_FONT, centered=True)
        self.draw_text('This game is a combination of two games, Pacman and Ludo!', self.screen,
                       [title[0], title[1] + 70], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('There can be 2, 3 and 4 players and all players are human.', self.screen,
                       [title[0], title[1] + 100], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('You select the number of players after pressing START GAME.',
                       self.screen, [title[0], title[1] + 130], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('The Ludo side of the game is a dice and moves are',
                        self.screen, [title[0], title[1] + 160], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('limited by the number the dice gives you.', self.screen, [title[0], title[1] + 190], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('The Pacman side is that you can move in any direction.',
                       self.screen, [title[0], title[1] + 220], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('The winner is the one that comes first to his color in', self.screen,
                       [title[0], title[1] + 280], START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('the center of the maze. I hope you will enjoy it! Good luck!', self.screen, [title[0], title[1] + 310],
                       START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)
        self.draw_text('To return to Main Menu, press ESC!', self.screen, [title[0], title[1] + 370],
                       START_TEXT_SIZE // 2, yellow, START_FONT, centered=True)

        pygame.display.update()
