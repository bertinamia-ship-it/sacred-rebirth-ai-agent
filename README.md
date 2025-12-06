# Sacred Rebirth AI Marketing Agent

Agente de IA automatizado para gestión de contenido y marketing de Sacred Rebirth.

## 🎯 Funcionalidades

- **Generación de Contenido**: Crea posts automáticos para redes sociales (Instagram, Facebook)
- **Email Marketing**: Envía campañas promocionales personalizadas
- **Programación de Posts**: Calendario automático de publicaciones
- **Análisis de Engagement**: Tracking de métricas y optimización
- **Gestión de Leads**: Seguimiento automático de clientes potenciales

## 🛠️ Tecnologías

- Python 3.11+
- OpenAI API (GPT-4)
- Meta Graph API (Instagram/Facebook)
- SendGrid/SMTP (Email)
- Schedule (Automatización)

## 📦 Instalación

```bash
pip install -r requirements.txt
```

## ⚙️ Configuración

1. Copia `.env.example` a `.env`
2. Configura tus API keys:
   - `OPENAI_API_KEY`
   - `META_ACCESS_TOKEN`
   - `SENDGRID_API_KEY`
   - `EMAIL_FROM`

## 🚀 Uso

```bash
# Generar contenido
python src/content_generator.py

# Programar posts
python src/scheduler.py

# Enviar email campaign
python src/email_campaign.py
```

## 📁 Estructura

```
sacred-rebirth-ai-agent/
├── src/
│   ├── content_generator.py   # Generación de contenido con IA
│   ├── social_media.py         # Publicación en redes sociales
│   ├── email_campaign.py       # Envío de emails
│   └── scheduler.py            # Automatización de tareas
├── config/
│   ├── prompts.py              # Templates de prompts para IA
│   └── settings.py             # Configuración general
├── data/
│   └── content_calendar.json  # Calendario de contenido
├── .env.example
├── requirements.txt
└── README.md
```

## 🌿 Sacred Rebirth

Website: https://sacred-rebirth.com
Instagram: @sacredrebirthvalle
Facebook: sacredbirthretreats
