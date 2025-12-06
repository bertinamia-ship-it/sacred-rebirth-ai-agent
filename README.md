# 🌟 Sacred Rebirth AI Marketing Agent

Sistema de **múltiples agentes IA** para automatización completa de marketing usando **CrewAI**.

## 🤖 ¿Qué es un Crew de Agentes?

Un **crew** es un equipo de agentes de IA especializados que trabajan juntos para lograr objetivos complejos. Cada agente tiene:
- **Rol específico** y expertise
- **Herramientas especializadas**
- **Capacidad de colaborar** con otros agentes
- **Memoria compartida** para aprender del contexto

## 👥 Nuestro Crew de 6 Agentes

1. **🎯 Estratega de Contenido** - Planifica estrategias de marketing
2. **✍️ Creador de Contenido** - Genera posts para Instagram, Facebook y Email
3. **📱 Community Manager** - Publica y gestiona redes sociales
4. **📧 Especialista en Email Marketing** - Crea y ejecuta campañas de email
5. **📊 Analista y Optimizador** - Analiza métricas y optimiza estrategias
6. **👥 Especialista en Customer Success** - Gestiona leads y clientes

## 🎯 Funcionalidades

- ✅ **Generación de Contenido IA**: Posts para Instagram, Facebook y Email
- ✅ **Publicación Automática**: Publica directamente en redes sociales
- ✅ **Email Marketing**: Campañas personalizadas con SendGrid
- ✅ **Gestión de Leads**: CRM básico con segmentación y nutrición
- ✅ **Calendario de Contenido**: Programación y organización automática
- ✅ **Análisis de Métricas**: Optimización basada en datos
- ✅ **Campañas Multicanal**: Coordinación entre todos los canales
- ✅ **Automatización Diaria**: Ejecuta tareas automáticamente
- 🆕 **Chat Conversacional**: Controla todo con lenguaje natural
- 🆕 **Bot de Telegram**: Usa el agente desde tu celular
- 🆕 **Bot de WhatsApp**: Conecta vía WhatsApp Business

## 🛠️ Tecnologías

- **Python 3.11+**
- **CrewAI** - Framework de agentes colaborativos
- **OpenAI API (GPT-4)** - Generación de contenido
- **LangChain** - Orquestación de LLMs
- **Meta Graph API** - Instagram/Facebook
- **SendGrid** - Email marketing
- **Telegram Bot API** - Bot de Telegram
- **Twilio** - WhatsApp Business API
- **Schedule** - Automatización de tareas

## 🚀 Inicio Rápido

### 1. Instalación

```bash
# Clonar repositorio
git clone <tu-repo>
cd sacred-rebirth-ai-agent

# Instalar dependencias
pip install -r requirements.txt
```

### 2. Configuración OBLIGATORIA

```bash
# Copiar archivo de configuración
cp .env.example .env

# Editar y agregar tu OpenAI API Key (OBLIGATORIO)
nano .env
# Cambiar: OPENAI_API_KEY=sk-TU-KEY-AQUI
```

**📖 Ver guía completa:** [CONFIGURACION.md](CONFIGURACION.md)

### 3. Modos de Uso

#### 💬 MODO CHAT (Terminal)

```bash
python chat.py
```

Háblale naturalmente:
```
💬 "crea un post de instagram sobre ayahuasca"
💬 "necesito una campaña completa para enero"  
💬 "muéstrame los leads"
💬 "envía un email promocional"
```

#### 📱 BOT DE TELEGRAM (Recomendado para celular)

```bash
# 1. Configura tu bot con @BotFather
# 2. Agrega TELEGRAM_BOT_TOKEN a .env
# 3. Ejecuta:
python telegram_bot.py
```

**📖 Guía completa:** [BOTS_GUIA.md](BOTS_GUIA.md)

#### 💚 BOT DE WHATSAPP (Empresarial)

```bash
# 1. Crea cuenta en Twilio
# 2. Configura WhatsApp Business API
# 3. Agrega credenciales a .env
# 4. Ejecuta:
python whatsapp_bot.py
```

**📖 Guía completa:** [BOTS_GUIA.md](BOTS_GUIA.md)

#### 🖥️ MODO TRADICIONAL (CLI)

```bash
# Modo interactivo con menú
python main.py

# Modo comando directo
python main.py --mode social --platform instagram --topic "Ayahuasca"
```

# Editar con tus credenciales
nano .env
```

**Mínimo requerido:**
```env
OPENAI_API_KEY=tu-api-key-aquí
```

**Para funcionalidad completa:**
```env
OPENAI_API_KEY=tu-api-key
META_ACCESS_TOKEN=tu-meta-token
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu-ig-id
FACEBOOK_PAGE_ID=tu-fb-id
SENDGRID_API_KEY=tu-sendgrid-key
```

### 3. Uso Básico

#### Modo Interactivo (Recomendado)
```bash
python main.py
```

#### Generar Contenido Rápido
```bash
# Post de Instagram
python main.py --mode social --platform instagram --topic "Ayahuasca"

# Post de Facebook  
python main.py --mode social --platform facebook --topic "Retiro espiritual"

# Email promocional
python main.py --mode email --type promotional
```

#### Campaña Completa Automatizada
```bash
python main.py --mode campaign --goal "Retiro de Enero 2026"
```

#### Automatización Diaria
```bash
python main.py --mode daily
```

## 📖 Documentación Completa

Ver **[GUIA_USO.md](GUIA_USO.md)** para:
- Guía detallada de todos los modos
- Uso programático desde Python
- Configuración avanzada
- Solución de problemas
- Casos de uso reales

## 💻 Ejemplos de Uso Programático

### Generar Post de Instagram
```python
from src.crew import quick_instagram_post

result = quick_instagram_post("Beneficios de la Ayahuasca")
print(result)
```

### Ejecutar Campaña Completa
```python
from src.crew import MarketingCrew

crew = MarketingCrew()
result = crew.run_full_campaign("Retiro de Enero 2026")
```

### Automatización Diaria
```python
from src.crew import MarketingCrew

crew = MarketingCrew()
crew.run_daily_automation()
```

## 📁 Estructura del Proyecto

```
sacred-rebirth-ai-agent/
├── main.py                     # 🎯 Punto de entrada principal
├── requirements.txt            # 📦 Dependencias
├── .env.example               # ⚙️ Configuración de ejemplo
├── README.md                  # 📖 Este archivo
├── GUIA_USO.md               # 📚 Guía completa de uso
│
├── config/
│   ├── settings.py            # Configuración general
│   └── prompts.py             # Templates de prompts para IA
│
├── src/
│   ├── crew.py                # 🤖 Orquestación del crew
│   ├── agents.py              # 👥 Definición de agentes
│   ├── tasks.py               # 📋 Definición de tareas
│   ├── tools.py               # 🔧 Herramientas personalizadas
│   ├── content_generator.py   # ✍️ Generación de contenido
│   ├── social_media.py        # 📱 Publicación en redes
│   ├── email_campaign.py      # 📧 Gestión de emails
│   └── scheduler.py           # ⏰ Programación de tareas
│
└── data/
    ├── content_calendar.json  # Calendario de contenido
    ├── leads.json             # Base de datos de leads
    ├── generated/             # Contenido generado
    └── reports/               # Reportes de análisis
```

## 🎮 Comandos Disponibles

| Comando | Descripción |
|---------|-------------|
| `python main.py` | Modo interactivo con menú |
| `--mode strategy` | Planificación estratégica |
| `--mode content` | Crear contenido |
| `--mode social` | Publicar en redes sociales |
| `--mode email` | Campaña de email |
| `--mode leads` | Gestión de leads |
| `--mode analytics` | Análisis de métricas |
| `--mode campaign` | Campaña completa multicanal |
| `--mode daily` | Automatización diaria |

Ver `python main.py --help` para más opciones.

## 📱 Opciones de Interfaz

| Modo | Dificultad | Uso Recomendado | Setup |
|------|-----------|-----------------|-------|
| **Telegram Bot** | ⭐ Fácil | Personal/Equipo, desde celular | 5 min |
| **Chat Terminal** | ⭐⭐ Media | Desarrollo, testing local | 1 min |
| **WhatsApp Bot** | ⭐⭐⭐ Avanzada | Producción, clientes reales | 30 min |
| **CLI Tradicional** | ⭐⭐ Media | Automatización, scripts | 1 min |

**🎯 Recomendación:** Empieza con **Telegram Bot** para usar el agente desde tu celular fácilmente.

## 🔧 Herramientas del Crew

Cada agente tiene acceso a herramientas especializadas:

- **content_generator_tool** - Genera contenido optimizado por plataforma
- **social_media_publish_tool** - Publica en Instagram/Facebook
- **email_campaign_tool** - Envía campañas de email
- **content_calendar_tool** - Gestiona calendario de contenido
- **leads_manager_tool** - Administra leads y segmentación

## 📊 Flujo de Trabajo Típico

```
1. Estrategia     → El estratega planifica contenido semanal
                    ↓
2. Creación      → El creador genera posts optimizados
                    ↓
3. Revisión      → El analista revisa y optimiza
                    ↓
4. Publicación   → El community manager publica
                    ↓
5. Email         → El especialista envía campañas
                    ↓
6. Seguimiento   → Customer success nutre leads
                    ↓
7. Análisis      → El analista reporta métricas
```

## 🌟 Casos de Uso

### 1. Desde Telegram (Más Fácil)
```
💬 "Crea una campaña completa para el retiro de enero"
💬 "Genera 5 posts para esta semana"
💬 "Envía email de seguimiento a leads interesados"
```

### 2. Lanzamiento de Retiro (CLI)
```bash
python main.py --mode campaign --goal "Retiro Enero 2026"
```

### 3. Contenido Diario Automatizado
```bash
python main.py --mode daily
```

### 4. Nutrición de Leads
```bash
python main.py --mode leads --action nurture --segment interested
```

## 🤝 Contribuir

Este es un proyecto en desarrollo activo. Sugerencias y mejoras son bienvenidas.

## 📞 Contacto

**Sacred Rebirth**
- 🌐 Website: https://sacred-rebirth.com
- 📸 Instagram: @sacredrebirthvalle  
- 📘 Facebook: sacredbirthretreats
- 📧 Email: rebirthsecred@gmail.com
- 📱 WhatsApp: +52 722 512 3413
- 📍 Valle de Bravo, México

## 📄 Licencia

Este proyecto es para uso interno de Sacred Rebirth.

---

Desarrollado con ❤️ usando **CrewAI** y **OpenAI GPT-4**
