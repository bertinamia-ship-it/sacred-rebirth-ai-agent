#!/usr/bin/env python3
"""
Bot de WhatsApp para Sacred Rebirth AI Agent
Usando Twilio API para WhatsApp Business
"""
import os
from dotenv import load_dotenv
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
from src.crew import MarketingCrew
from chat import ChatAgent

load_dotenv()

# Configuración
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_WHATSAPP_NUMBER = os.getenv('TWILIO_WHATSAPP_NUMBER', 'whatsapp:+14155238886')
AUTHORIZED_NUMBERS = os.getenv('WHATSAPP_AUTHORIZED_NUMBERS', '').split(',')

# Inicializar Flask
app = Flask(__name__)

# Inicializar agente
print("🤖 Inicializando Marketing Crew para WhatsApp...")
crew = MarketingCrew()
chat_agent = ChatAgent(crew)
print("✅ Bot de WhatsApp listo!")

# Cliente de Twilio (si está configurado)
twilio_client = None
if TWILIO_ACCOUNT_SID and TWILIO_AUTH_TOKEN:
    twilio_client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)


@app.route('/webhook', methods=['POST'])
def whatsapp_webhook():
    """Webhook que recibe mensajes de WhatsApp"""
    
    # Obtener datos del mensaje
    incoming_msg = request.values.get('Body', '').strip()
    from_number = request.values.get('From', '')
    
    print(f"\n💬 Mensaje WhatsApp de {from_number}: {incoming_msg}")
    
    # Verificar autorización
    phone_number = from_number.replace('whatsapp:', '')
    if AUTHORIZED_NUMBERS and phone_number not in AUTHORIZED_NUMBERS:
        resp = MessagingResponse()
        msg = resp.message()
        msg.body(
            f"⛔ Lo siento, no estás autorizado para usar este bot.\n\n"
            f"Tu número: {phone_number}\n\n"
            "Contacta al administrador para obtener acceso."
        )
        return str(resp)
    
    # Crear respuesta
    resp = MessagingResponse()
    msg = resp.message()
    
    try:
        # Comandos especiales
        if incoming_msg.lower() in ['hola', 'start', 'inicio', 'ayuda']:
            response_text = """
🙏 ¡Hola! Soy el asistente de marketing de Sacred Rebirth.

*Puedo ayudarte con:*
• Crear posts para Instagram/Facebook
• Generar campañas de email  
• Gestionar calendario de contenido
• Analizar leads
• Programar publicaciones

*Ejemplos:*
• "Crea un post sobre ayahuasca"
• "Muestra mi calendario"
• "Envía email a nuevos leads"

Solo escríbeme naturalmente 💬
"""
        
        elif incoming_msg.lower() in ['estado', 'status']:
            services = []
            if os.getenv('META_ACCESS_TOKEN'):
                services.append("✅ Instagram/Facebook")
            else:
                services.append("⚠️ Instagram/Facebook")
            
            if os.getenv('SENDGRID_API_KEY'):
                services.append("✅ Email")
            else:
                services.append("⚠️ Email")
            
            response_text = f"""
✅ *Estado del Sistema*

• Bot: Activo
• CrewAI: Operativo  
• Agentes: 6/6 funcionando

*Servicios:*
{chr(10).join(services)}
"""
        
        else:
            # Procesar con el agente de chat
            response_text = chat_agent.process_message(incoming_msg)
        
        # Dividir mensajes largos (WhatsApp recomienda < 1600 caracteres)
        if len(response_text) > 1500:
            chunks = [response_text[i:i+1500] for i in range(0, len(response_text), 1500)]
            for chunk in chunks:
                msg.body(chunk)
                # Para mensajes múltiples, crear nuevos mensajes
                if chunk != chunks[-1]:
                    msg = resp.message()
        else:
            msg.body(response_text)
        
    except Exception as e:
        error_text = f"❌ Error procesando tu solicitud: {str(e)}\n\nIntenta de nuevo."
        msg.body(error_text)
        print(f"Error: {e}")
    
    return str(resp)


@app.route('/send', methods=['POST'])
def send_whatsapp_message():
    """Endpoint para enviar mensajes proactivos (opcional)"""
    
    if not twilio_client:
        return {'error': 'Twilio no configurado'}, 400
    
    data = request.json
    to_number = data.get('to')
    message = data.get('message')
    
    if not to_number or not message:
        return {'error': 'Faltan parámetros: to, message'}, 400
    
    try:
        # Enviar mensaje
        twilio_message = twilio_client.messages.create(
            body=message,
            from_=TWILIO_WHATSAPP_NUMBER,
            to=f'whatsapp:{to_number}'
        )
        
        return {
            'success': True,
            'message_sid': twilio_message.sid
        }
    
    except Exception as e:
        return {'error': str(e)}, 500


@app.route('/health', methods=['GET'])
def health_check():
    """Endpoint de health check"""
    return {
        'status': 'healthy',
        'service': 'Sacred Rebirth WhatsApp Bot',
        'twilio_configured': bool(twilio_client)
    }


def main():
    """Inicia el servidor Flask para WhatsApp"""
    
    if not TWILIO_ACCOUNT_SID or not TWILIO_AUTH_TOKEN:
        print("⚠️ Advertencia: Twilio no configurado completamente")
        print("\nPara configurar WhatsApp:")
        print("1. Crea cuenta en https://www.twilio.com/")
        print("2. Configura WhatsApp Business API (Sandbox para pruebas)")
        print("3. Agrega credenciales a .env:")
        print("   TWILIO_ACCOUNT_SID=tu_account_sid")
        print("   TWILIO_AUTH_TOKEN=tu_auth_token")
        print("   TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886")
        print("\n4. Configura webhook en Twilio apuntando a:")
        print("   https://tu-dominio.com/webhook")
        print("\nEjecutando de todas formas...")
    
    print("\n🚀 Iniciando servidor WhatsApp...")
    print("📱 Webhook disponible en: /webhook")
    print("💚 Health check en: /health")
    
    if AUTHORIZED_NUMBERS:
        print(f"🔐 Números autorizados: {', '.join(AUTHORIZED_NUMBERS)}")
    else:
        print("⚠️ Advertencia: Todos los números pueden usar el bot")
    
    # Correr servidor
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)


if __name__ == '__main__':
    main()
