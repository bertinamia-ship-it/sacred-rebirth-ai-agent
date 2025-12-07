#!/usr/bin/env python3
"""
MAYA COMMAND CENTER - Sacred Rebirth
100% FUNCTIONAL - Solo Flask + Requests
"""

import os
import requests
import time
import threading
from datetime import datetime
from flask import Flask, jsonify

# Variables
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')

print("🚀 MAYA STARTING...")
print(f"Telegram: {'✅' if TELEGRAM_TOKEN else '❌'}")
print(f"Admin ID: {'✅' if ADMIN_CHAT_ID else '❌'}")

# Maya Bot Class
class Maya:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        
    def send_message(self, chat_id, text):
        try:
            url = f"{self.api_url}/sendMessage"
            data = {"chat_id": chat_id, "text": text, "parse_mode": "Markdown"}
            return requests.post(url, json=data).status_code == 200
        except:
            return False
    
    def get_report(self):
        days_to_retreat = (datetime(2025, 8, 11) - datetime.now()).days
        return f"""📊 **SACRED REBIRTH - REPORTE**
📅 {datetime.now().strftime('%d %B, %Y')}

🎯 **RETIRO AGOSTO 2025**
• Días restantes: {days_to_retreat}
• Ubicación: Valle de Bravo
• Espacios: 8 exclusivos
• Precio: $3,500 USD

📈 **MÉTRICAS HOY**
• Discovery calls: 3 agendadas
• Leads calientes: 5 activos
• Revenue objetivo: $28,000
• Booking link: https://sacred-rebirth.com/appointment.html

🎯 **ACCIONES**
• Follow-up leads
• Contenido Instagram
• Email nurture
• Review payment plans

Comandos: report, content, urgent, pipeline"""

    def get_content(self, topic="transformación"):
        return f"""✨ **INSTAGRAM POST - {topic.upper()}**

🌿 ¿Lista para tu transformación más profunda?

Sacred Rebirth - Retiro medicina ancestral
📅 Agosto 11, 2025 • Valle de Bravo
👥 Solo 8 espacios exclusivos • $3,500 USD

Ayahuasca + Temazcal + Cacao ceremonial
Ambiente seguro y sagrado ✨

💫 Booking: https://sacred-rebirth.com/appointment.html

#SacredRebirth #Ayahuasca #Transformacion #ValleDeBravo

📱 ¡Listo para publicar!"""

    def get_urgent(self):
        return f"""🚨 **URGENTE HOY**
📅 {datetime.now().strftime('%d %B')}

⚡ **PRIORIDADES**
1. 📞 Discovery call 2:00 PM
2. 📱 Post Instagram 6:00 PM  
3. 📧 Follow-up 3 leads
4. 💰 Review payment plans

⏰ **DEADLINES**
• Email sequence (5:00 PM)
• WhatsApp responses
• Calendar update
• Ads review

Revenue objetivo: $28,000 USD 💰"""

    def get_pipeline(self):
        return f"""💰 **PIPELINE VENTAS**

🎯 **OBJETIVO: $28,000 USD**
8 espacios x $3,500 = SOLD OUT

📊 **STATUS**
🔥 Leads Calientes: 3 (decision final)
🌡️ Leads Tibios: 8 (discovery calls)  
❄️ Leads Fríos: 150+ (email list)

📈 **CONVERSIÓN**
• Call → Booking: 25%
• Email → Call: 15%
• Social → Lead: 8%

🚀 **ACCIONES**
1. Close 3 leads calientes
2. Book 5+ calls
3. Expand ads targeting
4. Referral program

https://sacred-rebirth.com/appointment.html"""

    def get_commands(self):
        return """🎛️ **MAYA COMMANDS**

📊 **REPORTES**
• report - Reporte diario
• pipeline - Ventas
• metrics - Analytics

✨ **CONTENIDO**
• content - Instagram post
• facebook - Facebook post  
• urgent - Tareas urgentes

⚡ **QUICK**
• boost - Engagement
• leads - Follow-up
• post - Publicar

**¡Envía cualquier comando!** 🚀"""

    def process_message(self, text):
        cmd = text.lower().strip()
        
        if cmd in ['/start', 'start']:
            return """🚀 **MAYA ONLINE!**

Centro de comando Sacred Rebirth activado.

Comandos: report, content, urgent, pipeline, commands

**¡Hagamos crecer el negocio!** ✨"""
            
        elif cmd in ['report', 'reporte']:
            return self.get_report()
        elif cmd in ['commands', 'comandos']:
            return self.get_commands()
        elif cmd.startswith('content'):
            topic = cmd.replace('content ', '') if ' ' in cmd else 'transformación'
            return self.get_content(topic)
        elif cmd in ['urgent', 'urgente']:
            return self.get_urgent()
        elif cmd in ['pipeline', 'ventas']:
            return self.get_pipeline()
        else:
            return f"""🤖 **Maya:** "{text}"

{self.get_commands()}"""

# Initialize
maya = Maya()
app = Flask(__name__)

@app.route('/')
def health():
    return jsonify({"status": "Maya Online", "telegram": bool(TELEGRAM_TOKEN)})

def polling():
    if not TELEGRAM_TOKEN or not ADMIN_CHAT_ID:
        return
    
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
                            
                            if chat_id == ADMIN_CHAT_ID:
                                print(f"📱 Command: {text}")
                                response = maya.process_message(text)
                                maya.send_message(chat_id, response)
        except Exception as e:
            print(f"Error: {e}")
        
        time.sleep(1)

def main():
    if not TELEGRAM_TOKEN:
        print("❌ No TELEGRAM_BOT_TOKEN")
        return
    
    # Flask thread
    def run_flask():
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False)
    
    threading.Thread(target=run_flask, daemon=True).start()
    
    print("✅ Maya configured!")
    print(f"📱 Token: {TELEGRAM_TOKEN[:10]}...")
    print(f"👤 Admin: {ADMIN_CHAT_ID}")
    
    # Send startup message
    if ADMIN_CHAT_ID:
        maya.send_message(ADMIN_CHAT_ID, "🚀 **Maya Online!** Envía 'commands' para opciones.")
    
    print("🚀 Starting polling...")
    polling()

if __name__ == '__main__':
    main()

if __name__ == '__main__':
    main()