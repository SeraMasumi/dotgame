import pygame
from pygame.locals import *


class Dot(pygame.sprite.Sprite):
    def __init__(self):
        super(Dot, self).__init__()
        self.surf = pygame.Surface((30,30)) # 点的大小
        self.surf.fill((255,255,255)); # 填充颜色
        self.rec = self.surf.get_rect()

# 游戏初始化
pygame.init()

# 创建一个screen (1024*768)
screen = pygame.display.set_mode((1024, 768))

# 创建一个点(dot)
dot = Dot()

# 暂时还不需要
# background = pygame.Surface(screen.get_size())
# background.fill((200,100,0))

running = True

while running:
    # 监听键盘，按下ESC就退出
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if(event.key == K_ESCAPE):
                running = False
    # 画点
    # screen.blit(dot.surf, (400, 300))
    # pygame.display.flip()
    pygame.draw.circle(screen, (255,255,255), (400, 300), 10, 0)
    pygame.display.update()
