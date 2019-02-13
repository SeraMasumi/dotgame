#!/usr/bin/python
# import RPi.GPIO as GPIO
from fake_rpi.RPi import GPIO as GPIO
import threading
import queue

class AD_controller(threading.Thread):
    def __init__(self, display_x_queue, display_y_queue, joystick_x_queue, joystick_y_queue):
        threading.Thread.__init__(self)
        self.TABLET_IN_PIN = 2
        self.chan_list_out = [32, 33, 35, 36, 37, 38, 40]
        self.chan_list_in = [2, 3, 4]
        self.ratio_x = 0
        self.ratio_y = 0
        self.display_x_queue = display_x_queue
        self.display_y_queue = display_y_queue
        self.joystick_x_queue = joystick_x_queue
        self.joystick_y_queue = joystick_y_queue

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list_out, GPIO.OUT)
        GPIO.setup(self.chan_list_in, GPIO.IN)

    def measure_x(self):
        GPIO.output(32, GPIO.HIGH)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(36, GPIO.HIGH)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.HIGH)

    def measure_y(self):
        GPIO.output(32, GPIO.LOW)
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.HIGH)
        GPIO.output(40, GPIO.HIGH)

    def all_close(self):
        GPIO.output(32, GPIO.HIGH)
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.LOW)

    def run(self):
        # 主循环
        #   测x
        #   清零
        #   测y
        #   由电压比值计算xy坐标
        TABLET_X_MIN = 000
        TABLET_X_MAX = 000
        TABLET_Y_MIN = 000
        TABLET_Y_MAX = 000
        input_x_value_tablet = 0
        input_y_value_tablet = 0
        input_x_value_joystick = 0
        input_y_value_joystick = 0
        while True:
            # 测量平板xy
            AD_controller.measure_x()
            input_x_value_tablet = 读AD
            AD_controller.all_close()
            AD_controller.measure_y()
            input_y_value_tablet = 读AD

            # 计算要显示的xy坐标
            self.ratio_x = (TABLET_X_MAX - input_x_value_tablet) / (TABLET_X_MAX - TABLET_X_MIN)
            self.ratio_y = (TABLET_Y_MAX - input_y_value_tablet) / (TABLET_Y_MAX - TABLET_Y_MIN)

            self.display_x_queue.put(self.ratio_x)
            self.display_y_queue.put(self.ratio_y)

            # 测量手柄xy
            input_x_value_joystick = 读AD
            input_y_value_joystick = 读AD

            self.joystick_x_queue.put(input_x_value_joystick)
            self.joystick_y_queue.put(input_y_value_joystick)
