# content from kids can code: http://kidscancode.org/blog/
#Sources Andrew
# import libraries and modules
# from platform import platform
import pygame as pg
from pygame.sprite import Sprite
import random
from random import randint

# goal- survive as long as possible, score goes up 1 every 15 frames
# rules- mob hit = -1 to health
# feedback- score and health displayed at top of screen, You lose indicater once health = 0

vec = pg.math.Vector2

# game settings 
WIDTH = 1400
HEIGHT = 900
FPS = 30
FRAME = 1
SCORE = 0

# affects on the player(player settings)
PLAYER_FRIC = -0.2
PLAYER_GRAV = .98
HEALTH = 10

# colors(RGB values)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
# getting text to show on the screen in arial font
def draw_text(text, size, color, x, y):
        font_name = pg.font.match_font('Times New Roman')
        font = pg.font.Font(font_name, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect()
        text_rect.midtop = (x, y)
        screen.blit(text_surface, text_rect)

# Player Class
class Player(Sprite):
    def __init__(self):
        Sprite.__init__(self)
        self.image = pg.Surface((32, 32))
        self.image.fill(BLUE)
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH/2, HEIGHT/2)
        self.pos = vec(WIDTH/2, HEIGHT/2)
        self.vel = vec(0,0)
        self.acc = vec(0,0)
        self.hitx = 0
        self.hity = 0
        self.colliding = False
# controles that allow the Player to move across the x and y planes
    def controls(self):
        keys = pg.key.get_pressed()
        if keys[pg.K_a]:
            self.acc.y = 0
            self.acc.x = -5
        if keys[pg.K_d]:
            self.acc.y = 0
            self.acc.x = 5
        if keys[pg.K_w]:
            self.acc.y = -5
        if keys[pg.K_s]:
            self.acc.y = 5
# allows the player to go "through the walls" and appear on the oposite side of the walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.left - self.rect.width/2
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.pos.x = hits[0].rect.right + self.rect.width/2
                self.vel.x = 0
                self.centerx = self.pos.x
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False
    def warp(self):
        if self.pos.x > WIDTH:
            self.pos.x = 0
        if self.pos.x < 0:
            self.pos.x = WIDTH
        if self.pos.y > HEIGHT:
            self.pos.y = 0
        if self.pos.y < 0:
            self.pos.y = HEIGHT
    def update(self):
        self.acc = vec(0,0)
        self.controls()
        self.warp()
        # Friction
        self.rect.center = self.pos

        self.acc += self.vel * PLAYER_FRIC
        self.vel += self.acc
        self.pos += self.vel + 0.5 * self.acc
        self.rect.centerx = self.pos.x
        self.rect.centery = self.pos.y
        self.rect.center = self.pos
        self.hitx = self.hitx
        self.hity = self.hity



# The thing to avoid class
class Enemys(Sprite):
    def __init__(self, x, y, w, h, color):
        Sprite.__init__(self)
        self.image = pg.Surface((w,h))
        self.color = color
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speedx = 5*random.choice([-1,1])
        self.speedy = 5*random.choice([-1,1])
        self.inbounds = True
   # allows the Mobs to bounce off the walls
    def collide_with_walls(self, dir):
        if dir == 'x':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
              
                if hits[0].rect.centerx > self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                if hits[0].rect.centerx < self.rect.centerx and xdiff > ydiff:
                    self.speedx *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False

        if dir == 'y':
            hits = pg.sprite.spritecollide(self, all_platforms, False)
            if hits:
                self.colliding = True
                xdiff = abs(self.rect.centerx - hits[0].rect.centerx)
                ydiff = abs(self.rect.centery - hits[0].rect.centery)
             
                if hits[0].rect.centery > self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                if hits[0].rect.centery < self.rect.centery and xdiff < ydiff:
                    self.speedy *= -1
                self.hitx = hits[0].rect.centerx
                self.hity = hits[0].rect.centery
            else:
                self.colliding = False


    def boundscheck(self):
        if not self.rect.x > 0 or not self.rect.x < WIDTH:
            self.speedx *=-1
        if not self.rect.y > 0 or not self.rect.y < HEIGHT:
            self.speedy *= -1

    def update(self):
        self.boundscheck()
        self.collide_with_walls('x')
        self.collide_with_walls('y')
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        
        

# creates a window
pg.init()
pg.mixer.init()
screen = pg.display.set_mode((WIDTH, HEIGHT))
pg.display.set_caption("My Game...")
clock = pg.time.Clock()
  
# where all sprites are located(Group)
all_sprites = pg.sprite.Group()
all_platforms = pg.sprite.Group()
mobs = pg.sprite.Group()

# instantiate classes
player = Player()


# adds instances to groups
all_sprites.add(player)

#  Number of Mobs spawned
for i in range(30):
    # instantiate mob class repeatedly
    m = Enemys(randint(0, WIDTH), randint(0,HEIGHT), 25, 25, (randint(0,255), randint(0,255) , randint(0,255)))
    all_sprites.add(m)
    mobs.add(m)



running = True
while running:
    dt = clock.tick(FPS)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False
    
    ############ Update ##############
    mobhits = pg.sprite.spritecollide(player, mobs, True)
    if mobhits:
        HEALTH -= 1
    all_sprites.update()
    #makes the score increase over time every 15 frames +1 score 
    if FRAME % 15 == 0:
        SCORE += 1
    
    Health = 8
    Game_Over = Health = 0
    screen.fill(BLACK)
    # draw text(sprites) wanted on the screen with dimentions
    all_sprites.draw(screen)
    if HEALTH > 0:
        draw_text("Health: " + str(HEALTH), 22, GREEN, WIDTH / 2, HEIGHT / 24)
    else:
        draw_text("Health: " + str(HEALTH), 22, BLACK, WIDTH / 2, HEIGHT / 24)
        
    
   #draws text when a requirment is reached. Text apperes on screen when Health gets to 0
    if HEALTH == 0:
        draw_text("YOU LOSE"+ str(),60, RED, WIDTH / 2, HEIGHT / 5) 
        draw_text("Dodge Better Next Time"+ str(), 55, RED, WIDTH / 2, HEIGHT / 4)
    draw_text("Score: " + str(SCORE), 22, GREEN, WIDTH / 2 - 100, HEIGHT / 24)
    pg.display.update()
    pg.display.flip()
    FRAME += 1

pg.quit()