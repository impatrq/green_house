from machine import Pin, ADC
from time import sleep

led = Pin(2, Pin.OUT)

def getLDR():
    adc = ADC(Pin(39))
    val_read = adc.read() * (3.3/4096)
    print("El valor de tensión del LDR es: {:.2f}" .format(val_read))
    RLDR = (val_read * 10000)/(3.3 - val_read)
    print("El valor de la resistencia del LDR es: {:.0f}" .format(RLDR))
    sleep(2)
    return val_read

while True:                                                                 #Si el valor de tension es menor a 2, se enciende un LED del micro
    if (getLDR() <= 2):
        led.on()
    else:
        led.off()
        
        
