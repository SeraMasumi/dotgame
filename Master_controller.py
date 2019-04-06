#!/usr/bin/python
import queue

import ADS1256
import Motor
import threading
import time
# from pynput import keyboard
# import Game_controller
import AD_controller
import RPi.GPIO as GPIO


# from fake_rpi.RPi import GPIO as GPIO
# from fake_rpi import toggle_print
#
# toggle_print(False)


class Master_controller(threading.Thread):
    def __init__(self, game_dot_queue):
        threading.Thread.__init__(self)
        self.HALL_1_PIN = 31  # 霍尔开关端口
        self.HALL_2_PIN = 32
        self.hall_1_counter = 0  # 霍尔开关接收的脉冲计数
        self.hall_2_counter = 0
        self.hall_1_target = 0  # 霍尔开关接收的脉冲计数
        self.hall_2_target = 0
        self.motor_1_direction = 0  # 电机转动方向， 0--stop 1--Go 2--back
        self.motor_2_direction = 0
        self.game_dot_queue = game_dot_queue
        self.Last_direction_x = 0
        self.Last_direction_y = 0
        self.motor = Motor.Motor()
        self.time_1 = time.time()
        self.time_2 = time.time()

    def run(self):

        ads1256_controller = ADS1256.ADS1256()
        ads1256_controller.ADS1256_Init()

        ad_controller = AD_controller.AD_controller(self.game_dot_queue, ads1256_controller)
        ad_controller.start()

        # producer-consumer queue for AD input for tablet and joystick
        # joystick_x_queue = queue.Queue()
        # joystick_y_queue = queue.Queue()

        # 注册GPIO: 电机-2-OUT，霍尔开关-2-IN，平板-2-OUT
        GPIO.setup(self.HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.HALL_1_PIN, GPIO.RISING, callback=self.hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
        GPIO.add_event_detect(self.HALL_2_PIN, GPIO.RISING, callback=self.hall_2_callback)

        self.hall_1_target = self.hall_1_counter
        self.hall_2_target = self.hall_2_counter
        HALL_1_MAX = 50
        HALL_2_MAX = 50
        JOYSTICK_X_MAX = 8388607
        JOYSTICK_X_MIN = 28500
        JOYSTICK_Y_MAX = 8388607
        JOYSTICK_Y_MIN = 28500
        JOYSTICK_X_MID = 4451000
        JOYSTICK_Y_MID = 4397000
        joystick_x = 0
        joystick_y = 0

        loop_count = 0

        while True:

            # 0:jx, 1:jy, 2:h1t, 3:h1c, 4:h2t, 5:h2c, 6:m1, 7:m2, 8:loop_time
            status = [0, 0, 0, 0, 0, 0, 0, 0, 0]

            time_3 = time.time()
            '''
            if (not joystick_x_queue.empty()) and (not joystick_y_queue.empty()):
                joystick_x = joystick_x_queue.get()
                # print("joystick_x = ", joystick_x)
                joystick_y = joystick_y_queue.get()
                # print("joystick_y = ", joystick_y)

                # 计算所需脉冲值
                self.hall_1_target = (joystick_x - JOYSTICK_X_MIN - JOYSTICK_X_MID) / (
                        JOYSTICK_X_MAX - JOYSTICK_X_MIN) * HALL_1_MAX
                self.hall_2_target = (joystick_y - JOYSTICK_Y_MIN - JOYSTICK_Y_MID) / (
                        JOYSTICK_Y_MAX - JOYSTICK_Y_MIN) * HALL_2_MAX
                # print("In Master_controller, hall_1_target = ", int(hall_1_target), ", hall_2_target = ", int(hall_2_target))
                # print("In Master_controller, hall_1_counter = ", self.hall_1_counter, ", hall_2_counter = ", self.hall_2_counter)
            '''

            joystick_x = ads1256_controller.ADS1256_GetoneChannel(3)
            joystick_y = ads1256_controller.ADS1256_GetoneChannel(4)
            status[0] = joystick_x
            status[1] = joystick_y
            self.hall_1_target = int((joystick_x - JOYSTICK_X_MIN - JOYSTICK_X_MID) / (
                        JOYSTICK_X_MAX - JOYSTICK_X_MIN) * HALL_1_MAX)
            self.hall_2_target = int((joystick_y - JOYSTICK_Y_MIN - JOYSTICK_Y_MID) / (
                        JOYSTICK_Y_MAX - JOYSTICK_Y_MIN) * HALL_2_MAX)
            status[2] = self.hall_1_target
            status[4] = self.hall_2_target

            # 驱动电机
            status[3] = self.hall_1_counter
            if status[3] < (self.hall_1_target - 1):
                cur_time = time.time()
                status[6] = 1
                if (self.motor_1_direction == 2):
                    self.motor.Stop_1()
                    self.Last_direction_x = 2
                    self.motor_1_direction = 0
                    self.time_1 = time.time()
                    status[6] = 2
                elif not (self.Last_direction_x == 2 and cur_time - self.time_1 < 0.1):
                    self.motor.Go_1()
                    self.motor_1_direction = 1
                    self.Last_direction_x = 0
                    status[6] = 3
            elif status[3] > (self.hall_1_target + 1):
                cur_time = time.time()
                status[6] = 4
                if (self.motor_1_direction == 1):
                    self.motor.Stop_1()
                    self.Last_direction_x = 1
                    self.motor_1_direction = 0
                    self.time_1 = time.time()
                    status[6] = 5
                elif not (self.motor_1_direction == 1 and cur_time - self.time_1 < 0.1):
                    self.motor.Back_1()
                    self.motor_1_direction = 2
                    self.Last_direction_x = 0
                    status[6] = 6
            else:
                # if self.my_equal(self.hall_1_counter, self.hall_1_target):
                self.motor.Stop_1()
                status[6] = 7
                if (self.motor_1_direction != 0):
                    self.Last_direction_x = self.motor_1_direction
                    self.motor_1_direction = 0
                    self.time_1 = time.time()
                    status[6] = 8

            status[5] = self.hall_2_counter
            if status[5] < (self.hall_2_target - 1):
                cur_time = time.time()
                status[7] = 1
                if (self.motor_2_direction == 2):
                    self.motor.Stop_2()
                    self.Last_direction_y = 2
                    self.motor_2_direction = 0
                    self.time_2 = time.time()
                    status[7] = 2
                elif not (self.motor_2_direction == 2 and cur_time - self.time_2 < 0.1):
                    self.motor.Go_2()
                    self.motor_2_direction = 1
                    self.Last_direction_y = 0
                    status[7] = 3
            elif status[5] > (self.hall_2_target + 1):
                cur_time = time.time()
                status[7] = 4
                if (self.motor_2_direction == 1):
                    self.motor.Stop_2()
                    self.Last_direction_y = 1
                    self.motor_2_direction = 0
                    self.time_2 = time.time()
                    status[7] = 5
                elif not (self.motor_2_direction == 1 and cur_time - self.time_2 < 0.1):
                    self.motor.Back_2()
                    self.motor_2_direction = 2
                    self.Last_direction_y = 0
                    status[7] = 6
            else:
                # if self.my_equal(self.hall_2_counter, self.hall_2_target):
                self.motor.Stop_2()
                status[7] = 7
            if (self.motor_2_direction != 0):
                self.Last_direction_y = self.motor_2_direction
                self.motor_2_direction = 0
                self.time_2 = time.time()
                status[7] = 8

            status[8] = round(time.time() - time_3, 5)
            # status[9] = round(time.time(), 5)
            print(status)

    # 霍尔开关线程
    def hall_1_callback(self, channel1):
        if GPIO.event_detected(self.HALL_1_PIN):
            if self.motor_1_direction == 1:
                self.hall_1_counter = self.hall_1_counter + 1
                # print("hall signal detected, hall_1_counter + 1.")
            elif self.motor_1_direction == 2:
                self.hall_1_counter = self.hall_1_counter - 1
                # print("hall signal detected, hall_1_counter - 1.")
            elif self.motor_1_direction == 0:
                if (self.Last_direction_x == 1):
                    self.hall_1_counter = self.hall_1_counter + 1
                elif (self.Last_direction_x == 2):
                    self.hall_1_counter = self.hall_1_counter - 1

    def hall_2_callback(self, channel2):
        if GPIO.event_detected(self.HALL_2_PIN):
            if self.motor_2_direction == 1:
                self.hall_2_counter = self.hall_2_counter + 1
                # print("hall signal detected, hall_2_counter + 1.")
            elif self.motor_2_direction == 2:
                self.hall_2_counter = self.hall_2_counter - 1
                # print("hall signal detected, hall_2_counter - 1.")
            elif self.motor_2_direction == 0:
                if (self.Last_direction_y == 1):
                    self.hall_2_counter = self.hall_2_counter + 1
                elif (self.Last_direction_y == 2):
                    self.hall_2_counter = self.hall_2_counter - 1

    # 留有余量的比较
    def my_equal(self, a, b):
        EQUAL_BUFFER = 3
        if abs(a - b) < EQUAL_BUFFER:
            return True
        else:
            return False
