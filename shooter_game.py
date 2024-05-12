#Создай собственный Шутер!
from pygame import *
from random import *
#музыка
mixer.init()
mixer.music.load('space.ogg')
mixer.music.play()
fire_sound = mixer.Sound('fire.ogg')

#шрифты и надписи
font.init()
font1 = font.SysFont('Segoe Script',58)
win = font1.render('YOU WIN!', True, (50,150,50))
lose = font1.render(' YOU LOSE!', True, (180,0,0))
font2 = font.SysFont('Segoe Script',26)
#счет
lost = 0 #пропущено кораблей
score = 0 #сбито кораблей
max_lost = 3 #проиграли, если пропустили столько
goal = 10 #столько караблей нужно сбить для победы

#класс родитель для других спрайтов
class GameSprite (sprite.Sprite):
    def __init__(self, player_image, player_x, player_y,size_x,size_y, player_speed):
        sprite.Sprite.__init__(self)
        self.image = background = transform.scale(image.load(player_image),(size_x,size_y))
        self.speed = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y)) 
#класс главного героя
class Player(GameSprite):
    def update(self):
        key_pressed = key.get_pressed()
        if key_pressed[K_LEFT] and self.rect.x > 5:
            self.rect.x -= self.speed
        if key_pressed[K_RIGHT] and self.rect.x < 625:
            self.rect.x += self.speed   
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx, self.rect.top, 15, 20, 15)
        bullets.add(bullet)
#класс анти героя
class Enemy(GameSprite): 
    def update(self): 
        self.rect.y += self.speed 
        global lost 
        if self.rect.y > 470: 
            self.rect.y = 0 
            self.rect.x = randint(80, 620) 
            lost = lost + 1

class Bullet(GameSprite):
    def update(self):
        self.rect.y -= self.speed
        if self.rect.y < 0:
            self.kill()
#окно
window = display.set_mode((700,500))
display.set_caption('pygame window')
background = transform.scale(image.load('galaxy.jpg'),(700,500))

#сами челики
player = Player('rocket.png', 300, 400, 70, 90, 6)

clock = time.Clock()
FPS = 60
monters = sprite.Group()
for i in range(1, 6):
    monter = Enemy('asteroid.png', randint(11,620),-5,80,80,randint(1,3))
    monters.add(monter)

bullets = sprite.Group()
finish = False
game = True
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:
                fire_sound.play()
                player.fire()

    if finish != True:
        window.blit(background,(0,0))

        collides = sprite.groupcollide(monters,bullets,True,True)
        for c in collides:
            score = score + 1
            monter = Enemy('asteroid.png', randint(11,620),-40,70,70,randint(1,5))
            monters.add(monter)

        if sprite.spritecollide(player,monters,False) or lost >= max_lost:
            finish = True
            window.blit(lose,(200,200))

        if score >= goal:
            finish = True
            window.blit(win,(200,200))        

        text_lose = font2.render('Окручено: ' + str(lost), True, (255,215,255))
        window.blit(text_lose,(10,35))
        text = font2.render('Счет: ' + str(score), True, (255,215,255))
        window.blit(text,(10,5))

        monter.update()
        monter.reset()

        bullets.update()
        bullets.draw(window)

        monters.update()
        monters.draw(window)

        player.update()
        player.reset()
                        
        time.delay(20)
        display.update()