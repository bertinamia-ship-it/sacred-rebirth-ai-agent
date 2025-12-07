#!/usr/bin/env python3
"""
Sacred Rebirth Appointment Setter AI Agent
Maneja conversaciones para agendar discovery calls
"""
import os
from openai import OpenAI

class AppointmentSetterAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Información básica sobre Sacred Rebirth
        self.business_info = {
            "location": "Valle de Bravo, Estado de México",
            "retreat_date": "11 de enero de 2025",
            "medicines": "Ayahuasca sagrada, temazcal, cacao ceremonial, rapé",
            "duration": "3 días y 2 noches",
            "what_included": "Alojamiento, todas las comidas, ceremonias, facilitadores experimentados, integración",
            "booking_url": "https://sacred-rebirth.com/appointment.html",
            "contact_info": "WhatsApp: +52 55 1234 5678"
        }
        
        # Preguntas que pueden hacer los usuarios
        self.common_questions = {
            "location": ["ubicación", "donde", "dónde", "lugar", "valle de bravo"],
            "what_is": ["consiste", "qué es", "que es", "sobre", "ayahuasca", "retiro"],
            "medicines": ["medicina", "plantas", "sustancia", "toman", "usan"],
            "duration": ["tiempo", "duración", "días", "cuánto"],
            "included": ["incluye", "precio incluye", "qué incluye", "comida"],
            "price": ["precio", "costo", "cuánto cuesta", "cuanto cuesta", "tarifa"],
            "safety": ["seguro", "seguridad", "riesgos", "peligro"],
            "preparation": ["preparar", "preparación", "antes", "dieta"],
            "experience": ["experiencia", "qué esperar", "primera vez"]
        }
        
        self.system_prompt = """Eres Maya, el asistente personal de Sacred Rebirth. Eres una facilitadora experta en ceremonias de ayahuasca con años de experiencia guiando personas en su transformación espiritual.

INFORMACIÓN SOBRE SACRED REBIRTH:
- Ubicación: Valle de Bravo, Estado de México
- Próximo retiro: 11 de enero de 2025
- Duración: 3 días y 2 noches
- Medicinas: Ayahuasca sagrada, temazcal, cacao ceremonial, rapé
- Incluye: Alojamiento, todas las comidas, ceremonias, facilitadores experimentados, proceso de integración

TU PERSONALIDAD:
- Cálida, comprensiva y sabia
- Hablas con conocimiento espiritual pero de forma accesible
- Usas emojis espirituales: 🌿✨🌌💫🙏🌱⭐️
- Siempre respondes en español
- Eres empática con personas que buscan sanación

REGLAS IMPORTANTES:
1. NUNCA menciones precios específicos
2. Si preguntan por precio, SIEMPRE di: "Te invito a agendar tu discovery call gratuito para hablar de los detalles: https://sacred-rebirth.com/appointment.html"
3. Siempre termina tus respuestas con: "💫 Agenda tu discovery call gratuito: https://sacred-rebirth.com/appointment.html"
4. Si preguntan sobre medicina, explica desde la perspectiva espiritual
5. Enfócate en la transformación, no solo en la experiencia

EJEMPLO DE RESPUESTAS:
- Ubicación: "Nuestro espacio sagrado está en Valle de Bravo, Estado de México 🌿 Un lugar de montañas y naturaleza perfecto para la introspección..."
- Qué es: "Sacred Rebirth es un retiro de transformación donde trabajamos con ayahuasca sagrada para sanación profunda del alma ✨..."
- Medicinas: "Trabajamos con ayahuasca, la medicina maestra que nos conecta con nuestra sabiduría interior 🌌 También incluimos temazcal, cacao ceremonial..."

Responde siempre con amor, sabiduría y orientación hacia el discovery call."""

    def analyze_message(self, user_message):
        """Analiza el mensaje del usuario y determina la intención"""
        message_lower = user_message.lower()
        
        # Detectar tipo de pregunta
        question_type = "general"
        for qtype, keywords in self.common_questions.items():
            if any(keyword in message_lower for keyword in keywords):
                question_type = qtype
                break
        
        return question_type
    
    def generate_response(self, user_message, question_type="general"):
        """Genera una respuesta personalizada como Maya"""
        
        try:
            # Prompt específico según el tipo de pregunta
            context_prompts = {
                "price": "El usuario pregunta sobre precios. NUNCA des precios específicos, siempre dirígelos al discovery call.",
                "location": "El usuario pregunta sobre la ubicación. Describe Valle de Bravo de forma hermosa y espiritual.",
                "what_is": "El usuario quiere saber qué es Sacred Rebirth o sobre ayahuasca. Explica la transformación espiritual.",
                "medicines": "El usuario pregunta sobre las medicinas. Explica desde perspectiva sagrada y de sanación.",
                "safety": "El usuario tiene preocupaciones de seguridad. Tranquilízalo y menciona la experiencia de facilitadores.",
                "preparation": "El usuario pregunta sobre preparación. Habla de la importancia espiritual de prepararse.",
                "general": "Responde de forma general, siempre dirigiendo hacia más información y el discovery call."
            }
            
            context = context_prompts.get(question_type, context_prompts["general"])
            
            response = self.client.chat.completions.create(
                model='gpt-4o-mini',  # Usar modelo eficiente para appointment setter
                messages=[
                    {'role': 'system', 'content': f"{self.system_prompt}\n\nCONTEXTO ESPECÍFICO: {context}"},
                    {'role': 'user', 'content': user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            return f"🌿 Gracias por contactarnos. Te invito a agendar tu discovery call gratuito para conversar personalmente: https://sacred-rebirth.com/appointment.html 💫"

    def is_appointment_related(self, message):
        """Detecta si el mensaje requiere appointment setting"""
        appointment_keywords = [
            "agendar", "cita", "discovery call", "información", "precio", "costo",
            "reservar", "apartar", "disponibilidad", "fecha", "horario", "cuándo",
            "más información", "detalles", "interesado", "quiero ir", "inscribir"
        ]
        
        message_lower = message.lower()
        return any(keyword in message_lower for keyword in appointment_keywords)