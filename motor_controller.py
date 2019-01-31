import fake_rpi.RPi.GPIO as GPIO # Replace libraries by fake ones
# import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)

chan_list_out = [32,33,35,36,37,38,40]
GPIO.setup(chan_list_out, GPIO.OUT)

chan_list_in = [2,3,4]
GPIO.setup(chan_list_out, GPIO.IN)

touchpannel_value_x = 0
touchpannel_value_y = 0

def measure_x():
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.LOW)
    GPIO.output(36, GPIO.HIGH)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.HIGH)

def measure_y():
    GPIO.output(32, GPIO.LOW)
    GPIO.output(33, GPIO.LOW)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(37, GPIO.HIGH)
    GPIO.output(38, GPIO.HIGH)
    GPIO.output(40, GPIO.HIGH)

def all_close():
    GPIO.output(32, GPIO.HIGH)
    GPIO.output(33, GPIO.HIGH)
    GPIO.output(35, GPIO.HIGH)
    GPIO.output(36, GPIO.LOW)
    GPIO.output(37, GPIO.LOW)
    GPIO.output(38, GPIO.LOW)
    GPIO.output(40, GPIO.LOW)

while(True):
    measure_x()
    if(GPIO.input(2)):
        touchpannel_value_x = ???
