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


class test_hall(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.HALL_1_PIN = 31
        self.hall_1_counter = 0

    def run(self):

        motor = Motor.Motor()

        GPIO.setup(self.HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.add_event_detect(self.HALL_1_PIN, GPIO.RISING, callback=self.hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行

        motor.Go_1()

        while True:
            if self.hall_1_counter > 1000:
                motor.Stop_1()
                print("reached 1000.")

    # 霍尔开关线程
    def hall_1_callback(self, channel1):
        if GPIO.event_detected(self.HALL_1_PIN):
            self.hall_1_counter = self.hall_1_counter + 1

runner = test_hall()
runner.run()