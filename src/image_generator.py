#!/usr/bin/env python3
"""
Sacred Rebirth Image Generator
Genera imágenes automáticamente para contenido de marketing
"""
import os
import requests
from openai import OpenAI
from datetime import datetime

class SacredRebirthImageGenerator:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # Estilos base para Sacred Rebirth
        self.base_styles = {
            "spiritual": "mystical, spiritual, ethereal, soft lighting, nature elements, sacred geometry, warm earth tones",
            "nature": "lush jungle, sacred plants, ayahuasca vine, natural light, serene mountains, crystal clear water",
            "ceremony": "sacred ceremony, indigenous elements, feathers, crystals, candles, peaceful meditation",
            "healing": "healing energy, golden light, transformation, rebirth, spiritual awakening, inner peace",
            "retreat": "beautiful retreat center, Valle de Bravo mountains, peaceful sanctuary, meditation space"
        }
        
        # Elementos que siempre incluir
        self.sacred_elements = [
            "sacred ayahuasca plants",
            "spiritual symbols", 
            "nature elements",
            "warm golden lighting",
            "peaceful energy",
            "transformation imagery"
        ]
    
    def generate_retreat_image(self, content_theme="general", style="spiritual"):
        """Genera imagen específica para retiro del 11 de enero"""
        
        base_prompt = f"""
Professional marketing image for Sacred Rebirth ayahuasca retreat.

MAIN ELEMENTS:
- {self.base_styles.get(style, self.base_styles['spiritual'])}
- Sacred ayahuasca vine and plants
- Valle de Bravo mountain landscape in background
- Peaceful, welcoming atmosphere
- Professional quality, Instagram-ready

STYLE: 
- High resolution, professional photography style
- Warm, inviting colors (earth tones, soft greens, golden light)
- Spiritual but not overwhelming
- Clean, modern design suitable for social media

TEXT OVERLAY SPACE:
- Leave space for text overlay
- Clean areas for "Book your discovery call now" text

MOOD: Transformation, healing, spiritual awakening, safe space, professional retreat center

AVOID: Dark imagery, scary elements, overly psychedelic, unprofessional elements
        """
        
        # Prompts específicos por tema
        theme_additions = {
            "retreat_announcement": "Include welcoming energy, January 11 date importance, new beginnings theme",
            "transformation": "Focus on before/after energy, butterfly metaphors, personal growth",
            "medicine": "Beautiful ayahuasca plants, sacred ceremony elements, respectful indigenous honoring",
            "location": "Valle de Bravo beauty, mountain serenity, retreat center atmosphere",
            "testimonial": "Happy, peaceful energy, transformation success, community feeling"
        }
        
        if content_theme in theme_additions:
            base_prompt += f"\n\nTHEME FOCUS: {theme_additions[content_theme]}"
        
        return self.generate_image(base_prompt)
    
    def generate_image(self, prompt):
        """Genera imagen usando DALL-E"""
        try:
            response = self.client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1,
            )
            
            image_url = response.data[0].url
            
            # Descargar imagen
            img_response = requests.get(image_url)
            if img_response.status_code == 200:
                # Guardar imagen localmente
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"sacred_rebirth_{timestamp}.png"
                filepath = f"/tmp/{filename}"
                
                with open(filepath, 'wb') as f:
                    f.write(img_response.content)
                
                return {
                    "success": True,
                    "image_url": image_url,
                    "local_path": filepath,
                    "filename": filename
                }
            else:
                return {"success": False, "error": "Failed to download image"}
                
        except Exception as e:
            return {"success": False, "error": f"Error generating image: {str(e)}"}
    
    def create_campaign_images(self):
        """Genera set de imágenes para campaña del retiro enero 11"""
        images = {}
        
        campaign_themes = {
            "announcement": "retreat_announcement",
            "transformation": "transformation", 
            "medicine": "medicine",
            "location": "location",
            "testimonial": "testimonial"
        }
        
        for name, theme in campaign_themes.items():
            result = self.generate_retreat_image(content_theme=theme)
            images[name] = result
            
        return images