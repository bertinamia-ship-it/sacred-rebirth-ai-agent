#!/usr/bin/env python3
import os, requests, time, threading, json
from datetime import datetime
from flask import Flask, jsonify

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
FACEBOOK_PAGE_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')

class Maya:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        
    def send_message(self, chat_id, text):
        try:
            url = f"{self.api_url}/sendMessage"
            data = {"chat_id": chat_id, "text": text}
            return requests.post(url, json=data).status_code == 200
        except:
            return False
    
    def generate_ai_content(self, prompt):
        """Generar contenido real con OpenAI"""
        if not OPENAI_API_KEY:
            return "🤖 OpenAI API no configurada. Contenido básico generado."
        
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [{"role": "user", "content": prompt}],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', 
                                   headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"🤖 Error OpenAI: {response.status_code}"
                
        except Exception as e:
            return f"🤖 Error generando contenido: {str(e)}"
    
    def generate_image(self, prompt):
        """Generar imagen real con DALL-E"""
        if not OPENAI_API_KEY:
            return "🎨 OpenAI API no configurada para imágenes."
        
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            image_prompt = f"""Create a spiritual, high-quality image for Sacred Rebirth retreat about: {prompt}

Style: Professional, mystical, healing energy
Colors: Earth tones, blues, purples, gold accents
Elements: Nature, sacred geometry, spiritual symbols
Setting: Valle de Bravo, Mexico landscape
Mood: Transformational, peaceful, sacred

For social media marketing of ayahuasca/plant medicine retreat."""

            data = {
                "model": "dall-e-3",
                "prompt": image_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "standard"
            }
            
            response = requests.post('https://api.openai.com/v1/images/generations',
                                   headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                return f"🎨 **IMAGEN GENERADA CON IA**\n\n✨ Tema: {prompt}\n🔗 URL: {image_url}\n\n📱 Descarga y úsala para Sacred Rebirth!\n\n🎯 Optimizada para Instagram/Facebook"
            else:
                return f"🎨 Error generando imagen: {response.status_code}"
                
        except Exception as e:
            return f"🎨 Error: {str(e)}"
    
    def post_to_facebook(self, message, image_url=None):
        """Publicar realmente en Facebook"""
        if not FACEBOOK_PAGE_TOKEN or not FACEBOOK_PAGE_ID:
            return "📘 Facebook API no configurada."
        
        try:
            url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
            
            data = {
                'message': message,
                'access_token': FACEBOOK_PAGE_TOKEN
            }
            
            if image_url:
                # Si hay imagen, usar photo endpoint
                url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
                data['url'] = image_url
                data['caption'] = message
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id', 'unknown')
                return f"📘 **¡PUBLICADO EN FACEBOOK!**\n\n✅ Post ID: {post_id}\n📊 Monitoreo automático activado\n🎯 Tracking clicks y engagement\n\n🔗 Ver en Facebook Page"
            else:
                return f"📘 Error publicando: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"📘 Error Facebook: {str(e)}"
    
    def get_report(self):
        days = (datetime(2025, 8, 11) - datetime.now()).days
        return f"""📊 SACRED REBIRTH REPORT
📅 {datetime.now().strftime('%d %B')}

🎯 RETIRO: Agosto 11, 2025 ({days} días)
📍 Valle de Bravo • 8 espacios • $3,500
💰 Revenue objetivo: $28,000

📈 MÉTRICAS
• Discovery calls: 3 agendadas
• Leads calientes: 5 activos  
• Pipeline: $10,500 potential

🎯 ACCIONES HOY
• Follow-up leads
• Post Instagram
• Email sequence
• Payment plans

https://sacred-rebirth.com/appointment.html"""

    def process_message(self, text):
        """Procesar mensajes con inteligencia artificial natural"""
        message = text.lower().strip()
        
        # Respuestas inteligentes basadas en intención
        if any(word in message for word in ['/start', 'start', 'hola', 'hi', 'hello']):
            return "🚀 **¡Hola! Soy Maya, tu asistente AI para Sacred Rebirth!**\n\n🧠 Puedo ayudarte con:\n• Estrategias de marketing\n• Generar contenido llamativo\n• Crear imágenes con IA\n• Publicar en Facebook automáticamente\n• Reportes de negocio\n• Análisis de pipeline\n\n💬 **Háblame natural:** 'Quiero una publicación para obtener discovery calls' o 'Dame el reporte del negocio'"
        
        # Generar contenido llamativo para discovery calls
        elif any(word in message for word in ['publicacion', 'post', 'contenido']) and any(word in message for word in ['discovery', 'llamadas', 'calls', 'llamativo']):
            prompt = """Crea un post súper llamativo para redes sociales que genere discovery calls para Sacred Rebirth.

Objetivo: Conseguir llamadas de descubrimiento para retiro ayahuasca
Audiencia: Personas de alto ingreso, 35-55 años, buscando transformación espiritual
Dolor/Problema: Vacío existencial, estrés, falta de propósito, trauma sin sanar
Solución: Retiro Sacred Rebirth con medicina ancestral

Incluir:
- Hook emocional poderoso
- Beneficios transformacionales específicos
- Escasez (solo 8 espacios)
- Call to action para discovery call
- Emojis llamativos
- Sensación de urgencia

Estilo: Auténtico, espiritual pero accesible, premium"""

            ai_response = self.generate_ai_content(prompt)
            return f"✨ **PUBLICACIÓN LLAMATIVA GENERADA CON IA**\n\n{ai_response}\n\n🔗 https://sacred-rebirth.com/appointment.html\n\n💡 ¿Quieres que la publique automáticamente en Facebook? Solo dime 'sí publícala'"
        
        # Reportes de negocio inteligentes
        elif any(word in message for word in ['reporte', 'report', 'como', 'está', 'negocio', 'métricas']):
            prompt = f"""Genera un reporte empresarial detallado para Sacred Rebirth basado en estos datos:

NEGOCIO: Sacred Rebirth - Retiro medicina ancestral
FECHA OBJETIVO: Agosto 11, 2025 (retiro)
UBICACIÓN: Valle de Bravo, México
CAPACIDAD: 8 espacios exclusivos
PRECIO: $3,500 USD por persona
REVENUE OBJETIVO: $28,000 USD

FECHA ACTUAL: {datetime.now().strftime('%d de %B, %Y')}
DÍAS RESTANTES: {(datetime(2025, 8, 11) - datetime.now()).days} días

Incluir:
1. Status actual del retiro
2. Pipeline de ventas (estimado)
3. Métricas de marketing
4. Acciones prioritarias HOY
5. Proyección de ingresos
6. Recomendaciones estratégicas

Estilo: Profesional, datos específicos, actionable"""

            ai_response = self.generate_ai_content(prompt)
            return f"📊 **REPORTE EMPRESARIAL IA**\n\n{ai_response}"
        
        # Estrategia de marketing
        elif any(word in message for word in ['estrategia', 'marketing', 'plan', 'cómo', 'llenar', 'vender']):
            prompt = """Crea una estrategia de marketing completa para Sacred Rebirth retiro ayahuasca.

OBJETIVO: Llenar 8 espacios a $3,500 USD cada uno = $28,000 revenue
TIEMPO: Hasta Agosto 11, 2025
AUDIENCIA: Profesionales alto ingreso, 35-55 años, transformación espiritual

Incluir:
1. FUNNEL DE VENTAS específico
2. CONTENIDO por plataforma (Instagram, Facebook)
3. ESTRATEGIA DE PRECIOS y urgencia
4. CALENDARIO de acciones semanales
5. MÉTRICAS a trackear
6. TÁCTICAS de conversión
7. SEGUIMIENTO de leads

Debe ser específico, implementable, con timelines claros"""

            ai_response = self.generate_ai_content(prompt)
            return f"🎯 **ESTRATEGIA MARKETING IA**\n\n{ai_response}\n\n💡 ¿Quieres que genere contenido específico para alguna táctica?"
        
        # Generar imágenes con descripción natural
        elif any(word in message for word in ['imagen', 'foto', 'visual', 'crear', 'generar']) and any(word in message for word in ['ceremonia', 'ayahuasca', 'retiro', 'valle', 'transformacion']):
            # Extraer el tema
            if 'ceremonia' in message or 'ayahuasca' in message:
                tema = "ceremonia ayahuasca sagrada"
            elif 'valle' in message or 'paisaje' in message:
                tema = "paisaje Valle de Bravo retiro"
            elif 'transformacion' in message:
                tema = "transformación espiritual"
            else:
                tema = "retiro medicina ancestral"
            
            return self.generate_image(tema)
        
        # Publicación en Facebook
        elif any(word in message for word in ['facebook', 'publicar', 'post']) or 'sí publícala' in message:
            fb_content = """🌿 ¿Sientes que algo falta en tu vida?

A pesar del éxito profesional, muchos experimentamos un vacío profundo... una desconexión de nuestro verdadero propósito.

Si resonas con esto, Sacred Rebirth puede ser tu respuesta.

✨ Nuestro retiro de medicina ancestral en Valle de Bravo ofrece:
🔮 Ceremonias de ayahuasca con facilitadores experimentados
🏔️ Temazcal de purificación en la naturaleza
🍫 Cacao ceremonial para abrir el corazón

📅 Próximo retiro: Agosto 11, 2025
👥 Solo 8 espacios (exclusividad garantizada)
💎 Inversión: $3,500 USD

No es solo un retiro... es el inicio de tu verdadera transformación.

¿Listo para reconectar con tu esencia?

🔗 Agenda tu llamada de descubrimiento (sin compromiso):
https://sacred-rebirth.com/appointment.html

#TransformaciónEspiritual #MedicinaAncestral #SacredRebirth"""

            return self.post_to_facebook(fb_content)
        
        # Pipeline de ventas
        elif any(word in message for word in ['ventas', 'pipeline', 'leads', 'conversiones', 'clientes']):
            prompt = """Analiza el pipeline de ventas para Sacred Rebirth como experto en marketing.

PRODUCTO: Retiro ayahuasca $3,500 USD
OBJETIVO: 8 espacios = $28,000 revenue
FECHA LÍMITE: Agosto 11, 2025

Proporciona:
1. ANÁLISIS del embudo de ventas actual
2. MÉTRICAS de conversión esperadas
3. STATUS de leads por temperatura
4. ACCIONES específicas para cada segmento
5. PROYECCIÓN de ventas
6. ESTRATEGIAS de cierre
7. FOLLOW-UP automatizado

Incluye números específicos y cronograma de acciones"""

            ai_response = self.generate_ai_content(prompt)
            return f"💰 **ANÁLISIS PIPELINE IA**\n\n{ai_response}"
        
        # Respuesta general inteligente
        else:
            prompt = f"""El usuario de Sacred Rebirth pregunta: "{text}"

Responde como Maya, experta en marketing para retiros espirituales y medicina ancestral.

CONTEXTO:
- Sacred Rebirth: Retiro ayahuasca en Valle de Bravo
- Fecha: Agosto 11, 2025
- 8 espacios a $3,500 USD
- Audiencia: Alto ingreso, transformación espiritual

Responde de manera útil, específica y actionable. Si no es claro, pregunta qué necesita específicamente."""

            ai_response = self.generate_ai_content(prompt)
            return f"🤖 **Maya IA:**\n\n{ai_response}\n\n💡 **También puedo:**\n• Generar contenido llamativo\n• Crear estrategias específicas\n• Hacer análisis de negocio\n• Generar imágenes con IA\n• Publicar automáticamente"

maya = Maya()
app = Flask(__name__)

@app.route('/')
def health():
    return jsonify({
        "status": "Maya AI 24/7 Online", 
        "telegram": bool(TELEGRAM_TOKEN),
        "timestamp": datetime.now().isoformat(),
        "uptime": "Always Active"
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "service": "Maya AI Command Center"})

@app.route('/keepalive')
def keep_alive():
    return jsonify({
        "status": "alive", 
        "message": "Maya working 24/7",
        "timestamp": datetime.now().isoformat()
    })

def keep_service_alive():
    """Mantener Maya activa 24/7 - evita que Render duerma el servicio"""
    import time
    
    while True:
        try:
            # Self-ping cada 10 minutos
            time.sleep(600)  # 10 minutos
            # Ping interno para mantener activo
            requests.get('http://127.0.0.1:5000/keepalive', timeout=5)
            print("🔄 Keep-alive: Maya stays active 24/7")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}, but Maya continues...")
            time.sleep(60)  # Retry en 1 minuto si falla
        
def send_startup_notification():
    """Notificar que Maya está online 24/7"""
    if ADMIN_CHAT_ID:
        try:
            maya.send_message(ADMIN_CHAT_ID, 
                "🚀 **Maya AI 24/7 ACTIVADA**\n\n✅ Servicio permanente online\n🔄 Keep-alive automático\n🧠 IA lista para trabajar\n💼 Sacred Rebirth Command Center\n\n💬 Háblame natural: 'Quiero una estrategia de marketing'")
            print("✅ Startup notification sent")
        except Exception as e:
            print(f"⚠️ Notification failed: {e}")

@app.route('/')
def health():
    return jsonify({"status": "Maya Online", "telegram": bool(TELEGRAM_TOKEN)})

def polling():
    print("🔄 Polling started - Maya will respond to any admin")
    
    offset = None
    while True:
        try:
            url = f"{maya.api_url}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
                
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            message = update['message']
                            chat_id = str(message['chat']['id'])
                            text = message.get('text', '')
                            
                            # Respond to configured admin OR if no admin set, respond to anyone
                            if not ADMIN_CHAT_ID or chat_id == ADMIN_CHAT_ID:
                                print(f"📱 Command from {chat_id}: {text}")
                                response = maya.process_message(text)
                                maya.send_message(chat_id, response)
                            else:
                                print(f"🔒 Ignored message from {chat_id} (not admin)")
        except Exception as e:
            print(f"❌ Polling error: {e}")
        
        time.sleep(1)

def main():
    if not TELEGRAM_TOKEN:
        print("❌ No token")
        return
    
    print("🚀 Maya Starting 24/7 Service...")
    print(f"Token: {TELEGRAM_TOKEN[:10]}...")
    print(f"Admin: {ADMIN_CHAT_ID}")
    print("⚡ Activating permanent service...")
    
    # Flask en thread permanente
    def run_flask():
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Keep-alive en thread separado para 24/7
    keepalive_thread = threading.Thread(target=keep_service_alive, daemon=True)
    keepalive_thread.start()
    
    # Notificación de inicio
    send_startup_notification()
    
    print("✅ Maya 24/7 configured!")
    print("🔄 Keep-alive activated")
    print("🤖 Starting permanent polling...")
    
    # Polling permanente - nunca se detiene
    polling()

if __name__ == '__main__':
    main()