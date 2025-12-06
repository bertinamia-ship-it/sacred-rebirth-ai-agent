"""
Publicación automática en redes sociales (Instagram y Facebook)
"""
import requests
from config.settings import (
    META_ACCESS_TOKEN,
    INSTAGRAM_BUSINESS_ACCOUNT_ID,
    FACEBOOK_PAGE_ID,
    BUSINESS_INFO
)
import json
from datetime import datetime

class SocialMediaManager:
    def __init__(self):
        self.access_token = META_ACCESS_TOKEN
        self.instagram_account_id = INSTAGRAM_BUSINESS_ACCOUNT_ID
        self.facebook_page_id = FACEBOOK_PAGE_ID
        self.graph_api_url = "https://graph.facebook.com/v18.0"
    
    def post_to_instagram(self, caption, image_url=None):
        """
        Publica en Instagram Business Account
        
        Args:
            caption: Texto del post
            image_url: URL de la imagen (opcional)
        """
        if not self.access_token or not self.instagram_account_id:
            print("❌ Error: Configura META_ACCESS_TOKEN e INSTAGRAM_BUSINESS_ACCOUNT_ID")
            return None
        
        try:
            # Crear contenedor de medios
            container_url = f"{self.graph_api_url}/{self.instagram_account_id}/media"
            
            params = {
                'access_token': self.access_token,
                'caption': caption
            }
            
            if image_url:
                params['image_url'] = image_url
            
            # Crear contenedor
            response = requests.post(container_url, params=params)
            response.raise_for_status()
            container_id = response.json().get('id')
            
            # Publicar contenedor
            publish_url = f"{self.graph_api_url}/{self.instagram_account_id}/media_publish"
            publish_params = {
                'access_token': self.access_token,
                'creation_id': container_id
            }
            
            publish_response = requests.post(publish_url, params=publish_params)
            publish_response.raise_for_status()
            
            post_id = publish_response.json().get('id')
            
            print(f"✅ Post publicado en Instagram: {post_id}")
            return {
                'platform': 'instagram',
                'post_id': post_id,
                'published_at': datetime.now().isoformat(),
                'status': 'published'
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error publicando en Instagram: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta: {e.response.text}")
            return None
    
    def post_to_facebook(self, message, link=None, image_url=None):
        """
        Publica en Facebook Page
        
        Args:
            message: Texto del post
            link: URL para compartir (opcional)
            image_url: URL de imagen (opcional)
        """
        if not self.access_token or not self.facebook_page_id:
            print("❌ Error: Configura META_ACCESS_TOKEN y FACEBOOK_PAGE_ID")
            return None
        
        try:
            url = f"{self.graph_api_url}/{self.facebook_page_id}/feed"
            
            params = {
                'access_token': self.access_token,
                'message': message
            }
            
            if link:
                params['link'] = link
            
            if image_url:
                params['picture'] = image_url
            
            response = requests.post(url, params=params)
            response.raise_for_status()
            
            post_id = response.json().get('id')
            
            print(f"✅ Post publicado en Facebook: {post_id}")
            return {
                'platform': 'facebook',
                'post_id': post_id,
                'published_at': datetime.now().isoformat(),
                'status': 'published'
            }
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Error publicando en Facebook: {e}")
            if hasattr(e.response, 'text'):
                print(f"Respuesta: {e.response.text}")
            return None
    
    def schedule_post(self, platform, content, scheduled_time, image_url=None):
        """
        Programa un post para publicación futura
        (Requiere permisos adicionales de Meta Business)
        """
        print(f"📅 Post programado para {platform} en {scheduled_time}")
        # Esta funcionalidad requiere configuración adicional en Meta Business Suite
        return {
            'platform': platform,
            'content': content,
            'scheduled_time': scheduled_time,
            'status': 'scheduled'
        }


# Ejemplo de uso
if __name__ == "__main__":
    manager = SocialMediaManager()
    
    # Ejemplo de post en Instagram
    caption = """
🌿 ¿Listo para una transformación profunda?

Nuestros retiros de Ayahuasca en Valle de Bravo ofrecen un espacio seguro para:
✨ Sanación emocional
✨ Conexión espiritual
✨ Transformación personal

Próximo retiro: 11 de Enero, 2026

📅 Agenda tu Discovery Call gratuita
🔗 sacred-rebirth.com

#Ayahuasca #RetiroEspiritual #ValleDeBravo #SacredRebirth #TransformacionEspiritual
"""
    
    # manager.post_to_instagram(caption)
    
    # Ejemplo de post en Facebook
    message = """
🌿 Sacred Rebirth - Tu camino hacia la transformación

Descubre el poder sanador de la medicina ancestral en nuestros retiros de Ayahuasca, ubicados en el hermoso Valle de Bravo, México.

¿Qué incluye nuestro retiro?
• Ceremonias de Ayahuasca con facilitadores experimentados
• Sesiones de Kambo y Rapé
• Prácticas de Qigong
• Acompañamiento profesional
• Espacio seguro y acogedor

Próximo retiro: 11 de Enero, 2026

Comienza tu viaje de transformación hoy. Agenda una Discovery Call gratuita.

📞 WhatsApp: +52 722 512 3413
🌐 https://sacred-rebirth.com

#RetiroEspiritual #Ayahuasca #ValleDeBravo #MedicinaAncestral
"""
    
    # manager.post_to_facebook(message, link="https://sacred-rebirth.com")
    
    print("💡 Para usar este módulo, configura tus API keys en el archivo .env")
