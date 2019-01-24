import pygame
from pygame.locals import *
import text_input_sloth as inpututil

# 游戏初始化
pygame.init()

# 创建一个screen (1024*768)
screen = pygame.display.set_mode((1024, 768))

# 创建一个文本输入框
# textinput = pygame_textinput.TextInput()
# textinput.get_surface().fill((180,180,180))

# 文本输入框的surface
# text_surface = pygame.Surface((500,500)) # 尺寸
# text_surface.fill((180,180,180)) # 背景颜色
# screen.blit(textinput.get_surface(), (400,300)) # 在screen的位置

pos_x1 = 0
pos_y1 = 0
pos_x2 = 0
pos_y2 = 0

game_started = False

running = True

tips_font = pygame.font.SysFont('arial', 24)
start_game_words = tips_font.render('Click to Start Game', True, (255, 255, 255), (0, 0, 0))

pygame.display.set_caption('Dot Game')

# sloth lib init
clock = pygame.time.Clock()
manager = inpututil.WidgetManager()
manager.widgets.append(
    inpututil.TextInput(text_color=pygame.Color('grey'), cursor_color=pygame.Color('grey'),
                        rect=pygame.Rect(5, 5, 200, 35)))
manager.widgets.append(inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                           rect=pygame.Rect(5, 55, 200, 35), active=True))
dt = 0

while running:
    events = pygame.event.get()
    for event in events:
        if event.type == KEYDOWN: # 监听键盘，按下ESC就退出
            if event.key == K_ESCAPE:
                running = False
        elif event.type == QUIT: # 点击关闭就退出
            running = False
        elif (not game_started) and event.type == MOUSEBUTTONDOWN: # 点击开始就切换到坐标画面
            x, y = pygame.mouse.get_pos()
            if 213 <= x <= 422 and 304 <= y <= 342:
                game_started = True
                pos_x1 = int(manager.widgets[0].get_text())
                pos_y1 = int(manager.widgets[1].get_text())

    screen.fill((0, 0, 0))

    if game_started:
        # 画点
        pygame.draw.circle(screen, (255,255,255), (pos_x1, pos_y1), 10, 0)

    else:
        # 显示输入坐标界面
        screen.blit(start_game_words, (250,300))
        # sloth lib
        manager.draw(screen)
        manager.update(events, dt)
        # get input
        # if manager.update(events, dt):
        #     pos_x1 = int(manager.widgets[0].get_text())
        #     pos_y1 = int(manager.widgets[1].get_text())


    dt = clock.tick()
    pygame.display.update()
