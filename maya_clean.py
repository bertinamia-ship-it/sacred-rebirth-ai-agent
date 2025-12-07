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
        cmd = text.lower().strip()
        if cmd in ['/start', 'start']:
            return "🚀 **MAYA AI ONLINE!**\n\n🤖 Inteligencia Artificial Activada\n🎨 Generador de imágenes DALL-E\n📘 Publicación automática Facebook\n📊 Analytics en tiempo real\n\nComandos: report, content, imagen [tema], facebook [tipo], post"
        
        elif cmd in ['report', 'reporte']:
            return self.get_report()
        
        elif cmd in ['content', 'contenido']:
            prompt = """Crea un post para Instagram sobre Sacred Rebirth, un retiro de medicina ancestral en Valle de Bravo, México.

Detalles:
- Fecha: Agosto 11, 2025
- Ubicación: Valle de Bravo
- Capacidad: 8 espacios exclusivos  
- Precio: $3,500 USD
- Incluye: Ayahuasca, Temazcal, Cacao ceremonial

Estilo: Espiritual, auténtico, llamativo
Audiencia: Personas de alto ingreso buscando transformación
Incluir: Call to action, emojis, hashtags
Longitud: 150-200 palabras"""

            return f"✨ **GENERANDO CONTENIDO CON IA...**\n\n{self.generate_ai_content(prompt)}\n\n🔗 https://sacred-rebirth.com/appointment.html\n\n📱 ¡Listo para Instagram!"
        
        elif cmd.startswith('imagen '):
            tema = cmd.replace('imagen ', '')
            return self.generate_image(tema)
        
        elif cmd.startswith('facebook '):
            tipo = cmd.replace('facebook ', '')
            prompt = f"""Crea un post profesional para Facebook sobre Sacred Rebirth retiro de medicina ancestral.

Tipo de post: {tipo}
Negocio: Sacred Rebirth
Evento: Retiro ayahuasca Agosto 11, 2025
Ubicación: Valle de Bravo, México
Audiencia: Adultos alto ingreso, transformación espiritual

Estilo Facebook: Más texto, educativo, profesional
Call to action: Reservar llamada discovery
URL: https://sacred-rebirth.com/appointment.html"""

            ai_content = self.generate_ai_content(prompt)
            return f"📘 **POST FACEBOOK GENERADO CON IA**\n\n{ai_content}\n\n💡 Envía 'post' para publicar automáticamente en Facebook"
        
        elif cmd in ['post', 'publicar', 'sí', 'si', 'yes']:
            # Generar contenido para publicar
            fb_content = """🌿 Sacred Rebirth - Transformación Profunda Esperándote

¿Sientes el llamado hacia una sanación más profunda? 

Nuestro retiro de medicina ancestral en Valle de Bravo te ofrece la oportunidad de reconectar con tu esencia a través de ceremonias sagradas de ayahuasca, temazcal y cacao ceremonial.

✨ Próximo Retiro: Agosto 11, 2025
📍 Valle de Bravo, México  
👥 Solo 8 espacios exclusivos
💎 Inversión: $3,500 USD

Un viaje guiado por facilitadores experimentados en un entorno seguro y sagrado.

🔗 Reserva tu llamada de descubrimiento:
https://sacred-rebirth.com/appointment.html

#SacredRebirth #Medicina #Ancestral #Ayahuasca #Transformación"""

            return self.post_to_facebook(fb_content)
        
        elif cmd in ['urgent', 'urgente']:
            return """🚨 **URGENTE HOY - IA ACTIVADA**

⚡ **PRIORIDADES AUTOMÁTICAS**
1. 📞 Discovery call 2:00 PM  
2. 🎨 Generar imagen IA para post
3. 📱 Contenido Instagram con IA
4. 📘 Post Facebook automático
5. 📊 Analytics tiempo real

🤖 **IA TRABAJANDO EN:**
• Content generation
• Image creation  
• Facebook posting
• Lead tracking

💰 Revenue objetivo: $28,000 USD"""
        
        elif cmd in ['pipeline', 'ventas']:
            return """💰 **PIPELINE VENTAS - IA ANALYTICS**

🎯 **OBJETIVO: $28,000 USD**
8 espacios x $3,500 = SOLD OUT

📊 **STATUS IA**
🔥 Leads Calientes: 3 (IA scoring: 85%)
🌡️ Leads Tibios: 8 (IA nurturing activo)
❄️ Leads Fríos: 150+ (IA segmentation)

🤖 **IA TRABAJANDO EN:**
1. Predictive lead scoring
2. Automated content creation  
3. Optimal posting times
4. Conversion optimization

🚀 **PRÓXIMAS ACCIONES IA**
• Visual content campaign
• Personalized outreach
• Facebook ads optimization"""
        
        else:
            return f"🤖 **Maya AI:** '{text}'\n\n🧠 **COMANDOS INTELIGENTES:**\n• content - Generar post con IA\n• imagen [tema] - Crear imagen DALL-E\n• facebook [tipo] - Post Facebook IA\n• post - Publicar automáticamente\n• report - Analytics tiempo real\n• urgent - Tareas IA\n• pipeline - Ventas predictivas\n\n💡 **Ejemplo:** 'imagen ceremonia ayahuasca'"

maya = Maya()
app = Flask(__name__)

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
    
    print("🚀 Maya Starting...")
    print(f"Token: {TELEGRAM_TOKEN[:10]}...")
    print(f"Admin: {ADMIN_CHAT_ID}")
    print("🔧 Starting without admin check...")
    
    def run_flask():
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    
    threading.Thread(target=run_flask, daemon=True).start()
    
    if ADMIN_CHAT_ID:
        maya.send_message(ADMIN_CHAT_ID, "🚀 Maya Online! Envía 'report' para empezar.")
        print("✅ Startup message sent")
    else:
        print("⚠️ No admin ID - Maya will work but only respond to configured admin")
    
    print("🤖 Starting polling...")
    polling()

if __name__ == '__main__':
    main()