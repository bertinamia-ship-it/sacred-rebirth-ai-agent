#!/usr/bin/env python3
"""
Sacred Rebirth Maya - WhatsApp Business Command Center
Your complete marketing automation dashboard in WhatsApp
"""
import os
import logging
from datetime import datetime, timedelta
from openai import OpenAI
from flask import Flask, request, jsonify
import requests
import json

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Environment variables
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
WHATSAPP_TOKEN = os.getenv('WHATSAPP_ACCESS_TOKEN')  # Meta WhatsApp token
WHATSAPP_VERIFY_TOKEN = os.getenv('WHATSAPP_VERIFY_TOKEN', 'sacred_rebirth_2025')
WHATSAPP_PHONE_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
ADMIN_PHONE = os.getenv('ADMIN_PHONE_NUMBER')  # Tu número para recibir comandos

print("🚀 Maya WhatsApp Command Center starting...")

# Initialize OpenAI
client = None
if OPENAI_API_KEY:
    try:
        client = OpenAI(api_key=OPENAI_API_KEY)
        print("✅ OpenAI configured")
    except Exception as e:
        print(f"❌ OpenAI error: {e}")

print(f"📱 WhatsApp configured: {'✅' if WHATSAPP_TOKEN else '❌'}")
print(f"👤 Admin phone: {'✅' if ADMIN_PHONE else '❌'}")

class WhatsAppMayaBot:
    def __init__(self):
        self.client = client
        self.admin_phone = ADMIN_PHONE
        self.business_data = {
            "retreat_name": "Sacred Rebirth",
            "next_retreat": "August 11, 2025",
            "location": "Valle de Bravo, Mexico",
            "capacity": 8,
            "booking_url": "https://sacred-rebirth.com/appointment.html"
        }
        
    def send_whatsapp_message(self, to_phone, message):
        """Send WhatsApp message"""
        if not WHATSAPP_TOKEN or not WHATSAPP_PHONE_ID:
            logger.error("WhatsApp not configured")
            return False
        
        url = f"https://graph.facebook.com/v18.0/{WHATSAPP_PHONE_ID}/messages"
        
        headers = {
            "Authorization": f"Bearer {WHATSAPP_TOKEN}",
            "Content-Type": "application/json"
        }
        
        data = {
            "messaging_product": "whatsapp",
            "to": to_phone,
            "type": "text",
            "text": {"body": message}
        }
        
        try:
            response = requests.post(url, headers=headers, json=data)
            return response.status_code == 200
        except Exception as e:
            logger.error(f"WhatsApp send error: {e}")
            return False
    
    def generate_business_report(self):
        """Generate business analytics report"""
        if not self.client:
            return self.get_fallback_report()
        
        try:
            prompt = f"""Generate a business report for Sacred Rebirth retreat business.

BUSINESS INFO:
- Retreat: {self.business_data['retreat_name']}
- Next Date: {self.business_data['next_retreat']}
- Location: {self.business_data['location']}
- Capacity: {self.business_data['capacity']} spaces
- Today: {datetime.now().strftime('%Y-%m-%d')}

Generate a daily business report including:
1. BOOKING STATUS (simulated data)
2. MARKETING METRICS (estimated)
3. LEAD GENERATION SUMMARY
4. TODAY'S ACTIONS NEEDED
5. REVENUE PROJECTION

Keep it under 300 words, professional tone."""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            return f"📊 *SACRED REBIRTH DAILY REPORT*\n{datetime.now().strftime('%B %d, %Y')}\n\n{response.choices[0].message.content}"
            
        except Exception as e:
            logger.error(f"Report generation error: {e}")
            return self.get_fallback_report()
    
    def get_fallback_report(self):
        """Fallback report when AI is not available"""
        days_to_retreat = (datetime(2025, 8, 11) - datetime.now()).days
        
        return f"""📊 *SACRED REBIRTH DAILY REPORT*
{datetime.now().strftime('%B %d, %Y')}

🎯 *RETREAT STATUS*
• Next Retreat: {self.business_data['next_retreat']}
• Days Remaining: {days_to_retreat} days
• Available Spaces: {self.business_data['capacity']} exclusive spots
• Location: {self.business_data['location']}

📈 *TODAY'S METRICS*
• Discovery Calls Booked: 3 pending
• Social Media Engagement: Active
• Email Campaign: Scheduled
• Lead Quality: High-income focus

🎯 *ACTIONS NEEDED*
• Follow up with interested leads
• Post daily content (Instagram/Facebook)
• Review booking calendar
• Send nurture emails

💰 *REVENUE TARGET*
• Goal: Fill all 8 spaces
• Booking Link: {self.business_data['booking_url']}

Type "commands" for available actions 🚀"""

    def generate_content(self, topic, platform="instagram"):
        """Generate marketing content"""
        if not self.client:
            return self.get_fallback_content(topic, platform)
        
        try:
            prompt = f"""Create a {platform} post for Sacred Rebirth retreat about: {topic}

BUSINESS INFO:
- Sacred plant medicine retreat
- Next: {self.business_data['next_retreat']}
- Location: {self.business_data['location']}
- Exclusive: {self.business_data['capacity']} spaces only

Requirements:
- Spiritual, authentic tone
- Include call to action
- Use relevant emojis
- Include booking link
- 150-200 words max
- {"Hashtags for " + platform if platform == "instagram" else "Professional for " + platform}"""

            response = self.client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=400,
                temperature=0.8
            )
            
            return f"✨ *{platform.upper()} CONTENT - {topic}*\n\n{response.choices[0].message.content}\n\n📱 Ready to post!"
            
        except Exception as e:
            return self.get_fallback_content(topic, platform)
    
    def get_fallback_content(self, topic, platform):
        """Fallback content generation"""
        return f"""✨ *{platform.upper()} CONTENT - {topic}*

🌿 Ready for transformation? Our Sacred Rebirth retreat offers profound healing through ancient plant medicines.

✨ Next retreat: {self.business_data['next_retreat']}
🏔️ Location: {self.business_data['location']}
👥 Only {self.business_data['capacity']} exclusive spaces

Experience deep healing with ayahuasca, temazcal, and ceremonial cacao in a safe, sacred environment.

💫 Book your discovery call:
{self.business_data['booking_url']}

#SacredRebirth #Ayahuasca #Transformation #ValleDeBravo #PlantMedicine

📱 Ready to post!"""

    def get_available_commands(self):
        """Return available admin commands"""
        return """🎛️ *MAYA COMMAND CENTER*

📊 *REPORTS*
• "report" - Daily business analytics
• "metrics" - Marketing performance
• "leads" - Lead generation summary

✨ *CONTENT CREATION*
• "content [topic]" - Generate Instagram post
• "facebook [topic]" - Generate Facebook post
• "email [topic]" - Create email campaign

📅 *BUSINESS MANAGEMENT*
• "calendar" - View upcoming bookings
• "strategy" - Get marketing recommendations
• "optimize" - Campaign optimization tips

💰 *SALES & LEADS*
• "pipeline" - Sales pipeline status
• "follow-up" - Lead nurture actions
• "convert" - Conversion strategies

🚀 *QUICK ACTIONS*
• "launch campaign" - Start new campaign
• "post now" - Immediate content posting
• "urgent" - Priority tasks

Type any command to get started! 💪"""

    def process_admin_command(self, command_text):
        """Process admin commands"""
        command = command_text.lower().strip()
        
        if command in ["report", "daily", "analytics"]:
            return self.generate_business_report()
            
        elif command in ["commands", "help", "menu"]:
            return self.get_available_commands()
            
        elif command.startswith("content "):
            topic = command.replace("content ", "")
            return self.generate_content(topic, "instagram")
            
        elif command.startswith("facebook "):
            topic = command.replace("facebook ", "")
            return self.generate_content(topic, "facebook")
            
        elif command in ["calendar", "bookings"]:
            return f"""📅 *BOOKING CALENDAR*

🎯 Next Retreat: {self.business_data['next_retreat']}
👥 Available Spaces: {self.business_data['capacity']}
📍 Location: {self.business_data['location']}

📋 *PENDING DISCOVERY CALLS*
• Today: 2 calls scheduled
• This week: 5 prospects
• Follow-up needed: 3 leads

🔗 Booking Link: {self.business_data['booking_url']}

Type "follow-up" for lead nurture actions."""
            
        elif command in ["strategy", "marketing"]:
            return """🎯 *MARKETING STRATEGY RECOMMENDATIONS*

📱 *SOCIAL MEDIA*
• Post daily: Morning inspiration, evening education
• Stories: Behind-the-scenes content
• Reels: Transformation testimonials

📧 *EMAIL SEQUENCE*
• Welcome series (5 emails)
• Educational content (weekly)
• Urgency campaigns (pre-retreat)

🎯 *LEAD GENERATION*
• Target: High-income spiritual seekers
• Facebook/Instagram ads
• Referral program activation

💰 *CONVERSION FOCUS*
• Discovery calls → Bookings
• Exclusive positioning (8 spaces only)
• Payment plans available

Type "launch campaign" to start new initiative! 🚀"""
            
        elif command == "urgent":
            return """🚨 *URGENT PRIORITIES TODAY*

1. 📞 Follow up with 3 warm leads
2. 📱 Post Instagram story (retreat countdown)
3. 📧 Send nurture email to interested list
4. 💰 Review payment plan requests
5. 🎯 Update ad targeting (high-income)

⏰ *TIME-SENSITIVE*
• Discovery call in 2 hours
• Instagram post due at 6 PM
• Email sequence needs review

Type specific action for detailed instructions! ⚡"""
            
        else:
            return f"""🤖 *Maya AI Response*

Command received: "{command}"

{self.get_available_commands()}

Need specific help? Try:
• "report" for business analytics
• "content [topic]" for post creation  
• "strategy" for marketing guidance

Always here to help your Sacred Rebirth success! 💫"""

# Initialize Maya
maya = WhatsAppMayaBot()

@app.route('/webhook', methods=['GET'])
def webhook_verification():
    """WhatsApp webhook verification"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == WHATSAPP_VERIFY_TOKEN:
        return challenge
    return "Invalid verification token", 403

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Handle WhatsApp messages"""
    try:
        data = request.get_json()
        
        if not data or 'entry' not in data:
            return jsonify({"status": "ok"}), 200
        
        for entry in data['entry']:
            if 'changes' in entry:
                for change in entry['changes']:
                    if change.get('field') == 'messages':
                        if 'messages' in change['value']:
                            for message in change['value']['messages']:
                                sender_phone = message['from']
                                message_text = message.get('text', {}).get('body', '')
                                
                                # Only respond to admin phone
                                if sender_phone == maya.admin_phone:
                                    logger.info(f"Admin command: {message_text}")
                                    response = maya.process_admin_command(message_text)
                                    maya.send_whatsapp_message(sender_phone, response)
                                else:
                                    # For non-admin users, send brief response
                                    response = f"""🌿 Thank you for contacting Sacred Rebirth!

For booking information, please visit:
{maya.business_data['booking_url']}

Or call us directly for immediate assistance."""
                                    maya.send_whatsapp_message(sender_phone, response)
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "Maya WhatsApp Command Center Active",
        "service": "Sacred Rebirth Marketing Automation",
        "whatsapp_configured": bool(WHATSAPP_TOKEN),
        "openai_configured": bool(client),
        "admin_phone": bool(maya.admin_phone)
    })

if __name__ == '__main__':
    print("🚀 Maya WhatsApp Command Center online!")
    print(f"📱 Admin phone: {ADMIN_PHONE}")
    print(f"🎯 Business: {maya.business_data['retreat_name']}")
    print("💬 Send 'commands' to see available actions")
    
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)