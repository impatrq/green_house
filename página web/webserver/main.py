from hashlib import sha1
import socket
from dht import DHT11
from machine import Pin, ADC
from time import sleep

s1 = "24"
s2 = "59"
s3 = "48"   
s4 = "100" 

def getDHT():
        dht =DHT11(Pin(09))
        dht.measure()
        print("La temp es: " ,dht.temperature)
        sleep(3)
        

def getLDR():                                               
    adc = ADC(Pin(39))
    val_read = adc.read() * (3.3/4096)
    print("El valor de tensión del LDR es: {:.2f}" .format(val_read))
    RLDR = (val_read * 10000)/(3.3 - val_read)
    print("El valor de la resistencia del LDR es: {:.0f}" .format(RLDR))
    sleep(3)

def webPage():

    html = """
    
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta http-equiv="X-UA-Compatible" content="IE=edge">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Document</title>
        </head>
        <body>
            <h1>ESP32 Web Server</h1>
            <p>Medicion de sensores</p>
            <table>
                <tbody>
                    <tr>
                        <td>
                            <p>Sensor 1</p>
                        </td>
                        <td>
                            <strong> 59 %</strong>
                            <meter id="fuel" min="0" max="100" low="30" high="70" optimum="80" value="59">
                                at 50/100
                            </meter>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>Sensor 2</p>
                        </td>
                        <td>
                            <strong>14%</strong>
                            <meter id="fuel" min="0" max="100" low="30" high="70" optimum="80" value="14">
                                at 50/100
                            </meter>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>Sensor 3</p>
                        </td>
                        <td>
                            <strong> 20%</strong>
                            <meter id="fuel" min="0" max="100" low="30" high="70" optimum="80" value="20">
                                at 50/100
                            </meter>
                        </td>
                    </tr>
                    <tr>
                        <td>
                            <p>Sensor 4</p>
                        </td>
                        <td>
                            <strong> 90%</strong>
                            <meter id="fuel" min="0" max="100" low="30" high="70" optimum="80" value="90">
                                at 50/100
                            </meter>
                        </td>
                    </tr>
                </tbody>
            </table>
        </body>
        </html>
    
    """
    
    return html
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)


while True:
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)   
        update = request.find('/update')        
        
        if update == 6:
            print('update') 
            
        response = webPage()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print(e)

