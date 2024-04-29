x = 50
y = 60
import os
os.environ["SDL_VIDEO_WINDOW_POS"] = "%d,%d" % (x,y)

import time as timer
from pygame import *
from random import *
window_width = 1200
window_height = 600
window = display.set_mode((window_width,window_height))

display.set_caption("PingPong Game")

background = image.load("table.jpg")
crop_area = Rect(50,50,513,300)
background = background.subsurface(crop_area)
background = transform.scale(background,(window_width, window_height))

fps = 60
clock = time.Clock()
game = True

class Character(sprite.Sprite):
    def __init__(self, image, size_x, size_y, x, y, speed, score):
        sprite.Sprite.__init__(self)
        self.size_x = size_x
        self.size_y = size_y
        self.image = transform.scale( image, (size_x, size_y))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
        self.score = score
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Ball(Character):
    def __init__(self, image, size_x, size_y, x, y, speed, score):
        super().__init__(image, size_x, size_y, x, y, speed, score)
        self.rotate_image = self.image
        self.rotate_rect = self.rotate_image.get_rect()
        self.rotate_speed = 1
        self.angle = 0
    def rotate(self):
        self.angle += self.rotate_speed
        self.rotate_image = transform.rotate(self.image, self.angle)
        self.rotate_rect = self.rotate_image.get_rect(center=(self.rect.x, self.rect.y))
    def draw(self):
        window.blit(self.rotate_image, (self.rotate_rect.x, self.rotate_rect.y))

class Bomb(Character):
    def __init__(self, image, size_x, size_y, x, y, speed, score):
        super().__init__(image, size_x, size_y, x, y, speed, score)
        self.speed_x = choice([5, -5])
        self.speed_y = choice([1, -1])
        self.rotate_image = self.image
        self.rotate_rect = self.rotate_image.get_rect()
        self.rotate_speed = 1
        self.angle = 0
    def rotate(self):
        self.angle += self.rotate_speed
        self.rotate_image = transform.rotate(self.image, self.angle)
        self.rotate_rect = self.rotate_image.get_rect(center=(self.rect.x, self.rect.y))
    def draw(self):
        window.blit(self.rotate_image, (self.rotate_rect.x, self.rotate_rect.y))
    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y

img = image.load("strawberry.png")
crop_area = Rect(80, 30, 50, 180)
img = img.subsurface(crop_area)
player1 = Character(img, 50 , 200, 0, 215, 10, 0)
player2 = Character(img, 50 , 200, 1150, 215, 10, 0)

img = image.load("ball.png")
ball = Ball(img, 100, 100, 379, 250, 20, 0)
ball.speed_x = ball.speed
ball.speed_y = ball.speed

bomb_group = sprite.Group()
create_bomb_time = timer.time()

font.init()
style = font.SysFont(None, 36)
finish = False
pause = False

while game:
    window.blit(background, (0,0))
    player1.draw()
    player2.draw()
    ball.draw()
    bomb_group.draw(window)
    bomb_group.update()
    text_score = style.render("Player1 Score: " + str(player1.score) + " VS " + "Player2 Score: " + str(player2.score), 1, (0, 0, 0))
    window.blit(text_score, (400, 20))

    if finish == False:
        if pause == False:
            if (timer.time() - create_bomb_time > 10):
                img = image.load("bomb.png")
                bomb = Bomb(img, 100, 100, 500, 300, 3, 0)
                bomb_group.add(bomb)
                create_bomb_time = timer.time()
                bomb.rect.x += bomb.speed
                bomb.rect.y += bomb.speed

            ball.rotate()
            ball.rect.x += ball.speed_x
            ball.rect.y += ball.speed_y

            if ball.rect.x > window_width - ball.size_x:
                player1.score += 1
                ball.rect.y = player2.rect.y
                ball.rect.x = player2.rect.x - 100
                pause = True
                ready = timer.time()
            elif ball.rect.x < 0:
                player2.score += 1
                ball.rect.y = player1.rect.y
                ball.rect.x = player1.rect.x + 50
                pause = True
                ready = timer.time()
            
            if player1.score >= 10:
                text_score = style.render("Player1 Win!", 1, (0, 0, 0))
                window.blit(text_score, (520, 260))
                finish = True
            elif player2.score >= 10:
                text_score = style.render("Player2 Win!", 1, (0, 0, 0))
                window.blit(text_score, (520, 260))
                finish = True

            keys_pressed = key.get_pressed()

            if ball.rect.y > window_height-ball.size_y:
                ball.speed_y *= -1
            elif ball.rect.x > window_width-ball.size_x:
                ball.speed_x *= -1
            elif ball.rect.y < 0:
                ball.speed_y *= -1
            elif ball.rect.x < 0:
                ball.speed_x *= -1

            # if bomb.rect.y > window_height-ball.size_y:
            #     bomb.speed_y *= -1
            # elif bomb.rect.x > window_width-ball.size_x:
            #     bomb.speed_x *= -1
            # elif bomb.rect.y < 0:
            #     bomb.speed_y *= -1
            # elif bomb.rect.x < 0:
            #     bomb.speed_x *= -1

            if keys_pressed[K_w] and player1.rect.y > 0:
                    player1.rect.y -= player1.speed   
            elif keys_pressed[K_s] and player1.rect.y < window_height-player1.size_y:
                    player1.rect.y += player1.speed
            
            if keys_pressed[K_UP] and player2.rect.y > 0:
                    player2.rect.y -= player2.speed   
            elif keys_pressed[K_DOWN] and player2.rect.y < window_height-player2.size_y:
                    player2.rect.y += player2.speed

            if sprite.collide_rect(ball, player1):
                # ball.speed_y *= -1
                ball.speed_x *= -1

            if sprite.collide_rect(ball, player2):
                # ball.speed_y *= -1
                ball.speed_x *= -1

            # if sprite.spritecollide(bomb_group, player1, True):
            #     player2_score += 1

            # if sprite.spritecollide(bomb_group, player2, True):
            #     player1_score += 1

            collide_list = sprite.spritecollide(player1, bomb_group, True)
            if len(collide_list) > 0:
                player1.score -= 1

            collide_list = sprite.spritecollide(player2, bomb_group, True)
            if len(collide_list) > 0:
                player2.score -= 1

        elif (timer.time() - ready > 1):
            pause = False

    else:
        if player1.score >= 10:
                text_score = style.render("Player1 Win!", 1, (0, 0, 0))
                window.blit(text_score, (520, 260))
        elif player2.score >= 10:
                text_score = style.render("Player2 Win!", 1, (0, 0, 0))
                window.blit(text_score, (520, 260))
    
    for e in event.get():
        if e.type == QUIT:
            game = False

    display.update()
    clock.tick(fps)