try:
  import usocket as socket
except:
  import socket
  
from lcd_api import LcdApi
from i2c_lcd import I2cLcd
from machine import Pin, SoftI2C
import network
from dht import DHT11

import esp
esp.osdebug(None)

import gc
gc.collect()

def getDHT():
    dht = DHT11(Pin(9))
    dht.measure()
    print(dht.temperature())

ssid = 'Casa 2.4'
password = '24091999Juan'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

def lcdInit(network):
    i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)
    lcd = I2cLcd(i2c, 0x27, 2, 16)
    lcd.putstr("Escriba Online: ")
    lcd.cursor_pos = (1, 0) 
    lcd.putstr(network)

while station.isconnected() == False:
  networkRslt = 'Connection unsuccessful'
  print(networkRslt)
  pass

network = station.ifconfig()
networkRslt = 'Connection successful'
print(networkRslt)
print(network[0])
lcdInit(network[0])                                 #ifconfig() devuelve una tupla, con [0] accedo a la IP ADDRESS
led = Pin(2, Pin.OUT)
led.on()
