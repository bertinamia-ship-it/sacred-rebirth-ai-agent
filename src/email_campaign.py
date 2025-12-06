"""
Sistema de envío de emails promocionales
"""
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail, Email, To, Content
from config.settings import SENDGRID_API_KEY, EMAIL_FROM, EMAIL_FROM_NAME, BUSINESS_INFO
import json
import os
from datetime import datetime

class EmailCampaignManager:
    def __init__(self):
        self.api_key = SENDGRID_API_KEY
        self.from_email = EMAIL_FROM
        self.from_name = EMAIL_FROM_NAME
        
    def send_campaign_email(self, to_email, subject, html_content, plain_text_content=None):
        """
        Envía un email de campaña individual
        
        Args:
            to_email: Email del destinatario
            subject: Asunto del email
            html_content: Contenido HTML del email
            plain_text_content: Contenido en texto plano (opcional)
        """
        if not self.api_key:
            print("❌ Error: Configura SENDGRID_API_KEY en .env")
            return None
        
        try:
            message = Mail(
                from_email=Email(self.from_email, self.from_name),
                to_emails=To(to_email),
                subject=subject,
                html_content=html_content,
                plain_text_content=plain_text_content or self._html_to_text(html_content)
            )
            
            sg = SendGridAPIClient(self.api_key)
            response = sg.send(message)
            
            print(f"✅ Email enviado a {to_email} - Status: {response.status_code}")
            
            return {
                'to': to_email,
                'subject': subject,
                'status_code': response.status_code,
                'sent_at': datetime.now().isoformat(),
                'status': 'sent'
            }
            
        except Exception as e:
            print(f"❌ Error enviando email a {to_email}: {e}")
            return None
    
    def send_bulk_campaign(self, leads_list, subject, html_template):
        """
        Envía emails en masa a una lista de leads
        
        Args:
            leads_list: Lista de diccionarios con info de leads [{email, name}, ...]
            subject: Asunto del email
            html_template: Template HTML con placeholders {name}, {email}, etc.
        """
        results = []
        
        for lead in leads_list:
            # Personalizar contenido
            html_content = html_template.format(
                name=lead.get('name', 'Amigo'),
                email=lead.get('email'),
                **BUSINESS_INFO
            )
            
            result = self.send_campaign_email(
                to_email=lead.get('email'),
                subject=subject,
                html_content=html_content
            )
            
            if result:
                results.append(result)
        
        print(f"\n📊 Campaña completada: {len(results)}/{len(leads_list)} emails enviados")
        return results
    
    def _html_to_text(self, html):
        """Convierte HTML básico a texto plano"""
        # Remover tags HTML básicos
        import re
        text = re.sub('<[^<]+?>', '', html)
        return text
    
    def create_email_template(self, body_content):
        """
        Crea un template HTML profesional para emails
        
        Args:
            body_content: Contenido principal del email
        """
        template = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        body {{
            font-family: 'Arial', sans-serif;
            line-height: 1.6;
            color: #333;
            max-width: 600px;
            margin: 0 auto;
            padding: 20px;
            background-color: #f4f4f4;
        }}
        .email-container {{
            background-color: #ffffff;
            border-radius: 10px;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        .header {{
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 3px solid #2d5016;
            padding-bottom: 20px;
        }}
        .header h1 {{
            color: #2d5016;
            margin: 0;
            font-size: 28px;
        }}
        .content {{
            margin-bottom: 30px;
        }}
        .cta-button {{
            display: inline-block;
            background-color: #2d5016;
            color: #ffffff !important;
            padding: 15px 30px;
            text-decoration: none;
            border-radius: 5px;
            font-weight: bold;
            margin: 20px 0;
        }}
        .footer {{
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid #ddd;
            font-size: 12px;
            color: #666;
        }}
        .social-links {{
            margin: 20px 0;
        }}
        .social-links a {{
            color: #2d5016;
            text-decoration: none;
            margin: 0 10px;
        }}
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>🌿 {BUSINESS_INFO['name']}</h1>
            <p>Retiros de Transformación Espiritual</p>
        </div>
        
        <div class="content">
            {body_content}
        </div>
        
        <div style="text-align: center;">
            <a href="{BUSINESS_INFO['website']}/appointment" class="cta-button">
                Agenda tu Discovery Call Gratuita
            </a>
        </div>
        
        <div class="footer">
            <div class="social-links">
                <a href="https://instagram.com/{BUSINESS_INFO['instagram'].replace('@', '')}">Instagram</a> |
                <a href="https://facebook.com/{BUSINESS_INFO['facebook']}">Facebook</a> |
                <a href="{BUSINESS_INFO['website']}">Website</a>
            </div>
            <p>
                📍 {BUSINESS_INFO['location']}<br>
                📞 {BUSINESS_INFO['phone']}<br>
                📧 {BUSINESS_INFO['email']}
            </p>
            <p style="font-size: 10px; color: #999;">
                Estás recibiendo este email porque te interesaron nuestros retiros espirituales.<br>
                Si no deseas recibir más emails, <a href="#">haz click aquí</a>.
            </p>
        </div>
    </div>
</body>
</html>
"""
        return template
    
    def load_leads_from_file(self, filepath='data/leads.json'):
        """Carga la lista de leads desde un archivo JSON"""
        if os.path.exists(filepath):
            with open(filepath, 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            print(f"⚠️ Archivo de leads no encontrado: {filepath}")
            return []


# Ejemplo de uso
if __name__ == "__main__":
    manager = EmailCampaignManager()
    
    # Contenido del email
    body_content = """
    <h2>¿Listo para tu Transformación Espiritual? 🌿</h2>
    
    <p>Hola {{name}},</p>
    
    <p>Te invitamos a descubrir el poder sanador de la medicina ancestral en nuestros retiros de 
    Ayahuasca en Valle de Bravo, México.</p>
    
    <p><strong>Nuestro próximo retiro es el 11 de Enero, 2026</strong></p>
    
    <p>En este retiro vivirás:</p>
    <ul>
        <li>✨ Ceremonia de Ayahuasca con facilitadores experimentados</li>
        <li>🌱 Sesiones de Kambo y Rapé</li>
        <li>🧘 Prácticas de Qigong</li>
        <li>💚 Acompañamiento profesional completo</li>
    </ul>
    
    <p>Comienza tu viaje con una Discovery Call gratuita de 30 minutos donde:</p>
    <ul>
        <li>Conocerás más sobre el proceso</li>
        <li>Resolveremos tus dudas</li>
        <li>Evaluaremos si es el momento adecuado para ti</li>
    </ul>
    
    <p>Con amor y luz,<br>
    <strong>Sacred Rebirth Team</strong></p>
"""
    
    # Crear template completo
    html_email = manager.create_email_template(body_content)
    
    # Ejemplo de leads
    example_leads = [
        {'email': 'ejemplo@email.com', 'name': 'María'},
        # Agregar más leads aquí
    ]
    
    # Para enviar la campaña, descomenta:
    # manager.send_bulk_campaign(
    #     leads_list=example_leads,
    #     subject="🌿 Tu Transformación Espiritual te Espera - Retiro Ayahuasca",
    #     html_template=html_email
    # )
    
    print("💡 Para usar este módulo, configura SENDGRID_API_KEY en .env")
    print("📋 Agrega tus leads en data/leads.json")
