from hashlib import sha1
import socket
from dht import DHT11
from machine import Pin, ADC
from time import sleep
import _thread

adcLDR1 = ADC(Pin(34))
adcLDR2 = ADC(Pin(39))
adcHL = ADC(Pin(36))

humedadSuelo = ""
ldr1Oscuro = False
ldr2Oscuro = False

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
    lock.release() 

def getSensors():
    lock.acquire()
    print("Inicializando sensores")
    getLDR()
    getHL()
    lock.release()

def getLDR():
    global ldr1Oscuro
    global ldr2Oscuro
    ldrRead1 = adcLDR1.read() * (3.3/4096)
    #print("El valor de tensión del LDR es: {:.2f}" .format(ldrRead1))
    RLDR1 = (ldrRead1 * 10000)/(3.3 - ldrRead1)
    #print("El valor de la resistencia del LDR es: {:.0f}" .format(RLDR1))
    
    ldrRead2 = adcLDR2.read() * (3.3/4096)
    print("El valor de tensión del LDR es: {:.2f}" .format(ldrRead2))
    RLDR2 = (ldrRead2 * 10000)/(3.3 - ldrRead2)
    print("El valor de la resistencia del LDR es: {:.0f}" .format(RLDR2))    
    
    # 40952430 está oscuro (full)
    # 1000 ya está iluminado (full)

    if(RLDR1 > 2000):
        print("LDR 1: Oscuro, iluminar")
        ldr1Oscuro = True
    else:
        print("LDR 1: Iluminado")
        ldr1Oscuro = False
    sleep(1)
    
    if(RLDR2 > 2000):
        print("LDR 2: Oscuro, iluminar")
        ldr2Oscuro = True
    else:
        print("LDR 2: Iluminado")
        ldr2Oscuro = False
    sleep(1)

def getHL():
    adcHL.atten(ADC.ATTN_11DB)
    HLRead= adcHL.read()
    sleep(1)
    global humedadSuelo
    humedadSuelo = str(HLRead)
    print(humedadSuelo)
        
def webPage():
    global humedadSuelo
    global ldr1Oscuro
    global ldr2Oscuro
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
                <link rel="icon" href="img/favicon.ico"> 
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
                        background-image: url(img/Background_Guias.png);
                        display: flex;
                        flex-direction: column;
                        justify-content: center;
                        align-items: center;
                    }}

                    .contenedor {{
                        border-radius: 5rem;
                        width: 60%;
                        height: fit-content;
                        padding: 0 5% 5% 5%;
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
                        font-size: 1.5rem;
                        color: white;
                    }}

                    label {{
                        display: inline;
                        width: 20%;
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
                </style>
                <title>Mi invernadero</title>
            </head>
                    <body>
                        <main>
                            <h1>Mi invernadero</h1>
                            <div class="contenedor">
                                <h2>Datos</h2>
                                <div class="contenedor-variables">
                                    <!--<p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam nam sed placeat, assumenda dolores eveniet minus, reiciendis laborum fugit incidunt distinctio, iusto cumque aperiam sint repellat illo esse quidem vel.</p>
                                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam nam sed placeat, assumenda dolores eveniet minus, reiciendis laborum fugit incidunt distinctio, iusto cumque aperiam sint repellat illo esse quidem vel.</p>
                                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam nam sed placeat, assumenda dolores eveniet minus, reiciendis laborum fugit incidunt distinctio, iusto cumque aperiam sint repellat illo esse quidem vel.</p>
                                    <p>Lorem ipsum dolor sit amet consectetur adipisicing elit. Veniam nam sed placeat, assumenda dolores eveniet minus, reiciendis laborum fugit incidunt distinctio, iusto cumque aperiam sint repellat illo esse quidem vel.</p>
                                    -->
                                    <div class="datos">
                                        <label for="temp">Temperatura ambiente</label>
                                        <meter id="temp"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="hum">Humedad ambiente</label>
                                        <meter id="hum"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="hum_tierra">Humedad de la tierra</label>
                                        <meter id="hum_tierra"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="lum">Luminosidad</label>
                                        <meter id="lum"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="valvula">Electroválvula</label>
                                        <meter id="valvula"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="riego">Última vez regado</label>
                                        <meter id="riego"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="alertas">Alertas (?)</label>
                                        <meter id="alertas"></meter>
                                    </div>
                                    <div class="datos">
                                        <label for="temp">Apagar sistema</label>
                                        <meter id="temp"></meter>
                                    </div>
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