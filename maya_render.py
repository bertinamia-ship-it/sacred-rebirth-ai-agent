#!/usr/bin/env python3
"""
Maya - Sacred Rebirth Bot for Render
Guaranteed to work on Render with minimal dependencies
"""
import os
import sys

print("🚀 Maya starting on Render...")

# Check Python version
print(f"🐍 Python: {sys.version}")

# Load environment variables
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

print(f"🔑 Bot Token: {'✅ Found' if TELEGRAM_BOT_TOKEN else '❌ Missing'}")
print(f"🤖 OpenAI Key: {'✅ Found' if OPENAI_API_KEY else '❌ Missing'}")

if not TELEGRAM_BOT_TOKEN:
    print("❌ TELEGRAM_BOT_TOKEN is required!")
    print("Add it in Environment variables in Render dashboard")
    sys.exit(1)

# Import required libraries
try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✅ Telegram library imported")
except ImportError as e:
    print(f"❌ Telegram import failed: {e}")
    sys.exit(1)

try:
    from openai import OpenAI
    openai_available = True
    print("✅ OpenAI library imported")
except ImportError:
    openai_available = False
    print("⚠️ OpenAI not available, using fallback mode")

# Initialize OpenAI if available
ai_client = None
if OPENAI_API_KEY and openai_available:
    try:
        ai_client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI client initialized")
    except Exception as e:
        print(f"⚠️ OpenAI failed: {e}")

# Bot responses
def get_response(message, name=""):
    """Get intelligent response"""
    
    booking_link = "https://sacred-rebirth.com/appointment.html"
    
    # Use AI if available
    if ai_client:
        try:
            # Detect language
            spanish = any(w in message.lower() for w in ['hola', 'que', 'donde', 'precio'])
            lang = "Spanish" if spanish else "English"
            
            response = ai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "system",
                    "content": f"""You are Maya, Sacred Rebirth facilitator.

Sacred Plant Medicine Retreat:
- August 11, 2025
- Valle de Bravo, Mexico
- Only 8 exclusive spaces
- High-income spiritual seekers

Respond in {lang}. NEVER mention prices. Always include: {booking_link}
Be warm, spiritual, professional."""
                }, {
                    "role": "user", 
                    "content": f"{name}: {message}"
                }],
                max_tokens=200,
                temperature=0.8
            )
            
            ai_text = response.choices[0].message.content
            
            if booking_link not in ai_text:
                if spanish:
                    ai_text += f"\n\n💫 Agenda tu discovery call: {booking_link}"
                else:
                    ai_text += f"\n\n💫 Book your discovery call: {booking_link}"
            
            return ai_text
            
        except Exception as e:
            print(f"⚠️ AI error: {e}")
    
    # Fallback responses
    msg = message.lower()
    
    # Spanish responses
    if any(w in msg for w in ['hola', 'que', 'donde', 'precio', 'retiro']):
        if 'precio' in msg:
            return f"💎 Los detalles se discuten en tu discovery call personalizado. 🌿 Agenda: {booking_link}"
        elif 'retiro' in msg or 'que' in msg:
            return f"✨ Retiro exclusivo medicina sagrada (11 agosto 2025) Valle de Bravo. Solo 8 espacios. 🌿💫 Agenda: {booking_link}"
        else:
            return f"🌿 ¡Hola {name}! Soy Maya. Retiro exclusivo transformacional. 💫 Agenda: {booking_link}"
    
    # English responses
    else:
        if any(w in msg for w in ['price', 'cost']):
            return f"💎 Details discussed in your personalized discovery call. 🌿 Book: {booking_link}"
        elif any(w in msg for w in ['retreat', 'what']):
            return f"✨ Exclusive sacred medicine retreat (August 11, 2025) Valle de Bravo. Only 8 spaces. 🌿💫 Book: {booking_link}"
        else:
            return f"🌿 Hello {name}! I'm Maya. Exclusive transformational retreat. 💫 Book: {booking_link}"

# Telegram handlers
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user = update.effective_user
    
    await update.message.reply_text(f"""
🌟 Hello {user.first_name}!

I'm Maya, your Sacred Rebirth marketing agent.

**🌿 EXCLUSIVE RETREAT**
📅 August 11, 2025
📍 Valle de Bravo, Mexico
👥 ONLY 8 spaces
💎 Premium transformation

**🤖 ENTERPRISE FEATURES:**
• Intelligent appointment setter
• Marketing automation  
• Lead generation & conversion
• Business analytics
• Cost-optimized AI

💫 Book discovery call: https://sacred-rebirth.com/appointment.html

Ask me anything! 🌿✨
""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle messages"""
    user = update.effective_user
    message = update.message.text
    
    print(f"💬 {user.first_name}: {message[:30]}...")
    
    response = get_response(message, user.first_name)
    await update.message.reply_text(response)

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Activate marketing"""
    response = get_response("Activate complete marketing automation", update.effective_user.first_name)
    await update.message.reply_text(f"🚀 **ACTIVATED**\n\n{response}")

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate content"""
    response = get_response("Generate today's social media content", update.effective_user.first_name)
    await update.message.reply_text(f"📱 **CONTENT**\n\n{response}")

def main():
    """Main function"""
    
    print("🤖 Creating Telegram application...")
    
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("✅ Telegram app created")
    except Exception as e:
        print(f"❌ Failed to create app: {e}")
        sys.exit(1)
    
    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("content", content))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Maya ready! Starting polling...")
    
    try:
        app.run_polling()
    except Exception as e:
        print(f"❌ Polling failed: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()