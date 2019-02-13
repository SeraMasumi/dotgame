#!/usr/bin/python
import pygame
from pygame.locals import *
import text_input_sloth as inpututil
import threading


class Game_controller(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.input_x = -1
        self.input_y = -1

    def display(self, x, y):
        self.input_x = x # 传来的动点
        self.input_y = y

    def run(self):

        # 初始化固定点的坐标
        pos_x1 = 0
        pos_y1 = 0
        pos_x2 = 0
        pos_y2 = 0
        pos_x3 = 0
        pos_y3 = 0

        # 初始化click_box的坐标和宽高
        start_game_click_box_x = 390
        start_game_click_box_y = 500
        balanced_click_box_x = 300
        balanced_click_box_y = 400
        click_box_w = 225
        click_box_h = 20

        # 初始化游戏状态
        game_started = False
        running = True
        tablet_balanced = False

        # 设置欢迎界面的所有显示字符，并把字转化为surface
        tips_font = pygame.font.SysFont('arial', 36)
        start_game_string = tips_font.render('Click to Start Game', True, (255, 255, 255), (0, 0, 0))
        title_string = tips_font.render('Enter Coordinates', True, (255, 255, 255), (0, 0, 0))
        find_balance_string = tips_font.render('Please find balanced position', True, (255, 255, 255), (0, 0, 0))
        finish_balance_string = tips_font.render('Balance done', True, (255, 255, 255), (0, 0, 0))
        hint_x1 = tips_font.render('x1', True, (255, 255, 255), (0, 0, 0))
        hint_y1 = tips_font.render('y1', True, (255, 255, 255), (0, 0, 0))
        hint_x2 = tips_font.render('x2', True, (255, 255, 255), (0, 0, 0))
        hint_y2 = tips_font.render('y2', True, (255, 255, 255), (0, 0, 0))
        hint_x3 = tips_font.render('x3', True, (255, 255, 255), (0, 0, 0))
        hint_y3 = tips_font.render('y3', True, (255, 255, 255), (0, 0, 0))

        # 游戏初始化
        pygame.init()

        # 创建一个screen (1024*768)
        screen = pygame.display.set_mode((1024, 768))

        # 对话框标题
        pygame.display.set_caption('Dot Game')

        # sloth lib init 注册每一个输入框
        clock = pygame.time.Clock()
        manager = inpututil.WidgetManager()
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(362, 300, 100, 35), active=True))
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(562, 300, 100, 35)))
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(362, 365, 100, 35)))
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(562, 365, 100, 35)))
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(362, 430, 100, 35)))
        manager.widgets.append(
            inpututil.TextInput(text_color=pygame.Color('orange'), cursor_color=pygame.Color('orange'),
                                rect=pygame.Rect(562, 430, 100, 35)))

        dt = 0

        # 游戏主循环
        while running:
            # 监听用户事件
            events = pygame.event.get()
            for event in events:
                if event.type == KEYDOWN:  # 监听键盘，按下ESC就退出
                    if event.key == K_ESCAPE:
                        running = False
                elif event.type == QUIT:  # 点击关闭就退出
                    running = False
                elif (not game_started) and event.type == MOUSEBUTTONDOWN:  # 点击开始就获取输入框的坐标并切换到坐标画面
                    x, y = pygame.mouse.get_pos()
                    if start_game_click_box_x <= x <= (start_game_click_box_x + click_box_w) and start_game_click_box_y <= y <= (start_game_click_box_y + click_box_h):  # 如果点击在start_game_click_box之内
                        game_started = True  # 启动游戏
                        pos_x1 = int(manager.widgets[0].get_text())  # 依次获取所有输入的坐标
                        pos_y1 = int(manager.widgets[1].get_text())
                        pos_x2 = int(manager.widgets[2].get_text())
                        pos_y2 = int(manager.widgets[3].get_text())
                        pos_x3 = int(manager.widgets[4].get_text())
                        pos_y3 = int(manager.widgets[5].get_text())
                    if balanced_click_box_x <= x <= (balanced_click_box_x + click_box_w) and balanced_click_box_y <= y <= (balanced_click_box_y + click_box_h):
                        tablet_balanced = True

                # 背景设置为黑色
            screen.fill((0, 0, 0))

            if game_started:  # 游戏已经开始
                # 画点
                pygame.draw.circle(screen, (255, 255, 255), (pos_x1, pos_y1), 10, 0)
                pygame.draw.circle(screen, (255, 255, 255), (pos_x2, pos_y2), 10, 0)
                pygame.draw.circle(screen, (255, 255, 255), (pos_x3, pos_y3), 10, 0)
                if(self.input_x != -1 and self.input_y != -1):
                    pygame.draw.circle(screen, (255, 255, 255), (self.input_x, self.input_y), 10, 0)

            elif tablet_balanced:  # 游戏还没开始，显示欢迎界面
                screen.blit(start_game_string, (start_game_click_box_x, start_game_click_box_y))
                screen.blit(title_string, (395, 235))
                screen.blit(hint_x1, (320, 300))
                screen.blit(hint_y1, (320, 365))
                screen.blit(hint_x2, (320, 430))
                screen.blit(hint_y2, (520, 300))
                screen.blit(hint_x3, (520, 365))
                screen.blit(hint_y3, (520, 430))
                # sloth lib 输入框的活动
                manager.draw(screen)
                manager.update(events, dt)

            else: # 请找平
                screen.blit(finish_balance_string, (balanced_click_box_x, balanced_click_box_y))
                screen.blit(find_balance_string, (395, 235))

            # 更新clock和刷新屏幕
            dt = clock.tick()
            pygame.display.update()

runner = Game_controller();
runner.run();