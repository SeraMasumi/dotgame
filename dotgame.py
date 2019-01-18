import pygame
from pygame.locals import *

# 游戏初始化
pygame.init()

# 创建一个screen (1024*768)
screen = pygame.display.set_mode((1024, 768))

running = True

while running:
    # 监听键盘，按下ESC就退出
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if(event.key == K_ESCAPE):
                running = False
    # 画点
    pygame.draw.circle(screen, (255,255,255), (400, 300), 10, 0)
    pygame.display.update()
