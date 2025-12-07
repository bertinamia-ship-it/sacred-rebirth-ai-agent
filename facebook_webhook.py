#!/usr/bin/env python3
"""
Facebook Webhook Handler for Sacred Rebirth
Maneja mensajes entrantes de Facebook y responde automáticamente
"""
import os
import json
import requests
from flask import Flask, request, jsonify
from src.appointment_setter import AppointmentSetterAgent

app = Flask(__name__)

# Configuración
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')
WEBHOOK_VERIFY_TOKEN = os.getenv('FACEBOOK_WEBHOOK_VERIFY_TOKEN', 'sacred_rebirth_2025')

# Inicializar appointment setter
appointment_agent = AppointmentSetterAgent()

def send_facebook_message(sender_id, message_text):
    """Envía mensaje directo a usuario de Facebook"""
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        return {"error": "Token not configured"}
    
    try:
        url = f"https://graph.facebook.com/v18.0/me/messages"
        
        data = {
            'recipient': {'id': sender_id},
            'message': {'text': message_text},
            'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
        }
        
        response = requests.post(url, json=data)
        return response.json()
        
    except Exception as e:
        return {"error": f"Failed to send message: {str(e)}"}

@app.route('/webhook', methods=['GET'])
def webhook_verification():
    """Verificación del webhook de Facebook"""
    
    verify_token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    if verify_token == WEBHOOK_VERIFY_TOKEN:
        return challenge
    else:
        return "Invalid verification token", 403

@app.route('/webhook', methods=['POST'])
def webhook_handler():
    """Maneja mensajes entrantes de Facebook"""
    
    try:
        data = request.get_json()
        
        # Log para debugging
        print(f"📨 Facebook webhook data: {json.dumps(data, indent=2)}")
        
        if 'entry' in data:
            for entry in data['entry']:
                if 'messaging' in entry:
                    for messaging_event in entry['messaging']:
                        
                        # Verificar si es un mensaje de texto
                        if 'message' in messaging_event and 'text' in messaging_event['message']:
                            sender_id = messaging_event['sender']['id']
                            message_text = messaging_event['message']['text']
                            
                            print(f"💬 Mensaje de {sender_id}: {message_text}")
                            
                            # Generar respuesta usando appointment setter bilingüe
                            question_type = appointment_agent.analyze_message(message_text)
                            response_text = appointment_agent.generate_response(message_text, question_type)
                            
                            # Enviar respuesta
                            send_result = send_facebook_message(sender_id, response_text)
                            print(f"📤 Respuesta enviada: {send_result}")
                            
                            # Log para seguimiento
                            import datetime
                            log_entry = {
                                "timestamp": datetime.datetime.now().isoformat(),
                                "sender_id": sender_id,
                                "message": message_text,
                                "question_type": question_type,
                                "response": response_text[:100] + "...",
                                "language": appointment_agent.detect_language(message_text)
                            }
                            print(f"📊 Log: {log_entry}")
                        
                        # Manejar postback buttons (si se implementan en el futuro)
                        elif 'postback' in messaging_event:
                            sender_id = messaging_event['sender']['id']
                            payload = messaging_event['postback']['payload']
                            
                            # Respuesta basada en payload
                            if payload == 'DISCOVERY_CALL':
                                response_text = ("🌿 ¡Perfecto! Te invito a agendar tu discovery call gratuito para que podamos conocerte mejor y responder todas tus preguntas.\n\n"
                                               "💫 Agenda aquí: https://sacred-rebirth.com/appointment.html\n\n"
                                               "Hablaremos sobre tu proceso, el retiro del 11 de enero, y cómo Sacred Rebirth puede ayudarte en tu transformación. ✨")
                            else:
                                response_text = ("🙏 Gracias por contactarnos. Te invito a agendar tu discovery call gratuito para conversar personalmente.\n\n"
                                               "💫 https://sacred-rebirth.com/appointment.html")
                            
                            send_facebook_message(sender_id, response_text)
        
        return jsonify({"status": "success"}), 200
        
    except Exception as e:
        print(f"❌ Error en webhook: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/test', methods=['GET'])
def test_endpoint():
    """Endpoint de prueba"""
    return jsonify({
        "status": "Facebook webhook handler running",
        "service": "Sacred Rebirth Appointment Setter",
        "webhook_token_configured": bool(WEBHOOK_VERIFY_TOKEN),
        "facebook_token_configured": bool(FACEBOOK_PAGE_ACCESS_TOKEN)
    })

if __name__ == '__main__':
    print("🚀 Starting Facebook Webhook Handler for Sacred Rebirth")
    print(f"📱 Webhook verify token: {'✅ Configured' if WEBHOOK_VERIFY_TOKEN else '❌ Missing'}")
    print(f"🔑 Facebook token: {'✅ Configured' if FACEBOOK_PAGE_ACCESS_TOKEN else '❌ Missing'}")
    
    # Ejecutar en Puerto 5000 por defecto
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)