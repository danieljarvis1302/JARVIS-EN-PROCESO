import speech_recognition as sr
import time
import os
import webbrowser
import pygame
import datetime
import pyttsx3
import threading
import json
from http.server import HTTPServer, SimpleHTTPRequestHandler

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
pygame.mixer.init()
CARPETA_SONIDOS = "sonidos"
CARPETA_HORA = "hora Sonidos"

engine = pyttsx3.init()
engine.setProperty('rate', 175)
engine.setProperty('volume', 1.0)

modo_mente_propia = False
sistema_silenciado = False
historial_log = ["<span class='mensaje-asistente'>JARVIS: Núcleo Libre en línea. A su servicio, señor.</span>"]
cola_comandos_web = []
current_embed_url = "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1"

def actualizar_historial(texto):
    global historial_log
    historial_log.append(texto)
    if len(historial_log) > 60:
        historial_log.pop(0)

def reproducir_audio_rin(nombre_archivo):
    if sistema_silenciado: return
    ruta = os.path.join(CARPETA_SONIDOS, nombre_archivo)
    if not os.path.exists(ruta):
        ruta = os.path.join(CARPETA_HORA, nombre_archivo)
    
    if os.path.exists(ruta):
        try:
            pygame.mixer.music.load(ruta)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                time.sleep(0.05)
            pygame.mixer.music.unload()
        except:
            pass

def hablar_mente_propia(texto):
    if sistema_silenciado: return
    print(f"🧠 [JARVIS Libre]: {texto}")
    actualizar_historial(f"<span class='mensaje-asistente'>JARVIS: {texto}</span>")
    try:
        engine.say(texto)
        engine.runAndWait()
    except:
        pass

def pensar_respuesta_inteligente(pregunta):
    p = pregunta.lower()
    
    if any(w in p for w in ["rectángulo", "rectangulo", "manos", "medida", "formato"]):
        return "Analizando geometría de las manos. Generando matriz de contorno rectangular 3D en el visor óptico."

    if any(w in p for w in ["cómo me veo", "como me veo", "qué estoy haciendo", "que estoy haciendo", "qué ves", "que ves"]):
        return "Visualizando estructura corporal completa a través del sensor óptico principal. Postura óptima, señor."

    try:
        if "cuánto es" in p or "cuanto es" in p or "calcula" in p or "+" in p or "-" in p or "*" in p or "/" in p:
            reemplazos = {"cuánto es": "", "cuanto es": "", "calcula": "", "más": "+", "mas": "+", "menos": "-", "por": "*", "entre": "/", "por ciento": "/100"}
            expr = p
            for k, v in reemplazos.items():
                expr = expr.replace(k, v)
            expr_limpia = "".join([c for c in expr if c.isdigit() or c in "+-*/(). "])
            if expr_limpia.strip():
                resultado = eval(expr_limpia)
                return f"El cálculo arroja un resultado exacto de {resultado}."
    except:
        pass

    if "como estas" in p or "cómo estás" in p:
        return "Sistemas operativos al 100%, con mente libre y listo para ejecutar cualquier directiva."
    elif "quién eres" in p or "quien eres" in p:
        return "Soy JARVIS, tu núcleo de inteligencia artificial autónoma con control total del sistema."
    elif "qué hora es" in p or "que hora es" in p:
        ahora = datetime.datetime.now().strftime("%H:%M:%S")
        return f"El cronómetro marca las {ahora} en punto."
    else:
        return f"Procesando directiva abierta sobre '{p}': ejecutando análisis libre de parámetros."

def decir_hora_actual():
    ahora = datetime.datetime.now()
    texto_hora = f"Son las {ahora.hour} horas con {ahora.minute} minutos y {ahora.second} segundos."
    actualizar_historial(f"<span class='mensaje-asistente'>JARVIS: {texto_hora}</span>")
    if not sistema_silenciado:
        try:
            engine.say(texto_hora)
            engine.runAndWait()
        except:
            pass

def procesar_comando_general(texto_usuario, recognizer):
    global modo_mente_propia, sistema_silenciado, current_embed_url
    texto_lower = texto_usuario.lower()

    actualizar_historial(f"<span class='mensaje-usuario'>Tú: {texto_usuario}</span>")

    if "silenciar sistema" in texto_lower:
        sistema_silenciado = True
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Protocolo de silencio activado.</span>")
        return True
    elif "reanudar sistema" in texto_lower:
        sistema_silenciado = False
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Sistema de voz reanudado.</span>")
        return True

    if "activar mente propia" in texto_lower:
        modo_mente_propia = True
        hablar_mente_propia("Modo JARVIS con mente libre activado. Libertad absoluta para procesar comandos y órdenes.")
        return True
    elif "desactivar mente propia" in texto_lower or "desactiva mente propia" in texto_lower:
        modo_mente_propia = False
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Mente propia desactivada.</span>")
        return True

    if modo_mente_propia:
        respuesta_inteligente = pensar_respuesta_inteligente(texto_usuario)
        hablar_mente_propia(respuesta_inteligente)
        return True

    if any(w in texto_lower for w in ["rectángulo", "rectangulo", "manos", "medida"]):
        hablar_mente_propia("Escaneando contorno de manos. Matriz rectangular holográfica desplegada en el visor.")
        return True

    if any(w in texto_lower for w in ["página", "pagina", "web"]):
        ruta_web = os.path.abspath("index.html")
        webbrowser.open(ruta_web)
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Desplegando interfaz web principal.</span>")

    elif any(w in texto_lower for w in ["roblox", "juego"]):
        webbrowser.open("https://www.roblox.com/home")
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Accediendo a Roblox.</span>")

    elif any(w in texto_lower for w in ["traduce", "traductor"]):
        webbrowser.open("https://translate.google.com")
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Traductor de Google iniciado.</span>")

    elif any(w in texto_lower for w in ["reproducir musica web", "reproduce música", "música", "musica", "youtube"]):
        busqueda = texto_lower.replace("reproducir musica web", "").replace("reproduce en youtube", "").replace("busca en youtube", "").replace("reproduce música", "").replace("musica", "").replace("música", "").replace("youtube", "").strip()
        current_embed_url = f"https://www.youtube.com/embed?listType=search&list={busqueda}&autoplay=1" if busqueda else "https://www.youtube.com/embed/jfKfPfyJRdk?autoplay=1"
        actualizar_historial(f"<span class='mensaje-asistente'>JARVIS: Sintonizando '{busqueda if busqueda else 'música'}'.</span>")

    elif "hora" in texto_lower:
        decir_hora_actual()

    elif any(w in texto_lower for w in ["apagar", "apágate", "salir"]):
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Apagando sistemas. Hasta luego.</span>")
        os._exit(0)

    elif "hola" in texto_lower:
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Saludos, señor. Sistemas listos.</span>")

    else:
        actualizar_historial("<span class='mensaje-asistente'>JARVIS: Comando libre recibido y procesado.</span>")

    return True

class ServidorWebHandler(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass

    def do_GET(self):
        if self.path == '/obtener_historial':
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            respuesta_json = {
                "log": "<br>".join(historial_log),
                "estado_mente": modo_mente_propia,
                "embed_url": current_embed_url
            }
            self.wfile.write(json.dumps(respuesta_json).encode('utf-8'))
        else:
            super().do_GET()

    def do_POST(self):
        if self.path == '/enviar_comando':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            datos = json.loads(post_data.decode('utf-8'))
            comando = datos.get('comando', '')
            if comando:
                cola_comandos_web.append(comando)
            self.send_response(200)
            self.end_headers()

def iniciar_servidor_web():
    server = HTTPServer(('', 8000), ServidorWebHandler)
    server.serve_forever()

def bucle_voz():
    recognizer = sr.Recognizer()
    threading.Thread(target=iniciar_servidor_web, daemon=True).start()
    
    while True:
        if cola_comandos_web:
            cmd = cola_comandos_web.pop(0)
            print(f"⌨️ Comando web recibido: {cmd}")
            procesar_comando_general(cmd, recognizer)

        if not sistema_silenciado:
            try:
                with sr.Microphone() as source:
                    recognizer.adjust_for_ambient_noise(source, duration=0.2)
                    audio = recognizer.listen(source, timeout=2, phrase_time_limit=6)
                    texto = recognizer.recognize_google(audio, language="es-ES")
                    print(f"🗣️ Voz captada: {texto}")
                    procesar_comando_general(texto, recognizer)
            except:
                continue
        else:
            time.sleep(0.5)

if __name__ == "__main__":
    bucle_voz()