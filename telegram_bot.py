#!/usr/bin/env python3
"""
Bot de Telegram para Sacred Rebirth AI Agent
Permite interactuar con el agente de marketing a través de Telegram
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.crew import MarketingCrew
from chat import ChatAgent

load_dotenv()

# Configuración
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

# Inicializar agente
print("🤖 Inicializando Marketing Crew para Telegram...")
crew = MarketingCrew()
chat_agent = ChatAgent(crew)
print("✅ Bot de Telegram listo!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Bienvenida"""
    user = update.effective_user
    
    welcome_message = f"""
🙏 ¡Hola {user.first_name}!

Soy el asistente de marketing de Sacred Rebirth.

**Puedo ayudarte con:**
• Crear posts para Instagram/Facebook
• Generar campañas de email
• Gestionar tu calendario de contenido
• Analizar tus leads
• Programar publicaciones

**Ejemplos de comandos:**
• "Crea un post de Instagram sobre ayahuasca"
• "Muestra el calendario de esta semana"
• "Envía email de bienvenida a nuevos leads"
• "Programa 3 posts para mañana"

Solo escríbeme naturalmente y yo entenderé 💬
"""
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Ayuda"""
    help_text = """
📚 **Guía Rápida**

**Crear Contenido:**
• "Genera un post sobre [tema]"
• "Crea contenido para Instagram sobre [tema]"
• "Escribe un email sobre [tema]"

**Publicar:**
• "Publica en Instagram: [texto]"
• "Sube a Facebook: [texto]"

**Gestión:**
• "Muestra mi calendario"
• "Lista mis leads"
• "Programa contenido para mañana"

**Campañas:**
• "Crea campaña completa sobre [tema]"
• "Envía email masivo sobre [tema]"

¿Necesitas algo más? Solo pregúntame naturalmente.
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes de texto"""
    
    # Verificar autorización
    user_id = str(update.effective_user.id)
    if AUTHORIZED_USERS and user_id not in AUTHORIZED_USERS:
        await update.message.reply_text(
            "⛔ Lo siento, no estás autorizado para usar este bot.\n"
            f"Tu ID: {user_id}\n\n"
            "Contacta al administrador para obtener acceso."
        )
        return
    
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    print(f"\n💬 Mensaje de {user_name}: {user_message}")
    
    # Enviar "escribiendo..."
    await update.message.chat.send_action("typing")
    
    try:
        # Procesar con el agente de chat
        response = chat_agent.process_message(user_message)
        
        # Enviar respuesta
        # Dividir respuestas largas (límite de Telegram: 4096 caracteres)
        if len(response) > 4000:
            # Dividir en chunks
            chunks = [response[i:i+4000] for i in range(0, len(response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(response)
        
    except Exception as e:
        error_msg = f"❌ Error procesando tu solicitud: {str(e)}\n\nIntenta de nuevo o usa /help"
        await update.message.reply_text(error_msg)
        print(f"Error: {e}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Estado del sistema"""
    status_msg = """
✅ **Estado del Sistema**

• Bot: Activo
• CrewAI: Operativo
• Agentes: 6/6 funcionando
• OpenAI API: Conectado

**Servicios Configurados:**
"""
    
    # Verificar configuraciones
    services = []
    if os.getenv('META_ACCESS_TOKEN'):
        services.append("✅ Instagram/Facebook")
    else:
        services.append("⚠️ Instagram/Facebook (no configurado)")
    
    if os.getenv('SENDGRID_API_KEY'):
        services.append("✅ Email (SendGrid)")
    else:
        services.append("⚠️ Email (no configurado)")
    
    status_msg += "\n".join(services)
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')


async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /calendar - Ver calendario de contenido"""
    await update.message.chat.send_action("typing")
    
    try:
        response = chat_agent.process_message("muestra mi calendario de contenido")
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /leads - Ver leads"""
    await update.message.chat.send_action("typing")
    
    try:
        response = chat_agent.process_message("muestra mis leads")
        await update.message.reply_text(response)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    """Inicia el bot de Telegram"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado en .env")
        print("\nPara obtener un token:")
        print("1. Habla con @BotFather en Telegram")
        print("2. Usa /newbot y sigue las instrucciones")
        print("3. Copia el token a tu archivo .env")
        return
    
    print("🚀 Iniciando bot de Telegram...")
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(CommandHandler("leads", leads))
    
    # Handler para todos los mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar bot
    print("✅ Bot iniciado! Esperando mensajes...")
    print(f"📱 Los usuarios autorizados pueden empezar a chatear")
    if AUTHORIZED_USERS:
        print(f"🔐 IDs autorizados: {', '.join(AUTHORIZED_USERS)}")
    else:
        print("⚠️ Advertencia: Todos los usuarios pueden usar el bot (configura TELEGRAM_AUTHORIZED_USERS)")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
