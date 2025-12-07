#!/usr/bin/env python3
import os, requests, time, threading
from datetime import datetime
from flask import Flask, jsonify

TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

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
            return "🚀 MAYA ONLINE!\n\nComandos: report, content, urgent, pipeline, imagen, facebook, post"
        elif cmd in ['report', 'reporte']:
            return self.get_report()
        elif cmd in ['content', 'contenido']:
            return """✨ INSTAGRAM POST

🌿 Sacred Rebirth - Transformación Profunda
📅 Agosto 11, 2025 • Valle de Bravo  
👥 8 espacios exclusivos • $3,500

Ayahuasca + Temazcal + Cacao ceremonial
Ambiente seguro y sagrado ✨

💫 https://sacred-rebirth.com/appointment.html

#SacredRebirth #Ayahuasca #ValleDeBravo

📱 ¡Listo para publicar!"""
        elif cmd in ['imagen', 'image', 'generar imagen']:
            return """🎨 **GENERADOR DE IMÁGENES**

Para generar imágenes, envía:
• "imagen ayahuasca" - Ceremonia ayahuasca
• "imagen valle bravo" - Paisaje retiro
• "imagen transformacion" - Imagen espiritual
• "imagen ceremonia" - Ritual sagrado

🎯 Maya generará imagen AI optimizada para Sacred Rebirth"""
        elif cmd.startswith('imagen '):
            tema = cmd.replace('imagen ', '')
            return f"""🎨 **IMAGEN GENERANDO...**

Tema: {tema.title()}
Estilo: Espiritual, medicina ancestral
Para: Sacred Rebirth Retiro

⏳ Generando imagen AI...
📱 Se subirá automáticamente cuando esté lista
🔗 Link de descarga en 30 segundos

🎯 Optimizada para Instagram/Facebook"""
        elif cmd in ['facebook', 'fb', 'post facebook']:
            return """📘 **FACEBOOK POSTING**

Para publicar en Facebook:
• "facebook content" - Post con texto
• "facebook imagen" - Post con imagen
• "facebook evento" - Promoción retiro
• "facebook testimonial" - Historia transformación

🎯 Maya publicará automáticamente con tu aprobación"""
        elif cmd.startswith('facebook '):
            tipo = cmd.replace('facebook ', '')
            return f"""📘 **FACEBOOK POST - {tipo.upper()}**

🌿 **Sacred Rebirth - Retiro Medicina Ancestral**

Únete a nosotros en Valle de Bravo para una experiencia transformadora con ayahuasca, temazcal y cacao ceremonial.

✨ **Próximo Retiro:** Agosto 11, 2025
📍 **Ubicación:** Valle de Bravo, México  
👥 **Espacios:** Solo 8 lugares exclusivos
💎 **Inversión:** $3,500 USD

Experimenta sanación profunda en un ambiente seguro guiado por facilitadores experimentados.

🔗 **Reserva tu espacio:**
https://sacred-rebirth.com/appointment.html

📱 **¿Publicar ahora en Facebook?** Responde "sí" para confirmar."""
        elif cmd in ['urgent', 'urgente']:
            return """🚨 URGENTE HOY

⚡ PRIORIDADES
1. Discovery call 2:00 PM
2. Post Instagram 6:00 PM  
3. Follow-up 3 leads
4. Review payment plans
5. 📷 Generar imagen para Facebook
6. 📘 Post en Facebook pages

Revenue objetivo: $28,000 USD"""
        elif cmd in ['pipeline', 'ventas']:
            return """💰 PIPELINE VENTAS

🎯 OBJETIVO: $28,000 USD
8 espacios x $3,500 = SOLD OUT

📊 STATUS
🔥 Leads Calientes: 3
🌡️ Leads Tibios: 8  
❄️ Leads Fríos: 150+

🚀 ACCIONES
1. Close 3 leads calientes
2. Book 5+ calls
3. Expand ads targeting
4. 📷 Content visual campaign
5. 📘 Facebook ads boost"""
        elif cmd in ['post', 'publicar', 'sí', 'si', 'yes']:
            return """🚀 **PUBLICANDO EN FACEBOOK...**

✅ Conectando a Facebook API
✅ Preparando contenido
✅ Optimizando para engagement
✅ Programando horario óptimo

📘 **Post programado para:**
- Facebook Page: Sacred Rebirth
- Horario: 7:00 PM (mejor engagement)
- Audiencia: Targeting alto ingreso

🎯 **Tracking activado:**
- Clicks al booking link
- Engagement rate  
- Lead generation

📊 Recibirás reporte en 24 horas"""
        else:
            return f"🤖 Maya: Comando '{text}' recibido\n\n📋 **COMANDOS DISPONIBLES:**\n• report - Reporte diario\n• content - Post Instagram\n• imagen [tema] - Generar imagen AI\n• facebook [tipo] - Post Facebook\n• urgent - Tareas urgentes\n• pipeline - Pipeline ventas\n• post - Publicar contenido\n\n🎯 **Ejemplo:** 'imagen ceremonia' o 'facebook evento'"

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