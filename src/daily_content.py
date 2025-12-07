#!/usr/bin/env python3
"""
Sacred Rebirth Daily Content Automation
Genera y programa contenido diario automáticamente
"""
import os
import json
import schedule
import time
from datetime import datetime, timedelta
from openai import OpenAI
from src.image_generator import SacredRebirthImageGenerator

class DailyContentAutomation:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.image_generator = SacredRebirthImageGenerator()
        
        # Calendario temático semanal
        self.weekly_themes = {
            "Monday": {
                "theme": "Educación sobre Ayahuasca",
                "style": "informativo",
                "focus": "Desmitificar, educar, compartir conocimiento ancestral"
            },
            "Tuesday": {
                "theme": "Testimonios y Transformaciones",
                "style": "emocional",
                "focus": "Historias reales de sanación y crecimiento"
            },
            "Wednesday": {
                "theme": "Behind the Scenes",
                "style": "auténtico",
                "focus": "Preparativos, facilitadores, espacio sagrado"
            },
            "Thursday": {
                "theme": "Preparación para el Retiro",
                "style": "práctico",
                "focus": "Tips, dieta, preparación mental y física"
            },
            "Friday": {
                "theme": "Inspiración y Reflexiones",
                "style": "espiritual",
                "focus": "Mensajes profundos, citas inspiradoras"
            },
            "Saturday": {
                "theme": "Q&A y Mitos vs Realidad",
                "style": "conversacional",
                "focus": "Responder dudas comunes, eliminar miedos"
            },
            "Sunday": {
                "theme": "Reflexiones Dominicales",
                "style": "contemplativo",
                "focus": "Conexión espiritual, propósito de vida"
            }
        }
        
        # Horarios óptimos de publicación
        self.posting_times = {
            "Monday": "09:00",
            "Tuesday": "12:00", 
            "Wednesday": "15:00",
            "Thursday": "10:00",
            "Friday": "14:00",
            "Saturday": "11:00",
            "Sunday": "16:00"
        }
        
    def generate_daily_content(self, day_of_week=None):
        """Genera contenido específico para el día"""
        
        if not day_of_week:
            day_of_week = datetime.now().strftime("%A")
            
        theme_info = self.weekly_themes.get(day_of_week, self.weekly_themes["Monday"])
        
        content_prompt = f"""
Crea un post para redes sociales de Sacred Rebirth para {day_of_week}.

INFORMACIÓN DEL RETIRO:
- Próximo retiro: 11 de enero de 2025
- Ubicación: Valle de Bravo, Estado de México
- Tema: "Nuevo Año, Nueva Vida - Transformación Profunda"

TEMA DEL DÍA: {theme_info['theme']}
ESTILO: {theme_info['style']}
ENFOQUE: {theme_info['focus']}

REQUISITOS:
- 150-200 palabras
- Incluir emojis espirituales apropiados: 🌿✨🌌💫🙏🌱⭐️
- Tono cálido, profesional, auténtico
- Conectar con el dolor/necesidad de la audiencia
- Despertar curiosidad sin ser comercial
- SIEMPRE terminar con: "💫 Book your discovery call now: https://sacred-rebirth.com/appointment.html"

HASHTAGS: Incluir 5-7 hashtags relevantes

CALL TO ACTION: Debe fluir naturalmente, no forzado

AUDIENCIA: Personas buscando sanación, crecimiento espiritual, transformación personal

Crea contenido auténtico que invite a la reflexión y genere conexión emocional.
"""

        try:
            response = self.client.chat.completions.create(
                model='gpt-4o-mini',
                messages=[{'role': 'user', 'content': content_prompt}],
                max_tokens=500,
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            return {
                "success": True,
                "content": content,
                "theme": theme_info['theme'],
                "day": day_of_week,
                "posting_time": self.posting_times.get(day_of_week, "12:00"),
                "generated_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            return {"success": False, "error": f"Error generating content: {str(e)}"}
    
    def generate_weekly_calendar(self):
        """Genera calendario completo de la semana"""
        weekly_content = {}
        
        for day in self.weekly_themes.keys():
            content_result = self.generate_daily_content(day)
            if content_result["success"]:
                weekly_content[day] = content_result
                
        return weekly_content
    
    def generate_content_with_image(self, day_of_week=None):
        """Genera contenido + imagen para el día"""
        
        # Generar contenido
        content_result = self.generate_daily_content(day_of_week)
        if not content_result["success"]:
            return content_result
            
        # Determinar tema de imagen basado en el día
        image_themes = {
            "Monday": "medicine",      # Educación sobre medicina
            "Tuesday": "transformation", # Testimonios
            "Wednesday": "retreat",     # Behind scenes
            "Thursday": "preparation",  # Tips preparación  
            "Friday": "spiritual",     # Inspiración
            "Saturday": "general",     # Q&A
            "Sunday": "meditation"     # Reflexiones
        }
        
        current_day = day_of_week or datetime.now().strftime("%A")
        image_theme = image_themes.get(current_day, "general")
        
        # Generar imagen
        image_result = self.image_generator.generate_retreat_image(content_theme=image_theme)
        
        return {
            "success": True,
            "content": content_result["content"],
            "theme": content_result["theme"],
            "day": current_day,
            "posting_time": content_result["posting_time"],
            "image": image_result,
            "generated_at": datetime.now().isoformat()
        }
    
    def setup_daily_schedule(self):
        """Configura programación diaria automática"""
        
        # Programar para cada día de la semana
        for day, time_str in self.posting_times.items():
            schedule.every().monday.at(time_str).do(self.daily_post_job, "Monday")
            schedule.every().tuesday.at(time_str).do(self.daily_post_job, "Tuesday") 
            schedule.every().wednesday.at(time_str).do(self.daily_post_job, "Wednesday")
            schedule.every().thursday.at(time_str).do(self.daily_post_job, "Thursday")
            schedule.every().friday.at(time_str).do(self.daily_post_job, "Friday")
            schedule.every().saturday.at(time_str).do(self.daily_post_job, "Saturday")
            schedule.every().sunday.at(time_str).do(self.daily_post_job, "Sunday")
    
    def daily_post_job(self, day):
        """Job que se ejecuta diariamente para crear y publicar contenido"""
        try:
            # Generar contenido + imagen
            result = self.generate_content_with_image(day)
            
            if result["success"]:
                # Aquí se integraría con la función de Facebook posting
                # post_to_facebook(result["content"], result["image"]["local_path"])
                
                # Log para debug
                print(f"✅ Contenido generado para {day}: {result['theme']}")
                
                # Guardar en archivo de historial
                with open("/tmp/daily_content_log.json", "a") as f:
                    json.dump(result, f)
                    f.write("\n")
                    
            return result
            
        except Exception as e:
            print(f"❌ Error en daily job para {day}: {str(e)}")
            return {"success": False, "error": str(e)}
    
    def run_scheduler(self):
        """Ejecuta el scheduler de contenido diario"""
        self.setup_daily_schedule()
        
        print("🤖 Scheduler de contenido diario iniciado")
        print("📅 Horarios de publicación:")
        for day, time_str in self.posting_times.items():
            theme = self.weekly_themes[day]['theme']
            print(f"   {day}: {time_str} - {theme}")
        
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute