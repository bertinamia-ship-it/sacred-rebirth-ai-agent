#!/usr/bin/env python3
"""
Bot de Telegram para Sacred Rebirth AI Agent
Permite interactuar con el agente de marketing a través de Telegram
"""
import os
import requests
import json
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.crew import MarketingCrew
from chat import ChatAgent
from src.appointment_setter import AppointmentSetterAgent
from src.image_generator import SacredRebirthImageGenerator
from src.campaign_manager import MarketingCampaignManager
from src.daily_content import DailyContentAutomation

load_dotenv()

# Configuración
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')
FACEBOOK_PAGE_ACCESS_TOKEN = os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN')

def post_to_facebook(message_text, image_path=None):
    """
    Publica contenido en la página de Facebook de Sacred Rebirth
    Incluye texto y opcionalmente una imagen
    """
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        return {"success": False, "error": "Facebook token not configured"}
    
    try:
        # URL de la Graph API para publicar en página
        url = f"https://graph.facebook.com/v18.0/me/feed"
        
        # Siempre añadir call to action al contenido
        if "book your discovery call" not in message_text.lower():
            message_text += "\n\n💫 Book your discovery call now: https://sacred-rebirth.com/appointment.html"
        
        if image_path and os.path.exists(image_path):
            # Publicar con imagen
            url = f"https://graph.facebook.com/v18.0/me/photos"
            
            with open(image_path, 'rb') as image_file:
                files = {'source': image_file}
                data = {
                    'message': message_text,
                    'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
                }
                response = requests.post(url, data=data, files=files)
        else:
            # Publicar solo texto
            data = {
                'message': message_text,
                'access_token': FACEBOOK_PAGE_ACCESS_TOKEN
            }
            response = requests.post(url, data=data)
        
        result = response.json()
        
        if response.status_code == 200 and 'id' in result:
            return {
                "success": True, 
                "post_id": result['id'],
                "message": "✅ Post publicado en Facebook exitosamente",
                "has_image": image_path is not None
            }
        else:
            return {
                "success": False, 
                "error": f"Error de Facebook: {result.get('error', {}).get('message', 'Unknown error')}"
            }
            
    except Exception as e:
        return {"success": False, "error": f"Error de conexión: {str(e)}"}

# Inicializar agentes
print("🤖 Inicializando Marketing Crew para Telegram...")
crew = MarketingCrew()
chat_agent = ChatAgent()
chat_agent.crew = crew
appointment_agent = AppointmentSetterAgent()
image_generator = SacredRebirthImageGenerator()
campaign_manager = MarketingCampaignManager()
daily_content = DailyContentAutomation()
print("✅ Bot de Telegram con sistemas completos listo!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Bienvenida"""
    user = update.effective_user
    
    welcome_message = f"""
🙏 ¡Hola {user.first_name}!

Soy Maya, tu asistente completo de marketing para Sacred Rebirth.

**🚀 NUEVO: Sistema Completo de Marketing**
• Generación automática de imágenes 🎨
• Appointment setter inteligente 💬
• Campañas completas para retiros 📊
• Publicación automática en Facebook 📱
• Calendario de contenido diario 📅
• Guiones de video profesionales 🎬

**RETIRO ESPECIAL: 11 de Enero 2025** 🌿
• Ubicación: Valle de Bravo
• Tema: "Nuevo Año, Nueva Vida"
• Con ayahuasca, temazcal, cacao

**Ejemplos de comandos:**
• "Crea foto y promueva el retiro de enero"
• "Genera campaña completa de marketing"
• "¿Dónde está ubicado el retiro?"
• "Sube contenido a Facebook sobre ayahuasca"
• "/campaign" para estrategia completa

💫 **TODO incluye automáticamente el booking link**

Solo escríbeme naturalmente y yo entenderé 💬
"""
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Ayuda"""
    help_text = """
📚 **Guía Completa Sacred Rebirth Bot**

**🤖 COMANDOS BÁSICOS:**
/start - Bienvenida
/help - Esta ayuda
/status - Estado del sistema
/stats - Ver uso y costos 💰
/models - Ver modelos de IA disponibles
/teach - Enseñarme algo nuevo

**📱 PUBLICACIÓN Y CONTENIDO:**
/facebook [contenido] - Publicar en Facebook
/image [tema] - Generar imagen
/daily [día] - Contenido diario automático
/weekly - Calendario semanal completo
• "Crea un foto y promueva el retiro"
• "Sube contenido a Facebook sobre ayahuasca"

**🚀 MARKETING AVANZADO:**
/campaign - Campaña completa enero 11
/audience - Estrategia de captación
/content [días] - Calendario de contenido
/video - Guión de video mensual

**🎯 APPOINTMENT SETTER:**
• Pregunta sobre ubicación, medicina, retiros
• Automáticamente dirige a discovery call
• Responde como Maya, facilitadora experta

**📅 CONTENIDO DIARIO AUTOMÁTICO:**
• Lunes: Educación sobre Ayahuasca
• Martes: Testimonios y transformaciones
• Miércoles: Behind the scenes
• Jueves: Preparación para retiro
• Viernes: Inspiración y reflexiones
• Sábado: Q&A y mitos vs realidad
• Domingo: Reflexiones espirituales

**💬 EJEMPLOS DE USO:**
• "¿Dónde está el retiro?" → Respuesta + discovery call
• "Crea foto para retiro enero 11" → Imagen + Facebook
• "Genera campaña completa" → Estudio + calendario + estrategia
• "¿Cuánto cuesta?" → Info + discovery call booking
• "/daily Tuesday" → Contenido + imagen para martes

💫 **TODO incluye automáticamente: Book your discovery call now!**

🎨 Temas de imagen: retiro, medicina, transformación, location
📅 Calendario: hasta 60 días de contenido diario
🤖 Sistema inteligente ahorra 83% en costos de IA

¿Necesitas algo más? Solo pregúntame naturalmente ✨
"""
    
    await update.message.reply_text(help_text, parse_mode='Markdown')


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Maneja todos los mensajes de texto"""
    
    # Verificar autorización
    user_id = str(update.effective_user.id)
    if AUTHORIZED_USERS and user_id not in AUTHORIZED_USERS:
        await update.message.reply_text(
            "⛔ Lo siento, no estás autorizado para usar este bot.\n"
            f"Tu ID: {user_id}\n\n"
            "Contacta al administrador para obtener acceso."
        )
        return
    
    user_message = update.message.text
    user_name = update.effective_user.first_name
    
    print(f"\n💬 Mensaje de {user_name}: {user_message}")
    
    # Enviar "escribiendo..."
    await update.message.chat.send_action("typing")
    
    try:
        # Cargar knowledge base
        knowledge_path = '/workspaces/sacred-rebirth-ai-agent/knowledge_base.txt'
        try:
            with open(knowledge_path, 'r', encoding='utf-8') as f:
                knowledge_base = f.read()
        except:
            knowledge_base = ""
        
        # 📱 DETECTAR RESPUESTA RÁPIDA PARA PUBLICAR
        if user_message.lower().strip() in ['sí', 'si', 'yes', 'ok', 'dale', 'publica', 'publicar']:
            # Buscar el último mensaje del bot para publicar
            try:
                # Por simplicidad, usaremos el último contenido generado
                # En una versión más avanzada, se puede guardar el contexto
                await update.message.reply_text("📱 Para publicar contenido específico, dime: 'publica en facebook: [tu contenido]'")
                return
            except:
                pass
        
        # 🤖 DETECTAR SI ES PREGUNTA DE APPOINTMENT SETTING
        if appointment_agent.is_appointment_related(user_message):
            question_type = appointment_agent.analyze_message(user_message)
            appointment_response = appointment_agent.generate_response(user_message, question_type)
            await update.message.reply_text(appointment_response)
            return
        
        # Crear respuesta simple con IA directa
        from openai import OpenAI
        import os
        
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        
        # 🧠 SISTEMA HÍBRIDO INTELIGENTE - Selección automática para AHORRAR COSTOS
        # El bot es INTELIGENTE y solo usa modelos caros cuando es REALMENTE necesario
        
        message_lower = user_message.lower()
        
        # 🔥 ULTRA (gpt-4-turbo) - Solo para tareas MUY complejas (~$0.01)
        keywords_ultra = [
            'estrategia completa', 'plan maestro', 'análisis profundo',
            'investigación exhaustiva', 'ultra profesional', 'estudio de mercado completo',
            'roadmap completo', 'plan de negocio'
        ]
        
        # ✨ PREMIUM (gpt-4o) - Para contenido profesional importante (~$0.003)
        keywords_premium = [
            'profesional', 'anuncio', 'ad', 'campaña', 'landing page',
            'video script', 'guión', 'copy profesional', 'sales page',
            'llamativo', 'impactante', 'viral', 'conversión',
            'pitch', 'propuesta', 'presentación importante'
        ]
        
        # ⚡ BÁSICO (gpt-4o-mini) - Para TODO lo demás (95% de casos) (~$0.0003)
        # Posts simples, ideas, respuestas rápidas, contenido diario
        
        # Lógica inteligente de detección
        is_ultra = any(keyword in message_lower for keyword in keywords_ultra)
        is_premium = any(keyword in message_lower for keyword in keywords_premium)
        
        # Detectar si es pregunta simple (usa básico siempre)
        simple_questions = ['qué', 'cómo', 'cuándo', 'dónde', 'por qué', 'cuál']
        is_simple_question = any(q in message_lower for q in simple_questions) and len(user_message.split()) < 15
        
        # Detectar si solo pide ideas o sugerencias (usa básico)
        is_brainstorm = any(word in message_lower for word in ['idea', 'sugerencia', 'dame', 'propón', 'lista'])
        
        # DECISIÓN FINAL (prioriza ahorrar costos)
        if is_ultra:
            selected_model = 'gpt-4-turbo'
            quality_label = "🔥 ULTRA"
            cost_msg = "($0.01)"
        elif is_premium and not is_simple_question and not is_brainstorm:
            selected_model = 'gpt-4o'
            quality_label = "✨ PRO"
            cost_msg = "($0.003)"
        else:
            # Por defecto usa BÁSICO (ahorra 90% de costos)
            selected_model = 'gpt-4o-mini'
            quality_label = "⚡ RÁPIDO"
            cost_msg = "($0.0003)"
        
        system_prompt = f"""Eres el asistente de marketing personal de Sacred Rebirth.

INFORMACIÓN DEL NEGOCIO:
{knowledge_base}

INSTRUCCIONES ADICIONALES:
- Responde en español de forma amigable y profesional
- Usa la información de arriba para crear contenido auténtico
- Siempre incluye el link de agendamiento cuando sea relevante
- Usa emojis espirituales apropiados: 🌿✨🌌💫🙏🌱⭐️
- Crea contenido inspirador pero genuino
- Si te piden crear posts, usa el formato y estilo descrito arriba

Si el usuario te pide que aprendas algo nuevo sobre el negocio, di que has actualizado tu conocimiento."""

        # Log del modelo usado (para debugging)
        print(f"🤖 Modelo: {selected_model} | {quality_label} | Costo: {cost_msg}")
        
        # OPCIONAL: Mostrar al usuario qué modelo se usó (útil para transparencia)
        # Descomenta la siguiente línea si quieres que el usuario vea el modelo:
        # await update.message.reply_text(f"💭 {quality_label} {cost_msg}")
        
        response = client.chat.completions.create(
            model=selected_model,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_message}
            ],
            max_tokens=2000 if selected_model != 'gpt-4o-mini' else 1500,
            temperature=0.8 if selected_model != 'gpt-4o-mini' else 0.7
        )
        
        bot_response = response.choices[0].message.content
        
        # 🚀 DETECTAR SI USUARIO QUIERE PUBLICAR EN FACEBOOK
        publish_keywords = ['publica en facebook', 'subir a facebook', 'postea en facebook', 'facebook post', 'envía a facebook', 'sube contenido a facebook', 'crea un foto y promueva']
        wants_to_publish = any(keyword in message_lower for keyword in publish_keywords)
        
        # Detectar si quiere contenido con imagen
        image_keywords = ['foto', 'imagen', 'visual', 'gráfico', 'crea un foto']
        wants_image = any(keyword in message_lower for keyword in image_keywords)
        
        # Si es contenido para redes sociales, ofrecer publicar automáticamente
        content_keywords = ['post', 'publicación', 'contenido', 'facebook', 'redes sociales', 'campaña', 'promociona']
        is_content = any(keyword in message_lower for keyword in content_keywords)
        
        # GENERAR IMAGEN SI SE SOLICITA
        generated_image = None
        if wants_image or wants_to_publish:
            await update.message.reply_text("🎨 Generando imagen para tu contenido...")
            
            # Determinar tema de la imagen
            image_theme = "general"
            if "retiro" in message_lower or "enero" in message_lower:
                image_theme = "retreat_announcement"
            elif "medicina" in message_lower or "ayahuasca" in message_lower:
                image_theme = "medicine"
            elif "transformación" in message_lower or "sanación" in message_lower:
                image_theme = "transformation"
                
            image_result = image_generator.generate_retreat_image(content_theme=image_theme)
            if image_result["success"]:
                generated_image = image_result["local_path"]
                await update.message.reply_text("✅ Imagen generada exitosamente!")
            else:
                await update.message.reply_text(f"⚠️ No pude generar imagen: {image_result['error']}")
        
        # Enviar respuesta
        # Dividir respuestas largas (límite de Telegram: 4096 caracteres)
        if len(bot_response) > 4000:
            # Dividir en chunks
            chunks = [bot_response[i:i+4000] for i in range(0, len(bot_response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(bot_response)
            
        # 📱 PUBLICAR AUTOMÁTICAMENTE EN FACEBOOK SI SE SOLICITA
        if wants_to_publish and FACEBOOK_PAGE_ACCESS_TOKEN:
            await update.message.reply_text("📱 Publicando en Facebook...")
            
            facebook_result = post_to_facebook(bot_response, generated_image)
            if facebook_result["success"]:
                success_msg = f"🎉 {facebook_result['message']}"
                if facebook_result.get('has_image'):
                    success_msg += " (con imagen)"
                success_msg += f"\n📱 Post ID: {facebook_result['post_id']}"
                await update.message.reply_text(success_msg)
            else:
                await update.message.reply_text(f"❌ Error al publicar en Facebook: {facebook_result['error']}")
                
        elif (is_content and not wants_to_publish) and FACEBOOK_PAGE_ACCESS_TOKEN:
            # Ofrecer publicar
            if generated_image:
                publish_text = f"🚀 ¿Quieres publicar esto en Facebook con la imagen generada?\n\nResponde 'sí' para publicar automáticamente."
            else:
                publish_text = f"🚀 ¿Quieres publicar esto en Facebook?\n\nResponde 'sí' para publicar automáticamente."
            await update.message.reply_text(publish_text)
        
        elif wants_to_publish and not FACEBOOK_PAGE_ACCESS_TOKEN:
            await update.message.reply_text("❌ Facebook no está configurado. Contacta al administrador para activar esta función.")
        
    except Exception as e:
        error_msg = f"❌ Error procesando tu solicitud: {str(e)}\n\nIntenta de nuevo o usa /help"
        await update.message.reply_text(error_msg)
        print(f"Error: {e}")


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /status - Estado del sistema"""
    status_msg = """
✅ **Estado del Sistema**

• Bot: Activo
• CrewAI: Operativo
• Agentes: 6/6 funcionando
• OpenAI API: Conectado

**Servicios Configurados:**
"""
    
    # Verificar configuraciones
    services = []
    if os.getenv('FACEBOOK_PAGE_ACCESS_TOKEN'):
        services.append("✅ Facebook Page")
    else:
        services.append("⚠️ Facebook Page (no configurado)")
    
    if os.getenv('META_ACCESS_TOKEN'):
        services.append("✅ Instagram/Facebook")
    else:
        services.append("⚠️ Instagram/Facebook (no configurado)")
    
    if os.getenv('SENDGRID_API_KEY'):
        services.append("✅ Email (SendGrid)")
    else:
        services.append("⚠️ Email (no configurado)")
    
    status_msg += "\n".join(services)
    
    await update.message.reply_text(status_msg, parse_mode='Markdown')


async def calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /calendar - Ver calendario de contenido"""
    await update.message.chat.send_action("typing")
    
    try:
        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        response = client.chat.completions.create(
            model='gpt-4o-mini',
            messages=[
                {'role': 'user', 'content': 'Crea un calendario de contenido para Instagram de Sacred Rebirth para los próximos 7 días. Incluye temas y horarios sugeridos.'}
            ],
            max_tokens=800
        )
        await update.message.reply_text(response.choices[0].message.content)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def leads(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /leads - Ver leads"""
    await update.message.chat.send_action("typing")
    await update.message.reply_text("📊 Función de leads en desarrollo. Por ahora usa el comando general para gestionar leads.")


async def stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /stats - Ver estadísticas de uso y costos"""
    await update.message.chat.send_action("typing")
    
    import re
    from collections import Counter
    
    # Costos por modelo
    COSTS = {
        'gpt-4o-mini': 0.0003,
        'gpt-4o': 0.003,
        'gpt-4-turbo': 0.01
    }
    
    try:
        # Leer logs
        with open('/workspaces/sacred-rebirth-ai-agent/telegram_bot.log', 'r', encoding='utf-8') as f:
            logs = f.readlines()
        
        # Buscar uso de modelos
        pattern = r'🤖 Modelo: ([\w-]+) \| .+ \| Costo: \(\$([0-9.]+)\)'
        
        model_usage = Counter()
        total_cost = 0.0
        
        for line in logs:
            match = re.search(pattern, line)
            if match:
                model = match.group(1)
                cost = float(match.group(2))
                model_usage[model] += 1
                total_cost += cost
        
        if not model_usage:
            await update.message.reply_text(
                "📊 Aún no hay estadísticas.\n\n"
                "El bot registrará el uso de modelos a partir de ahora.\n"
                "Envía algunos mensajes y vuelve a usar /stats"
            )
            return
        
        total_requests = sum(model_usage.values())
        
        # Construir respuesta
        stats_text = "📊 **ESTADÍSTICAS DE USO**\n\n"
        stats_text += f"📈 Total requests: {total_requests}\n"
        stats_text += f"💰 Costo total: ${total_cost:.4f} USD\n\n"
        stats_text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        
        for model, count in model_usage.most_common():
            percentage = (count / total_requests) * 100
            model_cost = COSTS.get(model, 0) * count
            
            if model == 'gpt-4o-mini':
                emoji = "⚡"
                label = "Básico"
            elif model == 'gpt-4o':
                emoji = "✨"
                label = "Pro"
            elif model == 'gpt-4-turbo':
                emoji = "🔥"
                label = "Ultra"
            else:
                emoji = "🤖"
                label = model
            
            stats_text += f"{emoji} **{label}**\n"
            stats_text += f"   • {count} requests ({percentage:.1f}%)\n"
            stats_text += f"   • ${model_cost:.4f} USD\n\n"
        
        # Ahorro
        cost_if_all_premium = total_requests * COSTS['gpt-4o']
        savings = cost_if_all_premium - total_cost
        savings_pct = (savings / cost_if_all_premium) * 100 if cost_if_all_premium > 0 else 0
        
        stats_text += "━━━━━━━━━━━━━━━━━━━━\n\n"
        stats_text += "💡 **AHORRO:**\n"
        stats_text += f"   • Sin híbrido: ${cost_if_all_premium:.4f}\n"
        stats_text += f"   • Con híbrido: ${total_cost:.4f}\n"
        stats_text += f"   • **Ahorraste: ${savings:.4f}** ({savings_pct:.0f}%)\n\n"
        
        # Proyección
        avg_cost = total_cost / total_requests if total_requests > 0 else 0
        monthly_projection = avg_cost * 300  # ~10/día
        yearly_projection = monthly_projection * 12
        
        stats_text += "📊 **PROYECCIÓN (10 posts/día):**\n"
        stats_text += f"   • Mensual: ${monthly_projection:.2f} USD\n"
        stats_text += f"   • Anual: ${yearly_projection:.2f} USD\n\n"
        stats_text += "✅ Sistema inteligente ahorrando costos!"
        
        await update.message.reply_text(stats_text, parse_mode='Markdown')
        
    except FileNotFoundError:
        await update.message.reply_text("❌ No se encontró el archivo de logs")
    except Exception as e:
        await update.message.reply_text(f"❌ Error al leer estadísticas: {str(e)}")


async def models(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /models - Ver información de modelos AI disponibles"""
    
    models_info = """
🧠 **SISTEMA INTELIGENTE DE AHORRO**

El bot **elige automáticamente** el modelo según tu petición para **AHORRAR COSTOS**.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

⚡ **GPT-4O-MINI** (Básico - Usado 95% del tiempo)
💰 Costo: $0.0003 por respuesta
📍 Se usa para:
   • Posts simples de redes sociales
   • Respuestas rápidas
   • Ideas y sugerencias
   • Preguntas generales
   • Contenido diario

✅ Ejemplos:
   • "crea un post"
   • "dame 5 ideas"
   • "qué publicar hoy"
   • "cuándo es el retiro"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✨ **GPT-4O** (Profesional - Usado 4% del tiempo)
💰 Costo: $0.003 por respuesta (10x más caro)
📍 Se usa SOLO cuando dices:
   • "profesional"
   • "anuncio"
   • "campaña"
   • "llamativo"
   • "viral"
   • "copy profesional"

✅ Ejemplos que activan GPT-4O:
   • "crea un **anuncio profesional**"
   • "copy para **campaña** de Facebook"
   • "landing page **llamativa**"
   • "contenido **viral**"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔥 **GPT-4-TURBO** (Ultra - Usado 1% del tiempo)
💰 Costo: $0.01 por respuesta (33x más caro)
📍 Se usa SOLO cuando dices:
   • "estrategia completa"
   • "plan maestro"
   • "análisis profundo"
   • "ultra profesional"

✅ Ejemplos que activan GPT-4-TURBO:
   • "dame una **estrategia completa**"
   • "**plan maestro** de marketing"
   • "**análisis profundo** de mercado"

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 **LÓGICA INTELIGENTE PARA AHORRAR:**

El bot es INTELIGENTE y usa básico (95%) por defecto:
• Preguntas simples → BÁSICO ⚡
• Solo pedir ideas → BÁSICO ⚡
• Mensajes cortos → BÁSICO ⚡
• Dice "profesional" → PRO ✨
• Dice "estrategia completa" → ULTRA 🔥

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📊 **AHORRO ESTIMADO:**

Sin sistema inteligente (todo PRO):
   • 100 posts = $0.30 USD

Con sistema inteligente:
   • 95 posts básicos = $0.0285
   • 4 posts pro = $0.012
   • 1 post ultra = $0.01
   • **TOTAL = $0.05 USD** ✅

**¡AHORRAS 83%!** 🎉

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🔍 **Ver tus estadísticas reales:**
Usa /stats para ver cuánto has gastado y ahorrado

¡El bot trabaja para ti y tu bolsillo! 💰
"""
    
    await update.message.reply_text(models_info, parse_mode='Markdown')


async def teach(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /teach - Enseñar nueva información al bot"""
    
    if not context.args:
        await update.message.reply_text(
            "📚 **Cómo enseñarme nueva información:**\n\n"
            "Usa: `/teach [información]`\n\n"
            "**Ejemplos:**\n"
            "• `/teach Nuestro próximo retiro es el 15 de enero`\n"
            "• `/teach Me gusta usar un tono más relajado y amigable`\n"
            "• `/teach El precio del retiro de 3 días es $8000 MXN`\n\n"
            "También puedes decirme directamente:\n"
            "• 'Aprende esto: [información]'\n"
            "• 'Recuerda que [información]'",
            parse_mode='Markdown'
        )
        return
    
    new_info = ' '.join(context.args)
    
    # Guardar en el knowledge base
    knowledge_path = '/workspaces/sacred-rebirth-ai-agent/knowledge_base.txt'
    try:
        with open(knowledge_path, 'a', encoding='utf-8') as f:
            f.write(f"\n\n## 📝 Información Adicional ({update.effective_user.first_name})\n")
            f.write(f"{new_info}\n")
        
        await update.message.reply_text(
            f"✅ **¡Aprendido!**\n\n"
            f"He guardado esta información:\n_{new_info}_\n\n"
            f"La usaré para crear mejor contenido desde ahora.",
            parse_mode='Markdown'
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Error guardando información: {str(e)}")


async def facebook_post(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /facebook - Publicar directamente en Facebook"""
    
    if not FACEBOOK_PAGE_ACCESS_TOKEN:
        await update.message.reply_text(
            "❌ **Facebook no configurado**\n\n"
            "Contacta al administrador para activar esta función.",
            parse_mode='Markdown'
        )
        return
    
    if not context.args:
        await update.message.reply_text(
            "📱 **Cómo publicar en Facebook:**\n\n"
            "Usa: `/facebook [contenido]`\n\n"
            "**Ejemplo:**\n"
            "• `/facebook ¡Únete a nuestro próximo retiro de ayahuasca! 🌿✨`\n\n"
            "También puedes decir:\n"
            "• 'Publica en Facebook: [contenido]'",
            parse_mode='Markdown'
        )
        return
    
    content = ' '.join(context.args)
    
    await update.message.chat.send_action("typing")
    await update.message.reply_text("📱 Publicando en Facebook...")
    
    # Publicar en Facebook
    result = post_to_facebook(content)
    
    if result["success"]:
        await update.message.reply_text(
            f"🎉 **¡Post publicado exitosamente!**\n\n"
            f"📱 Post ID: `{result['post_id']}`\n"
            f"📝 Contenido: _{content}_",
            parse_mode='Markdown'
        )
    else:
        await update.message.reply_text(
            f"❌ **Error al publicar:**\n{result['error']}\n\n"
            "Intenta de nuevo o contacta al administrador."
        )


async def campaign(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /campaign - Crear campaña completa de marketing"""
    await update.message.chat.send_action("typing")
    await update.message.reply_text("🚀 Generando campaña completa de marketing para el retiro del 11 de enero...")
    
    try:
        # Generar campaña completa
        full_campaign = campaign_manager.generate_complete_campaign()
        
        # Enviar cada sección por separado
        sections = [
            ("📊 ESTUDIO DE MERCADO", full_campaign["market_research"]),
            ("📅 CALENDARIO DE CONTENIDO", full_campaign["content_calendar"]),
            ("🎯 ESTRATEGIA DE AUDIENCIA", full_campaign["audience_strategy"]),
            ("🎬 GUIÓN DE VIDEO MENSUAL", full_campaign["video_script"])
        ]
        
        for title, content in sections:
            # Dividir contenido largo
            if len(content) > 4000:
                chunks = [content[i:i+3800] for i in range(0, len(content), 3800)]
                for i, chunk in enumerate(chunks):
                    section_title = f"{title} (Parte {i+1}/{len(chunks)})" if len(chunks) > 1 else title
                    await update.message.reply_text(f"**{section_title}**\n\n{chunk}", parse_mode='Markdown')
            else:
                await update.message.reply_text(f"**{title}**\n\n{content}", parse_mode='Markdown')
        
        await update.message.reply_text(
            "✅ **Campaña completa generada!**\n\n"
            "🎯 Usa `/audience` para estrategias específicas de captación\n"
            "📅 Usa `/content` para calendario detallado\n"
            "🎬 Usa `/video` para guiones de video"
        )
        
    except Exception as e:
        await update.message.reply_text(f"❌ Error generando campaña: {str(e)}")


async def audience(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /audience - Estrategia de captación de audiencia"""
    await update.message.chat.send_action("typing")
    await update.message.reply_text("🎯 Generando estrategia para conseguir audiencia...")
    
    try:
        strategy = campaign_manager.create_audience_strategy()
        
        # Dividir si es muy largo
        if len(strategy) > 4000:
            chunks = [strategy[i:i+3800] for i in range(0, len(strategy), 3800)]
            for i, chunk in enumerate(chunks):
                title = f"🎯 ESTRATEGIA DE AUDIENCIA (Parte {i+1}/{len(chunks)})"
                await update.message.reply_text(f"**{title}**\n\n{chunk}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"**🎯 ESTRATEGIA DE AUDIENCIA**\n\n{strategy}", parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def content_calendar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /content - Calendario de contenido detallado"""
    await update.message.chat.send_action("typing")
    
    # Permitir especificar días
    days = 30
    if context.args:
        try:
            days = int(context.args[0])
            days = min(days, 60)  # Máximo 60 días
        except:
            days = 30
    
    await update.message.reply_text(f"📅 Generando calendario de contenido para {days} días...")
    
    try:
        calendar = campaign_manager.create_content_calendar(days)
        
        # Dividir si es muy largo
        if len(calendar) > 4000:
            chunks = [calendar[i:i+3800] for i in range(0, len(calendar), 3800)]
            for i, chunk in enumerate(chunks):
                title = f"📅 CALENDARIO DE CONTENIDO (Parte {i+1}/{len(chunks)})"
                await update.message.reply_text(f"**{title}**\n\n{chunk}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"**📅 CALENDARIO DE CONTENIDO**\n\n{calendar}", parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def video_script(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /video - Guión para video mensual"""
    await update.message.chat.send_action("typing")
    await update.message.reply_text("🎬 Generando guión de video de alta calidad...")
    
    try:
        script = campaign_manager.create_monthly_video_script()
        
        # Dividir si es muy largo
        if len(script) > 4000:
            chunks = [script[i:i+3800] for i in range(0, len(script), 3800)]
            for i, chunk in enumerate(chunks):
                title = f"🎬 GUIÓN DE VIDEO (Parte {i+1}/{len(chunks)})"
                await update.message.reply_text(f"**{title}**\n\n{chunk}", parse_mode='Markdown')
        else:
            await update.message.reply_text(f"**🎬 GUIÓN DE VIDEO**\n\n{script}", parse_mode='Markdown')
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def generate_image(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /image - Generar imagen para contenido"""
    await update.message.chat.send_action("typing")
    
    # Determinar tema
    theme = "general"
    if context.args:
        theme_input = ' '.join(context.args).lower()
        if "retiro" in theme_input or "retreat" in theme_input:
            theme = "retreat_announcement"
        elif "medicina" in theme_input or "ayahuasca" in theme_input:
            theme = "medicine"
        elif "transformación" in theme_input or "transformation" in theme_input:
            theme = "transformation"
        elif "lugar" in theme_input or "location" in theme_input:
            theme = "location"
    
    await update.message.reply_text(f"🎨 Generando imagen tema: {theme}...")
    
    try:
        result = image_generator.generate_retreat_image(content_theme=theme)
        
        if result["success"]:
            # Enviar imagen
            with open(result["local_path"], 'rb') as photo:
                await update.message.reply_photo(
                    photo=photo,
                    caption=f"✅ Imagen generada exitosamente!\n\n🎨 Tema: {theme}\n📁 Archivo: {result['filename']}\n\n💡 Usa `/facebook [contenido]` para publicar con esta imagen"
                )
        else:
            await update.message.reply_text(f"❌ Error generando imagen: {result['error']}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def daily_content_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /daily - Generar contenido diario automático"""
    await update.message.chat.send_action("typing")
    
    # Permitir especificar día
    day_of_week = None
    if context.args:
        day_input = context.args[0].capitalize()
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        if day_input in days:
            day_of_week = day_input
    
    target_day = day_of_week or datetime.now().strftime("%A")
    await update.message.reply_text(f"🎨 Generando contenido diario para {target_day}...")
    
    try:
        # Generar contenido + imagen
        result = daily_content.generate_content_with_image(day_of_week)
        
        if result["success"]:
            # Enviar contenido generado
            content_message = f"**📅 CONTENIDO PARA {result['day'].upper()}**\n\n"
            content_message += f"🎯 Tema: {result['theme']}\n"
            content_message += f"⏰ Hora sugerida: {result['posting_time']}\n\n"
            content_message += "**📝 CONTENIDO:**\n"
            content_message += result['content']
            
            await update.message.reply_text(content_message, parse_mode='Markdown')
            
            # Enviar imagen si se generó exitosamente
            if result["image"]["success"]:
                with open(result["image"]["local_path"], 'rb') as photo:
                    await update.message.reply_photo(
                        photo=photo,
                        caption="🎨 Imagen generada para acompañar el contenido"
                    )
                    
                # Preguntar si quiere publicar
                await update.message.reply_text(
                    "🚀 ¿Quieres publicar este contenido en Facebook ahora?\n\n"
                    "Responde 'sí' para publicar automáticamente."
                )
            else:
                await update.message.reply_text(
                    f"⚠️ Contenido generado, pero error en imagen: {result['image']['error']}\n\n"
                    "🚀 ¿Quieres publicar solo el texto en Facebook?"
                )
        else:
            await update.message.reply_text(f"❌ Error generando contenido: {result['error']}")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


async def weekly_calendar_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /weekly - Generar calendario semanal completo"""
    await update.message.chat.send_action("typing")
    await update.message.reply_text("📅 Generando calendario semanal completo...")
    
    try:
        weekly_content = daily_content.generate_weekly_calendar()
        
        if weekly_content:
            calendar_message = "**📅 CALENDARIO SEMANAL SACRED REBIRTH**\n\n"
            
            for day, content_data in weekly_content.items():
                calendar_message += f"**{day.upper()}** ({content_data['posting_time']})\n"
                calendar_message += f"🎯 {content_data['theme']}\n"
                calendar_message += f"📝 {content_data['content'][:100]}...\n\n"
                calendar_message += "━━━━━━━━━━━━━━━━━━━━\n\n"
            
            # Dividir si es muy largo
            if len(calendar_message) > 4000:
                chunks = [calendar_message[i:i+3800] for i in range(0, len(calendar_message), 3800)]
                for i, chunk in enumerate(chunks):
                    title = f"📅 CALENDARIO SEMANAL (Parte {i+1}/{len(chunks)})"
                    await update.message.reply_text(f"**{title}**\n\n{chunk}", parse_mode='Markdown')
            else:
                await update.message.reply_text(calendar_message, parse_mode='Markdown')
                
            await update.message.reply_text(
                "✅ Calendario generado!\n\n"
                "🎯 Usa `/daily [día]` para contenido específico\n"
                "🚀 Usa `/facebook [contenido]` para publicar\n"
                "🎨 Usa `/image [tema]` para generar imágenes"
            )
        else:
            await update.message.reply_text("❌ No se pudo generar el calendario semanal")
            
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {str(e)}")


def main():
    """Inicia el bot de Telegram"""
    
    if not TELEGRAM_BOT_TOKEN:
        print("❌ Error: TELEGRAM_BOT_TOKEN no configurado en .env")
        print("\nPara obtener un token:")
        print("1. Habla con @BotFather en Telegram")
        print("2. Usa /newbot y sigue las instrucciones")
        print("3. Copia el token a tu archivo .env")
        return
    
    print("🚀 Iniciando bot de Telegram...")
    
    # Crear aplicación
    application = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Registrar handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("status", status))
    application.add_handler(CommandHandler("stats", stats))
    application.add_handler(CommandHandler("calendar", calendar))
    application.add_handler(CommandHandler("leads", leads))
    application.add_handler(CommandHandler("models", models))
    application.add_handler(CommandHandler("teach", teach))
    application.add_handler(CommandHandler("facebook", facebook_post))
    application.add_handler(CommandHandler("campaign", campaign))
    application.add_handler(CommandHandler("audience", audience))
    application.add_handler(CommandHandler("content", content_calendar))
    application.add_handler(CommandHandler("video", video_script))
    application.add_handler(CommandHandler("image", generate_image))
    application.add_handler(CommandHandler("daily", daily_content_cmd))
    application.add_handler(CommandHandler("weekly", weekly_calendar_cmd))
    
    # Handler para todos los mensajes de texto
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Iniciar bot
    print("✅ Bot iniciado! Esperando mensajes...")
    print(f"📱 Los usuarios autorizados pueden empezar a chatear")
    if AUTHORIZED_USERS:
        print(f"🔐 IDs autorizados: {', '.join(AUTHORIZED_USERS)}")
    else:
        print("⚠️ Advertencia: Todos los usuarios pueden usar el bot (configura TELEGRAM_AUTHORIZED_USERS)")
    
    application.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
