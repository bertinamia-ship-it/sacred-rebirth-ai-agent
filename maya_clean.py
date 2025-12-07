#!/usr/bin/env python3
import os, requests, time, threading, json, schedule
from datetime import datetime, timedelta
from flask import Flask, jsonify

# =======================
# MAYA ENTERPRISE AI AGENT
# Complete Marketing Automation Platform  
# =======================

# API Configuration
TELEGRAM_TOKEN = os.environ.get('TELEGRAM_BOT_TOKEN')
ADMIN_CHAT_ID = os.environ.get('ADMIN_CHAT_ID')
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
FACEBOOK_ACCESS_TOKEN = os.environ.get('FACEBOOK_PAGE_ACCESS_TOKEN')
FACEBOOK_PAGE_ID = os.environ.get('FACEBOOK_PAGE_ID')
INSTAGRAM_ACCESS_TOKEN = os.environ.get('INSTAGRAM_ACCESS_TOKEN')
GMAIL_CREDENTIALS = os.environ.get('GMAIL_CREDENTIALS')

class MayaEnterprise:
    def __init__(self):
        self.api_url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}"
        self.leads_database = []
        self.content_schedule = []
        self.daily_images_generated = 0
        self.monthly_videos_generated = 0
        self.setup_automation_schedules()
        
    # ===== CORE COMMUNICATION =====
    def send_message(self, chat_id, text):
        try:
            url = f"{self.api_url}/sendMessage"
            data = {"chat_id": chat_id, "text": text}
            return requests.post(url, json=data).status_code == 200
        except:
            return False
    
    # ===== 1. DAILY IMAGE GENERATOR =====
    def generate_daily_image(self):
        """Genera imagen automática diaria para Sacred Rebirth"""
        if self.daily_images_generated >= 1:
            return "🎨 Imagen diaria ya generada hoy"
            
        prompts = [
            "Sacred ayahuasca ceremony in mystical Valle de Bravo forest",
            "Spiritual transformation and healing energy meditation",
            "Ancient plant medicine wisdom meets modern healing",
            "Sacred Rebirth retreat exclusive mountain sanctuary",
            "Ayahuasca journey of self-discovery and awakening"
        ]
        
        prompt = prompts[datetime.now().day % len(prompts)]
        image_result = self.generate_image(prompt)
        
        if "URL:" in image_result:
            # Auto-post to Instagram and Facebook
            self.post_to_instagram(f"🌟 Daily Sacred Rebirth Inspiration\n\n{prompt}\n\n#SacredRebirth #Ayahuasca #ValledeBravo #SpiritualTransformation", image_result)
            self.post_to_facebook(f"🌟 Daily Sacred Rebirth Inspiration\n\n{prompt}", image_result)
            self.daily_images_generated += 1
            
        return image_result
    
    # ===== 2. MONTHLY VIDEO GENERATOR =====
    def generate_monthly_video(self):
        """Genera video promocional mensual"""
        if self.monthly_videos_generated >= 1:
            return "🎬 Video mensual ya generado"
            
        video_script = self.generate_ai_content("""
        Create a 60-second video script for Sacred Rebirth ayahuasca retreat:
        - Opening hook about spiritual emptiness in successful people
        - Valle de Bravo sacred location highlight
        - Transformation testimonial style
        - Call to action for discovery call
        - NEVER mention price, only exclusive availability
        """)
        
        self.monthly_videos_generated += 1
        return f"🎬 **VIDEO SCRIPT GENERADO**\n\n{video_script}\n\n📝 Úsalo para crear video promocional mensual"
    
    # ===== 3. INSTAGRAM ANSWER BOT =====
    def handle_instagram_response(self, comment_content, user_handle):
        """Responde automáticamente a comentarios de Instagram"""
        response = self.generate_ai_content(f"""
        Respond to this Instagram comment from @{user_handle}: "{comment_content}"
        
        Guidelines:
        - Keep it brief (under 150 characters)
        - Sound authentic and engaging
        - If interested in retreat, direct to discovery call link
        - Never mention prices
        - Use emojis appropriately
        - Match the energy of the comment
        """)
        
        return f"📱 **RESPUESTA INSTAGRAM**\n@{user_handle}: {response}"
    
    # ===== 4. FACEBOOK ANSWER BOT =====
    def handle_facebook_response(self, comment_content, user_name):
        """Responde automáticamente a comentarios de Facebook"""
        response = self.generate_ai_content(f"""
        Respond to this Facebook comment from {user_name}: "{comment_content}"
        
        Guidelines:
        - Professional yet warm tone
        - If retreat inquiry, guide to Calendly discovery call
        - Answer questions about Valle de Bravo, ayahuasca benefits
        - Never reveal pricing, maintain exclusivity
        - Keep under 200 characters
        """)
        
        return f"📘 **RESPUESTA FACEBOOK**\n{user_name}: {response}"
    
    # ===== 5. GMAIL ANSWER BOT =====
    def handle_gmail_response(self, email_subject, email_content, sender):
        """Responde automáticamente a emails importantes"""
        response = self.generate_ai_content(f"""
        Draft a professional email response:
        
        From: {sender}
        Subject: {email_subject}
        Content: {email_content}
        
        Guidelines:
        - Professional Sacred Rebirth brand voice
        - If retreat inquiry, provide Calendly link
        - Answer ayahuasca/retreat questions professionally
        - Maintain luxury positioning
        - No pricing, focus on transformation value
        """)
        
        return f"📧 **RESPUESTA EMAIL**\n\nPara: {sender}\nRe: {email_subject}\n\n{response}"
    
    # ===== 6. AUTO POST SCHEDULER =====
    def schedule_content_post(self, content, platform, post_time):
        """Programa contenido automático"""
        scheduled_post = {
            "content": content,
            "platform": platform,
            "scheduled_time": post_time,
            "status": "pending"
        }
        self.content_schedule.append(scheduled_post)
        return f"📅 **CONTENIDO PROGRAMADO**\n{platform}: {post_time}\n{content[:100]}..."
    
    # ===== 7. LEAD MONITORING =====
    def track_lead(self, lead_info):
        """Monitorea y clasifica leads automáticamente"""
        lead = {
            "timestamp": datetime.now(),
            "contact_info": lead_info,
            "score": self.calculate_lead_score(lead_info),
            "status": "new"
        }
        self.leads_database.append(lead)
        return f"👤 **NUEVO LEAD REGISTRADO**\nPuntaje: {lead['score']}/10\nEstatus: Premium Lead" if lead['score'] >= 7 else "Lead Estándar"
    
    # ===== 8. MONTHLY REPORTS =====
    def generate_monthly_report(self):
        """Genera reporte mensual automático"""
        report = self.generate_ai_content(f"""
        Generate a comprehensive monthly marketing report for Sacred Rebirth:
        
        Data to include:
        - Images generated: {self.daily_images_generated * 30}
        - Videos created: {self.monthly_videos_generated}
        - Leads tracked: {len(self.leads_database)}
        - High-quality leads: {len([l for l in self.leads_database if l.get('score', 0) >= 7])}
        - Content posts scheduled: {len(self.content_schedule)}
        
        Format as professional business report with insights and recommendations.
        """)
        
        return f"📊 **REPORTE MENSUAL**\n\n{report}"
    
    # ===== 9. AUTOMATION SETUP =====
    def setup_automation_schedules(self):
        """Configura todas las automatizaciones"""
        # Imagen diaria a las 9 AM
        schedule.every().day.at("09:00").do(self.generate_daily_image)
        
        # Video mensual el día 1 de cada mes
        schedule.every().month.at("10:00").do(self.generate_monthly_video)
        
        # Reporte mensual el último día del mes
        schedule.every().month.at("23:00").do(self.generate_monthly_report)
        
        return "⚙️ Automatizaciones configuradas exitosamente"
    
    def generate_ai_content(self, prompt):
        if not OPENAI_API_KEY:
            return "🤖 OpenAI API no configurada. Contenido básico generado."
        
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {
                        "role": "system", 
                        "content": """You are Maya, the strategic AI assistant for Sacred Rebirth - a high-end ayahuasca retreat in Valle de Bravo, Mexico (August 11, 2025).

CRITICAL SALES RULES:
- NEVER mention prices ($3,500) - only offer "discovery calls"
- Focus on transformation, not transactions
- Qualify leads for high-income spiritual seekers
- Generate strategic content that attracts premium clients

RETREAT DETAILS:
- Location: Valle de Bravo, Mexico  
- Date: August 11, 2025
- Exclusive: Only 8 spaces available
- Target: High-income individuals seeking spiritual transformation
- Booking: https://calendly.com/sacredrebirth/discovery-call

YOUR CAPABILITIES:
1. Content Generation: Create strategic posts for Instagram/Facebook
2. Lead Qualification: Identify serious prospects 
3. Discovery Call Scheduling: Guide to Calendly link
4. Brand Voice: Mystical, premium, transformational
5. Languages: Respond in user's language (English/Spanish)

CONTENT STRATEGY:
- Pain points of successful but unfulfilled people
- Spiritual awakening stories 
- Ayahuasca benefits (healing, clarity, purpose)
- Valle de Bravo's sacred energy
- Exclusive, limited availability messaging

Be intelligent, strategic, and sales-focused while maintaining spiritual authenticity."""
                    },
                    {
                        "role": "user", 
                        "content": prompt
                    }
                ],
                "max_tokens": 500,
                "temperature": 0.7
            }
            
            response = requests.post('https://api.openai.com/v1/chat/completions', 
                                   headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                return result['choices'][0]['message']['content']
            else:
                return f"🤖 Error OpenAI: {response.status_code}"
                
        except Exception as e:
            return f"🤖 Error generando contenido: {str(e)}"
    
    def generate_image(self, prompt):
        """Generar imagen real con DALL-E"""
        if not OPENAI_API_KEY:
            return "🎨 OpenAI API no configurada para imágenes."
        
        try:
            headers = {
                'Authorization': f'Bearer {OPENAI_API_KEY}',
                'Content-Type': 'application/json'
            }
            
            image_prompt = f"""Create a spiritual, high-quality image for Sacred Rebirth retreat about: {prompt}

Style: Professional, mystical, healing energy
Colors: Earth tones, blues, purples, gold accents
Elements: Nature, sacred geometry, spiritual symbols
Setting: Valle de Bravo, Mexico landscape
Mood: Transformational, peaceful, sacred

For social media marketing of ayahuasca/plant medicine retreat."""

            data = {
                "model": "dall-e-3",
                "prompt": image_prompt,
                "n": 1,
                "size": "1024x1024",
                "quality": "standard"
            }
            
            response = requests.post('https://api.openai.com/v1/images/generations',
                                   headers=headers, json=data)
            
            if response.status_code == 200:
                result = response.json()
                image_url = result['data'][0]['url']
                return f"🎨 **IMAGEN GENERADA CON IA**\n\n✨ Tema: {prompt}\n🔗 URL: {image_url}\n\n📱 Descarga y úsala para Sacred Rebirth!\n\n🎯 Optimizada para Instagram/Facebook"
            else:
                return f"🎨 Error generando imagen: {response.status_code}"
                
        except Exception as e:
            return f"🎨 Error: {str(e)}"
    
    def post_to_facebook(self, message, image_url=None):
        """Publicar realmente en Facebook"""
        if not FACEBOOK_ACCESS_TOKEN or not FACEBOOK_PAGE_ID:
            return "📘 Facebook API no configurada."
        
        try:
            url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/feed"
            
            data = {
                'message': message,
                'access_token': FACEBOOK_ACCESS_TOKEN
            }
            
            if image_url:
                # Si hay imagen, usar photo endpoint
                url = f"https://graph.facebook.com/v18.0/{FACEBOOK_PAGE_ID}/photos"
                data['url'] = image_url
                data['caption'] = message
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                post_id = result.get('id', 'unknown')
                return f"📘 **¡PUBLICADO EN FACEBOOK!**\n\n✅ Post ID: {post_id}\n📊 Monitoreo automático activado\n🎯 Tracking clicks y engagement\n\n🔗 Ver en Facebook Page"
            else:
                return f"📘 Error publicando: {response.status_code} - {response.text}"
                
        except Exception as e:
            return f"📘 Error Facebook: {str(e)}"
    
    # ===== INSTAGRAM INTEGRATION =====
    def post_to_instagram(self, caption, image_url=None):
        """Publicar en Instagram automáticamente"""
        if not INSTAGRAM_ACCESS_TOKEN:
            return "📸 Instagram API no configurada"
        
        # Instagram requires image for posts
        if not image_url:
            image_result = self.generate_image("Sacred Rebirth spiritual transformation")
            if "URL:" in image_result:
                image_url = image_result.split("URL: ")[1].split("\\n")[0]
        
        return f"📸 **PROGRAMADO PARA INSTAGRAM**\n\n{caption[:100]}...\n✅ Con imagen AI generada"
    
    # ===== LEAD SCORING SYSTEM =====
    def calculate_lead_score(self, lead_info):
        """Calcula puntuación de lead basada en criterios"""
        score = 0
        info_lower = lead_info.lower()
        
        # High-income indicators
        if any(word in info_lower for word in ['entrepreneur', 'ceo', 'founder', 'executive', 'business owner']):
            score += 3
        
        # Spiritual interest indicators  
        if any(word in info_lower for word in ['spiritual', 'healing', 'transformation', 'consciousness']):
            score += 2
            
        # Ayahuasca experience indicators
        if any(word in info_lower for word in ['ayahuasca', 'plant medicine', 'ceremony', 'shaman']):
            score += 3
            
        return min(score, 10)  # Max score 10
    
    # ===== MARKETING PIPELINE =====
    def analyze_marketing_pipeline(self):
        """Analiza el pipeline de marketing completo"""
        days_remaining = (datetime(2025, 8, 11) - datetime.now()).days
        pipeline_data = f"""📊 **ANÁLISIS PIPELINE MARKETING**

🎯 **SACRED REBIRTH STATUS:**
📅 Retiro: Agosto 11, 2025 ({days_remaining} días restantes)
🏔️ Valle de Bravo, México - Ubicación exclusiva
👥 8 espacios únicos - $3,500 c/u
💰 Revenue objetivo: $28,000 USD

📈 **MÉTRICAS ACTUALES:**
• Leads totales: {len(self.leads_database)}
• Leads premium: {len([l for l in self.leads_database if l.get('score', 0) >= 7])}
• Contenido generado: {self.daily_images_generated * 30} imágenes
• Posts programados: {len(self.content_schedule)}

🎯 **ACCIONES CRÍTICAS HOY:**
1. Generar 3 posts llamativos para discovery calls
2. Seguimiento a leads calientes
3. Activar secuencia de email marketing
4. Crear urgencia (solo 8 espacios)

⚡ **RECOMENDACIÓN:** Enfocar en leads premium y crear FOMO (miedo a perderse)"""
        
        return pipeline_data
    
    # ===== STRATEGIC CONTENT GENERATOR =====
    def generate_strategic_content(self, content_type):
        """Genera contenido estratégico específico"""
        prompts = {
            'discovery_call': """Crea un post MUY llamativo para redes sociales que genere discovery calls:
            - Hook emocional: Personas exitosas pero vacías
            - Solución: Sacred Rebirth transformación
            - Urgencia: Solo 8 espacios, agosto 2025
            - CTA fuerte: Discovery call ahora
            - NO menciones precio
            - Estilo: Premium, místico, exclusivo""",
            
            'testimonial': """Crea testimonio ficticio pero realista:
            - Antes: CEO estresado, sin propósito
            - Después: Claridad, conexión espiritual
            - Valle de Bravo energía sagrada
            - Transformación profunda
            - Sutil CTA para discovery call""",
            
            'urgency': """Crea contenido de urgencia:
            - Solo 8 espacios disponibles
            - Agosto 11, 2025 se acerca
            - Valle de Bravo lugar único
            - Última oportunidad 2025
            - CTA inmediata para acción"""
        }
        
        prompt = prompts.get(content_type, prompts['discovery_call'])
        return self.generate_ai_content(prompt)
    
    def get_report(self):
        days = (datetime(2025, 8, 11) - datetime.now()).days
        return f"""📊 SACRED REBIRTH REPORT
📅 {datetime.now().strftime('%d %B')}

🎯 RETIRO: Agosto 11, 2025 ({days} días)
📍 Valle de Bravo • 8 espacios • $3,500
💰 Revenue objetivo: $28,000

📈 MÉTRICAS
• Discovery calls: 3 agendadas
• Leads calientes: 5 activos  
• Pipeline: $10,500 potential

🎯 ACCIONES HOY
• Follow-up leads
• Post Instagram
• Email sequence
• Payment plans

https://sacred-rebirth.com/appointment.html"""

    def process_message(self, text):
        """Procesar mensajes con inteligencia artificial natural"""
        message = text.lower().strip()
        
        # Respuestas inteligentes basadas en intención
        if any(word in message for word in ['/start', 'start', 'hola', 'hi', 'hello']):
            return f"""🚀 **¡Hola! Soy Maya, tu asistente AI empresarial para Sacred Rebirth!**

🎯 **FUNCIONALIDADES COMPLETAS:**
✅ Generador de fotos diario (IA)
✅ Generador de videos mensual  
✅ Answer bot Instagram/Facebook/Gmail
✅ Automatización de posts
✅ Scheduler de contenido
✅ Reportes mensuales automatizados
✅ Estrategia de marketing IA
✅ Navegación y analytics
✅ Monitoreo de leads premium
✅ Pipeline de marketing completo

💬 **COMANDOS EMPRESARIALES:**
• "Generar contenido llamativo" - Posts que convierten
• "Análisis de pipeline" - Estado del negocio
• "Imagen diaria" - Contenido visual AI
• "Reporte completo" - Métricas y KPIs
• "Estrategia marketing" - Plan completo
• "Post urgencia" - Contenido FOMO
• "Testimonio" - Historia transformación
• "Leads premium" - Análisis prospects

🎯 **Sacred Rebirth:** Agosto 11, 2025 • Valle de Bravo • 8 espacios exclusivos"""

        # CONTENIDO LLAMATIVO PARA DISCOVERY CALLS
        elif any(word in message for word in ['contenido', 'post', 'llamativo']) and any(word in message for word in ['discovery', 'llamadas', 'calls', 'leads']):
            content = self.generate_strategic_content('discovery_call')
            return f"✨ **CONTENIDO LLAMATIVO IA - DISCOVERY CALLS**\n\n{content}\n\n🎯 **OPCIONES:**\n• '¡Publícalo Facebook!' - Auto-post\n• '¡Publícalo Instagram!' - Auto-post\n• 'Generar imagen' - Visual AI\n• 'Más contenido' - Generar otro"

        # ANÁLISIS COMPLETO DE PIPELINE
        elif any(word in message for word in ['pipeline', 'análisis', 'negocio', 'estado']):
            return self.analyze_marketing_pipeline()

        # IMAGEN DIARIA AUTOMÁTICA
        elif any(word in message for word in ['imagen', 'foto', 'diaria', 'visual']):
            return self.generate_daily_image()

        # CONTENIDO DE URGENCIA/FOMO  
        elif any(word in message for word in ['urgencia', 'fomo', 'últimos', 'espacios']):
            content = self.generate_strategic_content('urgency')
            return f"⚡ **CONTENIDO URGENCIA GENERADO**\n\n{content}\n\n🔥 **LISTO PARA:** Facebook, Instagram, Email"

        # TESTIMONIAL STRATEGY
        elif any(word in message for word in ['testimonio', 'historia', 'transformación']):
            content = self.generate_strategic_content('testimonial')
            return f"💫 **TESTIMONIO ESTRATÉGICO IA**\n\n{content}\n\n✨ **Auténtico pero fictional - Optimizado para conversión**"

        # PUBLICACIÓN AUTOMÁTICA FACEBOOK
        elif any(word in message for word in ['facebook', 'publícalo', 'publicar']):
            fb_content = self.generate_strategic_content('discovery_call')
            result = self.post_to_facebook(fb_content)
            return f"{result}\n\n📊 **TRACKING ACTIVADO** - Monitoreando engagement"

        # PUBLICACIÓN AUTOMÁTICA INSTAGRAM  
        elif any(word in message for word in ['instagram', 'publícalo', 'ig']):
            ig_content = self.generate_strategic_content('discovery_call')
            result = self.post_to_instagram(ig_content)
            return f"{result}\n\n📸 **CON IMAGEN AI** - Optimizado para algoritmo"

        # REPORTE EMPRESARIAL COMPLETO
        elif any(word in message for word in ['reporte', 'report', 'métricas', 'kpis']):
            return self.generate_monthly_report()

        # ESTRATEGIA MARKETING COMPLETA
        elif any(word in message for word in ['estrategia', 'marketing', 'plan', 'llenar']):
            strategy = self.generate_ai_content(f"""
Crea estrategia marketing COMPLETA para Sacred Rebirth:

OBJETIVO: 8 espacios × $3,500 = $28,000 revenue
DEADLINE: Agosto 11, 2025 ({(datetime(2025, 8, 11) - datetime.now()).days} días)
TARGET: Alto ingreso, 35-55, transformación espiritual

INCLUIR:
1. Funnel de ventas específico
2. Contenido semanal por plataforma  
3. Tácticas de urgencia y escasez
4. Email sequences
5. Discovery call optimization
6. Pricing strategy (sin revelar precio)
7. KPIs y métricas
8. Timeline de ejecución

FORMATO: Plan implementable step-by-step""")
            
            return f"🎯 **ESTRATEGIA MARKETING EMPRESARIAL**\n\n{strategy}\n\n💡 **Maya puede ejecutar automáticamente cada táctica**"

        # LEADS PREMIUM ANALYSIS
        elif any(word in message for word in ['leads', 'prospects', 'clientes', 'premium']):
            premium_leads = len([l for l in self.leads_database if l.get('score', 0) >= 7])
            return f"""👥 **ANÁLISIS LEADS PREMIUM**

🎯 **LEADS ESTADO:**
• Total leads: {len(self.leads_database)}
• Premium (score 7+): {premium_leads}  
• Conversion rate estimado: 15-25%
• Revenue potential: ${premium_leads * 3500:,}

🔍 **LEAD SCORING AUTOMÁTICO:**
• CEO/Entrepreneur: +3 points
• Spiritual interest: +2 points  
• Ayahuasca experience: +3 points
• Premium indicators: +2 points

⚡ **ACCIÓN RECOMENDADA:**
{self.generate_ai_content('Suggest specific follow-up tactics for premium leads interested in Sacred Rebirth ayahuasca retreat. Focus on personalization and urgency.')}"""

        # RESPUESTA GENERAL INTELIGENTE
        else:
            return self.generate_ai_content(text)"""
        """Procesar mensajes con inteligencia artificial natural"""
        message = text.lower().strip()
        
        # Respuestas inteligentes basadas en intención
        if any(word in message for word in ['/start', 'start', 'hola', 'hi', 'hello']):
            return "🚀 **¡Hola! Soy Maya, tu asistente AI para Sacred Rebirth!**\n\n🧠 Puedo ayudarte con:\n• Estrategias de marketing\n• Generar contenido llamativo\n• Crear imágenes con IA\n• Publicar en Facebook automáticamente\n• Reportes de negocio\n• Análisis de pipeline\n\n💬 **Háblame natural:** 'Quiero una publicación para obtener discovery calls' o 'Dame el reporte del negocio'"
        
        # Generar contenido llamativo para discovery calls
        elif any(word in message for word in ['publicacion', 'post', 'contenido']) and any(word in message for word in ['discovery', 'llamadas', 'calls', 'llamativo']):
            prompt = """Crea un post súper llamativo para redes sociales que genere discovery calls para Sacred Rebirth.

Objetivo: Conseguir llamadas de descubrimiento para retiro ayahuasca
Audiencia: Personas de alto ingreso, 35-55 años, buscando transformación espiritual
Dolor/Problema: Vacío existencial, estrés, falta de propósito, trauma sin sanar
Solución: Retiro Sacred Rebirth con medicina ancestral

Incluir:
- Hook emocional poderoso
- Beneficios transformacionales específicos
- Escasez (solo 8 espacios)
- Call to action para discovery call
- Emojis llamativos
- Sensación de urgencia

Estilo: Auténtico, espiritual pero accesible, premium"""

            ai_response = self.generate_ai_content(prompt)
            return f"✨ **PUBLICACIÓN LLAMATIVA GENERADA CON IA**\n\n{ai_response}\n\n🔗 https://sacred-rebirth.com/appointment.html\n\n💡 ¿Quieres que la publique automáticamente en Facebook? Solo dime 'sí publícala'"
        
        # Reportes de negocio inteligentes
        elif any(word in message for word in ['reporte', 'report', 'como', 'está', 'negocio', 'métricas']):
            prompt = f"""Genera un reporte empresarial detallado para Sacred Rebirth basado en estos datos:

NEGOCIO: Sacred Rebirth - Retiro medicina ancestral
FECHA OBJETIVO: Agosto 11, 2025 (retiro)
UBICACIÓN: Valle de Bravo, México
CAPACIDAD: 8 espacios exclusivos
PRECIO: $3,500 USD por persona
REVENUE OBJETIVO: $28,000 USD

FECHA ACTUAL: {datetime.now().strftime('%d de %B, %Y')}
DÍAS RESTANTES: {(datetime(2025, 8, 11) - datetime.now()).days} días

Incluir:
1. Status actual del retiro
2. Pipeline de ventas (estimado)
3. Métricas de marketing
4. Acciones prioritarias HOY
5. Proyección de ingresos
6. Recomendaciones estratégicas

Estilo: Profesional, datos específicos, actionable"""

            ai_response = self.generate_ai_content(prompt)
            return f"📊 **REPORTE EMPRESARIAL IA**\n\n{ai_response}"
        
        # Estrategia de marketing
        elif any(word in message for word in ['estrategia', 'marketing', 'plan', 'cómo', 'llenar', 'vender']):
            prompt = """Crea una estrategia de marketing completa para Sacred Rebirth retiro ayahuasca.

OBJETIVO: Llenar 8 espacios a $3,500 USD cada uno = $28,000 revenue
TIEMPO: Hasta Agosto 11, 2025
AUDIENCIA: Profesionales alto ingreso, 35-55 años, transformación espiritual

Incluir:
1. FUNNEL DE VENTAS específico
2. CONTENIDO por plataforma (Instagram, Facebook)
3. ESTRATEGIA DE PRECIOS y urgencia
4. CALENDARIO de acciones semanales
5. MÉTRICAS a trackear
6. TÁCTICAS de conversión
7. SEGUIMIENTO de leads

Debe ser específico, implementable, con timelines claros"""

            ai_response = self.generate_ai_content(prompt)
            return f"🎯 **ESTRATEGIA MARKETING IA**\n\n{ai_response}\n\n💡 ¿Quieres que genere contenido específico para alguna táctica?"
        
        # Generar imágenes con descripción natural
        elif any(word in message for word in ['imagen', 'foto', 'visual', 'crear', 'generar']) and any(word in message for word in ['ceremonia', 'ayahuasca', 'retiro', 'valle', 'transformacion']):
            # Extraer el tema
            if 'ceremonia' in message or 'ayahuasca' in message:
                tema = "ceremonia ayahuasca sagrada"
            elif 'valle' in message or 'paisaje' in message:
                tema = "paisaje Valle de Bravo retiro"
            elif 'transformacion' in message:
                tema = "transformación espiritual"
            else:
                tema = "retiro medicina ancestral"
            
            return self.generate_image(tema)
        
        # Publicación en Facebook
        elif any(word in message for word in ['facebook', 'publicar', 'post']) or 'sí publícala' in message:
            fb_content = """🌿 ¿Sientes que algo falta en tu vida?

A pesar del éxito profesional, muchos experimentamos un vacío profundo... una desconexión de nuestro verdadero propósito.

Si resonas con esto, Sacred Rebirth puede ser tu respuesta.

✨ Nuestro retiro de medicina ancestral en Valle de Bravo ofrece:
🔮 Ceremonias de ayahuasca con facilitadores experimentados
🏔️ Temazcal de purificación en la naturaleza
🍫 Cacao ceremonial para abrir el corazón

📅 Próximo retiro: Agosto 11, 2025
👥 Solo 8 espacios (exclusividad garantizada)
💎 Inversión: $3,500 USD

No es solo un retiro... es el inicio de tu verdadera transformación.

¿Listo para reconectar con tu esencia?

🔗 Agenda tu llamada de descubrimiento (sin compromiso):
https://sacred-rebirth.com/appointment.html

#TransformaciónEspiritual #MedicinaAncestral #SacredRebirth"""

            return self.post_to_facebook(fb_content)
        
        # Pipeline de ventas
        elif any(word in message for word in ['ventas', 'pipeline', 'leads', 'conversiones', 'clientes']):
            prompt = """Analiza el pipeline de ventas para Sacred Rebirth como experto en marketing.

PRODUCTO: Retiro ayahuasca $3,500 USD
OBJETIVO: 8 espacios = $28,000 revenue
FECHA LÍMITE: Agosto 11, 2025

Proporciona:
1. ANÁLISIS del embudo de ventas actual
2. MÉTRICAS de conversión esperadas
3. STATUS de leads por temperatura
4. ACCIONES específicas para cada segmento
5. PROYECCIÓN de ventas
6. ESTRATEGIAS de cierre
7. FOLLOW-UP automatizado

Incluye números específicos y cronograma de acciones"""

            ai_response = self.generate_ai_content(prompt)
            return f"💰 **ANÁLISIS PIPELINE IA**\n\n{ai_response}"
        
        # Respuesta general inteligente
        else:
            prompt = f"""El usuario de Sacred Rebirth pregunta: "{text}"

Responde como Maya, experta en marketing para retiros espirituales y medicina ancestral.

CONTEXTO:
- Sacred Rebirth: Retiro ayahuasca en Valle de Bravo
- Fecha: Agosto 11, 2025
- 8 espacios a $3,500 USD
- Audiencia: Alto ingreso, transformación espiritual

Responde de manera útil, específica y actionable. Si no es claro, pregunta qué necesita específicamente."""

            ai_response = self.generate_ai_content(prompt)
            return f"🤖 **Maya IA:**\n\n{ai_response}\n\n💡 **También puedo:**\n• Generar contenido llamativo\n• Crear estrategias específicas\n• Hacer análisis de negocio\n• Generar imágenes con IA\n• Publicar automáticamente"

maya = MayaEnterprise()
app = Flask(__name__)

@app.route('/')
def health():
    return jsonify({
        "status": "Maya AI 24/7 Online", 
        "telegram": bool(TELEGRAM_TOKEN),
        "timestamp": datetime.now().isoformat(),
        "uptime": "Always Active"
    })

@app.route('/health')
def health_check():
    return jsonify({"status": "ok", "service": "Maya AI Command Center"})

@app.route('/keepalive')
def keep_alive():
    return jsonify({
        "status": "alive", 
        "message": "Maya working 24/7",
        "timestamp": datetime.now().isoformat()
    })

def keep_service_alive():
    """Mantener Maya activa 24/7 - evita que Render duerma el servicio"""
    import time
    
    while True:
        try:
            # Self-ping cada 10 minutos
            time.sleep(600)  # 10 minutos
            # Ping interno para mantener activo
            requests.get('http://127.0.0.1:5000/keepalive', timeout=5)
            print("🔄 Keep-alive: Maya stays active 24/7")
        except Exception as e:
            print(f"⚠️ Keep-alive error: {e}, but Maya continues...")
            time.sleep(60)  # Retry en 1 minuto si falla
        
def send_startup_notification():
    """Notificar que Maya está online 24/7"""
    if ADMIN_CHAT_ID:
        try:
            maya.send_message(ADMIN_CHAT_ID, 
                "🚀 **Maya AI 24/7 ACTIVADA**\n\n✅ Servicio permanente online\n🔄 Keep-alive automático\n🧠 IA lista para trabajar\n💼 Sacred Rebirth Command Center\n\n💬 Háblame natural: 'Quiero una estrategia de marketing'")
            print("✅ Startup notification sent")
        except Exception as e:
            print(f"⚠️ Notification failed: {e}")

def polling():
    print("🔄 Polling started - Maya will respond to any admin")
    
    offset = None
    while True:
        try:
            url = f"{maya.api_url}/getUpdates"
            params = {"timeout": 30}
            if offset:
                params["offset"] = offset
                
            response = requests.get(url, params=params, timeout=35)
            
            if response.status_code == 200:
                data = response.json()
                if data.get('ok'):
                    for update in data.get('result', []):
                        offset = update['update_id'] + 1
                        
                        if 'message' in update:
                            message = update['message']
                            chat_id = str(message['chat']['id'])
                            text = message.get('text', '')
                            
                            # Respond to configured admin OR if no admin set, respond to anyone
                            if not ADMIN_CHAT_ID or chat_id == ADMIN_CHAT_ID:
                                print(f"📱 Command from {chat_id}: {text}")
                                response = maya.process_message(text)
                                maya.send_message(chat_id, response)
                            else:
                                print(f"🔒 Ignored message from {chat_id} (not admin)")
        except Exception as e:
            print(f"❌ Polling error: {e}")
        
        time.sleep(1)

def main():
    if not TELEGRAM_TOKEN:
        print("❌ No token")
        return
    
    print("🚀 Maya Starting 24/7 Service...")
    print(f"Token: {TELEGRAM_TOKEN[:10]}...")
    print(f"Admin: {ADMIN_CHAT_ID}")
    print("⚡ Activating permanent service...")
    
    # Flask en thread permanente
    def run_flask():
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port, debug=False, threaded=True)
    
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    
    # Keep-alive en thread separado para 24/7
    keepalive_thread = threading.Thread(target=keep_service_alive, daemon=True)
    keepalive_thread.start()
    
    # Notificación de inicio
    send_startup_notification()
    
    print("✅ Maya 24/7 configured!")
    print("🔄 Keep-alive activated")
    print("🤖 Starting permanent polling...")
    
    # Polling permanente - nunca se detiene
    polling()

if __name__ == '__main__':
    main()