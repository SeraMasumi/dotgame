import pygame
from pygame.locals import *
import pygame_textinput


def main():

    # 游戏初始化
    pygame.init()

    # 创建一个screen (1024*768)
    screen = pygame.display.set_mode((1024, 768))

    # 创建一个输入框
    # textinput = pygame_textinput.TextInput()


    # game_started = True
    # running = True
    #
    # while running:
    #     for event in pygame.event.get():
    #         # 监听键盘，按下ESC就退出
    #         if event.type == KEYDOWN:
    #             if(event.key == K_ESCAPE):
    #                 running = False
    #         # 点击关闭就退出
    #         elif event.type == QUIT:
    #             running = False
    #
    #     # if game_started == True:
    #         # 画点并更新屏幕
    #     pygame.draw.circle(screen, (255,255,255), (400, 300), 10, 0)
    #     pygame.display.update()
    #     # elif game_started == False:
    #     #     # 接收坐标输入
    #     #     events = pygame.event.get()
    #     #     for event in events:
    #     #         if event.type == pygame.QUIT:
    #     #             exit()
    #     #
    #     #     # Feed it with events every frame
    #     #     textinput.update(events)
    #     #     # Blit its surface onto the screen
    #     #     screen.blit(textinput.get_surface(), (10, 10))
    #     #
    #     #     if textinput.update(events):
    #     #         print(textinput.get_text())
