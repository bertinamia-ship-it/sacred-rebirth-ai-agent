#!/usr/bin/env python3
"""
Sacred Rebirth Telegram Bot - Maya Appointment Setter
Version ultra-simplificada que funciona garantizado
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

# Configuración básica
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

print("🚀 Iniciando Sacred Rebirth Bot Ultra-Simple...")
print(f"🔑 Bot Token: {'✅ OK' if TELEGRAM_BOT_TOKEN else '❌ FALTA'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user = update.effective_user
    await update.message.reply_text(f"""
🙏 ¡Hola {user.first_name}!

Soy Maya, facilitadora de Sacred Rebirth.

**🌿 Retiro de Transformación**
📅 11 de enero de 2025  
📍 Valle de Bravo, México
⏱️ 3 días, 2 noches

**✨ Incluye:**
• Ayahuasca sagrada
• Temazcal ceremonial  
• Cacao ceremonial
• Acompañamiento completo

💫 Discovery call gratuito:
https://sacred-rebirth.com/appointment.html

¿En qué puedo ayudarte? 🌿
""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maya responde como appointment setter"""
    
    user_message = update.message.text.lower()
    user_name = update.effective_user.first_name
    
    print(f"💬 {user_name}: {update.message.text[:30]}...")

    # Maya responde automáticamente
    if 'hola' in user_message or 'hello' in user_message:
        response = f"🌿 ¡Hola {user_name}! Soy Maya de Sacred Rebirth. ¿En qué puedo ayudarte sobre nuestros retiros? 💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'donde' in user_message or 'ubicación' in user_message or 'where' in user_message:
        response = "🏔️ Valle de Bravo, Estado de México. Un lugar sagrado en las montañas, perfecto para transformación profunda. 🌿💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'retiro' in user_message or 'retreat' in user_message or 'que es' in user_message:
        response = "✨ Retiro de 3 días con ayahuasca sagrada, temazcal, cacao ceremonial. 11 enero 2025 en Valle de Bravo. 🌿💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'medicina' in user_message or 'ayahuasca' in user_message:
        response = "🌿 Ayahuasca sagrada, temazcal ceremonial, cacao del corazón y rapé. Con facilitadores experimentados en ambiente seguro. 💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'precio' in user_message or 'costo' in user_message or 'cost' in user_message:
        response = "💫 Te invito a agendar tu discovery call gratuito para hablar sobre inversión y detalles. Conversación personalizada sin compromiso. 🌿 https://sacred-rebirth.com/appointment.html"
        
    elif 'test' in user_message or 'prueba' in user_message:
        response = "✅ ¡Maya funcionando! Bot activo, listo para appointment setting. Sacred Rebirth operativo. 🌿✨"
        
    else:
        response = f"🌿 Hola {user_name}, soy Maya de Sacred Rebirth. Pregúntame sobre ubicación, retiro, medicinas o fechas. 💫 https://sacred-rebirth.com/appointment.html"

    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status del bot"""
    await update.message.reply_text("""✅ **Maya Status**
🤖 Bot: Activo
🌿 Appointment setter: OK
📅 Retiro: 11 enero 2025
📍 Valle de Bravo
💫 Sistema operativo""", parse_mode='Markdown')

def main():
    """Función principal ultra-simple"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN requerido")
        return

    print("🤖 Iniciando aplicación...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Handlers mínimos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Maya lista como appointment setter!")
    app.run_polling()

if __name__ == '__main__':
    main()