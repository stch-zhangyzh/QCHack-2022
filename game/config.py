# time: 2022/4/10
# author: YiZhou Zhang, XinYu Pan
# mails: zhangyzh@shanghaitech.edu.cn, k435508582@qq.com

import pygame
import os

WIDTH, HEIGHT = 1200, 820

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)

FPS = 60
VEL = 5
BULLET_VEL = 7
MAX_BULLETS = 3

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40
CORSOR_WIDTH, CORSOR_HEIGHT = 60, 60

Controller = pygame.Rect(0, 600, WIDTH, 220)

table = [[0] * 13] * 3

#BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
#BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')

YELLOW_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('utils/Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)

RED_SPACESHIP_IMAGE = pygame.image.load(
    os.path.join('utils/Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270)

SPACE = pygame.transform.scale(pygame.image.load(
    os.path.join('utils/Assets', 'space.png')), (WIDTH, HEIGHT))

CORSOR = pygame.image.load(
    os.path.join('utils/Assets', 'consor.png'))