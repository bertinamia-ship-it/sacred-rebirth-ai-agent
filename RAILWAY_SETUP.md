# 🚂 Guía Completa: Subir Bot a Railway

## 🎯 ¿Qué es Railway?

Railway es un hosting profesional para tu bot que:
- ✅ Funciona 24/7 sin necesidad de tu computadora
- ✅ Se reinicia automáticamente si hay errores
- ✅ Cuesta $5/mes (incluye $5 de crédito gratis el primer mes)
- ✅ Deploy automático desde GitHub
- ✅ Logs en tiempo real
- ✅ 99.9% uptime

---

## 📋 PASO A PASO (15 minutos)

### 1️⃣ PREPARAR TU REPOSITORIO EN GITHUB

**a) Crear repositorio en GitHub:**

1. Ve a https://github.com/new
2. Nombre: `sacred-rebirth-ai-agent`
3. Privado (para proteger tus datos)
4. No agregues README, .gitignore ni license
5. Click "Create repository"

**b) Subir tu código a GitHub:**

```bash
# En tu terminal (desde tu proyecto):
cd /workspaces/sacred-rebirth-ai-agent

# Inicializar git (si no lo has hecho)
git init

# Verificar que .env está ignorado
cat .gitignore | grep .env
# Si NO sale .env, agrégalo:
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo "backups/" >> .gitignore

# Agregar todos los archivos
git add .

# Hacer commit
git commit -m "Initial commit: Sacred Rebirth AI Bot"

# Conectar con GitHub (reemplaza TU-USUARIO)
git remote add origin https://github.com/TU-USUARIO/sacred-rebirth-ai-agent.git

# Subir código
git branch -M main
git push -u origin main
```

**⚠️ IMPORTANTE:** Nunca subas .env a GitHub (ya está en .gitignore)

---

### 2️⃣ CREAR PROYECTO EN RAILWAY

1. **Ir a Railway:**
   👉 https://railway.app

2. **Login con GitHub:**
   - Click "Login with GitHub"
   - Autoriza Railway

3. **Crear nuevo proyecto:**
   - Click "New Project"
   - Selecciona "Deploy from GitHub repo"
   - Busca: `sacred-rebirth-ai-agent`
   - Click en tu repositorio

4. **Railway detectará automáticamente:**
   - ✅ Python
   - ✅ requirements.txt
   - ✅ Instalará dependencias
   - ✅ Usará configuración de railway.json

---

### 3️⃣ CONFIGURAR VARIABLES DE ENTORNO

**Muy importante:** Railway necesita las mismas variables que tu .env

1. **En Railway, click en tu proyecto**

2. **Click en "Variables"**

3. **Agregar cada variable (una por una):**

```
OPENAI_API_KEY
sk-proj-TU_API_KEY_AQUI

OPENAI_MODEL
gpt-4o-mini

TELEGRAM_BOT_TOKEN
8203101309:AAE3e0845ulWgRWnIli7d7GjxTyuUWk4Mhk

TELEGRAM_AUTHORIZED_USERS
1582665697,7085030816

TELEGRAM_BOT_USERNAME
Marketing9502_bot

BUSINESS_NAME
Sacred Rebirth

BUSINESS_WEBSITE
https://sacred-rebirth.com

BUSINESS_PHONE
+52 722 512 3413

BUSINESS_LOCATION
Valle de Bravo, Mexico

INSTAGRAM_HANDLE
@sacredrebirthvalle

FACEBOOK_HANDLE
sacredbirthretreats
```

**Cómo agregar:**
- Click "New Variable"
- Pegar nombre de variable (ej: OPENAI_API_KEY)
- Pegar valor
- Click "Add"
- Repetir para cada variable

---

### 4️⃣ DEPLOY AUTOMÁTICO

Railway ahora:

1. ✅ Detectará cambios en GitHub
2. ✅ Instalará dependencias: `pip install -r requirements.txt`
3. ✅ Ejecutará: `python telegram_bot.py`
4. ✅ Bot estará online en ~2 minutos

**Ver progreso:**
- Tab "Deployments" → Ver build en tiempo real
- Tab "Logs" → Ver logs del bot (como `tail -f telegram_bot.log`)

---

### 5️⃣ VERIFICAR QUE FUNCIONA

**a) Ver logs en Railway:**
1. Click en "Logs"
2. Deberías ver:
   ```
   🚀 Iniciando bot de Telegram...
   ✅ Bot iniciado! Esperando mensajes...
   ```

**b) Probar en Telegram:**
1. Abre @Marketing9502_bot
2. Envía: `/start`
3. Debería responder inmediatamente
4. Envía: "crea un post sobre ayahuasca"
5. Debería generar contenido

**c) Ver en logs de Railway:**
- Verás cada mensaje procesado
- Verás qué modelo usa (básico/pro/ultra)

---

## 🔄 ACTUALIZAR EL BOT (DEPLOY AUTOMÁTICO)

Cada vez que quieras actualizar el bot:

```bash
# Hacer cambios en tu código local
nano telegram_bot.py  # O el archivo que quieras editar

# Guardar cambios en GitHub
git add .
git commit -m "Actualización: descripción del cambio"
git push

# Railway detectará el push y hará deploy automáticamente
# En ~1-2 minutos el bot estará actualizado
```

---

## 📊 MONITOREO Y MANTENIMIENTO

### Ver estadísticas en Railway:

1. **Métricas:**
   - CPU usage
   - Memory usage
   - Network

2. **Logs en tiempo real:**
   - Tab "Logs"
   - Ver todos los mensajes procesados
   - Ver errores si los hay

3. **Deployments:**
   - Historial de todos los deploys
   - Rollback a versión anterior si algo falla

### Comandos útiles:

**Ver logs del bot:**
- En Railway → Tab "Logs"

**Reiniciar bot:**
- Settings → "Restart Deployment"

**Ver uso/costos de Railway:**
- Dashboard → Ver créditos usados
- $5/mes incluye: 500 horas de ejecución (suficiente para 24/7)

---

## 🚨 SOLUCIÓN DE PROBLEMAS

### Bot no inicia:

**Ver error:**
1. Railway → Logs
2. Buscar líneas con ERROR

**Errores comunes:**

```
❌ "TELEGRAM_BOT_TOKEN not set"
→ Falta variable en Railway
→ Settings → Variables → Agregar TELEGRAM_BOT_TOKEN

❌ "No module named 'telegram'"
→ requirements.txt no se instaló
→ Verificar que railway.json existe
→ Redeploy: Settings → Redeploy

❌ "Unauthorized"
→ Token incorrecto o revocado
→ Generar nuevo token con @BotFather
→ Actualizar en Railway Variables

❌ "Connection timeout"
→ Problema de red de Railway (raro)
→ Settings → Restart
```

### Bot se cae constantemente:

1. **Ver logs** para encontrar error recurrente
2. **Aumentar memoria** (si dice "Out of memory"):
   - Settings → Change plan → Hobby ($5/mes con más RAM)
3. **Verificar créditos OpenAI:**
   - https://platform.openai.com/account/billing
   - Agregar más créditos si se acabaron

### Ver cuánto gastas:

**Railway:**
- Dashboard → Usage
- $5/mes plan Hobby (suficiente para bot 24/7)

**OpenAI:**
- Usa `/stats` en el bot
- O https://platform.openai.com/usage

---

## 💰 COSTOS MENSUALES

```
Railway:
• Plan Hobby: $5/mes
• Incluye: 500 horas/mes (suficiente para 24/7)
• Uptime: 99.9%

OpenAI (con sistema inteligente):
• Uso normal (300 posts/mes): $0.15/mes
• Uso intenso (1000 posts/mes): $0.50/mes

TOTAL: ~$5-6/mes para bot 24/7 profesional
```

---

## ✅ CHECKLIST FINAL

Antes de dar por terminado:

- [ ] Repositorio en GitHub creado
- [ ] Código subido sin .env
- [ ] Proyecto en Railway creado
- [ ] Variables de entorno configuradas (11 variables)
- [ ] Deploy exitoso (verde en Railway)
- [ ] Logs muestran "Bot iniciado"
- [ ] Bot responde en Telegram
- [ ] `/stats` funciona
- [ ] `/models` funciona
- [ ] Sistema híbrido detecta palabras clave

---

## 🎓 TIPS PROFESIONALES

1. **Usar branches para testing:**
   ```bash
   git checkout -b test-feature
   # Hacer cambios
   git push origin test-feature
   # Crear PR en Railway para testing antes de merge
   ```

2. **Monitoreo con cron:**
   Railway puede enviar webhooks si el bot se cae

3. **Backups automáticos:**
   GitHub ya es tu backup de código
   Para knowledge_base.txt, usa script de backup

4. **Logs persistentes:**
   Railway guarda logs por 7 días
   Para más tiempo, configura external logging

5. **Variables sensibles:**
   NUNCA las pongas en código
   SIEMPRE en Railway Variables

---

## 📞 SOPORTE

**Railway:**
- Docs: https://docs.railway.app
- Discord: https://discord.gg/railway
- Status: https://status.railway.app

**Errores del bot:**
1. Railway Logs (primero)
2. /stats en Telegram
3. OpenAI status: https://status.openai.com

---

## 🚀 PRÓXIMOS PASOS (OPCIONALES)

Después de tener el bot en Railway:

1. **Custom domain:**
   - Si tienes sitio web, puedes agregar dominio

2. **Webhooks:**
   - Recibir notificaciones en tu email si bot falla

3. **Staging environment:**
   - Crear segunda instancia para testing

4. **CI/CD avanzado:**
   - Tests automáticos antes de deploy

5. **Escalado:**
   - Si crece mucho, Railway escala automáticamente

---

¡Con esto tu bot Sacred Rebirth estará 24/7 en la nube profesionalmente! 🎉
