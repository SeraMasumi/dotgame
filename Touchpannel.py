import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BOARD)
chan_list = [32,33,35,36,37,38,40]
GPIO.setup(chan_list, GPIO.OUT)

while True:
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)
    
    print('X auflesen')
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(36, GPIO.HIGH)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.HIGH)
    time.sleep(2)

    GPIO.output(32, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)
    
    print('Y auflesen')
    GPIO.output(32, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(38, GPIO.HIGH)
    GPIO.output(40, GPIO.HIGH)
    time.sleep(2)

GPIO.cleanup()
