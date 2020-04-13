#Tom Jarman 20/10/2016
#Challenge 12.3
#SPACE INVADERS!

import pygame
from pygame.locals import *
import sys
import time

class Game(object):
    """ An object that represents the game """

    #Fps
    FPS = 60
    #Colours
    BLACK = (0,0,0)
    WHITE = (255,255,255)
    GREEN = (0,255,0)
    RED = (255,0,0)
    #Coordinates x
    LEFTTEXT = 60
    CENTERTEXT = 310
    RIGHTTEXT = 580
    #Coordinates Y
    TOPTEXT = 40
    MIDHIGHTEXT = 140
    MIDLOWTEXT = 240
    BOTTEXT = 670
    #fonts
    QUARTZ = "C:\\Windows\\Fonts\\calibri.ttf"
    SIZE = 20

    def __init__(self):
        """ Initializes the game """
        pygame.init()
        self.DISPLAYSURFACE = pygame.display.set_mode((640, 700))
        pygame.display.set_caption("Space Invaders")
        icon = pygame.image.load("Icon.png")
        pygame.display.set_icon(icon)
        self.FPSCLOCK = pygame.time.Clock()
        self.game_stage = "intro"
        self.direction = None
        self.main()

    def main(self):
        """ Game's mainloop """
        while True:
            self.check_quit()

            if self.game_stage == "intro":
                self.title()
                self.base_surface = self.DISPLAYSURFACE.copy() #surface with titles
                for i in range(14):
                    self.DISPLAYSURFACE.blit(self.base_surface,(0,0))
                    self.intro_animation(13-i)
                    pygame.display.update()
                    self.FPSCLOCK.tick(Game.FPS/4)
                self.score_table()
                self.DISPLAYSURFACE.blit(self.base_surface_2,(0,0))
                self.high_score = str(self.check_high_score())
                self.player1_score = str(0)
                self.player2_score = str(0)
                self.game_stage = "choose_player"
                self.invaders_destroyed_objects = []

            elif self.game_stage == "choose_player":
                self.choose_player()
                for event in pygame.event.get(KEYDOWN):
                    if event.key == K_1:
                        self.player = "1"
                        self.game_stage = "start_game"
                    elif event.key == K_2:
                        self.player = "2"
                        self.game_stage = "start_game"

            elif self.game_stage == "start_game":
                self.DISPLAYSURFACE.blit(self.base_surface_2,(0,0))
                self.ship_image = pygame.transform.scale(pygame.image.load("defender.png"), (42,24))
                self.ship_x = self.DISPLAYSURFACE.get_width() / 2 - 21
                self.SHIP_Y = self.DISPLAYSURFACE.get_height() - 75
                self.invader_x = 50
                direction = "right"
                missile_counter = 0
                invader_counter = 0
                invader_type = 0
                y_mod = 0
                self.shelter_on_screen = []
                self.missile_list = []
                self.invaders_list = [" "]
                self.invaders_destroyed = []
                self.create_shelter()
                self.game_stage = "main"

            elif self.game_stage == "main":

                if len(self.invaders_list) > 0:
                    self.DISPLAYSURFACE.fill(Game.BLACK)
                    self.draw_invaders(invader_type,y_mod)
                    self.draw_scores()
                    self.update_missiles()
                    self.DISPLAYSURFACE.blit(self.ship_image, (self.ship_x, self.SHIP_Y))
                    self.draw_shelter(self.shelter_list)
                    missile_counter += 1
                    invader_counter += 1

                    for event in pygame.event.get():
                        if event.type == KEYUP and (event.key == K_RIGHT or event.key == K_LEFT):
                            self.direction = None
                        elif event.type == KEYDOWN and (event.key == K_RIGHT or event.key == K_LEFT):
                            if not self.direction:
                                self.direction = event.key
                            elif self.direction:
                                pygame.event.post(event)
                        elif event.type == KEYDOWN and event.key == K_SPACE and missile_counter > 15:
                            missile = Missile(self)
                            self.missile_list.append(missile)
                            missile_counter = 0

                    if invader_counter % (56-len(self.invaders_destroyed))== 0:
                        invader_type = (invader_counter % 60)//30
                        for invader in self.invaders_list[len(self.invaders_list)-1]:
                            if invader.x >= self.DISPLAYSURFACE.get_width() - 20:
                                direction = "left"
                                y_mod -= 5
                        for invader in self.invaders_list[0]:
                            if invader.x <= 0:
                                direction = "right"
                                y_mod -= 5
                        if direction == "right":
                            self.invader_x += 10
                        elif direction == "left":
                            self.invader_x -= 10

                    if self.direction == K_RIGHT:
                        if (self.ship_x + 43) < self.DISPLAYSURFACE.get_width():
                            self.ship_x += 2
                    
                    elif self.direction == K_LEFT:
                        if (self.ship_x - 2) > 0:
                            self.ship_x -= 2

                elif len(self.invaders_list) == 0:
                    self.game_over("win")
                    self.game_stage = "waiting"

                if self.check_landed():
                    self.game_over("lose")
                    self.game_stage = "waiting"

            elif self.game_stage == "waiting":
                if pygame.event.get(KEYUP):
                    self.game_stage = "choose_player"
                    self.DISPLAYSURFACE.blit(self.base_surface_2,(0,0))
                    self.choose_player()

            pygame.display.update()
            self.FPSCLOCK.tick(Game.FPS)
            
    def check_quit(self):
        """ Safely quits the pygame window and end the program """
        if pygame.event.get(QUIT):
            pygame.display.quit()
            sys.exit()

    def create_text(self,file,size,list,colour_1,colour_2,display_surface):
        """ Creates text and adds it to the screen """
        fontobj = pygame.font.Font(file,size)
        textobj = fontobj.render(list[0], 1, colour_1, colour_2)
        rect_obj = textobj.get_rect()
        rect_obj.center = list[1]
        display_surface.blit(textobj, rect_obj)

    def title(self):
        """ Displays the opening message """
        intro_text = [["Score<1>",(Game.LEFTTEXT,Game.TOPTEXT),Game.WHITE],["HI-SCORE",(Game.CENTERTEXT,Game.TOPTEXT),Game.WHITE],["SCORE<2>",(Game.RIGHTTEXT,Game.TOPTEXT),Game.WHITE],
                      ["0000",(Game.LEFTTEXT-10,Game.TOPTEXT+40),Game.WHITE],["0000",(Game.CENTERTEXT,Game.TOPTEXT+40),Game.WHITE],["0000",(Game.RIGHTTEXT-10,Game.TOPTEXT+40),Game.WHITE],
                      ["CREDIT",(Game.CENTERTEXT+((Game.RIGHTTEXT - Game.CENTERTEXT)/2),Game.BOTTEXT),Game.WHITE],["00",(Game.RIGHTTEXT-20, Game.BOTTEXT),Game.WHITE],
                      ["THE SPACE INVADERS",(Game.CENTERTEXT,Game.MIDHIGHTEXT),Game.RED], ["PRESENTS",(Game.CENTERTEXT,Game.MIDHIGHTEXT + 40),Game.WHITE],
                      ["PART FOUR",(Game.CENTERTEXT,Game.MIDHIGHTEXT + 80),Game.WHITE]]
        for element in intro_text:
                self.create_text(Game.QUARTZ,Game.SIZE,element,element[2],Game.BLACK,self.DISPLAYSURFACE)
                if element == intro_text[7]:
                    self.base_surface_2 = self.DISPLAYSURFACE.copy() #surface with scores

    def intro_animation(self, invaders):
        """ Into text reveal animation """
        for i in range(invaders):
            title_invader = pygame.image.load("tier3_1.png")
            self.DISPLAYSURFACE.blit(title_invader,(170+(14-i)*16, Game.MIDHIGHTEXT+72))

    def score_table(self):
        """ Displays the point values for the different targets """
        score_text = [["*SCORE ADVANCE TABLE*", (Game.CENTERTEXT-100,Game.MIDLOWTEXT), Game.WHITE],["= ? MYSTERY",(Game.CENTERTEXT - 40, Game.MIDLOWTEXT + 20), Game.WHITE],
                      ["= 30  POINTS", (Game.CENTERTEXT - 40, Game.MIDLOWTEXT + 40), Game.WHITE],["= 20  POINTS", (Game.CENTERTEXT - 40, Game.MIDLOWTEXT + 60), Game.WHITE],
                      ["= 10  POINTS", (Game.CENTERTEXT - 40, Game.MIDLOWTEXT + 80), Game.GREEN]]
        score_image = [["ufo.png",(Game.CENTERTEXT - 90, Game.MIDLOWTEXT + 16)],["tier3_1.png",(Game.CENTERTEXT - 85, Game.MIDLOWTEXT + 35)],["tier2_1.png",(Game.CENTERTEXT - 90, Game.MIDLOWTEXT + 55)],
                       ["tier1_2_green.png",(Game.CENTERTEXT - 90, Game.MIDLOWTEXT + 75)]]
        for i in range(len(score_text)):
            letter_list = []
            on_screen = False                
            for j in range(len(score_text[i][0])):
                letter_list.append([score_text[i][0][j], (score_text[i][1][0]+j*10,score_text[i][1][1])])  
                self.create_text(Game.QUARTZ, Game.SIZE, letter_list[len(letter_list)-1], score_text[i][2], Game.BLACK, self.DISPLAYSURFACE)
                pygame.display.update()
                time.sleep(0.07)
            if on_screen == False and i < len(score_text)-1:
                score_icon = pygame.image.load(score_image[i][0])
                self.DISPLAYSURFACE.blit(score_icon, score_image[i][1])
                on_screen = True
        time.sleep(1)

    def choose_player(self):
        """ Waits for user to chose which player to use """
        player_text = [["PUSH",(Game.CENTERTEXT, Game.MIDHIGHTEXT)], ["1 OR 2 PLAYERS BUTTON", (Game.CENTERTEXT, Game.MIDHIGHTEXT + 20)]]
        for text in player_text:
            self.create_text(Game.QUARTZ, Game.SIZE, text, Game.WHITE, Game.BLACK, self.DISPLAYSURFACE)

    def draw_invaders(self,picture,y_mod):
        """ Creates all of the sprites present at the game start """
        self.invaders_list = []
        self.invaders_rect_list = []
        self.explosion_list = []
        for i in range(11):
            tier_1_1 = Invader("tier1_1.png","tier1_2.png",self.invader_x+(i*50),self.DISPLAYSURFACE.get_height()/2-40-y_mod,self,"tier1",picture)
            tier_2_1 = Invader("tier2_1.png","tier2_2.png",self.invader_x+(i*50),self.DISPLAYSURFACE.get_height()/2-80-y_mod,self,"tier2",picture)
            tier_1_2 = Invader("tier1_1.png","tier1_2.png",self.invader_x+(i*50),self.DISPLAYSURFACE.get_height()/2-60-y_mod,self,"tier1",picture)
            tier_2_2 = Invader("tier2_1.png","tier2_2.png",self.invader_x+(i*50),self.DISPLAYSURFACE.get_height()/2-100-y_mod,self,"tier2",picture)
            tier_3 = Invader("tier3_1.png","tier3_2.png",self.invader_x+(i*50)+4,self.DISPLAYSURFACE.get_height()/2-120-y_mod,self,"tier3",picture)
            column = [tier_3,tier_2_1,tier_2_2,tier_1_1,tier_1_2]
            self.invaders_list.append(column)
            column_rect = []
            for invader in column:
                invader_rect_obj = invader.image.get_rect()
                if invader.type == "tier3":
                    invader_rect = pygame.draw.rect(self.DISPLAYSURFACE,Game.BLACK,(invader.x,invader.y,16,15))
                else:
                    invader_rect = pygame.draw.rect(self.DISPLAYSURFACE,Game.BLACK,(invader.x,invader.y,25,15))
                
                column_rect.append(invader_rect)
            self.invaders_rect_list.append(column_rect)
        for index in self.invaders_destroyed:
            old_invader = self.invaders_list[index[0]].pop(index[1])
            self.invaders_rect_list[index[0]].pop(index[1])
            if index[2] > 0:
                explosion = Invader("explosion.png","explosion.png",old_invader.x,old_invader.y,self,old_invader.type,picture)
                index[2] -= 1
                self.explosion_list.append(explosion)
            self.invaders_destroyed_objects.append(old_invader)
        temp = self.invaders_list
        self.invaders_list = []
        for column_list in temp:
            if len(column_list) > 0:
                self.invaders_list.append(column_list)
        for column_list in self.invaders_list:
            for invader in column_list:
                invader.add()
        for exp in self.explosion_list:
            exp.add()

    def create_shelter(self):
        """ Creates the shelters """
        self.shelter_top = pygame.transform.scale(pygame.image.load("cover.png"),(72,36))
        self.shelter_list = []
        for i in range(4):
            left = (self.DISPLAYSURFACE,Game.GREEN,((i*150)+66, self.DISPLAYSURFACE.get_height() - 163, 12, 24),"left")
            right = (self.DISPLAYSURFACE,Game.GREEN,((i*150)+126, self.DISPLAYSURFACE.get_height() - 163, 12, 24),"right")
            self.shelter_list.append(left)
            self.shelter_list.append(right)
            top = (self.DISPLAYSURFACE,Game.BLACK,((i*150)+66, self.DISPLAYSURFACE.get_height() - 199,72,36),"top")          
            self.shelter_list.append(top)

    def draw_shelter(self,shelter_list):
        """ Draws the shelters """
        self.shelter_on_screen = []
        for shelter in shelter_list:
            draw = pygame.draw.rect(shelter[0],shelter[1],shelter[2])
            if shelter[3] == "top":
                self.DISPLAYSURFACE.blit(self.shelter_top,(shelter[2]))
            self.shelter_on_screen.append(draw)
            
    def update_missiles(self):
        """ Updates the y coordinate of the missiles """
        for missile in self.missile_list:
            if missile.check_collide("shelter"):
                self.shelter_list.remove(missile.check_collide("shelter"))
            if missile.check_collide("invader"):
                self.invaders_destroyed.append(missile.check_collide("invader"))
            missile.update()

    def draw_scores(self):
        """ Draws the score text to the screen """
        self.update_scores()
        label_text = [["Score<1>",(Game.LEFTTEXT,Game.TOPTEXT),Game.WHITE],["HI-SCORE",(Game.CENTERTEXT,Game.TOPTEXT),Game.WHITE],["SCORE<2>",(Game.RIGHTTEXT,Game.TOPTEXT),Game.WHITE],
                      [self.player1_score,(Game.LEFTTEXT-10,Game.TOPTEXT+40),Game.WHITE],[self.high_score,(Game.CENTERTEXT,Game.TOPTEXT+40),Game.WHITE],
                      [self.player2_score,(Game.RIGHTTEXT-10,Game.TOPTEXT+40),Game.WHITE],["CREDIT",(Game.CENTERTEXT+((Game.RIGHTTEXT - Game.CENTERTEXT)/2),Game.BOTTEXT),Game.WHITE],
                      ["00",(Game.RIGHTTEXT-20, Game.BOTTEXT),Game.WHITE]]
        for label in label_text:
            self.create_text(Game.QUARTZ,Game.SIZE,label,label[2],Game.BLACK,self.DISPLAYSURFACE)

    def check_landed(self):
        """ Checks if the invaders have landed """
        for invaders in self.invaders_list:
            for invader in invaders:
                if invader.y >= self.DISPLAYSURFACE.get_height() - 100:
                    time.sleep(2)
                    return True
            return False

    def game_over(self,mode):
        """ End game message """
        self.DISPLAYSURFACE.fill(Game.BLACK)
        if mode == "win":
            text = [["WELL DONE EARTHLING",(Game.CENTERTEXT-51,Game.MIDHIGHTEXT),Game.RED],["THIS TIME YOU WIN",(Game.CENTERTEXT-50,Game.MIDHIGHTEXT+80),Game.WHITE],
                    ["Press any key to restart",(Game.CENTERTEXT-107,Game.MIDLOWTEXT+20),Game.WHITE]]
        elif mode == "lose":
            text = [["YOU LOSE BAD LUCK",(Game.CENTERTEXT-44,Game.MIDHIGHTEXT),Game.RED],["Press any key to restart",(Game.CENTERTEXT-50,Game.MIDLOWTEXT),Game.WHITE]]
        for sentance in text:
            for i in range(len(sentance[0])):
                self.create_text(Game.QUARTZ,Game.SIZE,[sentance[0][i],(sentance[1][0]+i*10,sentance[1][1]),sentance[2]],Game.RED,Game.BLACK,self.DISPLAYSURFACE)
                pygame.display.update()
                time.sleep(0.07)
        self.game_stage = "waiting"

    def check_high_score(self):
        """ Checks the high score stored in the accomanpying text file """
        f = open("highscores.txt","r")
        highscore = f.readline()
        f.close()
        return highscore

    def update_scores(self):
        """ Updates the score attributes """
        types = [["tier1",10],["tier2",20],["tier3",30]]
        score = 0
        for invader in self.invaders_destroyed_objects:
            for type in types:
                if invader.type == type[0]:
                    score += type[1]
        self.invaders_destroyed_objects = []
        if self.player == "1":
            self.player1_score = str(score)
        elif self.player == "2":
            self.player2_score = str(score)      

class Invader(object):
    """ An object that represents each space invader """
    def __init__(self, image, image_2, x, y,game_ref,type,image_type):
        """ Sets up the invader """
        images = [image,image_2]
        self.type = type
        self.game_ref = game_ref
        self.image = pygame.image.load(images[image_type])
        self.x = x
        self.y = y

    def add(self):
        """ Adds the invader to the screen """
        self.game_ref.DISPLAYSURFACE.blit(self.image,(self.x,self.y))

class Missile(object):
    """ An object that represents a missile """
    def __init__(self, game_ref):
        """ Blits the missile """
        self.game_ref = game_ref
        self.X = self.game_ref.ship_x+20
        self.y = self.game_ref.SHIP_Y-14
        self.height = 14
        self.rect = pygame.draw.rect(self.game_ref.DISPLAYSURFACE, Game.WHITE,(self.X,self.y,4,self.height))
        self.game_ref.missile_list.append(self)
    def update(self):
        """ Updates the missile's position each loop of the main loop """
        self.y -= 4
        self.rect = pygame.draw.rect(self.game_ref.DISPLAYSURFACE, Game.WHITE,(self.X,self.y,4,self.height))
        if self.y < 0 or self.height < 0:
            self.game_ref.missile_list.remove(self)
    def check_collide(self,mode):
        """ Returns the rectangle missile has collided with """
        if mode == "shelter":
            for i in range(len(self.game_ref.shelter_list)):
                if pygame.Rect.colliderect(self.rect,self.game_ref.shelter_on_screen[i]):
                    self.game_ref.missile_list.remove(self)
                    return self.game_ref.shelter_list[i]
        else:
            for i in range(len(self.game_ref.invaders_rect_list)):
                for j in range(len(self.game_ref.invaders_rect_list[i])):
                    if pygame.Rect.colliderect(self.rect,self.game_ref.invaders_rect_list[i][j]):
                        self.game_ref.missile_list.remove(self)
                        return [i,j,6]

def main():
    """ Main function """
    game = Game()
main()
