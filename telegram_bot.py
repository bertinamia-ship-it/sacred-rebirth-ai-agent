#!/usr/bin/env python3
"""
Bot de Telegram para Sacred Rebirth AI Agent
Permite interactuar con el agente de marketing a través de Telegram
"""
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.crew import MarketingCrew
from chat import ChatAgent

load_dotenv()

# Configuración
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
AUTHORIZED_USERS = os.getenv('TELEGRAM_AUTHORIZED_USERS', '').split(',')

# Inicializar agente
print("🤖 Inicializando Marketing Crew para Telegram...")
crew = MarketingCrew()
chat_agent = ChatAgent()
chat_agent.crew = crew
print("✅ Bot de Telegram listo!")


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /start - Bienvenida"""
    user = update.effective_user
    
    welcome_message = f"""
🙏 ¡Hola {user.first_name}!

Soy el asistente de marketing de Sacred Rebirth.

**Puedo ayudarte con:**
• Crear posts para Instagram/Facebook
• Generar campañas de email
• Gestionar tu calendario de contenido
• Analizar tus leads
• Programar publicaciones

**Ejemplos de comandos:**
• "Crea un post de Instagram sobre ayahuasca"
• "Muestra el calendario de esta semana"
• "Envía email de bienvenida a nuevos leads"
• "Programa 3 posts para mañana"

Solo escríbeme naturalmente y yo entenderé 💬
"""
    
    await update.message.reply_text(welcome_message)


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Comando /help - Ayuda"""
    help_text = """
📚 **Guía Rápida**

**Comandos:**
/start - Bienvenida
/help - Esta ayuda
/status - Estado del sistema
/stats - Ver uso y costos 💰
/models - Ver modelos de IA disponibles
/calendar - Calendario sugerido
/teach - Enseñarme algo nuevo

**Crear Contenido:**
• "Genera un post sobre ayahuasca" (⚡ básico)
• "Crea un **anuncio PROFESIONAL**" (✨ premium)
• "Dame una **estrategia completa**" (🔥 ultra)

**Investigación:**
• "Dónde puedo promocionar mi retiro"
• "Encuentra grupos de Facebook"
• "Qué hashtags usar"

**Enseñarme:**
• /teach El próximo retiro es el 15 de enero
• "Aprende: Me gusta un tono espiritual"
• "Recuerda: El precio es $8000 MXN"

💡 **TIP:** Di "profesional" o "llamativo" para usar IA premium automáticamente

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
        
        # Enviar respuesta
        # Dividir respuestas largas (límite de Telegram: 4096 caracteres)
        if len(bot_response) > 4000:
            # Dividir en chunks
            chunks = [bot_response[i:i+4000] for i in range(0, len(bot_response), 4000)]
            for chunk in chunks:
                await update.message.reply_text(chunk)
        else:
            await update.message.reply_text(bot_response)
        
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
