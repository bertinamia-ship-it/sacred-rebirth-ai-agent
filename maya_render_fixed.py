#!/usr/bin/env python3
"""
Sacred Rebirth Maya Bot - Render Fixed Version
Fixed compatibility issue with python-telegram-bot
"""
import os
import logging
from datetime import datetime
from openai import OpenAI
import asyncio

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Environment variables
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

print("🚀 Maya starting...")

# Test imports
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✅ Telegram imported")
except Exception as e:
    print(f"❌ Telegram import failed: {e}")
    exit(1)

try:
    if OPENAI_API_KEY:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI available")
    else:
        client = None
        print("⚠️ OpenAI not configured")
except Exception as e:
    print(f"❌ OpenAI setup failed: {e}")
    client = None

# Validate tokens
if TOKEN:
    print("🔑 Token: ✅")
else:
    print("🔑 Token: ❌")
    print("❌ Need TELEGRAM_BOT_TOKEN")
    exit(1)

if client:
    print("🤖 OpenAI: ✅")
else:
    print("🤖 OpenAI: ❌")

print("✅ Maya AI ready")

# Business information
RETREAT_INFO = {
    "name": "Sacred Plant Medicine Retreat",
    "date": "August 11, 2025", 
    "location": "Valle de Bravo, Mexico",
    "capacity": "8 exclusive spaces",
    "booking_url": "https://sacred-rebirth.com/appointment.html",
    "facilitator": "Michelle Robles"
}

class MayaBot:
    def __init__(self):
        self.client = client
        self.retreat_info = RETREAT_INFO
        
    def get_ai_response(self, user_message, language="auto"):
        """Get AI response with fallback"""
        if not self.client:
            return self.get_fallback_response(user_message, language)
        
        try:
            # Detect language and respond appropriately
            is_spanish = any(word in user_message.lower() for word in 
                           ['hola', 'información', 'retiro', 'ayahuasca', 'cuando', 'donde', 'precio'])
            
            system_prompt = f"""You are Maya, a wise spiritual guide for Sacred Rebirth retreat.
            
RETREAT DETAILS:
- Name: {self.retreat_info['name']}
- Date: {self.retreat_info['date']}
- Location: {self.retreat_info['location']} 
- Capacity: {self.retreat_info['capacity']}
- Booking: {self.retreat_info['booking_url']}

RESPONSE LANGUAGE: {'Spanish' if is_spanish else 'English'}

PERSONALITY: Warm, wise, spiritual, conversational
NEVER mention prices - always direct to discovery call
ALWAYS include booking link
Use spiritual emojis: 🌿✨🌌💫🙏

Keep responses under 200 words."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            logger.error(f"OpenAI error: {e}")
            return self.get_fallback_response(user_message, language)
    
    def get_fallback_response(self, user_message, language="auto"):
        """Fallback responses when AI is not available"""
        is_spanish = any(word in user_message.lower() for word in 
                        ['hola', 'información', 'retiro', 'ayahuasca', 'cuando', 'donde'])
        
        if is_spanish:
            return f"""🌿 ¡Hola! Soy Maya de Sacred Rebirth.

Nuestro próximo retiro de medicina sagrada es el {self.retreat_info['date']} en {self.retreat_info['location']}.

✨ Un retiro de transformación profunda con:
• Ceremonias de ayahuasca
• Temazcal y cacao ceremonial
• Facilitado por {self.retreat_info['facilitator']}
• Solo {self.retreat_info['capacity']}

💫 Para más información, agenda tu discovery call:
{self.retreat_info['booking_url']}

¿Qué te gustaría saber? 🙏"""
        else:
            return f"""🌿 Hello! I'm Maya from Sacred Rebirth.

Our next sacred plant medicine retreat is {self.retreat_info['date']} in {self.retreat_info['location']}.

✨ A deep transformation retreat featuring:
• Ayahuasca ceremonies
• Temazcal & ceremonial cacao
• Facilitated by {self.retreat_info['facilitator']}
• Only {self.retreat_info['capacity']}

💫 For more information, book your discovery call:
{self.retreat_info['booking_url']}

What would you like to know? 🙏"""

# Initialize bot
maya = MayaBot()

# Bot handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    welcome = """🌿 Welcome to Sacred Rebirth! I'm Maya.

I'm here to guide you on your spiritual journey. Our sacred plant medicine retreats offer profound transformation in the beautiful Valle de Bravo, Mexico.

✨ August 11, 2025 - Next retreat
🏔️ Valle de Bravo, Mexico
👥 8 exclusive spaces only

What would you like to know about our retreat?

💫 Ready to begin? Book your discovery call:
https://sacred-rebirth.com/appointment.html"""

    await update.message.reply_text(welcome)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all messages"""
    user_message = update.message.text
    user_name = update.effective_user.first_name or "Friend"
    
    logger.info(f"Message from {user_name}: {user_message}")
    
    # Get AI response
    response = maya.get_ai_response(user_message)
    
    await update.message.reply_text(response)

def main():
    """Start the bot with improved error handling"""
    print("🤖 Starting Maya app...")
    
    try:
        # Create application with explicit configuration
        app = (Application.builder()
               .token(TOKEN)
               .build())
        
        print("✅ Application created")
        
        # Add handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        print("✅ Handlers added")
        
        # Start bot
        print("🚀 Maya is now online and ready!")
        print(f"📅 Next retreat: {RETREAT_INFO['date']}")
        print(f"📍 Location: {RETREAT_INFO['location']}")
        print(f"👥 Capacity: {RETREAT_INFO['capacity']}")
        print(f"🔗 Booking: {RETREAT_INFO['booking_url']}")
        
        # Run with webhook for Render
        port = int(os.environ.get('PORT', 5000))
        app.run_webhook(
            listen="0.0.0.0",
            port=port,
            url_path=TOKEN,
            webhook_url=f"https://sacred-rebirth-ai-agent.onrender.com/{TOKEN}"
        )
        
    except Exception as e:
        logger.error(f"Critical error starting bot: {e}")
        print(f"❌ Bot startup failed: {e}")
        
        # Try polling as fallback
        print("🔄 Trying polling mode...")
        try:
            app = Application.builder().token(TOKEN).build()
            app.add_handler(CommandHandler("start", start))
            app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
            app.run_polling(allowed_updates=Update.ALL_TYPES)
        except Exception as e2:
            logger.error(f"Polling also failed: {e2}")
            print(f"❌ Complete failure: {e2}")

if __name__ == '__main__':
    main()