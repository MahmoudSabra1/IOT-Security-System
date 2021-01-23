from machine import Pin
import config
import network
import utime
import ntptime
import camera

sta_if = network.WLAN(network.STA_IF)
buzzer = Pin(config.app_config["button"], Pin.IN, Pin.PULL_UP)

def do_connect():
    start = utime.time()
    timed_out = False

    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(config.wifi_config["ssid"], config.wifi_config["password"])
        while not sta_if.isconnected() and \
            not timed_out:        
            if utime.time() - start >= 20:
                timed_out = True
            else:
                pass

    if sta_if.isconnected():
        ntptime.settime()
        print('network config:', sta_if.ifconfig())
    else: 
        print('internet not available')

do_connect()