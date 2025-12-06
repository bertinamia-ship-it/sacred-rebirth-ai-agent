# 🌟 Guía de Uso - Sacred Rebirth AI Marketing Agent

## 📋 Descripción

Sistema de **múltiples agentes IA** (Crew) para automatizar el marketing de Sacred Rebirth usando **CrewAI**. El crew está compuesto por 6 agentes especializados que trabajan en conjunto:

### 👥 Agentes del Crew

1. **🎯 Estratega de Contenido** - Planifica estrategias de marketing
2. **✍️ Creador de Contenido** - Genera posts para Instagram, Facebook y Email
3. **📱 Community Manager** - Publica y gestiona redes sociales
4. **📧 Especialista en Email** - Crea y ejecuta campañas de email
5. **📊 Analista** - Analiza métricas y optimiza estrategias
6. **👥 Customer Success** - Gestiona leads y clientes

---

## 🚀 Instalación Rápida

### 1. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 2. Configurar variables de entorno

```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus credenciales
nano .env
```

### 3. Configurar API Keys necesarias

**Obligatorias:**
- `OPENAI_API_KEY` - Obtener en: https://platform.openai.com/api-keys

**Opcionales (para funcionalidad completa):**
- `META_ACCESS_TOKEN` - Para publicar en Instagram/Facebook
- `SENDGRID_API_KEY` - Para enviar emails
- `INSTAGRAM_BUSINESS_ACCOUNT_ID` - ID de tu cuenta de negocio
- `FACEBOOK_PAGE_ID` - ID de tu página de Facebook

---

## 💻 Modos de Uso

### 🎮 Modo Interactivo (Recomendado para principiantes)

```bash
python main.py
```

Muestra un menú interactivo con todas las opciones disponibles.

### ⚡ Modo Comando Rápido

#### 1. Planificación Estratégica
```bash
python main.py --mode strategy
```
Genera un plan estratégico de contenido para la semana.

#### 2. Crear Contenido
```bash
# Contenido automático
python main.py --mode content

# Contenido con temas específicos
python main.py --mode content --topics "Ayahuasca,Kambo,Qigong"
```

#### 3. Publicar en Redes Sociales
```bash
# Instagram
python main.py --mode social --platform instagram --topic "Transformación espiritual"

# Facebook
python main.py --mode social --platform facebook --topic "Beneficios de Ayahuasca"

# Ambas plataformas
python main.py --mode social --platform both --topic "Próximo retiro"
```

#### 4. Campaña de Email
```bash
# Email promocional
python main.py --mode email --type promotional

# Email educativo
python main.py --mode email --type educational

# Email con testimoniales
python main.py --mode email --type testimonial
```

#### 5. Gestión de Leads
```bash
# Ver todos los leads
python main.py --mode leads --action view

# Nutrir leads interesados
python main.py --mode leads --action nurture --segment interested

# Segmentar leads convertidos
python main.py --mode leads --action segment --segment converted
```

#### 6. Análisis de Métricas
```bash
# Análisis de engagement
python main.py --mode analytics --metric engagement

# Análisis de conversión
python main.py --mode analytics --metric conversion

# Análisis completo
python main.py --mode analytics --metric all
```

#### 7. Campaña Completa Multicanal
```bash
python main.py --mode campaign --goal "Promoción retiro de Enero"
```
Ejecuta una campaña completa coordinada entre todos los agentes.

#### 8. Automatización Diaria
```bash
python main.py --mode daily
```
Ejecuta las tareas diarias automáticamente:
- Genera contenido del día
- Revisa calendario
- Nutre leads
- Analiza métricas

---

## 🛠️ Uso Programático (Python)

### Ejemplo 1: Generar post de Instagram

```python
from src.crew import quick_instagram_post

# Generar post
result = quick_instagram_post("Beneficios de la Ayahuasca")
print(result)
```

### Ejemplo 2: Generar post de Facebook

```python
from src.crew import quick_facebook_post

result = quick_facebook_post("Preparación para retiros")
print(result)
```

### Ejemplo 3: Crear email rápido

```python
from src.crew import quick_email

result = quick_email(campaign_type='promotional')
print(result)
```

### Ejemplo 4: Usar el Crew completo

```python
from src.crew import MarketingCrew

# Inicializar crew
crew = MarketingCrew()

# Ejecutar planificación estratégica
strategy = crew.run_content_strategy()

# Crear contenido
content = crew.run_content_creation(['Ayahuasca', 'Kambo'])

# Campaña de email
email = crew.run_email_campaign('promotional')

# Gestión de leads
leads = crew.run_leads_management('nurture', 'interested')

# Análisis
analytics = crew.run_analytics('engagement')

# Campaña completa
campaign = crew.run_full_campaign("Retiro de Enero 2026")
```

---

## 📁 Estructura del Proyecto

```
sacred-rebirth-ai-agent/
├── main.py                 # Punto de entrada principal
├── requirements.txt        # Dependencias
├── .env.example           # Ejemplo de configuración
├── README.md              # Documentación general
├── GUIA_USO.md           # Esta guía
│
├── config/
│   ├── settings.py        # Configuración general
│   └── prompts.py         # Templates de prompts
│
├── src/
│   ├── agents.py          # Definición de agentes CrewAI
│   ├── tasks.py           # Definición de tareas
│   ├── crew.py            # Orquestación del crew
│   ├── tools.py           # Herramientas personalizadas
│   ├── content_generator.py   # Generador de contenido
│   ├── social_media.py    # Publicación en redes
│   ├── email_campaign.py  # Gestión de emails
│   └── scheduler.py       # Programación de tareas
│
└── data/
    ├── content_calendar.json   # Calendario de contenido
    ├── leads.json              # Base de datos de leads
    ├── generated/              # Contenido generado
    └── reports/                # Reportes de análisis
```

---

## 🔧 Configuración Avanzada

### Modificar configuración de agentes

Edita `src/agents.py` para personalizar el comportamiento de cada agente:

```python
def create_content_creator():
    return Agent(
        role='Creador de Contenido Multicanal',
        goal='Generar contenido atractivo...',
        backstory='Tu background personalizado...',
        verbose=True,  # Cambiar a False para menos output
        allow_delegation=False,
        tools=[ContentGeneratorTool(), ContentCalendarTool()],
        llm='gpt-4'  # Cambiar modelo si es necesario
    )
```

### Agregar nuevos temas de contenido

Edita `config/prompts.py`:

```python
CONTENT_TOPICS = [
    "Tu nuevo tema 1",
    "Tu nuevo tema 2",
    # ... más temas
]
```

### Personalizar horarios de publicación

Edita `config/settings.py`:

```python
POST_TIMES = [
    '09:00',   # Post matutino
    '14:00',   # Post medio día
    '18:00',   # Post vespertino
    '21:00'    # Post nocturno
]
```

---

## 📊 Gestión de Datos

### Agregar Leads Manualmente

Edita `data/leads.json`:

```json
[
  {
    "id": 1,
    "name": "Juan Pérez",
    "email": "juan@example.com",
    "phone": "+52 123 456 7890",
    "status": "interested",
    "source": "instagram",
    "created_at": "2025-01-06T10:00:00"
  }
]
```

**Estados de leads:**
- `new` - Lead nuevo
- `interested` - Mostró interés
- `contacted` - Fue contactado
- `converted` - Se convirtió en cliente

### Gestionar Calendario de Contenido

El archivo `data/content_calendar.json` almacena el contenido programado:

```json
{
  "content_calendar": [
    {
      "id": 1,
      "date": "2025-01-07",
      "platform": "instagram",
      "topic": "Beneficios de Ayahuasca",
      "status": "scheduled",
      "content": "Texto del post...",
      "created_at": "2025-01-06T10:00:00"
    }
  ]
}
```

---

## 🔍 Herramientas Disponibles

### 1. ContentGeneratorTool
Genera contenido optimizado para cada plataforma.

```python
from src.tools import ContentGeneratorTool

tool = ContentGeneratorTool()
result = tool._run(platform='instagram', topic='Ayahuasca')
```

### 2. SocialMediaPublishTool
Publica en Instagram y Facebook.

```python
from src.tools import SocialMediaPublishTool

tool = SocialMediaPublishTool()
result = tool._run(
    platform='instagram',
    content='Tu contenido aquí',
    image_url='https://...'
)
```

### 3. EmailCampaignTool
Envía campañas de email.

```python
from src.tools import EmailCampaignTool

tool = EmailCampaignTool()
result = tool._run(
    subject='Próximo Retiro',
    html_content='<h1>Contenido HTML</h1>',
    send_to_all=False  # True para enviar a todos
)
```

### 4. ContentCalendarTool
Gestiona el calendario de contenido.

```python
from src.tools import ContentCalendarTool

tool = ContentCalendarTool()

# Ver calendario
result = tool._run(action='view')

# Agregar contenido
result = tool._run(
    action='add',
    content_item={
        'date': '2025-01-08',
        'platform': 'facebook',
        'topic': 'Kambo',
        'status': 'draft'
    }
)
```

### 5. LeadsManagerTool
Gestiona la base de leads.

```python
from src.tools import LeadsManagerTool

tool = LeadsManagerTool()

# Ver leads
result = tool._run(action='view')

# Agregar lead
result = tool._run(
    action='add',
    lead_data={
        'name': 'María García',
        'email': 'maria@example.com',
        'status': 'interested'
    }
)

# Segmentar leads
result = tool._run(action='segment', segment_criteria='interested')
```

---

## 📅 Automatización con Cron

### Configurar tarea diaria (Linux/Mac)

```bash
# Editar crontab
crontab -e

# Agregar línea para ejecutar a las 8am diariamente
0 8 * * * cd /ruta/a/sacred-rebirth-ai-agent && /usr/bin/python3 main.py --mode daily
```

### Configurar tarea semanal para campañas

```bash
# Ejecutar campaña completa cada lunes a las 9am
0 9 * * 1 cd /ruta/a/sacred-rebirth-ai-agent && /usr/bin/python3 main.py --mode campaign
```

---

## 🐛 Solución de Problemas

### Error: "No module named 'crewai'"

```bash
pip install crewai crewai-tools
```

### Error: "OPENAI_API_KEY not found"

Asegúrate de tener el archivo `.env` con tu API key:

```bash
cp .env.example .env
nano .env  # Agregar tu API key
```

### Error al publicar en redes sociales

Verifica que tengas configuradas las credenciales de Meta:
- `META_ACCESS_TOKEN`
- `INSTAGRAM_BUSINESS_ACCOUNT_ID`
- `FACEBOOK_PAGE_ID`

### Contenido generado está vacío

Verifica tu saldo de OpenAI y que la API key sea válida.

---

## 📈 Mejores Prácticas

### 1. Frecuencia de Publicación
- Instagram: 1-2 posts diarios
- Facebook: 1 post diario
- Email: 1-2 por semana

### 2. Horarios Óptimos
- **Mañana**: 9:00 AM - Mayor alcance
- **Tarde**: 6:00 PM - Mayor engagement

### 3. Mix de Contenido (Regla 80/20)
- 80% contenido de valor (educativo, inspirador)
- 20% contenido promocional

### 4. Segmentación de Leads
- Nutrir leads `interested` con contenido educativo
- Leads `contacted` necesitan urgencia suave
- Leads `converted` requieren seguimiento post-compra

### 5. Análisis Regular
Ejecutar análisis semanalmente:
```bash
python main.py --mode analytics --metric all
```

---

## 🎯 Casos de Uso Comunes

### Caso 1: Lanzamiento de Nuevo Retiro

```bash
# 1. Crear estrategia
python main.py --mode strategy

# 2. Generar contenido
python main.py --mode content --topics "Retiro Enero,Preparación,Beneficios"

# 3. Campaña de email
python main.py --mode email --type promotional

# 4. Publicar en redes
python main.py --mode social --platform both --topic "Nuevo Retiro Enero 2026"

# 5. Nutrir leads
python main.py --mode leads --action nurture --segment interested
```

### Caso 2: Contenido Educativo Semanal

```bash
# Generar posts educativos
python main.py --mode content --topics "Ayahuasca 101,Beneficios Kambo,Qigong Básico"
```

### Caso 3: Seguimiento de Leads

```bash
# Ver leads
python main.py --mode leads --action view

# Nutrir leads interesados
python main.py --mode leads --action nurture --segment interested
```

### Caso 4: Campaña Completa Automatizada

```bash
# Una sola línea ejecuta todo
python main.py --mode campaign --goal "Llenar retiro de Enero 2026"
```

---

## 🔐 Seguridad

### Nunca compartas tu archivo `.env`
- Está incluido en `.gitignore`
- Contiene credenciales sensibles

### Rotación de API Keys
- Rota tus API keys cada 3-6 meses
- Usa diferentes keys para desarrollo y producción

### Límites de Rate
- OpenAI: Respeta los límites de tu plan
- SendGrid: Máximo 50 emails/día (configurable)
- Meta API: Varía según tu acceso

---

## 🤝 Soporte

### Documentación Adicional
- [CrewAI Docs](https://docs.crewai.com/)
- [OpenAI API](https://platform.openai.com/docs)
- [Meta Graph API](https://developers.facebook.com/docs/graph-api)
- [SendGrid API](https://docs.sendgrid.com/)

### Contacto
Para soporte del proyecto Sacred Rebirth:
- Email: rebirthsecred@gmail.com
- WhatsApp: +52 722 512 3413

---

## 📝 Notas Finales

- **Modo Test**: Usa `send_to_all=False` en emails para probar primero
- **Backup**: Haz backup regular de `data/` 
- **Monitoreo**: Revisa logs regularmente para detectar errores
- **Optimización**: Ajusta prompts en `config/prompts.py` según resultados

---

¡Listo para transformar tu marketing con IA! 🚀✨
