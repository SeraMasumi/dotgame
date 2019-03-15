#!/usr/bin/python
import RPi.GPIO as GPIO
import time
import threading
import queue
# import AD_reader
# from fake_rpi.RPi import GPIO as GPIO
# from fake_rpi import toggle_print
#
# toggle_print(False)


class AD_controller(threading.Thread):
    def __init__(self, display_queue, ads1256_controller):
        threading.Thread.__init__(self)
        self.chan_list_out = [33, 35, 36, 37, 38, 40]
        self.chan_list_in = [2, 3, 4]
        self.coordinate_x = 0
        self.coordinate_y = 0
        self.display_queue = display_queue
        # self.joystick_x_queue = joystick_x_queue
        # self.joystick_y_queue = joystick_y_queue
        # self.AD_reader_queue = queue.Queue()
        # self.AD_reader = AD_reader.AD_reader(self.AD_reader_queue, self.joystick_x_queue, self.joystick_y_queue)
        self.ads1256_controller = ads1256_controller

        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.chan_list_out, GPIO.OUT)

        # GPIO.setup(self.chan_list_in, GPIO.IN)

    def measure_x(self):
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(36, GPIO.LOW)
        GPIO.output(37, GPIO.HIGH)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.HIGH)

    def measure_y(self):
        GPIO.output(33, GPIO.LOW)
        GPIO.output(35, GPIO.LOW)
        GPIO.output(36, GPIO.HIGH)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(38, GPIO.HIGH)
        GPIO.output(40, GPIO.HIGH)

    def all_close(self):
        GPIO.output(33, GPIO.HIGH)
        GPIO.output(35, GPIO.HIGH)
        GPIO.output(36, GPIO.HIGH)
        GPIO.output(37, GPIO.LOW)
        GPIO.output(38, GPIO.LOW)
        GPIO.output(40, GPIO.LOW)

    def run(self):
        # self.AD_reader.start()

        TABLET_X_MIN = 1360000
        TABLET_X_MAX = 4184000
        TABLET_Y_MIN = 1561800
        TABLET_Y_MAX = 4208200
        PYGAME_RESOLUTION_X = 1024
        PYGAME_RESOLUTION_Y = 768

        while True:

            input_x_value_tablet = -1
            input_y_value_tablet = -1
            
            # 测量平板xy
            AD_controller.all_close(self)
            AD_controller.measure_x(self)
            time.sleep(0.5)

            input_x_value_tablet = self.ads1256_controller.ADS1256_GetoneChannel(2)
            self.coordinate_x = PYGAME_RESOLUTION_X - (TABLET_X_MAX - input_x_value_tablet) / (TABLET_X_MAX - TABLET_X_MIN) * PYGAME_RESOLUTION_X
            print("in AD_controller, get input_x_value_tablet = ", input_x_value_tablet)

            # if(not self.AD_reader_queue.empty()):
            #     input_x_value_tablet = self.AD_reader_queue.get()
            #     # print("in AD_controller, get input_x_value_tablet = ", input_x_value_tablet)
            #     self.coordinate_x = PYGAME_RESOLUTION_X - (TABLET_X_MAX - input_x_value_tablet) / (TABLET_X_MAX - TABLET_X_MIN) * PYGAME_RESOLUTION_X

            AD_controller.all_close(self)
            AD_controller.measure_y(self)
            time.sleep(0.5)

            input_y_value_tablet = self.ads1256_controller.ADS1256_GetoneChannel(2)
            self.coordinate_y = (TABLET_Y_MAX - input_y_value_tablet) / (TABLET_Y_MAX - TABLET_Y_MIN) * PYGAME_RESOLUTION_Y

            AD_controller.myPut_size1(self, self.display_queue, (self.coordinate_x, self.coordinate_y))


            # if(input_x_value_tablet != -1 and (not self.AD_reader_queue.empty())):
            #     input_y_value_tablet = self.AD_reader_queue.get()
            #     # print("in AD_controller, get input_y_value_tablet = ", input_y_value_tablet)
            #     self.coordinate_y = (TABLET_Y_MAX - input_y_value_tablet) / (TABLET_Y_MAX - TABLET_Y_MIN) * PYGAME_RESOLUTION_Y
            #     # self.display_queue.put((self.ratio_x, self.ratio_y))
            #     AD_controller.myPut_size1(self, self.display_queue, (self.coordinate_x, self.coordinate_y))
            #     # print("after put, ratio_x = ", self.coordinate_x, " ratio_y = ", self.coordinate_y)

    def myPut_size1(self, queue, element):
        QSIZE = 1
        if(queue.qsize() >= QSIZE):
            queue.queue.clear()
        queue.put(element)