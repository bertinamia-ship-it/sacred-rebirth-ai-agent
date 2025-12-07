#!/usr/bin/env python3
"""
Sacred Rebirth Marketing Campaign Manager
Gestiona campañas completas de marketing para retiros
"""
import os
import json
from datetime import datetime, timedelta
from openai import OpenAI

class MarketingCampaignManager:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Información del próximo retiro
        self.retreat_info = {
            "date": "11 de enero de 2025",
            "location": "Valle de Bravo, Estado de México",
            "duration": "3 días y 2 noches",
            "theme": "Nuevo Año, Nueva Vida - Transformación Profunda",
            "booking_url": "https://sacred-rebirth.com/appointment.html",
            "early_bird_deadline": "20 de diciembre de 2024"
        }
        
        # Estrategia de audiencia
        self.target_audiences = {
            "spiritual_seekers": {
                "description": "Personas interesadas en crecimiento espiritual",
                "demographics": "25-45 años, clase media-alta, urbanos",
                "interests": ["meditación", "yoga", "desarrollo personal", "espiritualidad"],
                "pain_points": ["ansiedad", "vacío existencial", "falta de propósito"],
                "platforms": ["Instagram", "Facebook", "YouTube", "TikTok"]
            },
            "healing_community": {
                "description": "Personas buscando sanación emocional/traumas",
                "demographics": "30-50 años, profesionistas, ingresos medios-altos",
                "interests": ["terapia alternativa", "sanación holística", "medicina ancestral"],
                "pain_points": ["depresión", "trauma", "adicciones", "relaciones tóxicas"],
                "platforms": ["Facebook", "Instagram", "LinkedIn"]
            },
            "wellness_enthusiasts": {
                "description": "Entusiastas del bienestar y vida saludable",
                "demographics": "25-40 años, activos en redes, disposición económica",
                "interests": ["wellness", "vida saludable", "experiencias únicas"],
                "pain_points": ["estrés", "burnout", "falta de autenticidad"],
                "platforms": ["Instagram", "TikTok", "Pinterest"]
            }
        }
        
    def create_market_research(self):
        """Genera estudio de mercado completo"""
        
        research_prompt = f"""
Crea un estudio de mercado completo para Sacred Rebirth, un negocio de retiros de ayahuasca en Valle de Bravo, México.

RETIRO OBJETIVO: {self.retreat_info['date']} - "{self.retreat_info['theme']}"

INCLUYE:

1. ANÁLISIS DE MERCADO:
- Tamaño del mercado de retiros espirituales en México
- Tendencias de turismo de bienestar 2024-2025
- Competencia directa e indirecta
- Precios promedio del mercado

2. AUDIENCIA TARGET:
- Segmentos principales
- Demografia detallada
- Psychographics y comportamientos
- Plataformas donde se encuentran

3. POSICIONAMIENTO:
- Propuesta de valor única
- Diferenciadores vs competencia
- Mensajes clave por audiencia

4. ESTRATEGIA DE PRECIOS:
- Análisis de sensibilidad al precio
- Estrategia de early bird
- Bundling de servicios

5. CANALES DE MARKETING:
- Canales más efectivos por audiencia
- Presupuesto sugerido por canal
- ROI esperado

6. CALENDARIO DE LANZAMIENTO:
- Timeline hasta enero 11
- Hitos importantes
- Fechas clave de marketing

7. RIESGOS Y OPORTUNIDADES:
- Regulaciones/marco legal
- Estacionalidad
- Eventos externos

Sé específico, incluye números estimados y recomendaciones accionables.
"""

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o',  # Usar modelo premium para análisis complejo
                messages=[{'role': 'user', 'content': research_prompt}],
                max_tokens=3000,
                temperature=0.3
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generando estudio de mercado: {str(e)}"
    
    def create_content_calendar(self, days=30):
        """Genera calendario de contenido diario"""
        
        calendar_prompt = f"""
Crea un calendario de contenido para Sacred Rebirth de {days} días leading hasta el retiro del 11 de enero.

OBJETIVOS:
- Educar sobre ayahuasca de forma segura y profesional
- Construir confianza y autoridad
- Generar discovery calls
- Mostrar transformaciones reales

TIPOS DE CONTENIDO DIARIO:
- Posts educativos (Lunes)
- Testimonios/historias (Martes)  
- Behind the scenes (Miércoles)
- Tips de preparación (Jueves)
- Contenido inspiracional (Viernes)
- Q&A/mitos vs realidad (Sábado)
- Reflexiones dominicales (Domingo)

FORMATO PARA CADA DÍA:
- Fecha
- Tipo de contenido
- Título/Hook
- Descripción del post
- Hashtags sugeridos
- Call to action
- Hora óptima de publicación

INCLUIR SIEMPRE:
- "Book your discovery call now: https://sacred-rebirth.com/appointment.html"
- Emojis espirituales apropiados
- Información del retiro enero 11

Haz el calendario específico, creativo y variado.
"""

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': calendar_prompt}],
                max_tokens=3000,
                temperature=0.7
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generando calendario: {str(e)}"
    
    def create_audience_strategy(self):
        """Crea estrategia específica para conseguir audiencia"""
        
        strategy_prompt = f"""
Crea una estrategia completa para conseguir audiencia para Sacred Rebirth.

AUDIENCIAS TARGET:
{json.dumps(self.target_audiences, indent=2)}

PARA CADA AUDIENCIA INCLUYE:

1. DÓNDE ENCONTRARLOS:
- Grupos específicos de Facebook
- Hashtags de Instagram/TikTok
- Influencers/colaboraciones potenciales
- Eventos/lugares físicos
- Comunidades online

2. ESTRATEGIAS DE CAPTACIÓN:
- Contenido específico que los atraiga
- Colaboraciones estratégicas
- Publicidad pagada targeting
- SEO keywords
- Marketing de referidos

3. MENSAJES CLAVE:
- Pain points específicos
- Beneficios más relevantes
- Tonos de comunicación
- Objeciones comunes y respuestas

4. MÉTRICAS Y KPIs:
- Cómo medir el éxito
- Conversiones esperadas
- Costo por lead estimado

5. PRESUPUESTOS SUGERIDOS:
- Inversión por canal
- ROI esperado
- Timeline de resultados

6. PLAN DE IMPLEMENTACIÓN:
- Pasos específicos
- Responsabilidades
- Calendario de ejecución

Sé muy específico y accionable. Incluye nombres reales de grupos, influencers, hashtags, etc.
"""

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': strategy_prompt}],
                max_tokens=3500,
                temperature=0.4
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generando estrategia de audiencia: {str(e)}"
    
    def create_monthly_video_script(self):
        """Genera guión para video mensual de alta calidad"""
        
        video_prompt = f"""
Crea un guión para video de alta calidad para Sacred Rebirth sobre el retiro de enero 11.

ESPECIFICACIONES:
- Duración: 3-5 minutos
- Formato: Testimonial + información + call to action
- Público: Personas considerando ayahuasca por primera vez
- Objetivo: Generar discovery calls

ESTRUCTURA DEL GUIÓN:

1. HOOK INICIAL (0-15 segundos):
- Frase impactante sobre transformación
- Visual compelling

2. INTRODUCCIÓN (15-30 segundos):
- Quién somos
- Credibilidad/experiencia
- Por qué Valle de Bravo

3. PROBLEMA/DOLOR (30-60 segundos):
- Conectar con audiencia
- Problemas que resuelve ayahuasca
- Sin dramatizar

4. SOLUCIÓN (60-180 segundos):
- Qué es Sacred Rebirth
- Proceso del retiro
- Seguridad y profesionalismo
- Testimonios breves

5. CREDIBILIDAD (180-240 segundos):
- Facilitadores
- Años de experiencia
- Protocolos de seguridad
- Ambiente seguro

6. CALL TO ACTION (240-300 segundos):
- Discovery call gratuito
- Qué incluye la llamada
- URL de agendamiento
- Urgencia suave (enero 11)

INCLUIR:
- Transitions específicas
- B-roll sugerido
- Música/audio suggestions
- Gráficos/texto overlay
- Shots específicos a grabar

TONO: Profesional, cálido, auténtico, no comercial
"""

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o',
                messages=[{'role': 'user', 'content': video_prompt}],
                max_tokens=2500,
                temperature=0.6
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generando guión de video: {str(e)}"
    
    def generate_complete_campaign(self):
        """Genera campaña completa de marketing"""
        campaign = {
            "market_research": self.create_market_research(),
            "content_calendar": self.create_content_calendar(),
            "audience_strategy": self.create_audience_strategy(),
            "video_script": self.create_monthly_video_script(),
            "retreat_info": self.retreat_info,
            "generated_at": datetime.now().isoformat()
        }
        return campaign