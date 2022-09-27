#                                           // GREENHOUSE //
#
#   El proyecto se basa en un sistema de control mediante sensores y actuadores. 
#   Se utilizan: DHT22, LDRs, HL69.
#   Protocolo Web: Socket




from hashlib import sha1
from machine import Pin, ADC, Timer, RTC
from time import sleep
import _thread, dht, socket, ntptime

#Init de sensores
sensor = dht.DHT22(Pin(32))
adcLDR1 = ADC(Pin(39))
adcLDR2 = ADC(Pin(34))
adcHL = ADC(Pin(35))
relayValve= Pin(25, Pin.OUT)
relayCoolers = Pin(26, Pin.OUT)
relayLights = Pin(33, Pin.OUT)
relayValve.value(0)
relayCoolers.value(0)
relayLights.value(0)

#Definicion variables
soilPercentage = 0
soilHumidity = 0
ldrState = ""
temp = 0
hum = 0
date = ""

lock = _thread.allocate_lock()                                  # El código tiene dos hilos, uno mide con los sensores, y el otro espera una conexion
                                                                # de un socket. Ambos trabajan de manera independiente mediante locks (semaphores)
def setNetwork():
    lock.acquire()
    print("Initializing WebServer. Awaiting Connection...")
    conn, addr = s.accept()                                     # Espera una conexion mediante un socket
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)
    request = str(request)
    print(request)
    update = request.find('/update')                            # Busca /update en URL     
       
    if update == 6:
        print('update') 
        
    response = webPage()                                        # Abre el HTML en la pagina
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)                                      # Envia el HTML
    conn.close()
    print("Releasing lock from network...")
    lock.release()                                                             

def getSensors():                                            # getSensors es una funcion que engloba todas las funciones que toman resultados de mediciones
    lock.acquire()                                           # Toma el lock para no sobre escribir/tomar mal datos
    print("Initializing sensors...")
    getLDR()
    getHL()
    getDHT()
    lock.release()


def getLDR():
    global ldrState
    ldrRead1 = adcLDR1.read() * (3.3/4096)                                          # Conversion ADC // valor lectura
    RLDR1 = (ldrRead1 * 10000)/(3.3 - ldrRead1)
    print("El valor de la resistencia del LDR1 es: {:.0f}" .format(RLDR1))
    
    ldrRead2 = adcLDR2.read() * (3.3/4096)                                           # 1000 ya está iluminado (full)
    RLDR2 = (ldrRead2 * 10000)/(3.3 - ldrRead2)                                      # 40952430 está oscuro (full)
    print("El valor de la resistencia del LDR2 es: {:.0f}" .format(RLDR2))

    ldrAverage = (RLDR1 + RLDR2) / 2                                                 # Calculo promedio de iluminacion entre ambos LDR // WIP
    print("Valor promedio LDRs: ", ldrAverage)
    if(ldrAverage > 10000000):
        ldrState = "Oscuro"
    else:
        ldrState = "Iluminado"
    sleep(1)

def getHL():
    adcHL.atten(ADC.ATTN_11DB)                                                        # La atenuacion tuvo que ser cambiada para poder tener mejores
    HLRead= adcHL.read()                                                              # Valores de lectura con el ADC.
    sleep(1)
    global soilHumidity
    global soilPercentage
    soilHumidity = HLRead
    max_moisture=65535
    min_moisture=0
    soilPercentage = (max_moisture-adcHL.read_u16())*100/(max_moisture-min_moisture)
    soilPercentage = (int(soilPercentage))
    print(soilPercentage)
    #print("moisture: " + "%.2f" % soilPercentage +"% (adc: "+str(adcHL.read_u16())+")")
    #print("La humedad de suelo: " ,soilHumidity)
        
def getDHT():
    global temp, hum
    temp = hum = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        hum = int(hum)
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        return('Failed to read sensor.')

def getStates(timer):                                                                 # Esta es la funcion que el timer activa cada vez que se triggerea mismo, se trata de una funcion que pregunta por el estado de los sensores    
    getLDR()
    getHL()
    getDHT()
    watering()                                                                        
    lighting()
    cooling()
    
def lighting():
    global ldrState
    if(ldrState == "Oscuro"):
        print("Debo iluminar")
    else:
        print("No debo iluminar")

def watering():
    optimalHumidity = 2200
    loopState = True
    global soilHumidity
    print(soilHumidity)
    if(int(soilHumidity) >= optimalHumidity):
        print("Debo regar")
        relayValve.value(1)                               #Activates Water Valve to start watering
        getTime()
        sleep(5)
        getHL()
        while(loopState):
            sleep(5)
            if(int(soilHumidity) >= optimalHumidity):
                relayValve.value(1)
                loopState = True
                print("Debo volver a regar")
                getHL()
            else:
                relayValve.value(0)
                loopState = False
                print("No debo volver a regar")

    else:
        print("No debo regar")
    soilHumidity = str(soilHumidity)
    
def cooling():
    optimalTemp = 20
    global temp
    if(int(temp) > optimalTemp):
        print("Hace calor")
    elif(int(temp) == optimalTemp):
        print("No hacer nada")
    else:
        print("Hace frio")
        
def getTime():
    """
    Utility: 
    
    """
    global date
    rtc = RTC()
    ntptime.settime()
    currentDate = rtc.datetime()
    currentDay = currentDate[2]
    currentMonth = currentDate[1]
    currentHour = int(currentDate[4]) - 3                       #-3 because of GMT-3 for Argentina
    currentMinute = int(currentDate[5])
    currentSecond = int(currentDate[6])
    completeHour = str(currentHour) + ":" + str(currentMinute)  # Hours + Minutes
    completeDate = str(currentDay) + "/" + str(currentMonth)    # Day + Month
    date = completeDate + " - " + completeHour                  # Complete Date (Time and Day)
    
def webPage():
    global soilPercentage, ldrState, temp, hum, date
    temp = str(temp)
    hum = str(hum)
    soilHumidity = str(soilPercentage)
    soilPercentage = str(soilPercentage)
    date = str(date)
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
                    }}

                    .contenedor {{
                        margin: 0 auto;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        border-radius: 5rem;
                        max-width: fit-content;
                        padding: 0 2rem;
                        height: fit-content;
                        background-color: rgba(0, 0, 0, 0.2);
                        box-sizing: border-box;
                    }}

                    .contenedor h2 {{
                        color: white;
                        text-align: center;
                        font-size: 2.5rem;
                    }}

                    .contenedor-variables {{
                        /*display: grid;
                        grid-template-columns: repeat(2, 1fr);
                        grid-gap: 0 1rem;
                        font-size: 1.5rem;
                        color: white;*/
                        display: flex;
                        flex-direction: column;
                        font-size: 1.5rem;
                        color: white;
                        gap: 0.7rem;
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
                        white-space: nowrap;
                    }}
                    
                    @media (max-width: 768px) {{
                        
                        .contenedor-variables {{
                            font-size: 1.25rem;
                            width: 100%;
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
                            <div class="datos mover"><label for="temp">Temperatura ambiente</label><meter id="temp" value ="{temp}" min="0" max="50"></meter><p>{temp + " °C"}</p></div>
                            <div class="datos"><label for="hum">Humedad ambiente</label><meter id="hum" value="{hum}" min="0" max="100"></meter><p>{hum + " %"}</p></div>
                            <div class="datos"><label for="hum_tierra">Humedad de la tierra</label><meter low="0" high="100" min="0" max="100" value= "{soilPercentage}" id="hum_tierra"></meter><p>{soilPercentage + " %"}</p></div>
                            <div class="datos"><label for="lum">Luminosidad:</label><p>{ldrState}</p></div>
                            <div class="datos"><label for="riego">Última vez regado: </label><p>{date}</p></div>
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

tim0 = Timer(0)                                                               # Este timer se activa cada 1 hora (3600000 milisegundos)  // 10000 ms TEST        
tim0.init(period=30000, mode=Timer.PERIODIC, callback=getStates)              # para verificar el estado    

while True:
        print("Hilo 0")  
        setNetwork()
        print("Hilo 1")
        _thread.start_new_thread(getSensors, ())
