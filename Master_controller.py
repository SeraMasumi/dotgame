#!/usr/bin/python
import queue
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
        self.Last_direction_x = 1
        self.Last_direction_y = 1
        self.motor = Motor.Motor()
        self.time_1 = time.time()
        self.time_2 = time.time()

    def run(self):

        # producer-consumer queue for AD input for tablet and joystick
        joystick_x_queue = queue.Queue()
        joystick_y_queue = queue.Queue()

        # game_controller = Game_controller.Game_controller()
        ad_controller = AD_controller.AD_controller(self.game_dot_queue, joystick_x_queue, joystick_y_queue)

        # 注册GPIO: 电机-2-OUT，霍尔开关-2-IN，平板-2-OUT
        GPIO.setup(self.HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.HALL_1_PIN, GPIO.RISING, callback=self.hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
        GPIO.add_event_detect(self.HALL_2_PIN, GPIO.RISING, callback=self.hall_2_callback)

        ad_controller.start()

        self.hall_1_target = self.hall_1_counter
        self.hall_2_target = self.hall_2_counter
        HALL_1_MAX = 100
        HALL_2_MAX = 100
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

            time_3 = time.time()

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
            print("jx=", joystick_x, " jy=", joystick_y, " h1t=", int(self.hall_1_target), "h2t=", int(self.hall_2_target), "h1c=", self.hall_1_counter, "h2c=", self.hall_2_counter)

            # 驱动电机
            if self.hall_1_counter < (self.hall_1_target - 1):
                cur_time = time.time()
                if not (self.motor_1_direction == 2 and cur_time - self.time_1 < 1):
                    self.motor.Go_1()
                    self.motor_1_direction = 1
                    print("Go_1", " h1t=", self.hall_1_target, " h1c=", self.hall_1_counter)

            if self.hall_1_counter > (self.hall_1_target + 1):
                cur_time = time.time()
                if not (self.motor_1_direction == 1 and cur_time - self.time_1 < 1):
                    self.motor.Back_1()
                    self.motor_1_direction = 2
                    print("Back_1", " h1t=", self.hall_1_target, " h1c=", self.hall_1_counter)

            if self.hall_2_counter < (self.hall_2_target - 1):
                cur_time = time.time()
                if not (self.motor_2_direction == 2 and cur_time - self.time_2 < 1):
                    self.motor.Go_2()
                    self.motor_2_direction = 1
                    print("Go_2", " h2t=", self.hall_2_target, " h2c=", self.hall_2_counter)

            if self.hall_2_counter > (self.hall_2_target + 1):
                cur_time = time.time()
                if not (self.motor_2_direction == 1 and cur_time - self.time_2 < 1):
                    self.motor.Back_2()
                    self.motor_2_direction = 2
                    print("Back_2", " h2t=", self.hall_2_target, " h2c=", self.hall_2_counter)

            # if self.my_equal(self.hall_1_counter, self.hall_1_target):
            #     motor.Stop_1()
            #     if (self.motor_1_direction != 0):
            #         self.Last_direction_x = self.motor_1_direction
            #         self.motor_1_direction = 0
            #         time_1 = time.time()
            #     # print("motor.Stop_1, counter reached target, ", "hall_1_counter = ", self.hall_1_counter, ", hall_1_target = ", int(hall_1_target))
            #     print("Stop_1 ", "h1c=", self.hall_1_counter, " h1t=", int(self.hall_1_target))

            # if self.my_equal(self.hall_2_counter, self.hall_2_target):
            #     self.motor.Stop_2()
            #     if (self.motor_2_direction != 0):
            #         self.Last_direction_y = self.motor_2_direction
            #         self.motor_2_direction = 0
            #         time_2 = time.time()
            #     # print("Stop_2, counter reached target, ", "hall_2_counter = ", self.hall_2_counter, ", hall_2_target = ", int(hall_2_target))
            #     print("Stop_2 ", "h2c=", self.hall_2_counter, " h2t=", int(self.hall_2_target))

            loop_count = loop_count + 1
            print("loop count=", loop_count, " loop time=", time.time() - time_3)

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

            if self.my_equal(self.hall_1_counter, self.hall_1_target):
                self.motor.Stop_1()
                if (self.motor_1_direction != 0):
                    self.Last_direction_x = self.motor_1_direction
                    self.motor_1_direction = 0
                    self.time_1 = time.time()
                # print("motor.Stop_1, counter reached target, ", "hall_1_counter = ", self.hall_1_counter, ", hall_1_target = ", int(hall_1_target))
                print("Stop_1 ", "h1c=", self.hall_1_counter, " h1t=", int(self.hall_1_target))

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

            if self.my_equal(self.hall_2_counter, self.hall_2_target):
                self.motor.Stop_2()
                if (self.motor_2_direction != 0):
                    self.Last_direction_y = self.motor_2_direction
                    self.motor_2_direction = 0
                    self.time_2 = time.time()
                # print("Stop_2, counter reached target, ", "hall_2_counter = ", self.hall_2_counter, ", hall_2_target = ", int(hall_2_target))
                print("Stop_2 ", "h2c=", self.hall_2_counter, " h2t=", int(self.hall_2_target))

    # 留有余量的比较
    def my_equal(self, a, b):
        EQUAL_BUFFER = 3
        if abs(a - b) < EQUAL_BUFFER:
            return True
        else:
            return False
