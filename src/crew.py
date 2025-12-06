"""
Crew Principal de Marketing IA - Sacred Rebirth
Orquesta múltiples agentes trabajando en conjunto
"""
from crewai import Crew, Process
from src.agents import (
    create_content_strategist,
    create_content_creator,
    create_social_media_manager,
    create_email_marketing_specialist,
    create_analytics_optimizer,
    create_customer_success_agent
)
from src.tasks import (
    create_content_strategy_task,
    create_instagram_content_task,
    create_facebook_content_task,
    create_email_campaign_task,
    create_social_media_publish_task,
    create_leads_nurture_task,
    create_calendar_management_task,
    create_analytics_task,
    create_full_campaign_task
)


class MarketingCrew:
    """
    Crew de agentes de marketing IA para Sacred Rebirth
    """
    
    def __init__(self):
        """Inicializa el crew con todos los agentes"""
        print("🚀 Inicializando Marketing Crew...")
        
        # Crear agentes
        self.strategist = create_content_strategist()
        self.creator = create_content_creator()
        self.social_manager = create_social_media_manager()
        self.email_specialist = create_email_marketing_specialist()
        self.analyst = create_analytics_optimizer()
        self.customer_success = create_customer_success_agent()
        
        print("✅ Agentes creados exitosamente")
    
    def run_content_strategy(self):
        """
        Ejecuta planificación estratégica de contenido
        """
        print("\n📋 Ejecutando: Planificación Estratégica de Contenido")
        
        # Tarea de estrategia
        strategy_task = create_content_strategy_task(self.strategist)
        
        # Crear crew
        crew = Crew(
            agents=[self.strategist],
            tasks=[strategy_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Estrategia de contenido completada")
        return result
    
    def run_content_creation(self, topics=None):
        """
        Ejecuta creación de contenido para múltiples plataformas
        
        Args:
            topics: Lista de temas ['tema1', 'tema2', ...] o None para usar por defecto
        """
        print("\n✍️ Ejecutando: Creación de Contenido")
        
        if not topics:
            topics = [
                'Beneficios de la Ayahuasca',
                'Preparación para ceremonia de Kambo',
                'Qigong y energía vital'
            ]
        
        tasks = []
        
        # Crear tareas para cada tema
        for topic in topics[:2]:  # Limitar a 2 temas por ejecución
            # Instagram
            tasks.append(create_instagram_content_task(self.creator, topic))
            # Facebook
            tasks.append(create_facebook_content_task(self.creator, topic))
        
        # Crear crew
        crew = Crew(
            agents=[self.creator],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Contenido creado exitosamente")
        return result
    
    def run_social_media_campaign(self, content_dict=None):
        """
        Ejecuta publicación en redes sociales
        
        Args:
            content_dict: {'instagram': 'contenido...', 'facebook': 'contenido...'}
        """
        print("\n📱 Ejecutando: Campaña de Redes Sociales")
        
        if not content_dict:
            print("⚠️ No se proporcionó contenido, generando automáticamente...")
            return self.run_content_creation()
        
        tasks = []
        
        if 'instagram' in content_dict:
            tasks.append(create_social_media_publish_task(
                self.social_manager,
                'instagram',
                content_dict['instagram']
            ))
        
        if 'facebook' in content_dict:
            tasks.append(create_social_media_publish_task(
                self.social_manager,
                'facebook',
                content_dict['facebook']
            ))
        
        # Crear crew
        crew = Crew(
            agents=[self.social_manager],
            tasks=tasks,
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Publicación en redes sociales completada")
        return result
    
    def run_email_campaign(self, campaign_type='promotional'):
        """
        Ejecuta campaña de email marketing
        
        Args:
            campaign_type: 'promotional', 'educational', 'testimonial', 'nurture'
        """
        print(f"\n📧 Ejecutando: Campaña de Email ({campaign_type})")
        
        # Tareas
        email_task = create_email_campaign_task(self.email_specialist, campaign_type)
        
        # Crear crew
        crew = Crew(
            agents=[self.email_specialist],
            tasks=[email_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Campaña de email completada")
        return result
    
    def run_leads_management(self, action='nurture', segment='interested'):
        """
        Ejecuta gestión y nutrición de leads
        
        Args:
            action: 'view', 'nurture', 'segment'
            segment: 'interested', 'converted', 'all'
        """
        print(f"\n👥 Ejecutando: Gestión de Leads ({action})")
        
        # Tarea de nutrición
        nurture_task = create_leads_nurture_task(self.customer_success, segment)
        
        # Crear crew
        crew = Crew(
            agents=[self.customer_success],
            tasks=[nurture_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Gestión de leads completada")
        return result
    
    def run_analytics(self, metric_type='engagement'):
        """
        Ejecuta análisis de métricas y optimización
        
        Args:
            metric_type: 'engagement', 'conversion', 'reach', 'all'
        """
        print(f"\n📊 Ejecutando: Análisis de Métricas ({metric_type})")
        
        # Tarea de análisis
        analytics_task = create_analytics_task(self.analyst, metric_type)
        
        # Crear crew
        crew = Crew(
            agents=[self.analyst],
            tasks=[analytics_task],
            process=Process.sequential,
            verbose=True
        )
        
        # Ejecutar
        result = crew.kickoff()
        print("\n✅ Análisis completado")
        return result
    
    def run_full_campaign(self, campaign_goal='próximo retiro'):
        """
        Ejecuta campaña completa multicanal coordinada por todos los agentes
        
        Args:
            campaign_goal: Objetivo de la campaña
        """
        print(f"\n🎯 Ejecutando: CAMPAÑA COMPLETA - {campaign_goal}")
        print("=" * 60)
        
        # Fase 1: Estrategia
        strategy_task = create_content_strategy_task(self.strategist)
        
        # Fase 2: Creación de contenido (usando output de estrategia)
        instagram_task = create_instagram_content_task(
            self.creator,
            'Transformación y sanación con Ayahuasca'
        )
        
        facebook_task = create_facebook_content_task(
            self.creator,
            'Guía completa de preparación para retiros'
        )
        
        # Fase 3: Email marketing
        email_task = create_email_campaign_task(self.email_specialist, 'promotional')
        
        # Fase 4: Análisis
        analytics_task = create_analytics_task(self.analyst, 'all')
        
        # Fase 5: Seguimiento de leads
        leads_task = create_leads_nurture_task(self.customer_success, 'interested')
        
        # Crear crew colaborativo
        crew = Crew(
            agents=[
                self.strategist,
                self.creator,
                self.email_specialist,
                self.analyst,
                self.customer_success
            ],
            tasks=[
                strategy_task,
                instagram_task,
                facebook_task,
                email_task,
                analytics_task,
                leads_task
            ],
            process=Process.sequential,
            verbose=True,
            memory=True,  # Habilita memoria compartida entre agentes
            embedder={
                "provider": "openai",
                "config": {
                    "model": "text-embedding-3-small"
                }
            }
        )
        
        # Ejecutar campaña completa
        result = crew.kickoff()
        
        print("\n" + "=" * 60)
        print("✅ CAMPAÑA COMPLETA FINALIZADA")
        print("=" * 60)
        
        return result
    
    def run_daily_automation(self):
        """
        Ejecuta automatización diaria de marketing
        """
        print("\n⏰ Ejecutando: Automatización Diaria")
        print("=" * 60)
        
        # 1. Generar contenido del día
        print("\n1️⃣ Generando contenido...")
        content_result = self.run_content_creation(['Tema del día'])
        
        # 2. Revisar calendario
        print("\n2️⃣ Revisando calendario...")
        calendar_task = create_calendar_management_task(self.strategist, 'view')
        
        # 3. Nutrir leads
        print("\n3️⃣ Nutriendo leads...")
        leads_result = self.run_leads_management('nurture', 'interested')
        
        # 4. Análisis rápido
        print("\n4️⃣ Analizando métricas...")
        analytics_result = self.run_analytics('engagement')
        
        print("\n" + "=" * 60)
        print("✅ Automatización diaria completada")
        print("=" * 60)
        
        return {
            'content': content_result,
            'leads': leads_result,
            'analytics': analytics_result
        }


# Funciones helper para uso directo
def quick_instagram_post(topic):
    """Genera rápidamente un post de Instagram"""
    crew = MarketingCrew()
    creator = crew.creator
    task = create_instagram_content_task(creator, topic)
    
    simple_crew = Crew(
        agents=[creator],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    return simple_crew.kickoff()


def quick_facebook_post(topic):
    """Genera rápidamente un post de Facebook"""
    crew = MarketingCrew()
    creator = crew.creator
    task = create_facebook_content_task(creator, topic)
    
    simple_crew = Crew(
        agents=[creator],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    return simple_crew.kickoff()


def quick_email(campaign_type='promotional'):
    """Genera rápidamente un email"""
    crew = MarketingCrew()
    specialist = crew.email_specialist
    task = create_email_campaign_task(specialist, campaign_type)
    
    simple_crew = Crew(
        agents=[specialist],
        tasks=[task],
        process=Process.sequential,
        verbose=True
    )
    
    return simple_crew.kickoff()
