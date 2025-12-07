#!/usr/bin/env python3
"""
Sacred Rebirth Facebook Bot - Standalone
Webhook independiente para responder mensajes de Facebook automáticamente
"""
import os
import json
import requests
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from openai import OpenAI

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
WEBHOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_WEBHOOK_VERIFY_TOKEN', 'sacred_rebirth_webhook_2025')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

class FacebookMayaBot:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        
        # Información del negocio
        self.business_info = {
            "location_es": "Valle de Bravo, Estado de México",
            "location_en": "Valle de Bravo, Estado de México, Mexico",
            "date_es": "11 de enero de 2025",
            "date_en": "January 11th, 2025",
            "booking_url": "https://sacred-rebirth.com/appointment.html"
        }
        
    def detect_language(self, message):
        """Detecta si el mensaje está en inglés o español"""
        english_words = ['hello', 'hi', 'how', 'what', 'where', 'when', 'why', 'retreat', 'price', 'cost', 'the', 'and', 'is', 'are']
        spanish_words = ['hola', 'como', 'cómo', 'qué', 'que', 'donde', 'dónde', 'cuando', 'cuándo', 'retiro', 'precio', 'el', 'la', 'y', 'es', 'están']
        
        message_lower = message.lower()
        english_count = sum(1 for word in english_words if word in message_lower)
        spanish_count = sum(1 for word in spanish_words if word in message_lower)
        
        return "english" if english_count > spanish_count else "spanish"
    
    def get_response_template(self, question_type, language):
        """Obtiene plantilla de respuesta según tipo y idioma"""
        
        templates = {
            "greeting": {
                "spanish": "¡Hola! 🌿 Soy Maya de Sacred Rebirth. Es un placer conocerte. Estoy aquí para ayudarte con cualquier pregunta sobre nuestros retiros de transformación. ¿En qué puedo asistirte? ✨",
                "english": "Hello! 🌿 I'm Maya from Sacred Rebirth. It's a pleasure to meet you. I'm here to help with any questions about our transformation retreats. How can I assist you? ✨"
            },
            "location": {
                "spanish": f"🏔️ Nuestro espacio sagrado está ubicado en {self.business_info['location_es']}, un hermoso lugar rodeado de montañas y naturaleza, perfecto para la introspección y sanación profunda. 🌿💫 Para más detalles sobre el lugar: {self.business_info['booking_url']}",
                "english": f"🏔️ Our sacred space is located in {self.business_info['location_en']}, a beautiful place surrounded by mountains and nature, perfect for introspection and deep healing. 🌿💫 For more details about the location: {self.business_info['booking_url']}"
            },
            "retreat_info": {
                "spanish": f"✨ Sacred Rebirth es un retiro de transformación profunda de 3 días y 2 noches. Trabajamos con ayahuasca sagrada, temazcal, cacao ceremonial y rapé. Nuestro próximo retiro es el {self.business_info['date_es']}. Incluye alojamiento, todas las comidas y acompañamiento completo. 🌿💫 Agenda tu discovery call: {self.business_info['booking_url']}",
                "english": f"✨ Sacred Rebirth is a 3-day, 2-night deep transformation retreat. We work with sacred ayahuasca, temazcal, ceremonial cacao, and rapé. Our next retreat is {self.business_info['date_en']}. Includes accommodation, all meals, and complete guidance. 🌿💫 Book your discovery call: {self.business_info['booking_url']}"
            },
            "medicine": {
                "spanish": f"🌿 Trabajamos con medicinas ancestrales sagradas: ayahuasca (la medicina maestra), temazcal (baño de vapor ceremonial), cacao ceremonial y rapé. Todas son administradas por facilitadores experimentados en un ambiente seguro y sagrado. 💫 Para más información: {self.business_info['booking_url']}",
                "english": f"🌿 We work with sacred ancestral medicines: ayahuasca (the master medicine), temazcal (ceremonial sweat lodge), ceremonial cacao, and rapé. All are administered by experienced facilitators in a safe and sacred environment. 💫 For more information: {self.business_info['booking_url']}"
            },
            "price": {
                "spanish": f"💫 Te invito a agendar tu discovery call gratuito para hablar sobre todos los detalles, incluyendo inversión y opciones de pago. Es una conversación personalizada donde podemos conocerte mejor: {self.business_info['booking_url']}",
                "english": f"💫 I invite you to book your free discovery call to discuss all details, including investment and payment options. It's a personalized conversation where we can get to know you better: {self.business_info['booking_url']}"
            },
            "safety": {
                "spanish": f"🙏 La seguridad es nuestra prioridad. Contamos con facilitadores certificados con años de experiencia, protocolos médicos, y un ambiente completamente seguro. Evaluamos cada participante individualmente. 💫 Hablemos en tu discovery call: {self.business_info['booking_url']}",
                "english": f"🙏 Safety is our priority. We have certified facilitators with years of experience, medical protocols, and a completely safe environment. We evaluate each participant individually. 💫 Let's talk in your discovery call: {self.business_info['booking_url']}"
            },
            "general": {
                "spanish": f"🌿 Gracias por tu interés en Sacred Rebirth. Somos un retiro de transformación espiritual profunda en Valle de Bravo. Te invito a agendar tu discovery call gratuito para conocerte mejor y responder todas tus preguntas: {self.business_info['booking_url']} ✨",
                "english": f"🌿 Thank you for your interest in Sacred Rebirth. We are a deep spiritual transformation retreat in Valle de Bravo. I invite you to book your free discovery call to get to know you better and answer all your questions: {self.business_info['booking_url']} ✨"
            }
        }
        
        return templates.get(question_type, templates["general"])[language]
    
    def analyze_message(self, message):
        """Analiza el mensaje para determinar tipo de pregunta"""
        message_lower = message.lower()
        
        # Detectar tipo de pregunta
        if any(word in message_lower for word in ['hola', 'hello', 'hi', 'buenas', 'hey']):
            return "greeting"
        elif any(word in message_lower for word in ['ubicación', 'donde', 'dónde', 'location', 'where']):
            return "location"
        elif any(word in message_lower for word in ['qué es', 'que es', 'what is', 'about', 'consiste', 'retiro', 'retreat']):
            return "retreat_info"
        elif any(word in message_lower for word in ['medicina', 'ayahuasca', 'plantas', 'medicine', 'plant']):
            return "medicine"
        elif any(word in message_lower for word in ['precio', 'costo', 'price', 'cost', 'cuánto', 'how much', 'money']):
            return "price"
        elif any(word in message_lower for word in ['seguro', 'seguridad', 'safe', 'safety', 'risk']):
            return "safety"
        else:
            return "general"
    
    def generate_response(self, message):
        """Genera respuesta apropiada"""
        language = self.detect_language(message)
        question_type = self.analyze_message(message)
        
        # Si OpenAI está disponible, usar IA, sino usar plantillas
        if self.client:
            try:
                system_prompt = f"""Eres Maya, facilitadora experta de Sacred Rebirth. Responde en {language} de forma cálida y profesional.

INFORMACIÓN:
- Retiro: 11 enero 2025, Valle de Bravo
- 3 días, medicinas sagradas: ayahuasca, temazcal, cacao, rapé
- NUNCA menciones precios específicos
- Siempre termina dirigiendo al discovery call: {self.business_info['booking_url']}

Usa emojis espirituales y sé empática."""

                response = self.client.chat.completions.create(
                    model='gpt-4o-mini',
                    messages=[
                        {'role': 'system', 'content': system_prompt},
                        {'role': 'user', 'content': message}
                    ],
                    max_tokens=200,
                    temperature=0.7
                )
                return response.choices[0].message.content
            except:
                pass
        
        # Fallback a plantillas
        return self.get_response_template(question_type, language)

# Inicializar bot
maya_bot = FacebookMayaBot()

def send_facebook_message(sender_id, message_text):
    """Envía mensaje a Facebook"""
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        return {"error": "Token not configured"}
    
    try:
        url = "https://graph.facebook.com/v18.0/me/messages"
        data = {
            'recipient': {'id': sender_id},
            'message': {'text': message_text},
            'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
        }
        
        response = requests.post(url, json=data)
        return response.json()
    except Exception as e:
        logger.error(f"Error sending message: {e}")
        return {"error": str(e)}

@app.route('/webhook', methods=['GET'])
def webhook_verification():
    """Verificación del webhook"""
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == WEBHOOK_VERIFY_TOKEN:
        logger.info("✅ Webhook verified successfully")
        return challenge
    else:
        logger.warning("❌ Invalid verification token")
        return "Invalid verification token", 403

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Maneja mensajes de Facebook"""
    try:
        data = request.get_json()
        logger.info(f"📨 Received webhook: {data}")
        
        if 'entry' in data:
            for entry in data['entry']:
                if 'messaging' in entry:
                    for messaging_event in entry['messaging']:
                        if 'message' in messaging_event and 'text' in messaging_event['message']:
                            sender_id = messaging_event['sender']['id']
                            message_text = messaging_event['message']['text']
                            
                            logger.info(f"💬 Message from {sender_id}: {message_text}")
                            
                            # Generar respuesta con Maya
                            response_text = maya_bot.generate_response(message_text)
                            
                            # Enviar respuesta
                            send_result = send_facebook_message(sender_id, response_text)
                            logger.info(f"📤 Response sent: {send_result}")
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        logger.error(f"❌ Webhook error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "Sacred Rebirth Facebook Bot Running",
        "service": "Maya - Bilingual Appointment Setter",
        "webhook_configured": bool(WEBHOOK_VERIFY_TOKEN),
        "facebook_configured": bool(FACEBOOK_PAGE_ACCESS_TOKEN),
        "openai_configured": bool(OPENAI_API_KEY)
    })

if __name__ == '__main__':
    logger.info("🚀 Starting Sacred Rebirth Facebook Bot")
    logger.info(f"📱 Webhook token: {'✅' if WEBHOOK_VERIFY_TOKEN else '❌'}")
    logger.info(f"🔑 Facebook token: {'✅' if FACEBOOK_PAGE_ACCESS_TOKEN else '❌'}")
    logger.info(f"🤖 OpenAI configured: {'✅' if OPENAI_API_KEY else '❌'}")
    
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port)