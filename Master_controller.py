#!/usr/bin/python
import queue
import Motor
# from pynput import keyboard
import AD_controller
import Game_controller
# import RPi.GPIO as GPIO
from fake_rpi.RPi import GPIO as GPIO

# 定义常量和变量

EQUAL_BUFFER = 3  # 判断相等的缓冲量
HALL_1_PIN = 31  # 霍尔开关端口
HALL_2_PIN = 32
hall_1_counter = 0  # 霍尔开关接收的脉冲计数
hall_2_counter = 0
motor_1_direction = 0  # 电机转动方向， 0--stop 1--Go 2--back
motor_2_direction = 0
motor = Motor.Motor()

# producer-consumer queue for AD input for tablet and joystick
display_x_queue = queue.Queue()
display_y_queue = queue.Queue()
joystick_x_queue = queue.Queue()
joystick_y_queue = queue.Queue()

# initialize pygame and AD-read object
game_controller = Game_controller.Game_controller()
AD_controller = AD_controller.AD_controller(display_x_queue, display_y_queue, joystick_x_queue, joystick_y_queue)

# 注册GPIO: 电机-2-OUT，霍尔开关-2-IN，平板-2-OUT
GPIO.setup(HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 找平程序


# 霍尔开关线程
def hall_1_callback(channel1):
    global hall_1_counter
    global motor_1_direction
    if GPIO.event_detected(HALL_1_PIN):
        if motor_1_direction == 1:
            hall_1_counter = hall_1_counter + 1
        elif motor_1_direction == 2:
            hall_1_counter = hall_1_counter - 1


def hall_2_callback(channel2):
    global hall_2_counter
    global motor_2_direction
    if GPIO.event_detected(HALL_2_PIN):
        if motor_2_direction == 1:
            hall_2_counter = hall_2_counter + 1
        elif motor_2_direction == 2:
            hall_2_counter = hall_2_counter - 1


GPIO.add_event_detect(HALL_1_PIN, GPIO.RISING, callback=hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
GPIO.add_event_detect(HALL_2_PIN, GPIO.RISING, callback=hall_2_callback)

# 启动游戏显示和平板测坐标线程
game_controller.run()
AD_controller.run()


# 留有余量的比较
def my_equal(a, b):
    global EQUAL_BUFFER
    if (a - b) < EQUAL_BUFFER or (a - b) > -EQUAL_BUFFER:
        return True
    else:
        return False


# 主线程
def master_thread_func():
    global hall_1_counter
    global hall_2_counter
    hall_1_target = hall_1_counter
    hall_2_target = hall_2_counter
    HALL_1_MAX = 60
    HALL_2_MAX = 60
    global motor_1_direction
    global motor_2_direction
    JOYSTICK_X_MAX = 8388607
    JOYSTICK_X_MIN = 28500
    JOYSTICK_Y_MAX = 8388607
    JOYSTICK_Y_MIN = 28500
    JOYSTICK_X_MID = 4451000
    JOYSTICK_Y_MID = 4397000
    joystick_x: int = 0
    joystick_y: int = 0
    PYGAME_RESOLUTION_X = 1024
    PYGAME_RESOLUTION_Y = 768

    while True:
        # 接收摇杆xy坐标
        if (not joystick_x_queue.empty()) and (not joystick_y_queue.empty()):
            joystick_x = joystick_x_queue.get()
            joystick_y = joystick_y_queue.get()

            # 计算所需脉冲值
            hall_1_target = (joystick_x - JOYSTICK_X_MIN - JOYSTICK_X_MID) / (
                        JOYSTICK_X_MAX - JOYSTICK_X_MIN) * HALL_1_MAX
            hall_2_target = (joystick_y - JOYSTICK_Y_MIN - JOYSTICK_Y_MID) / (
                        JOYSTICK_Y_MAX - JOYSTICK_Y_MIN) * HALL_2_MAX

            # 驱动电机
            if hall_1_counter < hall_1_target:
                motor.Go_1()
                motor_1_direction = 1

            if hall_1_counter > hall_1_target:
                motor.Back_1()
                motor_1_direction = 2

            if hall_2_counter < hall_2_target:
                motor.Go_2()
                motor_2_direction = 1

            if hall_2_counter > hall_2_target:
                motor.Back_2()
                motor_2_direction = 2

            if my_equal(hall_1_counter, hall_1_target):
                motor.Stop_1()
                motor_1_direction = 0

            if my_equal(hall_2_counter, hall_2_target):
                motor.Stop_2()
                motor_2_direction = 0
        else:
            motor.Stop_1()
            motor.Stop_2()

        # 平板坐标 --> 游戏显示
        if (not display_x_queue.empty()) and (not display_y_queue.empty()):
            temp_x = display_x_queue.get() * PYGAME_RESOLUTION_X
            temp_y = display_y_queue.get() * PYGAME_RESOLUTION_Y
            game_controller.display(temp_x, temp_y)


# TODO: 如何结束程序，执行cleanup？
GPIO.cleanup()
