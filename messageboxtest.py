#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: K_liu
import pygame
from pygame.locals import *
from sys import exit

pygame.init()
# Configuration file
window_size = (1280, 750)
screen = pygame.display.set_mode(window_size, 0, 32)
pygame.display.set_caption('Message Box Test')


def LoginPage():
    message_box = []  # Create a message box
    #back_image = pygame.image.load('logo2.jpg').convert()
    while True:
        break_switch = False
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            screen.fill((255, 255, 255))  # background color
            #screen.blit(back_image, (400, 100))
            # message box .....................................................................
            screen.set_clip(470, 300, 300, 50)  # message box's location
            screen.fill((47, 79, 79))  # message box's color
            x, y = pygame.mouse.get_pos()
            if 500 < x < 800 and 300 < y < 350:
                # print('mouse in the box')
                if event.type == KEYDOWN:
                    key_num = event.key
                    # print(key_num)
                    if key_num == 49:
                        message_box.append('1')  # get the value of keyboard
                    elif key_num == 50:
                        message_box.append('2')  # get the value of keyboard
                    elif key_num == 51:
                        message_box.append('3')  # get the value of keyboard
                    elif key_num == 52:
                        message_box.append('4')  # get the value of keyboard
                    elif key_num == 53:
                        message_box.append('5')  # get the value of keyboard
                    elif key_num == 54:
                        message_box.append('6')  # get the value of keyboard
                    elif key_num == 55:
                        message_box.append('7')  # get the value of keyboard
                    elif key_num == 56:
                        message_box.append('8')  # get the value of keyboard
                    elif key_num == 57:
                        message_box.append('9')  # get the value of keyboard
                    elif key_num == 48:
                        message_box.append('0')  # get the value of keyboard
                    elif key_num == 46:
                        message_box.append('.')  # get the value of keyboard
                    elif key_num == 8 and len(message_box) is not 0:
                        message_box.pop()  # delete the last value

            text = ''.join(message_box)  # join the list value to a string
            font_family = pygame.font.SysFont('arial', 26)  # setting the font
            IP_name = ' IP: '
            screen.blit(font_family.render(IP_name, True, (255, 255, 255)), (480, 310))
            screen.blit(font_family.render(text, True, (255, 255, 255)), (560, 310))
            # submit button ...................................................................
            screen.set_clip(470, 370, 300, 50)  # submit button's location
            screen.fill((47, 79, 79))  # submit button's color
            Login_name = 'Login'
            screen.blit(font_family.render(Login_name, True, (255, 255, 255)), (585, 380))
            if 470 < x < 770 and 370 < y < 420 and event.type == MOUSEBUTTONDOWN:
                screen.set_clip(470, 370, 300, 50)  # submit button's location
                screen.fill((84, 255, 159))  # change the submit button color
                print('you clicked the button')
                break_switch = True
        pygame.display.update()
        if break_switch:
            print('break')
            break


if __name__ == '__main__':
    LoginPage()






























#!/usr/bin/env python
# -*- coding:utf-8 -*-

""" 
@version: v1.0 
@author: Harp
@contact: liutao25@baidu.com 
@software: PyCharm 
@file: MySnake.py 
@time: 2018/1/15 0015 23:40 
"""


import pygame
from os import path
from sys import exit
from time import sleep
from random import choice
from itertools import product
from pygame.locals import QUIT, KEYDOWN


def direction_check(moving_direction, change_direction):
    directions = [['up', 'down'], ['left', 'right']]
    if moving_direction in directions[0] and change_direction in directions[1]:
        return change_direction
    elif moving_direction in directions[1] and change_direction in directions[0]:
        return change_direction
    return moving_direction


class Snake:

    colors = list(product([0, 64, 128, 192, 255], repeat=3))[1:-1]

    def __init__(self):
        self.map = {(x, y): 0 for x in range(32) for y in range(24)}
        self.body = [[100, 100], [120, 100], [140, 100]]
        self.head = [140, 100]
        self.food = []
        self.food_color = []
        self.moving_direction = 'right'
        self.speed = 4
        self.generate_food()
        self.game_started = False

    def check_game_status(self):
        if self.body.count(self.head) > 1:
            return True
        if self.head[0] < 0 or self.head[0] > 620 or self.head[1] < 0 or self.head[1] > 460:
            return True
        return False

    def move_head(self):
        moves = {
            'right': (20, 0),
            'up': (0, -20),
            'down': (0, 20),
            'left': (-20, 0)
        }
        step = moves[self.moving_direction]
        self.head[0] += step[0]
        self.head[1] += step[1]

    def generate_food(self):
        self.speed = len(self.body) // 16 if len(self.body) // 16 > 4 else self.speed
        for seg in self.body:
            x, y = seg
            self.map[x//20, y//20] = 1
        empty_pos = [pos for pos in self.map.keys() if not self.map[pos]]
        result = choice(empty_pos)
        self.food_color = list(choice(self.colors))
        self.food = [result[0]*20, result[1]*20]


def main():
    key_direction_dict = {
        119: 'up',  # W
        115: 'down',  # S
        97: 'left',  # A
        100: 'right',  # D
        273: 'up',  # UP
        274: 'down',  # DOWN
        276: 'left',  # LEFT
        275: 'right',  # RIGHT
    }

    fps_clock = pygame.time.Clock()
    pygame.init()
    pygame.mixer.init()
    snake = Snake()
    sound = False
    if path.exists('eat.wav'):
        sound_wav = pygame.mixer.Sound("eat.wav")
        sound = True
    title_font = pygame.font.SysFont('arial', 32) # 字体
    welcome_words = title_font.render('Welcome to My Snake', True, (0, 0, 0), (255, 255, 255)) # self, text, antialias, color, bg.
    tips_font = pygame.font.SysFont('arial', 24)
    start_game_words = tips_font.render('Click to Start Game', True, (0, 0, 0), (255, 255, 255))
    close_game_words = tips_font.render('Press ESC to Close', True, (0, 0, 0), (255, 255, 255))
    gameover_words = title_font.render('GAME OVER', True, (205, 92, 92), (255, 255, 255))
    win_words = title_font.render('THE SNAKE IS LONG ENOUGH AND YOU WIN!', True, (0, 0, 205), (255, 255, 255))
    screen = pygame.display.set_mode((640, 480), 0, 32) # screen
    pygame.display.set_caption('My Snake') # caption
    new_direction = snake.moving_direction
    while 1:
        for event in pygame.event.get():
            if event.type == QUIT:
                exit()
            elif event.type == KEYDOWN:
                if event.key == 27:
                    exit()
                if snake.game_started and event.key in key_direction_dict:
                    direction = key_direction_dict[event.key]
                    new_direction = direction_check(snake.moving_direction, direction)
            elif (not snake.game_started) and event.type == pygame.MOUSEBUTTONDOWN: # 获取鼠标点击位置，下面应该做选择，看输入的是哪个框，调用 get_input(int targetxy)
                x, y = pygame.mouse.get_pos()
                if 213 <= x <= 422 and 304 <= y <= 342: # 开始按钮
                    snake.game_started = True
        screen.fill((255, 255, 255))
        if snake.game_started: # 开始了就显示点
            snake.moving_direction = new_direction
            snake.move_head()
            snake.body.append(snake.head[:])
            if snake.head == snake.food:
                if sound:
                    sound_wav.play()
                snake.generate_food()
            else:
                snake.body.pop(0)
            for seg in snake.body:
                pygame.draw.rect(screen, [0, 0, 0], [seg[0], seg[1], 20, 20], 0)
            pygame.draw.rect(screen, snake.food_color, [snake.food[0], snake.food[1], 20, 20], 0)
            if snake.check_game_status():
                screen.blit(gameover_words, (241, 310))
                pygame.display.update()
                snake = Snake()
                new_direction = snake.moving_direction
                sleep(3)
            elif len(snake.body) == 512:
                screen.blit(win_words, (33, 210))
                pygame.display.update()
                snake = Snake()
                new_direction = snake.moving_direction
                sleep(3)
        else: # 输入框在这里显示
            screen.blit(welcome_words, (188, 100))
            screen.blit(start_game_words, (236, 310))
            screen.blit(close_game_words, (233, 350))
        pygame.display.update()
        fps_clock.tick(snake.speed)


if __name__ == '__main__':
    main()