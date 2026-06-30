from pygame import *
from random import *

window = display.set_mode

window = display.set_mode((700, 500))
display.set_caption("shoot")
background = transform.scale(image.load("galaxy.jpg"), (700, 500))

miss = 0
score = 0

class GameSprite(sprite.Sprite):
    def __init__(self, picture, x, y, w, h, speed):
        super().__init__()
        self.image = transform.scale(image.load(picture), (w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.visible = True
    def reset(self):
        if self.visible:
            window.blit(self.image, (self.rect.x, self.rect.y))

class Playersprite(GameSprite):
    def update(self):
        keys_pressed = key.get_pressed()
        if keys_pressed[K_a] and self.rect.x > 1:
            self.rect.x -= self.speed
        if keys_pressed[K_d] and self.rect.x < 650:
            self.rect.x += self.speed
    def fire(self):
         bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, randint(15,25), randint(15,25), randint(-67,-5))
         bullet.add(bullets)
    def firelaser(self):
         laser = Laser('Laser.png', self.rect.centerx-10, self.rect.top, 20, 10000, -1000)
         laser.add(lasers)
class Enemysprite(GameSprite):
    def __init__(self, picture, x, y, w, h, speed):
                super().__init__(picture, x, y, w, h, speed)
                self.active = True
                self.respawn_delay = randint(10,125)
                self.respawn_time = 0
    def update(self):
            global miss
            current_time = time.get_ticks()
            if self.active:
                self.rect.y += self.speed
                if self.rect.y >= 600:
                    miss += 1
                    self.active = False
                    self.respawn_time = current_time
                    self.respawn_delay = randint(10,1250)
                    self.rect.y = -55
                    self.rect.x = randint(0,700)
                    self.rect.w = randint(25,105)
                    self.rect.h = randint(25,105)
                    self.speed = randint(3,9)
            else:
                if current_time - self.respawn_time >= self.respawn_delay:
                     self.active = True
class Bullet(GameSprite):
     def update(self):
          self.rect.y += self.speed
          if self.rect.y < 0:
            self.kill()
class Laser(GameSprite):
     def __init__(self, image, x, y, w, h, speed):
         super().__init__(image, x, y, w, h, speed)
         self.offscreen_time = None
     def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            if self.offscreen_time is None:
                 self.offscreen_time = time.get_ticks()
            if time.get_ticks() - self.offscreen_time >= 2500:
                self.kill()
class Hearttohalf(GameSprite):
    def __init__(self, x, y, w, h):
        sprite.Sprite.__init__(self)
        self.full_heart = transform.scale(image.load("Full Heart.png"), (40,40))
        self.half_heart = transform.scale(image.load("Half_Heart.png"), (40, 40))
        self.image = self.full_heart
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x
        self.visible = True
    def NewState(self, state):
        if state == "full":
            self.image = self.full_heart
            self.visible = True
        if state == "half":
            self.image = self.half_heart
            self.visible = True
        if state == "broken":
            self.visible = False

speed = 6
sprite1 = Playersprite("rocket.png", 100, 400, 100, 100, 6)
aliens = sprite.Group()
sprite21 = Enemysprite("ufo.png", randint(0,600), 0, 55, 55, randint(11,11))
sprite22 = Enemysprite("ufo.png", randint(0,600), 0, randint(25,105), randint(25,105), randint(3,3)) 
sprite23 = Enemysprite("ufo.png", randint(0,600), 0, randint(25,105), randint(25,105), randint(4,4)) 
sprite24 = Enemysprite("ufo.png", randint(0,600), 0, randint(25,105), randint(25,105), randint(5,5)) 
sprite25 = Enemysprite("ufo.png", randint(0,600), 0, randint(25,105), randint(25,105), randint(7,7))
spriteheart1 = Hearttohalf(0, 450, 30, 30)
spriteheart2 = Hearttohalf(30, 450, 30, 30)
spriteheart3 = Hearttohalf(60, 450, 30, 30)
spriteheart4 = Hearttohalf(90, 450, 30, 30)
spriteheart5 = Hearttohalf(120, 450, 30, 30)
spriteheart6 = Hearttohalf(150, 450, 30, 30)
bullets = sprite.Group()
lasers = sprite.Group()
aliens.add(sprite21)
aliens.add(sprite22)
aliens.add(sprite23)
aliens.add(sprite24)
aliens.add(sprite25)
font.init()
big_font = font.SysFont("Arial", 70)
scorefont = font.SysFont("Verdana", 25)
Win = big_font.render('You Win', True, (255,215,0))
Lost = big_font.render('You Lose', True, (255, 215, 0))
Score = scorefont.render('Your Score:', True, (255, 255, 255))
Missed = scorefont.render('Enemies Missed:', True, (255, 255, 255))


run = True
clock = time.Clock()
FPS = 60
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')
firelaser_sound = mixer.Sound('Laser Shoot.mp3')
win = mixer.Sound('Ding.mp3')
lose = mixer.Sound('Fart.mp3')
Broke = mixer.Sound("Second Half Heart Broke.mp3")
Hroke = mixer.Sound("First Half Heart Broke.mp3")
laserState = False
laserCD = 1500
lasertimer1 = 0
lasertimer2 = 0

while run:
    window.blit(background,(0, 0))
    window.blit(Score, (0,0))
    window.blit(Missed, (600000,0))
    sprite1.update()
    aliens.update()
    bullets.update()
    lasers.update()
    spriteheart1.reset() 
    spriteheart2.reset()
    spriteheart3.reset()
    spriteheart4.reset()
    spriteheart5.reset()
    spriteheart6.reset()


    for e in event.get():
        if e.type == QUIT:
           run = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                sprite1.fire()
            if e.key == K_LALT or e.key == K_RALT:
                lasertimer1 = time.get_ticks()
                if lasertimer1- lasertimer2 >= laserCD:
                    firelaser_sound.play()
                    sprite1.firelaser()
                    lasertimer2  = lasertimer1

    
    if miss == 1:
        spriteheart6 = Hearttohalf(150, 450, 90, 30)
        spriteheart6.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 2:
        spriteheart6.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()
    if miss == 3:
        spriteheart5 = Hearttohalf(120, 450, 90, 30)
        spriteheart5.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 4:
        spriteheart5.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()
    if miss == 5:
        spriteheart4 = Hearttohalf(90, 450, 90, 30)
        spriteheart4.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 6:
        spriteheart4.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()
    if miss == 7:
        spriteheart3 = Hearttohalf(60, 450, 90, 30)
        spriteheart3.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 8:
        spriteheart3.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()
    if miss == 9:
        spriteheart2 = Hearttohalf(30, 450, 90, 30)
        spriteheart2.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 10:
        spriteheart2.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()
    if miss == 11:
        spriteheart1 = Hearttohalf(0, 450, 90, 30)
        spriteheart1.NewState("half")
        if not Hroke.get_num_channels():
            Hroke.play()
    if miss == 12:
        spriteheart1.NewState("broken")
        if not Broke.get_num_channels():
            Broke.play()

    sprite1.reset()
    for item in aliens:
         item.reset()
    bullets.draw(window)

    sprite1.reset()
    for item in aliens:
         item.reset()
    lasers.draw(window)

    if score >= 35:
        run = False
        window.blit(Win, (230,215))
        win.play()
        
    if miss >= 12:
        run = False
        window.blit(Lost, (230,215))
        lose.play()

    Missed = scorefont.render('Enemies Missed: '+ str(miss), True, (255, 255, 255))
    Score = scorefont.render('Your Score: '+ str(score), True, (255, 255, 255))

    collides = sprite.groupcollide(aliens, bullets, True, True)
    for collidedItem in collides:
        score = score + 1
        sprite61 = Enemysprite("ufo.png", randint(0,650), 0, 55, 55, randint(3,9))
        aliens.add(sprite61)
        collidedItem.kill()

    collidesTO = sprite.groupcollide(aliens, lasers, True, False)
    for collidedItem in collidesTO:
        score = score + 3
        sprite61 = Enemysprite("ufo.png", randint(0,650), 0, 55, 55, randint(3,9))
        aliens.add(sprite61)
        collidedItem.kill()
    display.update()
    clock.tick(FPS)