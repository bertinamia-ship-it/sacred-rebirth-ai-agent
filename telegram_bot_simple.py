#!/usr/bin/env python3
"""
Sacred Rebirth Telegram Bot - Version Simplificada
Bot básico garantizado que funciona
"""
import os
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

# Configuración básica
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

print("🚀 Iniciando Sacred Rebirth Bot...")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start"""
    user = update.effective_user
    welcome_msg = f"""
🙏 ¡Hola {user.first_name}!

Soy Maya, tu asistente de Sacred Rebirth.

**Retiro Especial: 11 de Enero 2025** 🌿
📍 Valle de Bravo, Estado de México
✨ 3 días de transformación profunda

**Puedo ayudarte con:**
• Información sobre el retiro
• Ubicación y detalles
• Responder tus preguntas

💫 Para más información: https://sacred-rebirth.com/appointment.html

Escríbeme cualquier pregunta 💬
"""
    await update.message.reply_text(welcome_msg)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja mensajes de texto"""
    
    # Verificar autorización
    user_id = str(update.effective_user.id)
    if AUTHORIZED_USERS and user_id not in AUTHORIZED_USERS:
        await update.message.reply_text(
            f"⛔ No estás autorizado.\nTu ID: {user_id}\nContacta al administrador."
        )
        return

    user_message = update.message.text.lower()
    user_name = update.effective_user.first_name
    
    print(f"💬 Mensaje de {user_name}: {update.message.text}")

    # Respuestas básicas como Maya
    if any(word in user_message for word in ['hola', 'hello', 'hi']):
        response = f"🌿 ¡Hola {user_name}! Soy Maya de Sacred Rebirth. ¿En qué puedo ayudarte con información sobre nuestros retiros de transformación? 💫"
        
    elif any(word in user_message for word in ['ubicación', 'donde', 'dónde', 'location', 'where']):
        response = """🏔️ Nuestro espacio sagrado está en Valle de Bravo, Estado de México. 
        
Un hermoso lugar rodeado de montañas y naturaleza, perfecto para la introspección y sanación profunda. 🌿

💫 Agenda tu discovery call gratuito para más detalles: https://sacred-rebirth.com/appointment.html"""

    elif any(word in user_message for word in ['retiro', 'retreat', 'qué es', 'what is', 'consiste']):
        response = """✨ Sacred Rebirth es un retiro de transformación profunda de 3 días y 2 noches.

🌿 Trabajamos con ayahuasca sagrada, temazcal, cacao ceremonial y rapé
📅 Próximo retiro: 11 de enero de 2025
🏠 Incluye alojamiento, comidas y acompañamiento completo

💫 Agenda tu discovery call gratuito: https://sacred-rebirth.com/appointment.html"""

    elif any(word in user_message for word in ['medicina', 'ayahuasca', 'medicine', 'plant']):
        response = """🌿 Trabajamos con medicinas ancestrales sagradas:

• Ayahuasca sagrada (la medicina maestra)
• Temazcal (baño de vapor ceremonial) 
• Cacao ceremonial
• Rapé

Todas administradas por facilitadores experimentados en ambiente seguro. 🙏

💫 Para más información: https://sacred-rebirth.com/appointment.html"""

    elif any(word in user_message for word in ['precio', 'costo', 'price', 'cost', 'cuánto', 'cuanto']):
        response = """💫 Te invito a agendar tu discovery call gratuito para hablar sobre todos los detalles, incluyendo inversión y opciones de pago.

Es una conversación personalizada donde podemos conocerte mejor y responder todas tus preguntas.

🔗 Agenda aquí: https://sacred-rebirth.com/appointment.html"""

    elif 'test' in user_message:
        response = "✅ ¡Maya funcionando correctamente! El bot está activo y listo para ayudar con información sobre Sacred Rebirth. 🌿✨"

    else:
        response = """🌿 Gracias por contactarnos. Soy Maya, facilitadora de Sacred Rebirth.

Puedo ayudarte con información sobre:
• Nuestros retiros de transformación
• Ubicación (Valle de Bravo)
• Medicinas sagradas que utilizamos
• Fechas y detalles

💫 Para conversación personalizada: https://sacred-rebirth.com/appointment.html

¿En qué más puedo ayudarte? ✨"""

    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status"""
    status_msg = """✅ **Sacred Rebirth Bot - Estado**

🤖 Bot: Activo y funcionando
🌿 Maya: Lista para ayudar
📅 Próximo retiro: 11 enero 2025
📍 Ubicación: Valle de Bravo

🔧 Servicios:"""
    
    if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'):
        status_msg += "\n✅ Facebook configurado"
    else:
        status_msg += "\n⚠️ Facebook pendiente"
        
    status_msg += "\n\n💫 Todo funcionando correctamente"
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')

def main():
    """Función principal"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN no configurado")
        return

    print("🤖 Creando aplicación...")
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Registrar handlers
    print("📝 Registrando handlers...")
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # Iniciar bot
    print("✅ Bot iniciado! Esperando mensajes...")
    print(f"🔐 IDs autorizados: {', '.join(AUTHORIZED_USERS) if AUTHORIZED_USERS else 'Todos'}")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == '__main__':
    main()# Force redeploy Sun Dec  7 04:11:11 UTC 2025
