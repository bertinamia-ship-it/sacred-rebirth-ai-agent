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
            return "🚀 MAYA ONLINE!\n\nComandos: report, content, urgent, pipeline"
        elif cmd in ['report', 'reporte']:
            return self.get_report()
        elif 'content' in cmd:
            return """✨ INSTAGRAM POST

🌿 Sacred Rebirth - Transformación Profunda
📅 Agosto 11, 2025 • Valle de Bravo  
👥 8 espacios exclusivos • $3,500

Ayahuasca + Temazcal + Cacao ceremonial
Ambiente seguro y sagrado ✨

💫 https://sacred-rebirth.com/appointment.html

#SacredRebirth #Ayahuasca #ValleDeBravo

📱 ¡Listo para publicar!"""
        else:
            return f"🤖 Maya: '{text}'\n\nComandos: report, content, urgent"

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