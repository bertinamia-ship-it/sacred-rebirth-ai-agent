# 🛠️ Comandos Útiles - Sacred Rebirth AI Agent

## 🚀 Inicio Rápido

```bash
# Instalar
pip install -r requirements.txt

# Configurar
cp .env.example .env
nano .env  # Agregar OPENAI_API_KEY

# Ejecutar
python main.py
```

---

## 📱 Generar Contenido

### Instagram
```bash
# Post sobre Ayahuasca
python main.py --mode social --platform instagram --topic "Beneficios de Ayahuasca"

# Post sobre retiro
python main.py --mode social --platform instagram --topic "Próximo retiro Enero 2026"

# Post sobre preparación
python main.py --mode social --platform instagram --topic "Cómo prepararse para ceremonia"
```

### Facebook
```bash
# Post educativo
python main.py --mode social --platform facebook --topic "Guía completa de Ayahuasca"

# Post sobre Valle de Bravo
python main.py --mode social --platform facebook --topic "Por qué Valle de Bravo es perfecto"

# Ambas plataformas a la vez
python main.py --mode social --platform both --topic "Transformación espiritual"
```

---

## 📧 Campañas de Email

```bash
# Email promocional
python main.py --mode email --type promotional

# Email educativo
python main.py --mode email --type educational

# Email con testimonios
python main.py --mode email --type testimonial

# Email de nutrición
python main.py --mode email --type nurture
```

---

## 🎯 Estrategia y Planificación

```bash
# Crear plan de contenido semanal
python main.py --mode strategy

# Generar múltiples contenidos
python main.py --mode content --topics "Ayahuasca,Kambo,Qigong,Valle de Bravo"

# Solo generar contenido (sin temas específicos)
python main.py --mode content
```

---

## 👥 Gestión de Leads

```bash
# Ver todos los leads
python main.py --mode leads --action view

# Nutrir leads interesados
python main.py --mode leads --action nurture --segment interested

# Nutrir leads contactados
python main.py --mode leads --action nurture --segment contacted

# Nutrir leads convertidos
python main.py --mode leads --action nurture --segment converted

# Segmentar leads
python main.py --mode leads --action segment --segment interested
```

---

## 📊 Análisis y Métricas

```bash
# Análisis de engagement
python main.py --mode analytics --metric engagement

# Análisis de conversión
python main.py --mode analytics --metric conversion

# Análisis de alcance
python main.py --mode analytics --metric reach

# Análisis completo
python main.py --mode analytics --metric all
```

---

## 🚀 Campañas Completas

```bash
# Campaña para retiro de Enero
python main.py --mode campaign --goal "Retiro de Enero 2026"

# Campaña de lanzamiento
python main.py --mode campaign --goal "Lanzamiento nueva oferta"

# Campaña general
python main.py --mode campaign
```

---

## ⏰ Automatización

```bash
# Automatización diaria (recomendado ejecutar cada mañana)
python main.py --mode daily

# Modo interactivo (menú)
python main.py

# Ejecutar ejemplos
python ejemplos.py
```

---

## 🔧 Mantenimiento

### Ver estructura del proyecto
```bash
tree -L 2 -I '__pycache__|*.pyc'
```

### Buscar archivos generados
```bash
ls -lh data/generated/
```

### Ver últimos leads agregados
```bash
cat data/leads.json | python -m json.tool
```

### Ver calendario de contenido
```bash
cat data/content_calendar.json | python -m json.tool
```

### Verificar configuración
```bash
cat .env | grep -v "^#" | grep -v "^$"
```

---

## 🐍 Comandos Python (uso programático)

### Script básico
```python
from src.crew import quick_instagram_post, quick_facebook_post, quick_email

# Post IG
quick_instagram_post("Ayahuasca")

# Post FB
quick_facebook_post("Retiro")

# Email
quick_email('promotional')
```

### Script avanzado
```python
from src.crew import MarketingCrew

crew = MarketingCrew()

# Estrategia
crew.run_content_strategy()

# Contenido
crew.run_content_creation(['Tema 1', 'Tema 2'])

# Email
crew.run_email_campaign('promotional')

# Leads
crew.run_leads_management('nurture', 'interested')

# Analytics
crew.run_analytics('engagement')

# Campaña completa
crew.run_full_campaign("Mi objetivo")
```

---

## 🔄 Automatización con Cron (Linux/Mac)

### Editar crontab
```bash
crontab -e
```

### Ejecutar diariamente a las 8am
```bash
0 8 * * * cd /ruta/a/sacred-rebirth-ai-agent && /usr/bin/python3 main.py --mode daily >> /tmp/marketing-agent.log 2>&1
```

### Ejecutar campaña cada lunes a las 9am
```bash
0 9 * * 1 cd /ruta/a/sacred-rebirth-ai-agent && /usr/bin/python3 main.py --mode campaign >> /tmp/marketing-campaign.log 2>&1
```

### Generar contenido 2 veces al día (9am y 6pm)
```bash
0 9,18 * * * cd /ruta/a/sacred-rebirth-ai-agent && /usr/bin/python3 main.py --mode content >> /tmp/content-gen.log 2>&1
```

### Ver logs de cron
```bash
tail -f /tmp/marketing-agent.log
```

---

## 🧪 Testing y Debugging

### Verificar instalación
```bash
python --version
pip list | grep -i crew
pip list | grep -i openai
```

### Probar conexión con OpenAI
```bash
python -c "from openai import OpenAI; import os; from dotenv import load_dotenv; load_dotenv(); client = OpenAI(api_key=os.getenv('OPENAI_API_KEY')); print('✅ Conexión OK')"
```

### Ver ayuda completa
```bash
python main.py --help
```

### Modo verbose (más output)
Edita `src/agents.py` y cambia `verbose=True` a `verbose=2`

---

## 📦 Gestión de Dependencias

### Actualizar dependencias
```bash
pip install --upgrade -r requirements.txt
```

### Ver versiones instaladas
```bash
pip freeze | grep -E "crewai|openai|langchain"
```

### Reinstalar todo
```bash
pip uninstall -r requirements.txt -y
pip install -r requirements.txt
```

---

## 💾 Backup y Restore

### Backup de datos
```bash
tar -czf backup-$(date +%Y%m%d).tar.gz data/ .env
```

### Restaurar backup
```bash
tar -xzf backup-20251206.tar.gz
```

### Backup solo de leads
```bash
cp data/leads.json data/leads.json.backup-$(date +%Y%m%d)
```

---

## 🔍 Búsqueda y Filtrado

### Buscar en archivos Python
```bash
grep -r "def " src/ --include="*.py"
```

### Ver todos los agentes definidos
```bash
grep "def create_" src/agents.py
```

### Ver todas las tareas disponibles
```bash
grep "def create_.*_task" src/tasks.py
```

### Contar líneas de código
```bash
find . -name "*.py" -not -path "./__pycache__/*" | xargs wc -l
```

---

## 🎨 Personalización

### Editar prompts
```bash
nano config/prompts.py
```

### Editar configuración
```bash
nano config/settings.py
```

### Agregar nuevo tema de contenido
Edita `config/prompts.py` y agrega a `CONTENT_TOPICS`

### Cambiar horarios de publicación
Edita `config/settings.py` y modifica `POST_TIMES`

---

## 🐛 Troubleshooting

### Limpiar cache de Python
```bash
find . -type d -name __pycache__ -exec rm -rf {} +
find . -type f -name "*.pyc" -delete
```

### Reinstalar CrewAI
```bash
pip uninstall crewai crewai-tools -y
pip install crewai crewai-tools
```

### Verificar permisos
```bash
chmod +x main.py ejemplos.py
```

### Ver variables de entorno cargadas
```bash
python -c "from config.settings import *; import pprint; pprint.pprint({k:v for k,v in globals().items() if k.isupper()})"
```

---

## 📊 Estadísticas

### Contar archivos del proyecto
```bash
find . -type f -name "*.py" | wc -l
```

### Ver tamaño total
```bash
du -sh .
```

### Ver archivos más grandes
```bash
find . -type f -exec ls -lh {} \; | sort -k5 -h -r | head -10
```

---

## 🚀 Comandos de Producción

### Ejecutar en background
```bash
nohup python main.py --mode daily > output.log 2>&1 &
```

### Ver procesos activos
```bash
ps aux | grep python
```

### Matar proceso si se queda colgado
```bash
pkill -f "python main.py"
```

---

## 🎯 Workflows Comunes

### Workflow 1: Preparar semana
```bash
# Lunes por la mañana
python main.py --mode strategy
python main.py --mode content --topics "Ayahuasca,Kambo,Qigong,Valle de Bravo,Testimonios"
```

### Workflow 2: Nutrición de leads
```bash
# Miércoles y viernes
python main.py --mode leads --action nurture --segment interested
python main.py --mode email --type nurture
```

### Workflow 3: Análisis semanal
```bash
# Domingo por la noche
python main.py --mode analytics --metric all
```

### Workflow 4: Campaña especial
```bash
# Cuando tengas un evento especial
python main.py --mode campaign --goal "Retiro especial de Luna Llena"
```

---

## 📝 Scripts Útiles

### Ver todos los comandos disponibles
```bash
python main.py --help
```

### Listar todos los modos
```bash
python -c "import argparse; print('Modos disponibles: strategy, content, campaign, daily, email, social, leads, analytics')"
```

---

## 💡 Tips Finales

1. **Usa `--help`** para ver todas las opciones
2. **Ejecuta ejemplos** primero con `python ejemplos.py`
3. **Revisa logs** regularmente en modo automatizado
4. **Haz backup** de `data/` antes de cambios grandes
5. **Personaliza** `config/prompts.py` para tu voz de marca
6. **Experimenta** con diferentes temas y configuraciones

---

**¡Happy Automation!** 🚀✨
