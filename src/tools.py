"""
Herramientas personalizadas para los agentes de CrewAI
"""
from crewai.tools import tool
import json
from datetime import datetime
from src.content_generator import ContentGenerator
from src.social_media import SocialMediaManager
from src.email_campaign import EmailCampaignManager


@tool("Generador de Contenido")
def content_generator_tool(platform: str, topic: str) -> str:
    """
    Genera contenido optimizado para Instagram, Facebook o Email usando IA.
    
    Args:
        platform: Plataforma ('instagram', 'facebook' o 'email')
        topic: Tema del contenido a generar
    
    Returns:
        Contenido generado y ruta del archivo guardado
    """
    generator = ContentGenerator()
    
    if platform.lower() == 'instagram':
        result = generator.generate_instagram_post(topic)
    elif platform.lower() == 'facebook':
        result = generator.generate_facebook_post(topic)
    elif platform.lower() == 'email':
        result = generator.generate_email_campaign(topic)
    else:
        return f"Error: Plataforma '{platform}' no soportada"
    
    if result:
        # Guardar en archivo
        filename = f"data/generated/{platform}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(result, f, ensure_ascii=False, indent=2)
        
        return f"✅ Contenido generado:\n\n{result['content']}\n\nGuardado en: {filename}"
    else:
        return "❌ Error generando contenido"



@tool("Publicador en Redes Sociales")
def social_media_publish_tool(platform: str, content: str, image_url: str = None) -> str:
    """
    Publica contenido en Instagram o Facebook.
    
    Args:
        platform: Plataforma ('instagram' o 'facebook')
        content: Contenido a publicar
        image_url: URL de la imagen (opcional)
    
    Returns:
        Confirmación de publicación o error
    """
    manager = SocialMediaManager()
    
    if platform.lower() == 'instagram':
        result = manager.post_to_instagram(content, image_url)
    elif platform.lower() == 'facebook':
        result = manager.post_to_facebook(content, image_url=image_url)
    else:
        return f"Error: Plataforma '{platform}' no soportada"
    
    if result:
        return f"✅ Publicado en {platform}: Post ID {result.get('post_id')}"
    else:
        return f"❌ Error publicando en {platform}"


@tool("Gestor de Campañas Email")
def email_campaign_tool(subject: str, html_content: str, send_to_all: bool = False) -> str:
    """
    Envía campañas de email a leads.
    
    Args:
        subject: Asunto del email
        html_content: Contenido HTML del email
        send_to_all: Enviar a todos (True) o solo testear (False)
    
    Returns:
        Resumen del envío
    """
    manager = EmailCampaignManager()
    
    # Cargar leads
    try:
        with open('data/leads.json', 'r') as f:
            leads = json.load(f)
    except:
        leads = []
    
    if not leads:
        return "⚠️ No hay leads disponibles en data/leads.json"
    
    if send_to_all:
        template = manager.create_email_template(html_content)
        results = manager.send_bulk_campaign(leads, subject, template)
        return f"✅ Campaña enviada a {len(results)} leads"
    else:
        # Modo test: enviar solo al primer lead
        template = manager.create_email_template(html_content)
        test_lead = [leads[0]]
        result = manager.send_bulk_campaign(test_lead, subject, template)
        return f"📧 Email de prueba enviado a {leads[0]['email']}"


@tool("Gestor de Calendario de Contenido")
def content_calendar_tool(action: str, content_item: dict = None) -> str:
    """
    Gestiona el calendario de contenido programado.
    
    Args:
        action: Acción ('view', 'add' o 'update')
        content_item: Ítem de contenido a agregar/actualizar
    
    Returns:
        Estado del calendario
    """
    calendar_path = 'data/content_calendar.json'
    
    try:
        with open(calendar_path, 'r') as f:
            calendar = json.load(f)
    except:
        calendar = []
    
    if action == 'view':
        if not calendar:
            return "📅 El calendario está vacío"
        return f"📅 Calendario de contenido:\n\n{json.dumps(calendar, indent=2, ensure_ascii=False)}"
    
    elif action == 'add':
        if not content_item:
            return "❌ Error: Se requiere content_item para agregar"
        
        content_item['id'] = len(calendar) + 1
        content_item['created_at'] = datetime.now().isoformat()
        calendar.append(content_item)
        
        with open(calendar_path, 'w') as f:
            json.dump(calendar, f, ensure_ascii=False, indent=2)
        
        return f"✅ Contenido agregado al calendario (ID: {content_item['id']})"
    
    elif action == 'update':
        if not content_item or 'id' not in content_item:
            return "❌ Error: Se requiere content_item con 'id' para actualizar"
        
        item_id = content_item['id']
        for i, item in enumerate(calendar):
            if item.get('id') == item_id:
                calendar[i] = content_item
                with open(calendar_path, 'w') as f:
                    json.dump(calendar, f, ensure_ascii=False, indent=2)
                return f"✅ Contenido actualizado (ID: {item_id})"
        
        return f"❌ No se encontró contenido con ID: {item_id}"
    
    else:
        return f"❌ Acción no válida: {action}"


@tool("Gestor de Leads")
def leads_manager_tool(action: str, lead_data: dict = None, segment_criteria: str = None) -> str:
    """
    Gestiona la base de datos de leads y clientes potenciales.
    
    Args:
        action: Acción ('view', 'add' o 'segment')
        lead_data: Datos del lead para agregar
        segment_criteria: Criterio de segmentación
    
    Returns:
        Información de leads
    """
    leads_path = 'data/leads.json'
    
    try:
        with open(leads_path, 'r') as f:
            leads = json.load(f)
    except:
        leads = []
    
    if action == 'view':
        if not leads:
            return "👥 No hay leads en la base de datos"
        return f"👥 Total de leads: {len(leads)}\n\n{json.dumps(leads[:5], indent=2, ensure_ascii=False)}\n\n(Mostrando primeros 5)"
    
    elif action == 'add':
        if not lead_data:
            return "❌ Error: Se requiere lead_data para agregar"
        
        lead_data['id'] = len(leads) + 1
        lead_data['created_at'] = datetime.now().isoformat()
        leads.append(lead_data)
        
        with open(leads_path, 'w') as f:
            json.dump(leads, f, ensure_ascii=False, indent=2)
        
        return f"✅ Lead agregado: {lead_data.get('email', 'Sin email')}"
    
    elif action == 'segment':
        # Segmentación básica
        if segment_criteria == 'interested':
            segmented = [l for l in leads if l.get('status') == 'interested']
        elif segment_criteria == 'converted':
            segmented = [l for l in leads if l.get('status') == 'converted']
        else:
            segmented = leads
        
        return f"📊 Segmento '{segment_criteria}': {len(segmented)} leads\n\n{json.dumps(segmented[:3], indent=2, ensure_ascii=False)}"
    
    else:
        return f"❌ Acción no válida: {action}"
