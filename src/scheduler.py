"""
Automatización y programación de tareas para el agente IA
"""
import schedule
import time
from datetime import datetime
import pytz
from config.settings import TIMEZONE, POST_TIMES, POSTS_PER_DAY
from src.content_generator import ContentGenerator
from src.social_media import SocialMediaManager
from src.email_campaign import EmailCampaignManager
import json
import os

class MarketingScheduler:
    def __init__(self):
        self.content_gen = ContentGenerator()
        self.social_media = SocialMediaManager()
        self.email_manager = EmailCampaignManager()
        self.timezone = pytz.timezone(TIMEZONE)
        
    def generate_and_post_instagram(self):
        """Genera y publica contenido en Instagram"""
        print(f"\n📸 [{datetime.now()}] Generando post para Instagram...")
        
        # Generar contenido
        post = self.content_gen.generate_instagram_post()
        
        if post:
            # Guardar contenido
            self.content_gen.save_content(post)
            
            # Publicar (comentado por defecto para testing)
            # result = self.social_media.post_to_instagram(post['content'])
            # if result:
            #     post['status'] = 'published'
            #     post['post_id'] = result['post_id']
            
            print(f"✅ Post de Instagram generado: {post['topic']}")
            return post
        
        return None
    
    def generate_and_post_facebook(self):
        """Genera y publica contenido en Facebook"""
        print(f"\n📘 [{datetime.now()}] Generando post para Facebook...")
        
        # Generar contenido
        post = self.content_gen.generate_facebook_post()
        
        if post:
            # Guardar contenido
            self.content_gen.save_content(post)
            
            # Publicar (comentado por defecto para testing)
            # result = self.social_media.post_to_facebook(
            #     message=post['content'],
            #     link='https://sacred-rebirth.com'
            # )
            # if result:
            #     post['status'] = 'published'
            #     post['post_id'] = result['post_id']
            
            print(f"✅ Post de Facebook generado: {post['topic']}")
            return post
        
        return None
    
    def send_weekly_newsletter(self):
        """Envía newsletter semanal a la lista de leads"""
        print(f"\n📧 [{datetime.now()}] Preparando newsletter semanal...")
        
        # Generar contenido del email
        email = self.content_gen.generate_email_campaign()
        
        if email:
            # Guardar contenido
            self.content_gen.save_content(email)
            
            # Cargar lista de leads
            leads = self.email_manager.load_leads_from_file()
            
            if leads:
                # Crear template HTML
                html_content = self.email_manager.create_email_template(email['body'])
                
                # Enviar campaña (comentado por defecto para testing)
                # results = self.email_manager.send_bulk_campaign(
                #     leads_list=leads,
                #     subject=email['subject'],
                #     html_template=html_content
                # )
                
                print(f"✅ Newsletter generada para {len(leads)} leads")
            else:
                print("⚠️ No hay leads en la base de datos")
            
            return email
        
        return None
    
    def daily_report(self):
        """Genera reporte diario de actividades"""
        print(f"\n📊 [{datetime.now()}] Reporte diario generado")
        
        report = {
            'date': datetime.now().isoformat(),
            'posts_generated': 0,
            'posts_published': 0,
            'emails_sent': 0
        }
        
        # Aquí puedes agregar lógica para contar posts y emails
        
        # Guardar reporte
        report_dir = 'data/reports'
        os.makedirs(report_dir, exist_ok=True)
        report_file = f"{report_dir}/report_{datetime.now().strftime('%Y%m%d')}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)
        
        return report
    
    def setup_schedule(self):
        """Configura el calendario de tareas automáticas"""
        print("🗓️ Configurando calendario de automatización...\n")
        
        # Posts diarios en Instagram y Facebook
        for post_time in POST_TIMES:
            schedule.every().day.at(post_time).do(self.generate_and_post_instagram)
            schedule.every().day.at(post_time).do(self.generate_and_post_facebook)
            print(f"📅 Posts programados a las {post_time}")
        
        # Newsletter semanal (cada lunes a las 10:00)
        schedule.every().monday.at("10:00").do(self.send_weekly_newsletter)
        print("📅 Newsletter semanal programada para lunes 10:00")
        
        # Reporte diario (cada día a las 23:00)
        schedule.every().day.at("23:00").do(self.daily_report)
        print("📅 Reporte diario programado para 23:00")
        
        print("\n✅ Calendario configurado exitosamente")
    
    def run(self):
        """Ejecuta el scheduler en loop infinito"""
        self.setup_schedule()
        
        print("\n🤖 Agente IA de Marketing iniciado")
        print("⏰ Esperando tareas programadas...")
        print("Presiona Ctrl+C para detener\n")
        
        try:
            while True:
                schedule.run_pending()
                time.sleep(60)  # Revisar cada minuto
        except KeyboardInterrupt:
            print("\n\n👋 Agente IA detenido")


# Ejemplo de uso inmediato (testing)
def test_run():
    """Ejecuta una prueba de generación de contenido"""
    scheduler = MarketingScheduler()
    
    print("🧪 MODO TESTING - Generando contenido de prueba\n")
    
    # Generar contenido sin publicar
    scheduler.generate_and_post_instagram()
    scheduler.generate_and_post_facebook()
    # scheduler.send_weekly_newsletter()
    
    print("\n✨ Prueba completada. Revisa la carpeta data/generated/")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        # Modo testing: python scheduler.py test
        test_run()
    else:
        # Modo producción: python scheduler.py
        scheduler = MarketingScheduler()
        scheduler.run()
