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
        self.motor_1_direction = 0  # 电机转动方向， 0--stop 1--Go 2--back
        self.motor_2_direction = 0
        self.game_dot_queue = game_dot_queue
        self.Last_direction_x = 1
        self.Last_direction_y = 1

    def run(self):

        # producer-consumer queue for AD input for tablet and joystick
        joystick_x_queue = queue.Queue()
        joystick_y_queue = queue.Queue()

        # initialize motor, pygame and AD-read object
        motor = Motor.Motor()
        # game_controller = Game_controller.Game_controller()
        ad_controller = AD_controller.AD_controller(self.game_dot_queue, joystick_x_queue, joystick_y_queue)

        # 注册GPIO: 电机-2-OUT，霍尔开关-2-IN，平板-2-OUT
        GPIO.setup(self.HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        GPIO.add_event_detect(self.HALL_1_PIN, GPIO.RISING, callback=self.hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
        GPIO.add_event_detect(self.HALL_2_PIN, GPIO.RISING, callback=self.hall_2_callback)

        ad_controller.start()

        hall_1_target = self.hall_1_counter
        hall_2_target = self.hall_2_counter
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

        time_1 = time.time()
        time_2 = time.time()

        while True:
            # print("entered Master_controller while loop")
            # print("In Master_controller, joystick_x_queue size is ", joystick_x_queue.qsize())
            # print("In Master_controller, joystick_y_queue size is ", joystick_y_queue.qsize())
            # 接收摇杆xy坐标
            if (not joystick_x_queue.empty()) and (not joystick_y_queue.empty()):
                joystick_x = joystick_x_queue.get()
                # print("joystick_x = ", joystick_x)
                joystick_y = joystick_y_queue.get()
                # print("joystick_y = ", joystick_y)

                # 计算所需脉冲值
                hall_1_target = (joystick_x - JOYSTICK_X_MIN - JOYSTICK_X_MID) / (
                        JOYSTICK_X_MAX - JOYSTICK_X_MIN) * HALL_1_MAX
                hall_2_target = (joystick_y - JOYSTICK_Y_MIN - JOYSTICK_Y_MID) / (
                        JOYSTICK_Y_MAX - JOYSTICK_Y_MIN) * HALL_2_MAX
                # print("In Master_controller, hall_1_target = ", int(hall_1_target), ", hall_2_target = ", int(hall_2_target))
                # print("In Master_controller, hall_1_counter = ", self.hall_1_counter, ", hall_2_counter = ", self.hall_2_counter)


            # 驱动电机
            if self.hall_1_counter < (hall_1_target - 1):
                cur_time = time.time()
                if not (self.motor_1_direction == 2 and cur_time - time_1 < 1):
                    motor.Go_1()
                    self.motor_1_direction = 1
                    # print("In Master_controller main loop, motor.Go_1")

            if self.hall_1_counter > (hall_1_target + 1):
                cur_time = time.time()
                if not (self.motor_1_direction == 1 and cur_time - time_1 < 1):
                    motor.Back_1()
                    self.motor_1_direction = 2
                    # print("In Master_controller main loop, motor.Back_1")

            if self.hall_2_counter < (hall_2_target - 1):
                cur_time = time.time()
                if not (self.motor_2_direction == 2 and cur_time - time_2 < 1):
                    motor.Go_2()
                    self.motor_2_direction = 1
                    # print("In Master_controller main loop, motor.Go_2")

            if self.hall_2_counter > (hall_2_target + 1):
                cur_time = time.time()
                if not (self.motor_2_direction == 1 and cur_time - time_2 < 1):
                    motor.Back_2()
                    self.motor_2_direction = 2
                    # print("In Master_controller main loop, motor.Back_2")

            if self.my_equal(self.hall_1_counter, hall_1_target):
                motor.Stop_1()
                if (self.motor_1_direction != 0):
                    self.Last_direction_x = self.motor_1_direction
                    self.motor_1_direction = 0
                    time_1 = time.time()
                # print("In Master_controller main loop, motor.Stop_1")
                # print("In Master_controller, hall_1_counter = ", self.hall_1_counter, ", hall_1_target = ", int(hall_1_target))

            if self.my_equal(self.hall_2_counter, hall_2_target):
                motor.Stop_2()
                if (self.motor_2_direction != 0):
                    self.Last_direction_y = self.motor_2_direction
                    self.motor_2_direction = 0
                    time_2 = time.time()
                # print("In Master_controller main loop, motor.Stop_2")
                # print("In Master_controller, hall_2_counter = ", self.hall_2_counter, ", hall_2_target = ", int(hall_2_target))

            # 平板坐标 --> 游戏显示
            # print("display_x_queue size = ", display_x_queue.qsize(), " display_y_queue size = ", display_y_queue.qsize())
            # if not display_queue.empty():
            #     temp_tuple = display_queue.get()
            #     temp_x = int(temp_tuple[0])
            #     temp_y = int(temp_tuple[1])
            #     print("in display loop, put x = ", temp_x, " put y = ", temp_y)
            #     Master_controller.myPut_size1(self, self.game_x_queue, temp_x)
            #     Master_controller.myPut_size1(self, self.game_y_queue, temp_y)


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
        EQUAL_BUFFER = 1
        if abs(a - b) < EQUAL_BUFFER:
            return True
        else:
            return False