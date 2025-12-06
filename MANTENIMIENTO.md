# 🛠️ Guía de Mantenimiento - Bot Siempre Funcional

## 🎯 Objetivo
Mantener el bot de Telegram funcionando 24/7 sin interrupciones.

## 📋 Índice
1. [Pagar API de OpenAI](#1-pagar-api-de-openai)
2. [Mejorar Inteligencia del Bot](#2-mejorar-inteligencia)
3. [Monitoreo Automático](#3-monitoreo-automático)
4. [Servidor 24/7](#4-servidor-247)
5. [Respaldo y Seguridad](#5-respaldo-y-seguridad)

---

## 1. 💳 Pagar API de OpenAI

### Paso 1: Agregar Método de Pago
1. Ve a: https://platform.openai.com/settings/organization/billing/overview
2. Click en **"Add payment method"**
3. Agrega tarjeta de crédito/débito
4. Configura límite mensual (recomendado: $50 USD)

### Paso 2: Comprar Créditos
- **Mínimo:** $5 USD
- **Recomendado:** $20-50 USD (dura 3-6 meses)
- Los créditos **NO expiran**

### Paso 3: Verificar Balance
```bash
# Ver cuántos créditos tienes
curl https://api.openai.com/v1/dashboard/billing/credit_grants \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

---

## 2. 🧠 Mejorar Inteligencia del Bot

### Modelos Disponibles

#### ACTUAL (Básico)
```env
OPENAI_MODEL=gpt-4o-mini
```
- ✅ Barato: ~$1/año para 10 posts diarios
- ❌ Menos creativo
- ❌ Menos profesional

#### RECOMENDADO ⭐ (Ya Configurado)
```env
OPENAI_MODEL=gpt-4o
```
- ✅ 10x mejor calidad
- ✅ Más profesional y persuasivo
- ✅ Mejor para "anuncios llamativos"
- ✅ Entiende emociones mejor
- ✅ Solo ~$11/año para 10 posts diarios

#### MÁXIMO (Profesional)
```env
OPENAI_MODEL=gpt-4-turbo
```
- ✅ Máxima calidad
- ✅ Creatividad superior
- ✅ Análisis profundo
- 💰 ~$37/año para 10 posts diarios

### Cómo Cambiar de Modelo

**Opción 1: Editar .env**
```bash
nano .env
# Cambiar OPENAI_MODEL=gpt-4o-mini a:
# OPENAI_MODEL=gpt-4o (recomendado)
# OPENAI_MODEL=gpt-4-turbo (máxima calidad)
```

**Opción 2: Desde Telegram**
```
/teach Usar modelo gpt-4-turbo para máxima calidad
```

Luego reinicia el bot:
```bash
./restart_bot.sh
```

---

## 3. 🔍 Monitoreo Automático

### Configurar Monitoreo Cada 5 Minutos

**Linux/Mac (Cron):**
```bash
# Hacer ejecutable el monitor
chmod +x monitor_bot.sh

# Editar crontab
crontab -e

# Agregar esta línea (revisa cada 5 minutos):
*/5 * * * * /workspaces/sacred-rebirth-ai-agent/monitor_bot.sh

# O cada 1 minuto (más confiable):
* * * * * /workspaces/sacred-rebirth-ai-agent/monitor_bot.sh
```

**Windows (Task Scheduler):**
1. Abrir "Programador de Tareas"
2. Crear Tarea Básica
3. Nombre: "Monitor Bot Telegram"
4. Desencadenador: "Repetir cada 5 minutos"
5. Acción: Ejecutar `monitor_bot.sh`

### Verificar Estado Manualmente
```bash
# Ver si el bot está corriendo
ps aux | grep telegram_bot.py

# Ver últimas 50 líneas del log
tail -50 telegram_bot.log

# Ver errores
tail -50 bot_errors.log

# Reiniciar manualmente
./restart_bot.sh
```

---

## 4. 🌐 Servidor 24/7 (Recomendado)

### Opción 1: Replit (GRATIS) ⭐ Más Fácil
1. Ve a https://replit.com
2. Crea cuenta gratuita
3. "Create Repl" → "Import from GitHub"
4. Pega tu repositorio
5. Agrega archivo `.replit`:
```
run = "python telegram_bot.py"
```
6. Agrega Secrets (variables .env)
7. Click "Run" - ¡Ya está 24/7!

**Ventajas:**
- ✅ Gratis
- ✅ Siempre activo
- ✅ Fácil de configurar
- ✅ No necesitas servidor

### Opción 2: PythonAnywhere (GRATIS)
1. https://www.pythonanywhere.com
2. Cuenta gratuita
3. Subir código
4. Configurar "Always-on task"
5. Bot corre 24/7 gratis

### Opción 3: Railway ($5/mes)
1. https://railway.app
2. Connect GitHub
3. Deploy automático
4. Bot 24/7 con mejor rendimiento

### Opción 4: VPS Propio ($5-10/mes)
**DigitalOcean, Linode, Vultr:**
```bash
# SSH a tu servidor
ssh root@tu-ip

# Instalar Python
apt update && apt install python3 python3-pip

# Clonar proyecto
git clone tu-repo
cd sacred-rebirth-ai-agent

# Instalar dependencias
pip3 install -r requirements.txt

# Crear servicio systemd
sudo nano /etc/systemd/system/telegram-bot.service
```

**Contenido del servicio:**
```ini
[Unit]
Description=Sacred Rebirth Telegram Bot
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/root/sacred-rebirth-ai-agent
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Activar:**
```bash
sudo systemctl enable telegram-bot
sudo systemctl start telegram-bot
sudo systemctl status telegram-bot
```

---

## 5. 💾 Respaldo y Seguridad

### Respaldo Automático de knowledge_base.txt

**Script de respaldo:**
```bash
#!/bin/bash
# backup_knowledge.sh

DATE=$(date +%Y%m%d_%H%M%S)
cp knowledge_base.txt "backups/knowledge_base_$DATE.txt"

# Mantener solo últimos 30 respaldos
ls -t backups/knowledge_base_*.txt | tail -n +31 | xargs rm -f
```

**Automatizar (cada día a las 3 AM):**
```bash
crontab -e
# Agregar:
0 3 * * * /workspaces/sacred-rebirth-ai-agent/backup_knowledge.sh
```

### Proteger API Keys
```bash
# Nunca subas .env a GitHub
echo ".env" >> .gitignore

# Rotar API key cada 3 meses
# Ve a https://platform.openai.com/api-keys
# "Revoke" key vieja → "Create new"
```

### Monitoreo de Uso/Costos
1. Ve a: https://platform.openai.com/usage
2. Configura alertas de presupuesto
3. Revisa semanalmente

---

## 6. 🚨 Solución de Problemas

### Bot No Responde
```bash
# 1. Ver errores
tail -100 telegram_bot.log

# 2. Verificar proceso
ps aux | grep telegram_bot.py

# 3. Reiniciar
pkill -9 -f telegram_bot.py
python telegram_bot.py &

# 4. Verificar créditos OpenAI
curl https://api.openai.com/v1/models \
  -H "Authorization: Bearer $OPENAI_API_KEY"
```

### Error "Rate Limit Exceeded"
- Has alcanzado límite de requests por minuto
- Solución: Espera 1 minuto o mejora tier de OpenAI
- Tier 1 (después de $5): 500 requests/minuto

### Error "Insufficient Credits"
```bash
# Verificar balance
# Ve a: https://platform.openai.com/account/billing/overview
# Agregar más créditos
```

### Bot Se Cae Constantemente
1. Revisa `bot_errors.log`
2. Verifica RAM del servidor
3. Aumenta RestartSec en systemd
4. Considera usar servidor más potente

---

## 7. 📊 Estadísticas y Métricas

### Ver Uso Real
```bash
# Contar mensajes procesados hoy
grep "$(date +%Y-%m-%d)" telegram_bot.log | wc -l

# Ver último error
grep ERROR telegram_bot.log | tail -1

# Ver modelo en uso
grep "model=" telegram_bot.py
```

### Calcular Costos
```python
# En Telegram, escribe:
# "¿cuánto he gastado en la API?"
# El bot puede calcular basado en logs
```

---

## ✅ Checklist de Mantenimiento

### Diario
- [ ] Verificar que bot responde en Telegram
- [ ] Revisar `tail -20 telegram_bot.log`

### Semanal
- [ ] Revisar uso de API en OpenAI dashboard
- [ ] Ver `bot_errors.log` para errores
- [ ] Probar comandos: /status, /help

### Mensual
- [ ] Verificar balance de créditos OpenAI
- [ ] Respaldar `knowledge_base.txt`
- [ ] Actualizar información con `/teach`
- [ ] Revisar calidad de contenido generado

### Cada 3 Meses
- [ ] Rotar API key de OpenAI (seguridad)
- [ ] Evaluar cambio de modelo (si hay nuevos)
- [ ] Limpiar logs antiguos

---

## 🎓 Mejores Prácticas

1. **Siempre ten $5+ en créditos** - Evita interrupciones
2. **Usa gpt-4o** - Balance perfecto calidad/precio
3. **Monitoreo automático** - Configura cron/systemd
4. **Servidor dedicado** - Replit/PythonAnywhere gratis
5. **Respaldos regulares** - knowledge_base.txt es oro
6. **Revisa logs** - Detecta problemas temprano
7. **Actualiza conocimiento** - Usa `/teach` frecuentemente

---

## 📞 Soporte

**Si algo falla:**
1. Revisa esta guía
2. Consulta logs: `telegram_bot.log` y `bot_errors.log`
3. Verifica créditos OpenAI
4. Reinicia: `./restart_bot.sh`

**Recursos:**
- OpenAI Status: https://status.openai.com
- Telegram Bot API: https://core.telegram.org/bots/api
- Este proyecto: /workspaces/sacred-rebirth-ai-agent

---

¡Tu bot ahora es 10x más inteligente y estará siempre funcional! 🚀
