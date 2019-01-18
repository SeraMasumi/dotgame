import pygame
from pygame.locals import *

# 游戏初始化
pygame.init()

# 创建一个screen (1024*768)
screen = pygame.display.set_mode((1024, 768))

running = True

while running:
    for event in pygame.event.get():
        # 监听键盘，按下ESC就退出
        if event.type == KEYDOWN:
            if(event.key == K_ESCAPE):
                running = False
        # 点击关闭就退出
        elif event.type == QUIT:
            running = False
    # 画点并更新屏幕
    pygame.draw.circle(screen, (255,255,255), (400, 300), 10, 0)
    pygame.display.update()
