from random import*
from pygame import *
from time import time as timer
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, player_speed, width, height):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (width, height))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def update(self): #метод движения спрайта 
        keys_pressed = key.get_pressed()
        if keys_pressed[K_RIGHT] and  self.rect.x < w - 75:
            self.rect.x += self.speed
        if keys_pressed[K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
    def fire(self):
        bullet = Bullet('bullet1.png', self.rect.centerx, self.rect.top, -15, 15, 30)
        bullets.add(bullet)

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(50, 800)
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()


class Asteroid(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y > h:
            self.rect.y = 0
            self.rect.x = randint(50, 800)

    

            





player = Player('player.png', 450, 500, 15, 70, 80) #Экземпляр класса
monsters = sprite.Group()
for _ in range(5):
    enemy = Enemy('enemy1_1.png', randint(50, 800), 90, randint(2, 4), 60, 50)
    monsters.add(enemy)
asteroids = sprite.Group()
for _ in range(3):
    asteroid = Asteroid('asteroid.png', randint(50,800), 90, randint(2, 3), 60, 50)
    asteroids.add(asteroid)

    


bullets = sprite.Group()

w, h = (900, 600)
window = display.set_mode((w, h))
display.set_caption('Шутер')
background = transform.scale(image.load('background2.png'), (w, h))
font.init()
font = font.Font(None, 40)


mixer.init()
mixer.music.load('space.ogg')
mixer.music.set_volume(0.2)
mixer.music.play()
kick = mixer.Sound('fire.ogg')
finish = False
score = 0
num_fire = 0
life = 3
rel_time = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        if e.type == KEYDOWN:
            if e.key == K_w:
                if num_fire < 5 and rel_time == False:
                    player.fire()
                    kick.play()
                    num_fire += 1
                if num_fire >= 5 and rel_time == False:
                    rel_time = True
                    start = timer()


    if finish != True:
        window.blit(background,(0, 0))
        player.reset()
        player.update()
        bullets.update()
        bullets.draw(window)            
        monsters.update()
        monsters.draw(window)
        asteroids.update()
        asteroids.draw(window)
        skip = font.render('Пропущено:' + str(lost), True, (51, 51, 255))
        amount = font.render('Счет:' + str(score), True, (51, 51, 255))
        win = font.render('YOU WIN!', True, (255, 215, 0))
        lose = font.render('YOU LOSE!', True, (204, 0, 0))
        window.blit(skip, (0, 0))
        window.blit(amount, (0, 60))


        if rel_time == True:
            end = timer()
            if end - start < 3:
                wait = font.render('Wait, repload...', True, (255, 0, 0))
                window.blit(wait, (350, 20))
            else:
                num_fire = 0
                rel_time = False

        collides = sprite.groupcollide(monsters, bullets, True, True)
        for _ in collides:
            score += 1
            enemy = Enemy('enemy1_1.png', randint(50, 800), 90, randint(2, 7), 60, 50)
            monsters.add(enemy)
        if sprite.spritecollide(player, monsters, True) or sprite.spritecollide(player, asteroids, True):
            life -= 1

        if lost >= 3 or life == 0:
            window.blit(lose, (200, 200))
            finish = True
        
        if score >= 10:
            window.blit(win, (200, 200))
            finish = True

        if life == 3:
            life_color = (0, 255, 0)
        if life == 2:
            life_color = (255, 255, 0)
        if life == 1:
            life_color = (255, 0, 0)

        life_bar = font.render('Осталось жизней: ' + str(life), True, life_color)
        window.blit(life_bar, (600, 20))
        display.update()
    time.delay(60)



