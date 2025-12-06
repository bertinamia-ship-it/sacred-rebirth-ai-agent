"""
Generador de contenido usando OpenAI GPT-4
"""
import os
from openai import OpenAI
from config.settings import OPENAI_API_KEY, OPENAI_MODEL
from config.prompts import (
    INSTAGRAM_POST_PROMPT, 
    FACEBOOK_POST_PROMPT,
    EMAIL_CAMPAIGN_PROMPT,
    CONTENT_TOPICS,
    HASHTAGS_INSTAGRAM,
    HASHTAGS_FACEBOOK
)
import random
import json
from datetime import datetime

class ContentGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=OPENAI_API_KEY)
        
    def generate_instagram_post(self, topic=None):
        """Genera un post para Instagram"""
        if not topic:
            topic = random.choice(CONTENT_TOPICS)
        
        prompt = INSTAGRAM_POST_PROMPT.format(topic=topic)
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing de wellness y retiros espirituales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content.strip()
            
            # Agregar hashtags si no están incluidos
            if '#' not in content:
                hashtags = random.sample(HASHTAGS_INSTAGRAM, 10)
                content += '\n\n' + ' '.join(hashtags)
            
            return {
                'platform': 'instagram',
                'topic': topic,
                'content': content,
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
            
        except Exception as e:
            print(f"Error generando post de Instagram: {e}")
            return None
    
    def generate_facebook_post(self, topic=None):
        """Genera un post para Facebook"""
        if not topic:
            topic = random.choice(CONTENT_TOPICS)
        
        prompt = FACEBOOK_POST_PROMPT.format(topic=topic)
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un experto en marketing de wellness y retiros espirituales."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=1200
            )
            
            content = response.choices[0].message.content.strip()
            
            # Agregar hashtags si no están incluidos
            if '#' not in content:
                hashtags = random.sample(HASHTAGS_FACEBOOK, 8)
                content += '\n\n' + ' '.join(hashtags)
            
            return {
                'platform': 'facebook',
                'topic': topic,
                'content': content,
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
            
        except Exception as e:
            print(f"Error generando post de Facebook: {e}")
            return None
    
    def generate_email_campaign(self, topic=None):
        """Genera un email de campaña"""
        if not topic:
            topic = random.choice(CONTENT_TOPICS)
        
        prompt = EMAIL_CAMPAIGN_PROMPT.format(topic=topic)
        
        try:
            response = self.client.chat.completions.create(
                model=OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "Eres un experto en email marketing para wellness."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=1500
            )
            
            content = response.choices[0].message.content.strip()
            
            # Separar subject y body
            parts = content.split('---BODY---')
            subject = parts[0].replace('---SUBJECT---', '').strip()
            body = parts[1].strip() if len(parts) > 1 else content
            
            return {
                'type': 'email_campaign',
                'topic': topic,
                'subject': subject,
                'body': body,
                'created_at': datetime.now().isoformat(),
                'status': 'draft'
            }
            
        except Exception as e:
            print(f"Error generando email campaign: {e}")
            return None
    
    def save_content(self, content_data, filename=None):
        """Guarda el contenido generado en un archivo JSON"""
        if not filename:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            platform = content_data.get('platform', content_data.get('type', 'content'))
            filename = f"data/generated/{platform}_{timestamp}.json"
        
        os.makedirs(os.path.dirname(filename), exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(content_data, f, ensure_ascii=False, indent=2)
        
        print(f"✅ Contenido guardado en: {filename}")
        return filename


# Ejemplo de uso
if __name__ == "__main__":
    generator = ContentGenerator()
    
    print("🌿 Generando contenido para Sacred Rebirth...\n")
    
    # Generar post de Instagram
    print("📸 Generando post de Instagram...")
    instagram_post = generator.generate_instagram_post()
    if instagram_post:
        print(f"\nTema: {instagram_post['topic']}")
        print(f"\n{instagram_post['content']}\n")
        generator.save_content(instagram_post)
    
    # Generar post de Facebook
    print("\n📘 Generando post de Facebook...")
    facebook_post = generator.generate_facebook_post()
    if facebook_post:
        print(f"\nTema: {facebook_post['topic']}")
        print(f"\n{facebook_post['content']}\n")
        generator.save_content(facebook_post)
    
    # Generar email campaign
    print("\n📧 Generando email campaign...")
    email = generator.generate_email_campaign()
    if email:
        print(f"\nTema: {email['topic']}")
        print(f"\nAsunto: {email['subject']}")
        print(f"\n{email['body']}\n")
        generator.save_content(email)
    
    print("✨ ¡Contenido generado exitosamente!")
