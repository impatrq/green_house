from hashlib import sha1
from machine import Pin, ADC, Timer, RTC
from time import sleep
import _thread, dht, socket, ntptime

#Init de sensores
sensor = dht.DHT22(Pin(09))
adcLDR1 = ADC(Pin(39))
adcLDR2 = ADC(Pin(34))
adcHL = ADC(Pin(36))
relayValvula = Pin(27, Pin.OUT)
relayVentiladores = Pin(25, Pin.OUT)
relayLuces = Pin(32, Pin.OUT)

#Definicion variables
humedadSuelo = ""
ldrEstado = ""
temp = ""
hum = ""

lock = _thread.allocate_lock()
        
def setNetwork():
    lock.acquire()
    print("Inicializando WebServer. Esperando Conexion...")
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
    #tim0 =Timer(0)
    #tim0.init(period=10000, mode=Timer.PERIODIC, callback=getEstados)         #Este timer se activa cada 1 hora (3600000 milisegundos)                                                            #de la humedad del suelo
    lock.release()                                                             #para verificar el estado

def getSensors():
    lock.acquire()
    print("Inicializando sensores...")
    getLDR()
    getHL()
    getDHT()
    lock.release()

def getLDR():
    global ldrEstado
    ldrRead1 = adcLDR1.read() * (3.3/4096)
    RLDR1 = (ldrRead1 * 10000)/(3.3 - ldrRead1)
    print("El valor de la resistencia del LDR1 es: {:.0f}" .format(RLDR1))
    
    ldrRead2 = adcLDR2.read() * (3.3/4096)         # 1000 ya está iluminado (full)
    RLDR2 = (ldrRead2 * 10000)/(3.3 - ldrRead2)    # 40952430 está oscuro (full)
    print("El valor de la resistencia del LDR2 es: {:.0f}" .format(RLDR2))

    ldrPromedio = (RLDR1 + RLDR2) / 2
    print("El promedio es: ", ldrPromedio)
    if(ldrPromedio > 2000):
        ldrEstado = " Oscuro"
    else:
        ldrEstado = " Iluminado"
    sleep(1)

def getHL():
    adcHL.atten(ADC.ATTN_11DB)
    HLRead= adcHL.read()
    sleep(1)
    global humedadSuelo
    humedadSuelo = str(HLRead)
    print("La humedad de suelo: " ,humedadSuelo)
        
def getDHT():
  global temp, hum
  temp = hum = 0
  try:
    sensor.measure()
    temp = sensor.temperature() 
    hum = sensor.humidity()
    temp = str(temp)
    hum = str(hum)
  except OSError as e:
    return('Failed to read sensor.')

def getEstados(timer):
    watering()
    lighting()
    cooling()
    
def lighting():
    global ldrEstado
    if(ldrEstado == false):
        print("Debo iluminar")
    else:
        print("No debo iluminar")

def watering():
    optimalHumidity = 800
    global humedadSuelo
    if(humedadSuelo >= optimalHumidity):
        print("Debo regar")
        getTime()
    else:
        print("No debo regar")
    
def cooling():
    optimalTemp = 20
    global temp
    if(temp > optimalTemp):
        print("Hace calor")
    elif(temp == optimalTemp):
        print("No hacer nada")
    else:
        print("Hace frio")
        
def getTime():
    rtc = RTC()
    fecha = rtc.datetime()
    fechaActual = fecha[4:6]
    print(str(fechaActual))
    
def webPage():
    global humedadSuelo, ldrEstado, temp, hum
    html = f"""
            <!DOCTYPE html>
            <html lang="es">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <link rel="preconnect" href="https://fonts.googleapis.com">
                <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
                <link href="https://fonts.googleapis.com/css2?family=Jost&display=swap" rel="stylesheet">
                <link rel="icon" href="https://i.ibb.co/BVqKJ0z/Frame-22-1.png"> 
                <style>
                    html {{
                        box-sizing: border-box;
                    }}

                    *, *:before, *:after {{
                        box-sizing: inherit;
                    }}

                    body {{
                        margin: 0%;
                        font-size: 62.5%;
                        font-family: 'Jost', sans-serif;
                    }}

                    main {{
                        height: 100vh;
                        background-image: url("https://i.ibb.co/C8Q6ddJ/Background-Guias.png");
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    }}

                    .contenedor {{
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        border-radius: 5rem;
                        max-width: fit-content;
                        height: fit-content;
                        padding: 0 5% 0 5%;
                        background-color: rgba(0, 0, 0, 0.2);
                    }}

                    .contenedor h2 {{
                        color: white;
                        text-align: center;
                        font-size: 2.5rem;
                    }}
                    .contenedor-variables {{
                        display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        grid-gap: 0 1rem;
                        font-size: 1.5rem;
                        color: white;
                    }}

                    label {{
                        display: inline;
                        margin-left: 0;
                    }}

                    meter {{
                        margin-left: 1rem;
                    }}

                    h1 {{
                        font-size: 2.5rem;
                        text-align: center;
                        color: white;
                        font-weight: 700;
                    }}

                    h2 {{
                        font-weight: lighter;
                    }}

                    .datos {{
                        display: flex;
                        justify-content: flex-start;
                        align-items: center;
                    }}
                    
                    #boton {{
                        margin-top: 2rem;
                        margin-bottom: 2rem;
                    }}
                        
                    #boton button {{
                        border: none;
                        border-radius: 1rem;
                        padding: 1rem;
                        color: #347e49;
                        font-size: 1rem;
                        font-weight: bolder;
                        cursor:pointer;
                    }}
                    
                    .datos p {{
                        margin: 0 0 0 1rem;
                    }}
                    
                    @media (max-width: 768px) {{
                        
                        .contenedor-variables {{
                            display: flex;
                            flex-direction: column;
                        }}
                    }}
                    
                </style>
                <title>Mi invernadero</title>
            </head>
            <body>
                <main>
                    <h1>Mi invernadero</h1>
                    <div class="contenedor">
                        <h2>Datos</h2>
                        <div class="contenedor-variables">
                            <div class="datos"><label for="temp">Temperatura ambiente</label><meter id="temp" value ="{temp}" min="0" max="50"></meter><p>{temp + " °C"}</p></div>
                            <div class="datos"><label for="hum">Humedad ambiente</label><meter id="hum" value="{hum}" min="0" max="100"></meter><p>{hum + " %"}</p></div>
                            <div class="datos"><label for="hum_tierra">Humedad de la tierra</label><meter optimum="1000" high="3000" min="1" max="4095" value= "{humedadSuelo}" id="hum_tierra"></meter></div>
                            <div class="datos"><label for="lum">Luminosidad:</label><p>{ldrEstado}</p></div>
                            <div class="datos"><label for="riego">Última vez regado:</label><p></p></div>
                        </div>
                        <div id= "boton">
                            <a href="/update"><button>Actualizar Datos</button></a>
                        </div>
                    </div>
                </main>
            </body>
            </html>
            """
    return html
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

while True:
        print("Hilo 0")  
        setNetwork()
        print("Hilo 1")
        _thread.start_new_thread(getSensors, ())