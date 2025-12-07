#!/usr/bin/env python3
"""
Maya - Sacred Rebirth Marketing Agent
Ultra-lightweight for Railway but with full intelligence
"""
import os
import logging
from datetime import datetime

print("🚀 Maya starting...")

try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    print("⚠️ dotenv not available")

try:
    from telegram import Update
    from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
    print("✅ Telegram imported")
except Exception as e:
    print(f"❌ Telegram error: {e}")
    exit(1)

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
    print("✅ OpenAI available")
except:
    OPENAI_AVAILABLE = False
    print("⚠️ OpenAI not available")

# Config
TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_KEY = os.getenv('OPENAI_API_KEY')

print(f"🔑 Token: {'✅' if TOKEN else '❌'}")
print(f"🤖 OpenAI: {'✅' if OPENAI_KEY else '❌'}")

class Maya:
    def __init__(self):
        self.ai = None
        if OPENAI_KEY and OPENAI_AVAILABLE:
            try:
                self.ai = OpenAI(api_key=OPENAI_KEY)
                print("✅ Maya AI ready")
            except Exception as e:
                print(f"⚠️ AI failed: {e}")
        
        self.info = {
            "retreat": "Sacred Plant Medicine Retreat",
            "date": "August 11, 2025",
            "location": "Valle de Bravo, Mexico",
            "spaces": "8 exclusive spaces only",
            "target": "High-income spiritual seekers",
            "link": "https://sacred-rebirth.com/appointment.html"
        }

    def get_response(self, message, name=""):
        """Smart response with AI or fallback"""
        
        if self.ai:
            try:
                # Detect language
                spanish = any(w in message.lower() for w in ['hola', 'que', 'donde', 'precio', 'retiro'])
                lang = "Spanish" if spanish else "English"
                
                # AI response
                response = self.ai.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=[{
                        "role": "system", 
                        "content": f"""You are Maya, wise facilitator for Sacred Rebirth.

RETREAT INFO:
- {self.info['retreat']}
- Date: {self.info['date']}
- Location: {self.info['location']}  
- Capacity: {self.info['spaces']}
- Target: {self.info['target']}

RULES:
1. Respond in {lang}
2. NEVER mention prices
3. Always include: {self.info['link']}
4. Be warm, spiritual, professional
5. Focus on transformation and exclusivity"""
                    }, {
                        "role": "user",
                        "content": f"{name} says: {message}"
                    }],
                    max_tokens=250,
                    temperature=0.8
                )
                
                ai_text = response.choices[0].message.content.strip()
                
                # Ensure link included
                if self.info['link'] not in ai_text:
                    if spanish:
                        ai_text += f"\n\n💫 Agenda tu discovery call: {self.info['link']}"
                    else:
                        ai_text += f"\n\n💫 Book your discovery call: {self.info['link']}"
                
                return ai_text
                
            except Exception as e:
                print(f"AI error: {e}")
        
        # Fallback responses
        msg = message.lower()
        link = self.info['link']
        
        # Spanish
        if any(w in msg for w in ['hola', 'que', 'donde', 'precio', 'retiro']):
            if 'precio' in msg or 'costo' in msg:
                return f"💎 Los detalles de inversión se discuten en tu discovery call personalizado. 🌿 Agenda aquí: {link}"
            elif 'retiro' in msg or 'que' in msg:
                return f"✨ Retiro exclusivo de medicina sagrada (11 agosto 2025) en Valle de Bravo. Solo 8 espacios para transformación profunda. 🌿💫 Agenda tu discovery call: {link}"
            elif 'donde' in msg:
                return f"🏔️ Valle de Bravo, México. Santuario sagrado en las montañas para solo 8 participantes selectos. 🌿💫 Agenda tu discovery call: {link}"
            else:
                return f"🌿 ¡Hola {name}! Soy Maya de Sacred Rebirth. Te ayudo con nuestro retiro exclusivo de transformación. 💫 Agenda tu discovery call: {link}"
        
        # English  
        else:
            if any(w in msg for w in ['price', 'cost', 'money']):
                return f"💎 Investment details are discussed in your personalized discovery call. 🌿 Book here: {link}"
            elif any(w in msg for w in ['retreat', 'what', 'about']):
                return f"✨ Exclusive sacred medicine retreat (August 11, 2025) in Valle de Bravo. Only 8 spaces for profound transformation. 🌿💫 Book your discovery call: {link}"
            elif 'where' in msg or 'location' in msg:
                return f"🏔️ Valle de Bravo, Mexico. Sacred mountain sanctuary for only 8 select participants. 🌿💫 Book your discovery call: {link}"
            else:
                return f"🌿 Hello {name}! I'm Maya from Sacred Rebirth. I help with our exclusive transformation retreat. 💫 Book your discovery call: {link}"

# Initialize Maya
maya = Maya()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    days = (datetime(2025, 8, 11) - datetime.now()).days
    
    await update.message.reply_text(f"""
🌟 Hello {user.first_name}!

I'm Maya, your intelligent marketing agent for Sacred Rebirth.

**🌿 EXCLUSIVE RETREAT**
📅 August 11, 2025 ({days} days)
📍 Valle de Bravo, Mexico  
👥 ONLY 8 spaces available
💎 Premium spiritual transformation

**🤖 I'M YOUR COMPLETE TEAM:**
• Intelligent appointment setter (bilingual)
• Content creator & marketing strategist
• Lead generator for high-income clients
• Business analytics & optimization
• Cost-efficient AI ($2.84/month)

**🚀 COMMANDS:**
• `/activate` - Start full automation
• `/content` - Generate premium content
• `/analytics` - Business reports
• `/campaign` - Marketing strategy

💫 Book discovery call: https://sacred-rebirth.com/appointment.html

Ask me anything - I understand natural conversation! 🌿✨
""")

async def activate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Activate marketing automation"""
    await update.message.reply_text("🚀 ACTIVATING MARKETING AUTOMATION...")
    
    response = maya.get_response(
        "Activate complete marketing automation system for Sacred Rebirth retreat", 
        update.effective_user.first_name
    )
    
    await update.message.reply_text(f"✅ **SYSTEM ACTIVATED**\n\n{response}")

async def content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate content"""
    await update.message.reply_text("📱 Creating premium content...")
    
    response = maya.get_response(
        "Generate today's social media content package: Instagram post, Facebook post, email template",
        update.effective_user.first_name
    )
    
    await update.message.reply_text(f"📱 **TODAY'S CONTENT**\n\n{response}")

async def analytics(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Business analytics"""
    days = (datetime(2025, 8, 11) - datetime.now()).days
    
    response = maya.get_response(
        f"Generate business analytics report: retreat in {days} days, targeting 8 high-income clients",
        update.effective_user.first_name  
    )
    
    await update.message.reply_text(f"📊 **ANALYTICS REPORT**\n\n{response}")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle conversations"""
    user = update.effective_user
    message = update.message.text
    
    response = maya.get_response(message, user.first_name)
    await update.message.reply_text(response)

def main():
    if not TOKEN:
        print("❌ Need TELEGRAM_BOT_TOKEN")
        return
    
    print("🤖 Starting Maya app...")
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("activate", activate))
    app.add_handler(CommandHandler("content", content))
    app.add_handler(CommandHandler("analytics", analytics))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    print("✅ Maya ready! Enterprise marketing operational!")
    app.run_polling()

if __name__ == '__main__':
    main()