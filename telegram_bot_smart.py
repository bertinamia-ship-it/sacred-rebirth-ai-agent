#!/usr/bin/env python3
"""
Sacred Rebirth Telegram Bot - Smart Maya
AI-powered appointment setter with marketing features
"""
import os
import json
import logging
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

# Try to import OpenAI, fallback if not available
try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

load_dotenv()

# Configuration
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

print(f"🚀 Starting Sacred Rebirth Smart Maya...")
print(f"🔑 Bot Token: {'✅ OK' if TELEGRAM_BOT_TOKEN else '❌ MISSING'}")
print(f"🤖 OpenAI API: {'✅ OK' if OPENAI_API_KEY and OPENAI_AVAILABLE else '❌ MISSING'}")

class SmartMaya:
    def __init__(self):
        self.openai_client = None
        if OPENAI_API_KEY and OPENAI_AVAILABLE:
            try:
                self.openai_client = OpenAI(api_key=OPENAI_API_KEY)
                logger.info("✅ OpenAI initialized successfully")
            except Exception as e:
                logger.error(f"❌ OpenAI initialization failed: {e}")
        
        # Updated retreat information from website
        self.retreat_info = {
            "name": "Sacred Plant Medicine Retreat",
            "dates": "January 11-18, 2025",
            "duration": "7 nights, 8 days",
            "location": "Valle de Bravo, Mexico",
            "ceremonies": "4 Sacred ayahuasca ceremonies",
            "daily_activities": "Daily cacao ceremonies, Temazcal (sweat lodge), Breathwork sessions, Integration circles, Yoga & meditation",
            "medicines": "Rapé & sananga medicines",
            "included": "All plant-based meals, Accommodation, Airport transfers",
            "booking_url": "https://sacred-rebirth.com/appointment.html"
        }
        
        self.maya_personality = """You are Maya, a wise and compassionate facilitator for Sacred Rebirth. 
You have years of experience guiding people through spiritual transformation with plant medicines.
You are bilingual (Spanish/English) and respond in the language the person writes to you.
You are warm, understanding, and professional. You NEVER mention prices - always direct to discovery call.
Use spiritual emojis: 🌿✨🌌💫🙏🌱⭐️"""

    async def get_ai_response(self, user_message: str, user_name: str = "") -> str:
        """Get intelligent response from OpenAI"""
        
        if not self.openai_client:
            # Fallback to basic responses if OpenAI not available
            return self.get_basic_response(user_message, user_name)
        
        try:
            # Detect language
            language = "Spanish" if any(word in user_message.lower() for word in ['hola', 'que', 'donde', 'cuando', 'como', 'precio', 'costo']) else "English"
            
            system_prompt = f"""{self.maya_personality}

RETREAT INFORMATION:
- Name: {self.retreat_info['name']}
- Dates: {self.retreat_info['dates']} 
- Duration: {self.retreat_info['duration']}
- Location: {self.retreat_info['location']}
- Ceremonies: {self.retreat_info['ceremonies']}
- Daily Activities: {self.retreat_info['daily_activities']}
- Medicines: {self.retreat_info['medicines']}
- Included: {self.retreat_info['included']}

CRITICAL RULES:
1. NEVER mention specific prices in any language
2. If asked about price/cost/investment, always say: "I invite you to book your free discovery call: {self.retreat_info['booking_url']}"
3. Always end responses with the booking link
4. Respond in {language}
5. Be warm, wise, and spiritual
6. Focus on transformation and healing"""

            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User {user_name} says: {user_message}"}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            ai_response = response.choices[0].message.content.strip()
            
            # Ensure booking link is always included
            if self.retreat_info['booking_url'] not in ai_response:
                ai_response += f"\n\n💫 {self.retreat_info['booking_url']}"
                
            return ai_response
            
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            return self.get_basic_response(user_message, user_name)

    def get_basic_response(self, user_message: str, user_name: str = "") -> str:
        """Fallback basic responses if OpenAI not available"""
        
        message_lower = user_message.lower()
        booking_link = self.retreat_info['booking_url']
        
        # Detect language
        if any(word in message_lower for word in ['hola', 'que', 'donde', 'cuando', 'como', 'precio', 'costo']):
            # Spanish responses
            if any(word in message_lower for word in ['hola', 'hello', 'hi']):
                return f"🌿 ¡Hola {user_name}! Soy Maya de Sacred Rebirth. ¿En qué puedo ayudarte con nuestro retiro de medicina sagrada de 7 noches? 💫 {booking_link}"
            elif any(word in message_lower for word in ['donde', 'ubicación', 'lugar']):
                return f"🏔️ Nuestro retiro es en Valle de Bravo, México. Un santuario sagrado en las montañas perfecto para transformación profunda. 🌿💫 {booking_link}"
            elif any(word in message_lower for word in ['que', 'qué', 'retiro', 'incluye']):
                return f"✨ Retiro de medicina sagrada de 7 noches: 4 ceremonias de ayahuasca, cacao diario, temazcal, trabajo de respiración, yoga, círculos de integración. Comidas y alojamiento incluidos. 11-18 enero 2025. 🌿💫 {booking_link}"
            elif any(word in message_lower for word in ['precio', 'costo', 'cuanto']):
                return f"💫 Te invito a agendar tu discovery call gratuito para hablar sobre la inversión y detalles personalizados. 🌿 {booking_link}"
            else:
                return f"🌿 Hola {user_name}, soy Maya de Sacred Rebirth. Pregúntame sobre nuestro retiro de 7 noches, ubicación, ceremonias o fechas. 💫 {booking_link}"
        else:
            # English responses
            if any(word in message_lower for word in ['hello', 'hi', 'hey']):
                return f"🌿 Hello {user_name}! I'm Maya from Sacred Rebirth. How can I help you with our 7-night sacred plant medicine retreat? 💫 {booking_link}"
            elif any(word in message_lower for word in ['where', 'location']):
                return f"🏔️ Our retreat is in Valle de Bravo, Mexico. A sacred mountain sanctuary perfect for deep transformation. 🌿💫 {booking_link}"
            elif any(word in message_lower for word in ['what', 'retreat', 'include']):
                return f"✨ 7-night sacred plant medicine retreat: 4 ayahuasca ceremonies, daily cacao, temazcal, breathwork, yoga, integration circles. All meals & accommodation included. January 11-18, 2025. 🌿💫 {booking_link}"
            elif any(word in message_lower for word in ['price', 'cost', 'money']):
                return f"💫 I invite you to book your free discovery call to discuss investment and personalized details. 🌿 {booking_link}"
            else:
                return f"🌿 Hello {user_name}, I'm Maya from Sacred Rebirth. Ask me about our 7-night retreat, location, ceremonies, or dates. 💫 {booking_link}"

# Initialize Smart Maya
maya = SmartMaya()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Start command"""
    user = update.effective_user
    await update.message.reply_text(f"""
🙏 Hello {user.first_name}!

I'm Maya, your intelligent facilitator for Sacred Rebirth.

**🌿 Sacred Plant Medicine Retreat**
📅 January 11-18, 2025  
📍 Valle de Bravo, Mexico
⏱️ 7 nights, 8 days immersion

**✨ What's Included:**
• 4 Sacred ayahuasca ceremonies
• Daily cacao ceremonies
• Temazcal (sweat lodge) 
• Rapé & sananga medicines
• Breathwork sessions
• Integration circles
• Yoga & meditation
• All meals (plant-based)
• Accommodation
• Airport transfers

**🤖 I'm AI-powered and can:**
• Answer questions intelligently
• Respond in Spanish or English
• Provide personalized guidance
• Generate marketing content
• Create reports and analytics

💫 Free discovery call to discuss your journey:
{maya.retreat_info['booking_url']}

Ask me anything! I understand natural conversation. 🌿✨
""")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle all text messages with AI"""
    
    user = update.effective_user
    user_message = update.message.text
    
    logger.info(f"💬 {user.first_name}: {user_message[:50]}...")
    
    # Get AI response
    response = await maya.get_ai_response(user_message, user.first_name)
    
    await update.message.reply_text(response)

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Status command"""
    ai_status = "✅ Active" if maya.openai_client else "⚠️ Basic Mode"
    await update.message.reply_text(f"""
✅ **Maya Smart Status**
🤖 Bot: Active
🧠 AI: {ai_status}
🌿 Appointment setter: Ready
📅 Retreat: January 11-18, 2025 (7 nights)
📍 Valle de Bravo, Mexico
💫 System operational

{f"🎯 OpenAI Model: gpt-4o-mini" if maya.openai_client else "🔧 Using basic responses"}
""", parse_mode='Markdown')

async def generate_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate marketing campaign"""
    if not maya.openai_client:
        await update.message.reply_text("🚨 AI features require OpenAI API key. Using basic mode.")
        return
    
    await update.message.reply_text("🎯 Generating marketing campaign... Please wait.")
    
    try:
        response = maya.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are a marketing expert for Sacred Rebirth. 
Generate a complete marketing campaign for the retreat: {maya.retreat_info['name']}
Dates: {maya.retreat_info['dates']}
Include: social media posts, email subject lines, target audience strategies.
Always include booking link: {maya.retreat_info['booking_url']}"""},
                {"role": "user", "content": "Generate a complete 7-day marketing campaign for the January retreat"}
            ],
            max_tokens=1000,
            temperature=0.7
        )
        
        campaign = response.choices[0].message.content
        await update.message.reply_text(f"📊 **Marketing Campaign Generated:**\n\n{campaign}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating campaign: {str(e)}")

def main():
    """Main function"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN required")
        return

    print("🤖 Starting Smart Maya application...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Add handlers
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("campaign", generate_campaign))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Smart Maya ready! AI-powered appointment setter operational!")
    app.run_polling()

if __name__ == '__main__':
    main()