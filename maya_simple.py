#!/usr/bin/env python3
"""
Sacred Rebirth Telegram Bot - Maya Appointment Setter
Ultra-simplified version that works guaranteed
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

load_dotenv()

# Basic configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

print("🚀 Starting Sacred Rebirth Bot Ultra-Simple...")
print(f"🔑 Bot Token: {'✅ OK' if TELEGRAM_BOT_TOKEN else '❌ MISSING'}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Command /start"""
    user = update.effective_user
    await update.message.reply_text(f"""
🙏 Hello {user.first_name}!

I'm Maya, facilitator for Sacred Rebirth.

**🌿 Transformation Retreat**
📅 January 11th, 2025  
📍 Valle de Bravo, Mexico
⏱️ 3 days, 2 nights

**✨ Includes:**
• Sacred ayahuasca
• Ceremonial temazcal  
• Ceremonial cacao
• Complete guidance

💫 Free discovery call:
https://sacred-rebirth.com/appointment.html

How can I help you? 🌿
""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maya responds as appointment setter"""
    
    user_message = update.message.text.lower()
    user_name = update.effective_user.first_name
    
    print(f"💬 {user_name}: {update.message.text[:30]}...")

    # Maya responds automatically
    if 'hola' in user_message or 'hello' in user_message or 'hi' in user_message:
        response = f"🌿 Hello {user_name}! I'm Maya from Sacred Rebirth. How can I help you with our retreats? 💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'donde' in user_message or 'ubicación' in user_message or 'where' in user_message or 'location' in user_message:
        response = "🏔️ Valle de Bravo, Estado de México. A sacred place in the mountains, perfect for deep transformation. 🌿💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'retiro' in user_message or 'retreat' in user_message or 'what is' in user_message or 'que es' in user_message:
        response = "✨ 3-day retreat with sacred ayahuasca, temazcal, ceremonial cacao. January 11th 2025 in Valle de Bravo. 🌿💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'medicina' in user_message or 'ayahuasca' in user_message or 'medicine' in user_message:
        response = "🌿 Sacred ayahuasca, ceremonial temazcal, heart cacao and rapé. With experienced facilitators in safe environment. 💫 https://sacred-rebirth.com/appointment.html"
        
    elif 'precio' in user_message or 'costo' in user_message or 'cost' in user_message or 'price' in user_message:
        response = "💫 I invite you to schedule your free discovery call to discuss investment and details. Personalized conversation with no commitment. 🌿 https://sacred-rebirth.com/appointment.html"
        
    elif 'test' in user_message or 'prueba' in user_message:
        response = "✅ Maya working! Bot active, ready for appointment setting. Sacred Rebirth operational. 🌿✨"
        
    else:
        response = f"🌿 Hello {user_name}, I'm Maya from Sacred Rebirth. Ask me about location, retreat, medicines or dates. 💫 https://sacred-rebirth.com/appointment.html"

    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Bot status"""
    await update.message.reply_text("""✅ **Maya Status**
🤖 Bot: Active
🌿 Appointment setter: OK
📅 Retreat: January 11th 2025
📍 Valle de Bravo
💫 System operational""", parse_mode='Markdown')

def main():
    """Ultra-simple main function"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN required")
        return

    print("🤖 Starting application...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Minimal handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Maya ready as appointment setter!")
    app.run_polling()

if __name__ == '__main__':
    main()