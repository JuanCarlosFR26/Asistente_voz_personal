import pyttsx3
import speech_recognition as sr
import pywhatkit
import yfinance as yf
import pyjokes
import webbrowser
import datetime
import wikipedia

# Opciones de voz / idioma
id1 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_ES-ES_HELENA_11.0'
id2 = 'HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0'


# Escuchar nuestro micrófono y devolver el audio como texto
def transformar_audio_en_texto():

    # Almacenar el reconocedor en variable
    r = sr.Recognizer()

    # Configurar el micrófono
    with sr.Microphone() as origen:

        # Tiempo de espera
        r.pause_threshold = 0.8

        # Informar que comenzó la grabación
        print("Ya puedes hablar")

        # Guardar lo escuchado
        audio = r.listen(origen)

        try:
            # Buscar en Google lo que haya escuchado
            pedido = r.recognize_google(audio, language="es")

            # Prueba de que se puede ingresar la voz
            print("Dijiste: " + pedido)

            # Devolver pedido
            return pedido

        # En caso de que no comprenda el audio
        except sr.UnknownValueError:

            # Prueba de que no comprendió el audio
            print("Ups, no entendí")

            # Devolver error
            return "Sigo esperando"

        # En caso de no resolver el pedido
        except sr.RequestError:

            # Prueba de que no comprendió el audio
            print("No hay servicio para tu petición")

            # Devolver error
            return "Sigo esperando"

        # Error inesperado
        except:

            # Prueba de que no comprendió el audio
            print("Ups, algo ha salido mal")

            # Devolver error
            return "Sigo esperando"


# Función para que el asistente pueda ser escuchado
def hablar(mensaje):

    # Encender pyttsx3
    engine = pyttsx3.init()
    engine.setProperty('voice', id1)

    # Pronunciar mensaje
    engine.say(mensaje)
    engine.runAndWait()


# Informar del día de la semana
def pedir_dia():

    # Crear variable con datos de hoy
    dia = datetime.date.today()


    # Crear variable para el día de la semana
    dia_semana = dia.weekday()

    # Diccionario semana
    calendario = {0: "Lunes",
                  1: "Martes",
                  2: "Miércoles",
                  3: "Jueves",
                  4: "Viernes",
                  5: "Sábado",
                  6: "Domingo"}

    # Decir el día de la semana
    hablar(f'Hoy es {calendario[dia_semana]}')


# Informar de la hora
def pedir_hora():

    # Crear una variable con datos de la hora
    hora = datetime.datetime.now()
    hora = f'En este momento son las {hora.hour} y {hora.minute}'

    # Decir la hora
    hablar(hora)


# Abrir el asistente con un saludo
def saludo_inicial():

    # Crear variable de hora
    hora = datetime.datetime.now()
    if hora.hour < 6 or hora.hour > 20:
        momento = 'Buenas noches'
    elif 6 <= hora.hour < 13:
        momento = "Buenos días"
    else:
        momento = "Buenas tardes"



    # Decir el saludo
    hablar(f"{momento}, soy Jarvis, tu asistente personal")


# Función central de pedidos
def pedir_solicitud():

    # Activar el saludo inicial
    saludo_inicial()

    # Variable de corte
    comenzar = True

    # loop central
    while comenzar:

        # Activar el micrófono y guardar el pedido en string
        pedido = transformar_audio_en_texto().lower()

        if 'abrir youtube' in pedido:
            hablar('Abriendo Youtube')
            webbrowser.open('https://www.youtube.com/')
            continue
        elif 'abrir navegador' in pedido:
            hablar('Abriendo el navegador')
            webbrowser.open('https://www.google.es/')
            continue
        elif 'abrir twitter' in pedido:
            hablar('Abriendo Twitter')
            webbrowser.open('https://twitter.com/home')
            continue
        elif 'qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'dime qué día es hoy' in pedido:
            pedir_dia()
            continue
        elif 'qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'dime qué hora es' in pedido:
            pedir_hora()
            continue
        elif 'busca en wikipedia' in pedido:
            hablar('Esta es la información que me aparece en wikipedia')
            pedido = pedido.replace('busca en wikipedia', '')
            wikipedia.set_lang('es')
            resultado = wikipedia.summary(pedido, sentences=1)
            hablar(resultado)
            continue
        elif 'busca en internet' in pedido:
            hablar('Realizando la búsqueda en Internet')
            pedido = pedido.replace('busca en internet', '')
            pywhatkit.search(pedido)
            hablar('Esto es lo que he encontrado')
            continue
        elif 'reproduce' in pedido:
            hablar('Comenzando a reproducir')
            pywhatkit.playonyt(pedido)
            continue
        elif 'cuenta un chiste' in pedido:
            hablar(pyjokes.get_joke('es'))
            continue
        elif 'precio de las acciones' in pedido:
            accion = pedido.split('de')[-1].strip()
            cartera = {'apple': 'APPL',
                       'amazon': 'AMZN',
                       'google': 'GOOGL'}
            try:
                accion_buscada = cartera[accion]
                accion_buscada = yf.Ticker(accion_buscada)
                precio_actual = accion_buscada.info['regularMarketPrice']
                hablar(f'Encontré lo que me has solicitado. El precio de {accion} es {precio_actual}')
                continue
            except:
                hablar('Perdón, pero no he encontrado lo que me has solicitado')
                continue
        elif 'adiós' in pedido:
            hablar('Apago las funciones de mi ordenador. Avísame si me necesitas')
            break



pedir_solicitud()