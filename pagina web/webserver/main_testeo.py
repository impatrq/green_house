#                                           // GREENHOUSE PROJECT//
#
#   This project is based on a control system using sensors and relays that trigger a cooling, lighting and watering system.
#   It uses: DHT22 (temperature, humidity), LDRs (light), HL69 (soil moisture).
#   Web Protocol: Socket


from hashlib import sha1
from machine import Pin, ADC, Timer, RTC
from time import sleep
import _thread, dht, socket, ntptime

#Declaration of PINS and relay values are set to Off on start.
sensor = dht.DHT22(Pin(32))
adcLDR1 = ADC(Pin(39))
adcLDR2 = ADC(Pin(34))
adcHL = ADC(Pin(35))
relayValve= Pin(25, Pin.OUT)
relayCoolers = Pin(33, Pin.OUT)
relayLights = Pin(26, Pin.OUT)
waterLevel = Pin(5, Pin.IN)

relayValve.value(1)
relayCoolers.value(1)
relayLights.value(1)

#Global Variables used by webpage(). They're global to be used inside each function. Most of these functions need to share data between them.
soilPercentage = 0
soilHumidity = 0
ldrState = ""
loopStateLDR = True
loopStateTemp = True
temp = 0
hum = 0
date = ""
lock = _thread.allocate_lock()                                  # This code uses 2 threads, the first one reads all the sensor data and the other one waits for connection
                                                                # from a socket. Each of them are using a lock to prevent that to get wrong values.
def setNetwork():
    """

    Utility: This function is called to initialize the WebServer. It looks for a connection from a socket. If true, it sends the webpage() return value as
    a html file. It works with locks as semaphores to prevent that to get null data, or even old values.
    
    Takes: None
    
    Returns: None
    
    """
    lock.acquire()
    print("Initializing WebServer. Awaiting Connection...")
    conn, addr = s.accept()                                     # Waits for a connection from a socket (IP from DISPLAY 16x2)
    print('Got a connection from %s' % str(addr))
    request = conn.recv(1024)                                   #It sets the amount of information (1024 bytes) that can be sent at once.
    request = str(request)
    print(request)
    update = request.find('/update')                            # Looks for "/update" on the URL from the WebServer      
       
    if update == 6:
        print('update') 
        
    response = webPage()                                        # Uses the webpage() function return value to open it as a HTML file.
    conn.send('HTTP/1.1 200 OK\n')
    conn.send('Content-Type: text/html\n')
    conn.send('Connection: close\n\n')
    conn.sendall(response)                                      # Sends the HTML file to the WebServer
    conn.close()
    print("Releasing lock from network...")
    lock.release()                                                             

def getSensors():                                            
    """

    Utility: This function is called everytime Thread 1 is initialized. It contains all the functions that read sensor values. It also uses locks, to prevent 
    from being read by the WebServer. After reading the sensor values, it'll leave the lock, ready to be used for setNetwork().
    
    Takes: None
    
    Returns: None
    
    """
    lock.acquire()                                           
    print("Initializing sensors...")
    getLDR()
    getHL()
    getDHT()
    lock.release()


def getLDR():
    """

    Utility: This function is called by getSensors(), it gets LDR state from an ADC conversion. It works with 2 ADC inputs (2 LDRs), and it sums them up to get
    an average. It sets a boolean variable: On or Off.
    
    Takes: None
    
    Returns: It works with a global variable ldrState. Later, they it'll be used by getHTML().
    
    """
    global ldrState
    ldrRead1 = adcLDR1.read() * (3.3/4096)                                          # ADC Conversion // Value
    RLDR1 = (ldrRead1 * 10000)/(3.3 - ldrRead1)
    print("El valor de la resistencia del LDR1 es: {:.0f}" .format(RLDR1))
    
    ldrRead2 = adcLDR2.read() * (3.3/4096)                                           
    RLDR2 = (ldrRead2 * 10000)/(3.3 - ldrRead2)                                      
    print("El valor de la resistencia del LDR2 es: {:.0f}" .format(RLDR2))

    ldrAverage = (RLDR1 + RLDR2) / 2                                                 
    print("Valor promedio LDRs: ", ldrAverage)
    if(ldrAverage <= 34000):
        ldrState = "Iluminado"
    else:
        ldrState = "Oscuro"
    sleep(1)

def getHL():
    """

    Utility: This function is called by getSensors(), it gets the soil moisture from an ADC. It needs an attenuation of 11dB to get proper results. 
    From this value, it calculates the percentage of moisture.
    
    Takes: None
    
    Returns: It works with global variables as soilHumidity (ADC Value) and soilPercentage (% of moisture). Later, they will be used by getHTML().
    
    """
    adcHL.atten(ADC.ATTN_11DB)                                                        
    HLRead= adcHL.read()                                                              
    sleep(1)
    global soilHumidity
    global soilPercentage
    soilHumidity = HLRead
    max_moisture=65535
    min_moisture=0
    soilPercentage = (max_moisture-adcHL.read_u16())*100/(max_moisture-min_moisture)
    soilPercentage = (int(soilPercentage))
    print(soilPercentage)
        
def getDHT():
    """

    Utility: This function is called by getSensors(), it gets the temperature and humidity.
    
    Takes: None
    
    Returns: It works with global variables as temp (temperature) and hum (humidity). Later, these variables will be used by getHTML().
    
    """
    global temp, hum
    temp = hum = 0
    try:
        sensor.measure()
        temp = sensor.temperature()
        temp = temp - 3                                          #It needs to be changed, 3 °C less to get the same temperature as in real life.
        hum = sensor.humidity()
        hum = int(hum)
        print('Temperature: %3.1f C' %temp)
        print('Humidity: %3.1f %%' %hum)
    except OSError as e:
        return('Failed to read sensor.')

def getStates(timer):
    """

    Utility: This function is a group of functions. Its purpose is to call all these functions to read the values from each sensor. This function is called by
    a timer (tim0), seconds after connecting with the WebServer's socket.
    
    Takes: To call this function, it needs the keyword "timer".
    
    Returns: None
    
    """
    getLDR()
    getHL()
    getDHT()
    watering()                                                                        
    lighting()
    cooling()
    
def lighting():
    """

    Utility: This function checks the LDR state every hour by getSensors(). It's in charge of activating the lighting relays in case the light isn't enough.
    Also, this function calls the tim1 to initialization in case the light isn't enough after 5 seconds.
    
    Parameters: None
    
    Returns: It works with global variables as ldrState and loopStateLDR. Later, these variables will be used by getHTML().
    
    """
    global ldrState
    global loopStateLDR
    loopStateLDR = True
    print("El estado del LDR es: ",ldrState)
    if(ldrState == "Oscuro"):
        print("Debo iluminar")
        relayLights.value(0)
        sleep(5)
        if(loopStateLDR):
            print("Inicio de conteo LDR...")
            tim1.init(period= 10000, mode=Timer.PERIODIC, callback=checkLighting)              # 1800000 ms as 30 minutes    
    else:
        print("No debo iluminar")
        relayLights.value(1)
        tim1.deinit()

def checkLighting(timer):
    """

    Utility: This function is called by tim1, this means the LDRs are not getting enough light, so the lighting system detected this issue. If it's dark, it'll light up the green house and 
    and every 30 minutes, it'll turn off the lights, wait 1 second and ask if there's enough light. If not, it'll continue with the lights on.
    
    Parameters: To call this function, it needs the keyword "timer".
    
    Returns: None
    
    """
    global ldrState
    global loopStateLDR
    relayLights.value(1)
    sleep(1)
    if(ldrState == "Oscuro"):
        relayLights.value(0)
        print("Sigue estando oscuro")
    else:
        print("Dejó de estar oscuro, luces apagadas")
        print("Apagando TIMER 1")
        tim1.deinit()
        relayLights.value(1)

def watering():
    """

    Utility: This function checks the soil moisture (it's triggered every hour by getSensors()). If it's lower than 2200, it means that soil is wet. If lower, soil is dry and it should start watering.
    After 5 seconds, it'll read the ADC Value from the sensor, and if it's still dry (and loopState is true), it'll water again activating the watering valve.
    It also has an emergency stop in case the water container has no water left.

    Takes: None
    
    Returns: None
    
    """
    optimalHumidity = 2200
    loopState = True
    global soilHumidity
    print(soilHumidity)
    if(int(soilHumidity) >= optimalHumidity):
        print("Debo regar")
        relayValve.value(0)                               #Activates Water Valve to start watering
        getTime()
        sleep(5)
        getHL()
        while(loopState):                                 #If loopState is true, it will start a loop until soil is wet.
            sleep(5)
            if(int(soilHumidity) >= optimalHumidity):
                relayValve.value(0)
                loopState = True
                print("Debo volver a regar")
                getHL()
            else:
                relayValve.value(1)
                loopState = False                         #When it doesn't need to keep watering, 
                print("No debo volver a regar")
    else:
        print("No debo regar")
    soilHumidity = str(soilHumidity)
    
    if(waterLevel.value(0)):                              #Emergency Stop if water pump has no water
        relayValve.value(1)

    
def cooling():
    """

    Utility: This function checks the temperature from the DHT22 (this function is called every hour by getSensors()). If it's higher than 22 °C, it triggers the cooling system, waits 5 seconds and
    if loopStateTemp is true, it means that after 5 seconds the temperature is still high, so it needs to start a timer (tim2) that will call CheckCooling()
    
    Takes: None
    
    Returns: None
    
    """
    optimalTemp = 22
    global temp
    loopStateTemp = True
    if(int(temp) > optimalTemp):
        print("Hace calor")
        relayCoolers.value(0)
        sleep(5)
        if(loopStateTemp):
            print("Inicio de conteo Temp...")
            tim2.init(period= 10000, mode=Timer.PERIODIC, callback=checkCooling)              # 1800000 ms // media hora para verificar el estado
            
    elif(int(temp) <= optimalTemp):
        print("Hace frio")
        
def checkCooling(timer):
    """

    Utility: This function is called by tim2. It checks if the DHT22 temperature, is lower or higher than 22 degrees °C. If it's higher the relay activates the cooling system. 
    If not, it stops the timer and turns off the relay.
    
    Takes: To call this function, it needs the keyword "timer".
    
    Returns: None
    
    """
    print("Check Cooling initialized")
    global temp
    global loopStateTemp
    relayCoolers.value(1)
    sleep(1)
    if(int(temp) > 22):
        relayCoolers.value(0)
        print("Sigue estando caliente")
    else:
        print("Dejó de estar caluroso, ventiladores apagados")
        print("Apagando TIMER 2")
        tim2.deinit()
        relayCoolers.value(1)
        
def getTime():
    """

    Utility: This function gets the current time based on the RTC (Real Time Clock) and the NTP (Network Time Protocol). 
    It gets a tuple with a format from which we only use Day, Month, Hour, Minute and Second.
    
    Takes: None
    
    Returns: It works with a global variable "date". Later, this variable will be used by webpage().
    
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
    """

    Utility: This function is used to print its content into the Webserver's HTML.
    
    Takes: None
    
    Returns: the "html" variable that contains the whole content. This is used by the SetNetwork() / conn.sendall(response)
    
    """
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
            <script>
                const buttonDatos = document.getElementByID("boton");
                buttonDatos.addEventListener("click", function(){
                    setTimeout(disable, 1000);
                    setTimeout(enable, 1000);
                })
                function disable(){
                buttonDatos.disable() = true;
                }
                function enable(){
                buttonDatos.disable() = false;
                }
            </script>
            </body>
            </html>
            """
    return html 
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(('', 80))
s.listen(5)

tim0 = Timer(0)                                                               # This timer is triggered every hour (3600000 ms)  // 30000 ms TEST        
tim1 = Timer(1)                                                               # Timer 1 is used to check the lighting value every 30 mins. Init is inside lighting()
tim2 = Timer(2)                                                               # Timer 2 is used to check the cooling value every 30 mins. Init is inside cooling()
tim0.init(period=30000, mode=Timer.PERIODIC, callback=getStates)                 

while True:
        print("Hilo 0")  
        setNetwork()
        print("Hilo 1")
        _thread.start_new_thread(getSensors, ())
