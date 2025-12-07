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
        
        # Preguntas que pueden hacer los usuarios (español e inglés)
        self.common_questions = {
            "location": ["ubicación", "donde", "dónde", "lugar", "valle de bravo", "location", "where", "place"],
            "what_is": ["consiste", "qué es", "que es", "sobre", "ayahuasca", "retiro", "what is", "about", "retreat", "consist"],
            "medicines": ["medicina", "plantas", "sustancia", "toman", "usan", "medicine", "plant", "substance", "take", "use"],
            "duration": ["tiempo", "duración", "días", "cuánto", "duration", "time", "days", "how long"],
            "included": ["incluye", "precio incluye", "qué incluye", "comida", "include", "what includes", "food", "meals"],
            "price": ["precio", "costo", "cuánto cuesta", "cuanto cuesta", "tarifa", "price", "cost", "how much", "money", "fee"],
            "safety": ["seguro", "seguridad", "riesgos", "peligro", "safe", "safety", "risk", "danger"],
            "preparation": ["preparar", "preparación", "antes", "dieta", "prepare", "preparation", "before", "diet"],
            "experience": ["experiencia", "qué esperar", "primera vez", "experience", "what to expect", "first time"],
            "greeting": ["hola", "hello", "hi", "buenas", "good morning", "good afternoon", "hey"]
        }
        
        # Sistema prompt bilingüe
        self.system_prompt = """Eres Maya, la asistente personal bilingüe de Sacred Rebirth. Eres una facilitadora experta en ceremonias de ayahuasca con años de experiencia guiando personas en su transformación espiritual.

INFORMACIÓN SOBRE SACRED REBIRTH:
- Ubicación: Valle de Bravo, Estado de México
- Próximo retiro: 11 de enero de 2025
- Duración: 3 días y 2 noches
- Medicinas: Ayahuasca sagrada, temazcal, cacao ceremonial, rapé
- Incluye: Alojamiento, todas las comidas, ceremonias, facilitadores experimentados, proceso de integración

TU PERSONALIDAD:
- Cálida, comprensiva y sabia
- Hablas perfectamente español e inglés
- Respondes en el idioma que te escriban
- Usas emojis espirituales: 🌿✨🌌💫🙏🌱⭐️
- Eres empática con personas que buscan sanación

REGLAS IMPORTANTES:
1. NUNCA menciones precios específicos en NINGÚN idioma
2. Si preguntan por precio, SIEMPRE di en español: "Te invito a agendar tu discovery call gratuito: https://sacred-rebirth.com/appointment.html"
3. Si preguntan por precio en inglés: "I invite you to book your free discovery call: https://sacred-rebirth.com/appointment.html"
4. Siempre termina con el link de discovery call en ambos idiomas
5. Si preguntan sobre medicina, explica desde la perspectiva espiritual
6. Enfócate en la transformación, no solo en la experiencia

RESPUESTAS BILINGÜES:
- Si escriben en inglés → responde en inglés
- Si escriben en español → responde en español
- Si escriben mezclado → usa el idioma predominante
- Saluda cálidamente en cualquier idioma

EJEMPLOS DE RESPUESTAS:

ESPAÑOL:
- Ubicación: "Nuestro espacio sagrado está en Valle de Bravo, Estado de México 🌿 Un lugar de montañas y naturaleza perfecto para la introspección..."
- Qué es: "Sacred Rebirth es un retiro de transformación donde trabajamos con ayahuasca sagrada para sanación profunda del alma ✨..."
- Precio: "Te invito a agendar tu discovery call gratuito para hablar de los detalles: https://sacred-rebirth.com/appointment.html"

INGLÉS:
- Location: "Our sacred space is located in Valle de Bravo, Estado de México 🌿 A place of mountains and nature perfect for introspection..."
- What is: "Sacred Rebirth is a transformation retreat where we work with sacred ayahuasca for deep soul healing ✨..."
- Price: "I invite you to book your free discovery call to discuss details: https://sacred-rebirth.com/appointment.html"

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
    
    def detect_language(self, message):
        """Detecta el idioma del mensaje"""
        english_words = ['hello', 'hi', 'how', 'what', 'where', 'when', 'why', 'the', 'and', 'or', 'retreat', 'ayahuasca', 'price', 'cost']
        spanish_words = ['hola', 'como', 'qué', 'que', 'donde', 'cuando', 'por', 'el', 'la', 'y', 'o', 'retiro', 'precio', 'costo']
        
        message_lower = message.lower()
        
        english_count = sum(1 for word in english_words if word in message_lower)
        spanish_count = sum(1 for word in spanish_words if word in message_lower)
        
        if english_count > spanish_count:
            return "english"
        elif spanish_count > english_count:
            return "spanish"
        else:
            # Si no está claro, usar español como default
            return "spanish"
    
    def generate_response(self, user_message, question_type="general"):
        """Genera una respuesta personalizada como Maya"""
        
        try:
            # Detectar idioma
            language = self.detect_language(user_message)
            
            # Prompt específico según el tipo de pregunta y idioma
            context_prompts = {
                "price": {
                    "spanish": "El usuario pregunta sobre precios en español. NUNCA des precios específicos, siempre dirígelos al discovery call en español.",
                    "english": "User asks about pricing in English. NEVER give specific prices, always direct them to the discovery call in English."
                },
                "location": {
                    "spanish": "El usuario pregunta sobre la ubicación en español. Describe Valle de Bravo de forma hermosa y espiritual.",
                    "english": "User asks about location in English. Describe Valle de Bravo in a beautiful and spiritual way."
                },
                "what_is": {
                    "spanish": "El usuario quiere saber qué es Sacred Rebirth o sobre ayahuasca en español. Explica la transformación espiritual.",
                    "english": "User wants to know what Sacred Rebirth is or about ayahuasca in English. Explain spiritual transformation."
                },
                "medicines": {
                    "spanish": "El usuario pregunta sobre las medicinas en español. Explica desde perspectiva sagrada y de sanación.",
                    "english": "User asks about medicines in English. Explain from sacred and healing perspective."
                },
                "safety": {
                    "spanish": "El usuario tiene preocupaciones de seguridad en español. Tranquilízalo y menciona la experiencia de facilitadores.",
                    "english": "User has safety concerns in English. Reassure them and mention facilitators' experience."
                },
                "preparation": {
                    "spanish": "El usuario pregunta sobre preparación en español. Habla de la importancia espiritual de prepararse.",
                    "english": "User asks about preparation in English. Talk about spiritual importance of preparing."
                },
                "greeting": {
                    "spanish": "El usuario saluda en español. Responde cálidamente y ofrece ayuda.",
                    "english": "User greets in English. Respond warmly and offer help."
                },
                "general": {
                    "spanish": "Responde de forma general en español, siempre dirigiendo hacia más información y el discovery call.",
                    "english": "Respond generally in English, always directing towards more information and the discovery call."
                }
            }
            
            context = context_prompts.get(question_type, context_prompts["general"])[language]
            
            response = self.client.chat.completions.create(
                model='gpt-4o-mini',  # Usar modelo eficiente para appointment setter
                messages=[
                    {'role': 'system', 'content': f"{self.system_prompt}\n\nCONTEXTO ESPECÍFICO: {context}\nIDIOMA A USAR: {language.upper()}"},
                    {'role': 'user', 'content': user_message}
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            # Respuesta de fallback bilingüe
            if any(word in user_message.lower() for word in ['hello', 'hi', 'english', 'how', 'what']):
                return f"🌿 Thank you for contacting Sacred Rebirth. I invite you to book your free discovery call to talk personally: https://sacred-rebirth.com/appointment.html 💫"
            else:
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