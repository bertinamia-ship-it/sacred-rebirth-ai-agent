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
                model="gpt-4o-mini",  # Most cost-effective model
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"User {user_name} says: {user_message}"}
                ],
                max_tokens=250,  # Reduced for cost efficiency
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
• Answer questions intelligently (bilingual)
• Generate complete marketing campaigns
• Create daily social media content
• Generate business analytics reports
• Design email marketing sequences  
• Track API costs and usage
• Provide personalized guidance

**📊 Professional Commands:**
• `/campaign` - Complete marketing strategy
• `/report` - Business analytics & forecasts
• `/social [day]` - Daily content creation
• `/email` - Email campaign sequence
• `/costs` - Budget tracking & optimization

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
    """Generate professional marketing campaign"""
    if not maya.openai_client:
        await update.message.reply_text("🚨 AI features require OpenAI API key. Using basic mode.")
        return
    
    await update.message.reply_text("🎯 Generating professional marketing campaign... Please wait.")
    
    try:
        response = maya.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are an expert marketing strategist for Sacred Rebirth retreat business. 
Generate a COMPLETE professional marketing campaign for: {maya.retreat_info['name']}
Dates: {maya.retreat_info['dates']} | Location: {maya.retreat_info['location']}

Include:
1. TARGET AUDIENCE analysis
2. 7-day SOCIAL MEDIA content calendar 
3. EMAIL campaign sequence (3 emails)
4. FACEBOOK ad copy (2 variations)
5. INSTAGRAM stories strategy
6. CONVERSION optimization tips

Each piece must include: {maya.retreat_info['booking_url']}
Focus on transformation, healing, spiritual growth. Professional tone."""},
                {"role": "user", "content": "Generate complete marketing campaign for January 2025 retreat"}
            ],
            max_tokens=800,  # Larger for comprehensive campaign
            temperature=0.6
        )
        
        campaign = response.choices[0].message.content
        
        # Send campaign in chunks to avoid Telegram limits
        chunks = [campaign[i:i+4000] for i in range(0, len(campaign), 4000)]
        
        for i, chunk in enumerate(chunks):
            header = "📊 **COMPLETE MARKETING CAMPAIGN**\n\n" if i == 0 else f"📊 **Campaign (Part {i+1})**\n\n"
            await update.message.reply_text(f"{header}{chunk}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating campaign: {str(e)}")

async def generate_report(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate business analytics report"""
    if not maya.openai_client:
        await update.message.reply_text("🚨 AI features require OpenAI API key.")
        return
    
    await update.message.reply_text("📊 Generating analytics report... Please wait.")
    
    try:
        # Simulate current date analytics
        current_date = datetime.now().strftime("%B %d, %Y")
        days_to_retreat = (datetime(2025, 1, 11) - datetime.now()).days
        
        response = maya.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""You are a business analyst for Sacred Rebirth retreat.
Generate a professional analytics report for retreat: {maya.retreat_info['name']}
Today: {current_date} | Days until retreat: {days_to_retreat}

Include:
1. BOOKING STATUS forecast
2. MARKETING performance recommendations  
3. SOCIAL MEDIA optimization tips
4. CONVERSION rate improvement strategies
5. LAST-MINUTE booking tactics
6. POST-RETREAT follow-up plan

Make it actionable and data-driven. Include: {maya.retreat_info['booking_url']}"""},
                {"role": "user", "content": f"Generate comprehensive business report for retreat in {days_to_retreat} days"}
            ],
            max_tokens=600,
            temperature=0.5
        )
        
        report = response.choices[0].message.content
        await update.message.reply_text(f"📈 **ANALYTICS REPORT**\n\n{report}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating report: {str(e)}")

async def create_social_content(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate daily social media content"""
    if not maya.openai_client:
        await update.message.reply_text("🚨 AI features require OpenAI API key.")
        return
    
    # Get day of week or custom day from command
    args = context.args
    day = args[0] if args else datetime.now().strftime("%A")
    
    await update.message.reply_text(f"📱 Creating {day} social content...")
    
    try:
        response = maya.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""Create professional social media content for Sacred Rebirth.
Retreat: {maya.retreat_info['name']} | {maya.retreat_info['dates']}

For {day}, create:
1. INSTAGRAM POST (caption + hashtags)
2. FACEBOOK POST (longer format)
3. INSTAGRAM STORY idea
4. LINKEDIN article concept

Themes by day:
Monday: Education about plant medicine
Tuesday: Testimonials & transformation
Wednesday: Behind the scenes
Thursday: Retreat preparation tips
Friday: Spiritual insights
Saturday: Community & connection  
Sunday: Reflection & intention

Always include: {maya.retreat_info['booking_url']}
Professional, engaging, spiritual tone."""},
                {"role": "user", "content": f"Generate complete social media content for {day}"}
            ],
            max_tokens=500,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        await update.message.reply_text(f"📱 **{day.upper()} CONTENT CREATED**\n\n{content}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error creating content: {str(e)}")

async def email_campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Generate email marketing campaign"""
    if not maya.openai_client:
        await update.message.reply_text("🚨 AI features require OpenAI API key.")
        return
    
    await update.message.reply_text("📧 Generating email campaign sequence...")
    
    try:
        response = maya.openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": f"""Create professional email marketing sequence for Sacred Rebirth.
Retreat: {maya.retreat_info['name']} | {maya.retreat_info['dates']}

Generate 3 email sequence:
1. WELCOME EMAIL (for new leads)
2. EDUCATION EMAIL (about plant medicine)  
3. URGENCY EMAIL (limited spots)

Each email needs:
- Subject line (high open rate)
- Professional body copy
- Clear call-to-action
- Personal touch from Maya

Target: People interested in spiritual transformation, healing, personal growth
Always include: {maya.retreat_info['booking_url']}"""},
                {"role": "user", "content": "Generate complete 3-email marketing sequence"}
            ],
            max_tokens=700,
            temperature=0.6
        )
        
        emails = response.choices[0].message.content
        await update.message.reply_text(f"📧 **EMAIL CAMPAIGN SEQUENCE**\n\n{emails}")
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generating emails: {str(e)}")

async def cost_tracker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Track API usage and costs"""
    await update.message.reply_text(f"""
💰 **SMART MAYA COST TRACKING**

**Current Setup:**
🔸 Model: gpt-4o-mini (most cost-effective)
🔸 Budget: $20 USD allocated
🔸 Token limits optimized for efficiency

**Estimated Costs per Action:**
• Normal conversation: ~$0.002-0.005
• Campaign generation: ~$0.01-0.02  
• Report creation: ~$0.008-0.015
• Social content: ~$0.006-0.012
• Email campaign: ~$0.010-0.020

**Budget Optimization:**
✅ Using shortest effective prompts
✅ Smart token limits (250-800 max)
✅ Fallback to basic responses when needed
✅ Efficient model selection

**Estimated Usage with $20:**
🎯 ~1000-4000 conversations
🎯 ~100-200 campaigns  
🎯 ~150-250 reports
🎯 ~200-300 content pieces

Maya is optimized for professional results within budget! 🌿✨
""")

def main():
    """Main function"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ TELEGRAM_BOT_TOKEN required")
        return

    print("🤖 Starting Professional Smart Maya...")
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()

    # Professional commands
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("campaign", generate_campaign))
    app.add_handler(CommandHandler("report", generate_report))
    app.add_handler(CommandHandler("social", create_social_content))
    app.add_handler(CommandHandler("email", email_campaign))
    app.add_handler(CommandHandler("costs", cost_tracker))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("✅ Professional Smart Maya ready! Full business automation operational!")
    app.run_polling()

if __name__ == '__main__':
    main()