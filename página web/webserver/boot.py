try:
  import usocket as socket
except:
  import socket

from machine import Pin
import network

import esp
esp.osdebug(None)

import gc
gc.collect()

ssid = 'iPhone de Juan'
password = 'ejemplo0409'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
  print('Connection unsuccessful')
  pass

print('Connection successful')
print(station.ifconfig())

led = Pin(2, Pin.OUT)
led.on()


