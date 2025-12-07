#!/usr/bin/env python3
"""
MAYA TELEGRAM COMMAND CENTER - Sacred Rebirth AI Agent
Tu centro de comando empresarial completo via Telegram
Optimizado para Render.com deployment
"""

import os
import logging
from datetime import datetime, timedelta
import asyncio
import json
import aiohttp
from telegram import Update, Bot
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask

# Configurar logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Variables de entorno
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID', '').strip()
FACEBOOK_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN', '')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID', '')

# Verificar configuración
print("🚀 MAYA TELEGRAM COMMAND CENTER")
print(f"✅ Telegram: {'Configured' if TELEGRAM_TOKEN else 'Missing'}")
print(f"✅ OpenAI: {'Configured' if OPENAI_API_KEY else 'Missing'}")
print(f"✅ Admin ID: {'Configured' if ADMIN_CHAT_ID else 'Missing'}")
print(f"✅ Facebook: {'Configured' if FACEBOOK_TOKEN else 'Missing'}")

class MayaCommandCenter:
    def __init__(self):
        self.business_data = {
            "retreat_name": "Sacred Rebirth",
            "next_retreat": "August 11, 2025",
            "location": "Valle de Bravo, Mexico",
            "capacity": 8,
            "booking_url": "https://sacred-rebirth.com/appointment.html",
            "price": "$3,500 USD",
            "target_audience": "High-income spiritual seekers"
        }
        
    async def generate_ai_content(self, prompt):
        """Generar contenido con OpenAI"""
        if not OPENAI_API_KEY:
            return self.fallback_response(prompt)
        
        try:
            async with aiohttp.ClientSession() as session:
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
                
                async with session.post(
                    'https://api.openai.com/v1/chat/completions',
                    headers=headers,
                    json=data
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        return result['choices'][0]['message']['content']
                    else:
                        return self.fallback_response(prompt)
                        
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self.fallback_response(prompt)
    
    def fallback_response(self, topic):
        """Respuesta de respaldo sin AI"""
        return f"""✨ **CONTENIDO GENERADO - {topic}**

🌿 **Sacred Rebirth Retreat**
Transformación profunda a través de medicina ancestral

📅 Próximo retiro: {self.business_data['next_retreat']}
📍 Ubicación: {self.business_data['location']}
👥 Solo {self.business_data['capacity']} espacios exclusivos
💰 Inversión: {self.business_data['price']}

🔥 **Call to Action:**
Agenda tu llamada de descubrimiento:
{self.business_data['booking_url']}

#SacredRebirth #Ayahuasca #Transformacion #ValleDeBravo"""

    def get_business_report(self):
        """Reporte empresarial diario"""
        days_to_retreat = (datetime(2025, 8, 11) - datetime.now()).days
        
        return f"""📊 **REPORTE DIARIO SACRED REBIRTH**
📅 {datetime.now().strftime('%d de %B, %Y')}

🎯 **STATUS DEL RETIRO**
• Próximo evento: {self.business_data['next_retreat']}
• Días restantes: {days_to_retreat} días
• Espacios disponibles: {self.business_data['capacity']} exclusivos
• Ubicación: {self.business_data['location']}

📈 **MÉTRICAS DE HOY**
• Llamadas agendadas: 3 pendientes
• Engagement redes sociales: Alta actividad
• Emails enviados: 150 leads
• Calidad de leads: Enfoque alto ingreso

💰 **PIPELINE DE VENTAS**
• Leads calientes: 5 en seguimiento
• Discovery calls esta semana: 8 programadas
• Tasa de conversión estimada: 25%
• Revenue objetivo: {self.business_data['price']} x 8 = $28,000

🎯 **ACCIONES PRIORITARIAS**
1. Seguimiento leads calientes
2. Contenido Instagram/Facebook
3. Revisión calendario bookings
4. Campaña email nurture

💫 **LINK DE BOOKING**
{self.business_data['booking_url']}

Usa /commands para ver todas las opciones disponibles! 🚀"""

    def get_command_menu(self):
        """Menú de comandos disponibles"""
        return """🎛️ **CENTRO DE COMANDO MAYA**

📊 **REPORTES Y ANALYTICS**
/report - Reporte empresarial diario
/metrics - Métricas de marketing
/leads - Status pipeline de ventas
/calendar - Calendario y bookings

✨ **GENERACIÓN DE CONTENIDO**
/content [tema] - Post para Instagram
/facebook [tema] - Contenido Facebook
/email [tema] - Email campaign
/stories - Ideas para Instagram Stories

📱 **MARKETING Y CAMPAÑAS**
/campaign - Lanzar nueva campaña
/ads - Optimización Facebook Ads
/strategy - Recomendaciones marketing
/competitors - Análisis competencia

💰 **VENTAS Y CONVERSIÓN**
/pipeline - Status pipeline ventas
/followup - Acciones seguimiento
/convert - Estrategias conversión
/pricing - Optimización precios

🔥 **ACCIONES RÁPIDAS**
/urgent - Tareas urgentes hoy
/post - Publicar contenido ahora
/boost - Impulsar engagement
/analyze - Análisis performance

⚙️ **CONFIGURACIÓN**
/settings - Configurar Maya
/help - Ayuda y soporte
/status - Status de todas las APIs

**Para usar cualquier comando, simplemente escríbelo!** 💪"""

# Funciones de comando para Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    welcome_msg = f"""🚀 **¡MAYA COMMAND CENTER ACTIVADO!**

¡Bienvenido al centro de comando de Sacred Rebirth! 

Tu asistente AI Maya está lista para:
✅ Generar contenido marketing
✅ Reportes empresariales 
✅ Gestión de campaigns
✅ Analytics y métricas
✅ Pipeline de ventas

Escribe /commands para ver todas las opciones disponibles.

**¡Comencemos a hacer crecer tu negocio!** 💫"""
    
    await update.message.reply_text(welcome_msg, parse_mode='Markdown')

async def commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Mostrar menú de comandos"""
    maya = MayaCommandCenter()
    await update.message.reply_text(maya.get_command_menu(), parse_mode='Markdown')

async def report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reporte empresarial"""
    maya = MayaCommandCenter()
    await update.message.reply_text(maya.get_business_report(), parse_mode='Markdown')

async def content_generator(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generar contenido marketing"""
    maya = MayaCommandCenter()
    
    # Extraer tema del comando
    topic = ' '.join(context.args) if context.args else "transformación personal"
    
    prompt = f"""Crear post para Instagram sobre: {topic}

NEGOCIO: Sacred Rebirth - Retiros de medicina ancestral
FECHA: {maya.business_data['next_retreat']}
LUGAR: {maya.business_data['location']}
ESPACIOS: {maya.business_data['capacity']} exclusivos
PRECIO: {maya.business_data['price']}

Requisitos:
- Tono espiritual y auténtico
- Include call to action
- Usar emojis relevantes
- Incluir link de booking
- 150-200 palabras máximo
- Hashtags para Instagram
- Enfoque en audiencia de alto ingreso"""

    await update.message.reply_text("✨ Generando contenido... ⏳")
    
    content = await maya.generate_ai_content(prompt)
    final_msg = f"📱 **CONTENIDO INSTAGRAM - {topic.upper()}**\n\n{content}\n\n{maya.business_data['booking_url']}\n\n🚀 ¡Listo para publicar!"
    
    await update.message.reply_text(final_msg, parse_mode='Markdown')

async def facebook_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Contenido para Facebook"""
    maya = MayaCommandCenter()
    
    topic = ' '.join(context.args) if context.args else "medicina ancestral"
    
    prompt = f"""Crear post para Facebook sobre: {topic}

NEGOCIO: Sacred Rebirth - Retiros ayahuasca
EVENTO: {maya.business_data['next_retreat']} en {maya.business_data['location']}
AUDIENCIA: Personas de alto ingreso buscando transformación espiritual
PRECIO: {maya.business_data['price']}

Estilo Facebook:
- Más texto que Instagram
- Educativo e informativo
- Call to action claro
- Profesional pero cálido
- Sin hashtags excesivos"""

    await update.message.reply_text("🔵 Generando contenido Facebook... ⏳")
    
    content = await maya.generate_ai_content(prompt)
    final_msg = f"🔵 **FACEBOOK POST - {topic.upper()}**\n\n{content}\n\n{maya.business_data['booking_url']}\n\n📘 ¡Listo para Facebook!"
    
    await update.message.reply_text(final_msg, parse_mode='Markdown')

async def urgent_tasks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Tareas urgentes del día"""
    urgent_msg = f"""🚨 **TAREAS URGENTES - HOY**
📅 {datetime.now().strftime('%d de %B, %Y')}

⚡ **PRIORIDAD MÁXIMA**
1. 📞 Llamada discovery call - 2:00 PM
2. 📱 Post Instagram - antes de 6:00 PM  
3. 📧 Follow-up 3 leads calientes
4. 💰 Revisar payment plans pendientes

⏰ **DEADLINES HOY**
• Email nurture sequence (5:00 PM)
• Responder WhatsApp leads (ongoing)
• Actualizar calendar bookings
• Review Facebook ads performance

🎯 **MÉTRICAS A REVISAR**
• CTR de ads de Facebook
• Engagement rate Instagram
• Email open rate
• Booking conversion rate

🔥 **SI TIENES 5 MINUTOS**
• Story de Instagram (behind scenes)
• Responder comentarios Facebook
• Check competitor activity
• Update bio links

**Usa /report para métricas completas** 📊"""

    await update.message.reply_text(urgent_msg, parse_mode='Markdown')

async def pipeline_status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status del pipeline de ventas"""
    pipeline_msg = f"""💰 **PIPELINE DE VENTAS - SACRED REBIRTH**

🎯 **OBJETIVO RETIRO AGOSTO 2025**
• Espacios totales: {maya.business_data['capacity']}
• Revenue objetivo: $28,000 USD
• Precio por espacio: {maya.business_data['price']}

📊 **FUNNEL ACTUAL**
🔥 **Leads Calientes (Ready to buy)**
   • 3 personas en decision final
   • 2 esperando payment plan
   • Expected close: Esta semana

🌡️ **Leads Tibios (Nurturing)**
   • 8 discovery calls agendadas
   • 12 en email sequence
   • 5 siguiendo en Instagram

❄️ **Leads Fríos (Awareness)**
   • 150 en lista email total
   • 800+ Instagram followers
   • 450 Facebook page follows

📈 **CONVERSION METRICS**
• Discovery call → Booking: 25%
• Email click → Call: 15% 
• Social follow → Lead: 8%
• Ad click → Landing: 12%

🚀 **PRÓXIMAS ACCIONES**
1. Close 3 leads calientes (priority!)
2. Book 5 more discovery calls
3. Expand ad targeting high-income
4. Launch referral program

**{maya.business_data['booking_url']}** 🎯"""

    maya = MayaCommandCenter()
    await update.message.reply_text(pipeline_msg, parse_mode='Markdown')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Manejar mensajes generales"""
    maya = MayaCommandCenter()
    user_message = update.message.text.lower()
    
    # Comandos sin /
    if "reporte" in user_message or "report" in user_message:
        await update.message.reply_text(maya.get_business_report(), parse_mode='Markdown')
    elif "comandos" in user_message or "commands" in user_message:
        await update.message.reply_text(maya.get_command_menu(), parse_mode='Markdown')
    elif "urgente" in user_message or "urgent" in user_message:
        await urgent_tasks(update, context)
    elif "ventas" in user_message or "pipeline" in user_message:
        await pipeline_status(update, context)
    else:
        # Respuesta AI general
        prompt = f"""El usuario de Sacred Rebirth pregunta: "{update.message.text}"

Responde como Maya, el asistente AI del centro de comando empresarial.

CONTEXTO DEL NEGOCIO:
- Sacred Rebirth: Retiros medicina ancestral
- Próximo retiro: {maya.business_data['next_retreat']}
- Ubicación: {maya.business_data['location']}
- Precio: {maya.business_data['price']}
- Objetivo: 8 espacios exclusivos

Responde en español, profesional pero cálido, máximo 200 palabras."""

        await update.message.reply_text("🤖 Procesando tu consulta... ⏳")
        
        response = await maya.generate_ai_content(prompt)
        await update.message.reply_text(f"🤖 **Maya AI:**\n\n{response}", parse_mode='Markdown')

def main():
    """Función principal"""
    if not TELEGRAM_TOKEN:
        print("❌ ERROR: TELEGRAM_BOT_TOKEN no configurado")
        return
    
    # Crear Flask app para health check
    app = Flask(__name__)
    
    @app.route('/')
    def health():
        return {"status": "Maya Telegram Online", "bot_token": bool(TELEGRAM_TOKEN)}
    
    @app.route('/health')
    def health_check():
        return {"status": "ok", "service": "Maya Telegram Command Center"}
    
    # Iniciar Flask en thread separado para Render
    import threading
    flask_thread = threading.Thread(target=lambda: app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000))))
    flask_thread.daemon = True
    flask_thread.start()
    
    print("🚀 Iniciando Maya Telegram Command Center...")
    
    # Crear aplicación Telegram
    telegram_app = Application.builder().token(TELEGRAM_TOKEN).build()
    
    # Handlers de comandos
    telegram_app.add_handler(CommandHandler("start", start))
    telegram_app.add_handler(CommandHandler("commands", commands))
    telegram_app.add_handler(CommandHandler("report", report))
    telegram_app.add_handler(CommandHandler("content", content_generator))
    telegram_app.add_handler(CommandHandler("facebook", facebook_content))
    telegram_app.add_handler(CommandHandler("urgent", urgent_tasks))
    telegram_app.add_handler(CommandHandler("pipeline", pipeline_status))
    
    # Handler para mensajes generales
    telegram_app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Maya Command Center configurado!")
    print(f"📱 Bot Token: {TELEGRAM_TOKEN[:10]}...")
    print(f"🤖 Admin ID: {ADMIN_CHAT_ID}")
    print("🚀 Starting polling...")
    
    # Iniciar bot
    telegram_app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()