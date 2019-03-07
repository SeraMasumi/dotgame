#!/usr/bin/python
import RPi.GPIO as GPIO
import threading
import queue
import AD_reader
# from fake_rpi.RPi import GPIO as GPIO
# from fake_rpi import toggle_print
#
# toggle_print(False)


class AD_controller(threading.Thread):
    def __init__(self, display_x_queue, display_y_queue, joystick_x_queue, joystick_y_queue):
        threading.Thread.__init__(self)
        self.chan_list_out = [33, 35, 36, 37, 38, 40]
        self.chan_list_in = [2, 3, 4]
        self.ratio_x = 0
        self.ratio_y = 0
        self.display_x_queue = display_x_queue
        self.display_y_queue = display_y_queue
        self.joystick_x_queue = joystick_x_queue
        self.joystick_y_queue = joystick_y_queue
        self.AD_reader = AD_reader.AD_reader(self.joystick_x_queue, self.joystick_y_queue)

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list_out, GPIO.OUT)
        '''
        GPIO.setup(self.chan_list_in, GPIO.IN)
        '''


    def measure_x(self):
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(36, GPIO.HIGH)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.HIGH)

    def measure_y(self):
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.HIGH)
        GPIO.output(40, GPIO.HIGH)

    def all_close(self):
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.LOW)

    def run(self):
        self.AD_reader.start()

        # 主循环
        #   测x
        #   清零
        #   测y
        #   由电压比值计算xy坐标
        TABLET_X_MIN = 1363000
        TABLET_X_MAX = 4218000
        TABLET_Y_MIN = 975000
        TABLET_Y_MAX = 2322000
        input_x_value_tablet = 0
        input_y_value_tablet = 0
        input_x_value_joystick = 0
        input_y_value_joystick = 0
        while True:
            '''
            # 测量平板xy
            AD_controller.measure_x(self)
            input_x_value_tablet = self.AD_reader.AD_tablet_value
            print("in AD_controller, get input_x_value_tablet = ", input_x_value_tablet)
            AD_controller.all_close(self)
            AD_controller.measure_y(self)
            input_y_value_tablet = self.AD_reader.AD_tablet_value
            print("in AD_controller, get input_y_value_tablet = ", input_y_value_tablet)

            # 计算要显示的xy坐标
            self.ratio_x = (TABLET_X_MAX - input_x_value_tablet) / (TABLET_X_MAX - TABLET_X_MIN)
            self.ratio_y = (TABLET_Y_MAX - input_y_value_tablet) / (TABLET_Y_MAX - TABLET_Y_MIN)

            self.display_x_queue.put(self.ratio_x)
            # print("in AD_controller, ratio_x put in queue. display ratio_x = ", self.ratio_x)
            self.display_y_queue.put(self.ratio_y)
            # print("in AD_controller, ratio_y put in queue. display ratio_y = ", self.ratio_y)
            '''

            # print("in AD_controller, joystick_x_queue size = ", self.joystick_x_queue.qsize())
            # print("in AD_controller, joystick_y_queue size = ", self.joystick_y_queue.qsize())

            # 测量手柄xy
            # if ((not self.AD_reader.AD_joystick_x_queue.empty()) and (not self.AD_reader.AD_joystick_y_queue.empty())):
            #     input_x_value_joystick = self.AD_reader.AD_joystick_x_queue.get()
            #     input_y_value_joystick = self.AD_reader.AD_joystick_y_queue.get()
            #     self.joystick_x_queue.put(input_x_value_joystick)
            #     print("in AD_controller, input_x_value_joystick put in queue. display input_x_value_joystick = ",
            #           input_x_value_joystick)
            #     self.joystick_y_queue.put(input_y_value_joystick)
            #     print("in AD_controller, input_y_value_joystick put in queue. display input_y_value_joystick = ",
            #           input_y_value_joystick)
