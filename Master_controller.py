#!/usr/bin/python
import queue
import Motor
import AD_controller
import Game_controller
# import RPi.GPIO as GPIO
from fake_rpi.RPi import GPIO as GPIO

# 定义常量和变量

HALL_1_PIN = 99  # TODO: 是哪个端口？
HALL_2_PIN = 99
hall_1_counter = 0  # 霍尔开关接收的脉冲计数
hall_2_counter = 0
motor = Motor.Motor()

display_x_queue = queue.Queue()
display_y_queue = queue.Queue()
joystick_x_queue = queue.Queue()
joystick_y_queue = queue.Queue()

game_controller = Game_controller.Game_controller()
touchpannel_controller = AD_controller.AD_controller(display_x_queue, display_y_queue, joystick_x_queue, joystick_y_queue)



# 注册GPIO: 电机-2-OUT，霍尔开关-2-IN，平板-2-OUT
GPIO.setup(HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 找平程序


# 霍尔开关线程
def hall_1_callback(channel1):  # 这里的channel和channel1无须赋确定值，但不能不写?
    global hall_1_counter
    if GPIO.event_detected(HALL_1_PIN):
        hall_1_counter = hall_1_counter + 1


def hall_2_callback(channel2):
    global hall_2_counter
    if GPIO.event_detected(HALL_2_PIN):
        hall_2_counter = hall_2_counter + 1


GPIO.add_event_detect(HALL_1_PIN, GPIO.RISING, callback=hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
GPIO.add_event_detect(HALL_2_PIN, GPIO.RISING, callback=hall_2_callback)

# 启动游戏显示和平板测坐标线程
game_controller.run()
touchpannel_controller.run()


def master_thread_func():
    global hall_1_counter
    global hall_2_counter
    hall_1_target = hall_1_counter
    hall_2_target = hall_2_counter
    HALL_1_MAX = 000
    HALL_2_MAX = 000
    motor_1_direction = 0  # 电机转动方向，0--Go 1--back
    motor_2_direction = 0
    motor_1_running = False
    motor_2_running = False
    JOYSTICK_X_MAX = 000
    JOYSTICK_X_MIN = 000
    JOYSTICK_Y_MAX = 000
    JOYSTICK_Y_MIN = 000
    joystick_x = 0
    joystick_y = 0
    while True:
        # 接收摇杆xy坐标
        if (not joystick_x_queue.empty()) and (not joystick_y_queue.empty()):
            joystick_x = joystick_x_queue.get()
            joystick_y = joystick_y_queue.get()

            # 计算所需脉冲值
            hall_1_target = (joystick_x - JOYSTICK_X_MIN) / (JOYSTICK_X_MAX - JOYSTICK_X_MIN) * HALL_1_MAX
            hall_2_target = (joystick_y - JOYSTICK_Y_MIN) / (JOYSTICK_Y_MAX - JOYSTICK_Y_MIN) * HALL_2_MAX

            # 驱动电机 TODO: 判断方向
            if hall_1_counter < hall_1_target:
                motor.Go_1()
                motor_1_running = True

            if hall_2_counter < hall_2_target:
                motor.Go_2()
                motor_2_running = True

            if hall_1_counter >= hall_1_target:
                motor.Stop_1()
                motor_1_running = False

            if hall_2_counter >= hall_2_target:
                motor.Stop_2()
                motor_2_running = False
        else:
            motor.Stop_1()
            motor.Stop_2()

        # 平板坐标 --> 游戏显示
        if (not display_x_queue.empty()) and (not display_y_queue.empty()):
            tempX = display_x_queue.get()
            tempY = display_y_queue.get()
            game_controller.display(tempX, tempY)


# TODO: 如何结束程序，执行cleanup？
GPIO.cleanup()