"""
Definición de tareas para los agentes del crew
"""
from crewai import Task
from datetime import datetime, timedelta


def create_content_strategy_task(agent, context=None):
    """
    Tarea: Crear estrategia de contenido semanal
    """
    return Task(
        description="""Desarrolla una estrategia de contenido para la próxima semana.
        
        Requisitos:
        1. Define 5-7 temas de contenido relevantes para Sacred Rebirth
        2. Considera el próximo retiro del 11 de Enero, 2026
        3. Mezcla contenido educativo, testimonial y promocional
        4. Incluye temas sobre: Ayahuasca, Kambo, Rapé, Qigong, preparación para retiros
        5. Define objetivos específicos para cada pieza de contenido
        
        Entrega un plan detallado con:
        - Tema del contenido
        - Plataforma recomendada (Instagram/Facebook/Email)
        - Objetivo (awareness/engagement/conversión)
        - Día recomendado de publicación
        - Llamado a la acción sugerido
        """,
        expected_output="""Plan estratégico de contenido semanal con 5-7 temas detallados,
        cada uno con plataforma, objetivo y timing recomendado.""",
        agent=agent,
        context=context
    )


def create_instagram_content_task(agent, topic, context=None):
    """
    Tarea: Generar contenido para Instagram
    """
    return Task(
        description=f"""Genera un post optimizado para Instagram sobre: {topic}
        
        Requisitos:
        1. Usa el generador de contenido con plataforma='instagram' y topic='{topic}'
        2. Asegura que incluya emojis relevantes
        3. Máximo 2200 caracteres
        4. Incluye 8-10 hashtags relevantes
        5. Call to action claro al final
        6. Tono: Espiritual, acogedor, auténtico
        
        El contenido debe:
        - Educar o inspirar a la audiencia
        - Mencionar Sacred Rebirth de forma natural
        - Incluir información sobre el retiro del 11 de Enero si es relevante
        - Ser visualmente descriptivo (para acompañar con imagen)
        """,
        expected_output=f"Post completo para Instagram sobre {topic}, listo para publicar con hashtags incluidos.",
        agent=agent,
        context=context
    )


def create_facebook_content_task(agent, topic, context=None):
    """
    Tarea: Generar contenido para Facebook
    """
    return Task(
        description=f"""Genera un post informativo para Facebook sobre: {topic}
        
        Requisitos:
        1. Usa el generador de contenido con plataforma='facebook' y topic='{topic}'
        2. 300-500 palabras
        3. Tono educativo y profesional
        4. Incluye información útil y detallada
        5. 5-8 hashtags al final
        6. Call to action con enlace a website
        
        El contenido debe:
        - Proporcionar valor educativo
        - Posicionar a Sacred Rebirth como expertos
        - Abordar preguntas comunes o preocupaciones
        - Incluir datos o información verificable cuando sea relevante
        """,
        expected_output=f"Post educativo para Facebook sobre {topic}, 300-500 palabras con hashtags.",
        agent=agent,
        context=context
    )


def create_email_campaign_task(agent, campaign_type='promotional', context=None):
    """
    Tarea: Crear campaña de email
    """
    campaign_topics = {
        'promotional': 'Promoción del próximo retiro del 11 de Enero, 2026',
        'educational': 'Guía de preparación para ceremonias de Ayahuasca',
        'testimonial': 'Testimonios de transformación de participantes anteriores',
        'nurture': 'Serie de emails para nutrir leads interesados'
    }
    
    topic = campaign_topics.get(campaign_type, 'Actualización de Sacred Rebirth')
    
    return Task(
        description=f"""Crea una campaña de email {campaign_type} sobre: {topic}
        
        Requisitos:
        1. Asunto atractivo (máximo 50 caracteres)
        2. Preview text optimizado
        3. Contenido HTML profesional y responsive
        4. Personalización con nombre del destinatario
        5. Call to action claro y visible
        6. Incluye información de contacto: +52 722 512 3413
        7. Enlace al website: https://sacred-rebirth.com
        
        El email debe:
        - Ser visualmente atractivo pero simple
        - Incluir beneficios claros
        - Generar urgencia o interés (sin presionar)
        - Proporcionar próximos pasos claros
        - Mantener tono cálido y profesional
        """,
        expected_output=f"Email completo con asunto, contenido HTML y texto plano para campaña {campaign_type}.",
        agent=agent,
        context=context
    )


def create_social_media_publish_task(agent, platform, content, context=None):
    """
    Tarea: Publicar en redes sociales
    """
    return Task(
        description=f"""Publica el siguiente contenido en {platform}:
        
        {content}
        
        Pasos:
        1. Revisa que el contenido cumple con las mejores prácticas de {platform}
        2. Usa la herramienta de publicación con platform='{platform}'
        3. Si es posible, incluye una imagen relevante
        4. Confirma la publicación exitosa
        5. Registra el post_id para seguimiento
        """,
        expected_output=f"Confirmación de publicación exitosa en {platform} con post_id.",
        agent=agent,
        context=context
    )


def create_leads_nurture_task(agent, segment='interested', context=None):
    """
    Tarea: Nutrir leads
    """
    return Task(
        description=f"""Ejecuta una campaña de nutrición para leads en segmento: {segment}
        
        Pasos:
        1. Usa LeadsManagerTool para obtener leads del segmento '{segment}'
        2. Analiza el perfil y estado de cada lead
        3. Crea email personalizado según su etapa del customer journey
        4. Para leads en etapa temprana: contenido educativo
        5. Para leads interesados: información sobre próximo retiro
        6. Para leads casi convertidos: incentivos y urgencia suave
        
        Objetivo:
        - Mover leads al siguiente estado del funnel
        - Mantener engagement sin ser invasivo
        - Proporcionar valor en cada interacción
        - Identificar leads listos para conversión
        """,
        expected_output=f"Reporte de campaña de nutrición ejecutada para segmento {segment} con métricas.",
        agent=agent,
        context=context
    )


def create_calendar_management_task(agent, action='view', context=None):
    """
    Tarea: Gestionar calendario de contenido
    """
    return Task(
        description=f"""Gestiona el calendario de contenido - Acción: {action}
        
        Si action='view':
        - Obtén y muestra el calendario actual
        - Identifica gaps o días sin contenido programado
        - Sugiere mejoras en la distribución
        
        Si action='add':
        - Agrega nuevos contenidos al calendario
        - Distribuye equitativamente por plataforma
        - Mantén balance entre contenido educativo, promocional y engagement
        
        Si action='update':
        - Actualiza contenidos según feedback o métricas
        - Optimiza horarios de publicación
        - Ajusta frecuencia según engagement
        """,
        expected_output=f"Calendario de contenido actualizado o reporte del estado actual.",
        agent=agent,
        context=context
    )


def create_analytics_task(agent, metric_type='engagement', context=None):
    """
    Tarea: Analizar métricas y optimizar
    """
    return Task(
        description=f"""Analiza métricas de {metric_type} y proporciona recomendaciones
        
        Analiza:
        1. Contenido del calendario y su performance
        2. Patrones de engagement por tipo de contenido
        3. Mejores horarios de publicación
        4. Hashtags más efectivos
        5. Temas que generan más interacción
        
        Proporciona:
        - Top 3 contenidos con mejor performance
        - Recomendaciones accionables para mejorar
        - Sugerencias de nuevos temas basados en datos
        - Optimizaciones de timing y frecuencia
        - Insights sobre la audiencia
        """,
        expected_output=f"Reporte de análisis de {metric_type} con insights y recomendaciones accionables.",
        agent=agent,
        context=context
    )


def create_full_campaign_task(agent, campaign_goal='próximo retiro', context=None):
    """
    Tarea: Orquestar campaña completa multicanal
    """
    return Task(
        description=f"""Diseña y ejecuta una campaña multicanal completa para: {campaign_goal}
        
        La campaña debe incluir:
        1. 3-5 posts para Instagram
        2. 2-3 posts para Facebook
        3. 1 campaña de email (3-5 emails en secuencia)
        4. Calendario de publicación optimizado
        5. Seguimiento y nutrición de leads
        
        Fases:
        1. PLANIFICACIÓN: Define objetivos, métricas y timeline
        2. CREACIÓN: Genera todo el contenido necesario
        3. PROGRAMACIÓN: Organiza en calendario
        4. EJECUCIÓN: Publica contenido según plan
        5. SEGUIMIENTO: Nutre leads y hace seguimiento
        
        Objetivo principal: {campaign_goal}
        Meta: Llenar el retiro del 11 de Enero, 2026
        """,
        expected_output=f"Campaña completa ejecutada para '{campaign_goal}' con reporte de actividades.",
        agent=agent,
        context=context
    )
