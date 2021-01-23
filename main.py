from machine import Pin, Timer
from config import app_config, blynk_config
from webserver import webcam
from boot import sta_if, buzzer
import blynklib

server = webcam()
server.run(app_config)

LED = Pin(app_config["led"], Pin.OUT)

blynk = blynklib.Blynk(blynk_config["auth_token"])

@blynk.handle_event('write V4')
def write_virtual_pin_handler(pin, value):
    if(int(value[0])):
        LED.on()
    else:
        LED.off()

@blynk.handle_event('read V0')
def read_virtual_pin_handler(pin):
    blynk.virtual_write(pin, sta_if.ifconfig()[0])

def button_pressed(p):
    @blynk.handle_event("connect")
    def connect_handler():
        blynk.email('msabra388@gmail.com', 'Someone is at your door!', '')
        blynk.notify('Someone is at your door!')

def debounce(h):
    timer.init(mode=Timer.ONE_SHOT, period=300, callback= button_pressed)

buzzer.irq(handler=debounce, trigger=Pin.IRQ_FALLING)

timer = Timer(0)

while(True):
    blynk.run()