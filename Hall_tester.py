import RPi.GPIO as GPIO
from time import sleep

HALL_1_PIN = 99  # 把这两个99替换成霍尔开关的端口
HALL_2_PIN = 99

hall_1_counter = 0
hall_2_counter = 0

GPIO.setmode(GPIO.BCM)
GPIO.setup(HALL_1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(HALL_2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# 霍尔开关线程
def hall_1_callback(channel1):
    global hall_1_counter
    if GPIO.event_detected(HALL_1_PIN):
        hall_1_counter = hall_1_counter + 1
        print("Hall 1 counter value = " + str(hall_1_counter))


def hall_2_callback(channel2):
    global hall_2_counter
    if GPIO.event_detected(HALL_2_PIN):
        hall_2_counter = hall_2_counter + 1
        print("Hall 2 counter value = " + str(hall_2_counter))


GPIO.add_event_detect(HALL_1_PIN, GPIO.RISING, callback=hall_1_callback)  # 会为回调函数另外开启一个线程，与主程序并发运行
GPIO.add_event_detect(HALL_2_PIN, GPIO.RISING, callback=hall_2_callback)


try:
    print("detecting edge...")
    sleep(30)  # 三十秒测试时间，可调整
    print("time up, exiting...")

finally:
    GPIO.cleanup()
