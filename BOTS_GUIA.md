# 🤖 Guía de Bots - Telegram y WhatsApp

Este agente puede conectarse tanto a **Telegram** como a **WhatsApp** para que puedas controlarlo desde tu celular.

---

## 📱 Bot de Telegram (RECOMENDADO - Más Fácil)

### ✅ Ventajas de Telegram:
- **Gratis** y sin límites
- Configuración en **5 minutos**
- No requiere servidor público (puede correr en tu PC)
- Comandos y botones interactivos
- Más flexible y personalizable

### 🚀 Configuración Paso a Paso

#### 1. Crear el Bot en Telegram

1. Abre Telegram y busca **@BotFather**
2. Envíale el comando: `/newbot`
3. Elige un nombre (ej: "Sacred Rebirth Assistant")
4. Elige un username (debe terminar en 'bot', ej: `sacred_rebirth_bot`)
5. **BotFather te dará un TOKEN** - ¡Guárdalo!

Ejemplo de token: `1234567890:ABCdefGHIjklMNOpqrsTUVwxyz`

#### 2. Configurar el .env

Agrega tu token al archivo `.env`:

```env
# Bot de Telegram
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
TELEGRAM_AUTHORIZED_USERS=123456789,987654321
```

Para obtener tu **user ID**:
1. Busca en Telegram: **@userinfobot**
2. Envíale cualquier mensaje
3. Te dirá tu ID numérico
4. Agrégalo a `TELEGRAM_AUTHORIZED_USERS` (separa múltiples IDs con comas)

#### 3. Instalar Dependencias

```bash
pip install python-telegram-bot
```

#### 4. Iniciar el Bot

```bash
python telegram_bot.py
```

Deberías ver:
```
🤖 Inicializando Marketing Crew para Telegram...
✅ Bot de Telegram listo!
🚀 Iniciando bot de Telegram...
✅ Bot iniciado! Esperando mensajes...
```

#### 5. Usar el Bot

1. Busca tu bot en Telegram (el username que elegiste)
2. Envía `/start`
3. ¡Empieza a chatear!

**Ejemplos:**
- "Crea un post de Instagram sobre ayahuasca"
- "Muestra mi calendario de esta semana"
- "Envía email de bienvenida"
- "Programa 3 posts para mañana"

**Comandos útiles:**
- `/start` - Inicio y bienvenida
- `/help` - Ver ayuda
- `/status` - Estado del sistema
- `/calendar` - Ver calendario
- `/leads` - Ver leads

---

## 💚 Bot de WhatsApp (Requiere Servidor)

### ⚠️ Consideraciones de WhatsApp:
- Requiere **servidor público** con URL (no puede correr solo en tu PC)
- Usa **Twilio** (gratis para pruebas, luego de pago)
- Más pasos de configuración
- Mejor para uso empresarial/producción

### 🚀 Configuración WhatsApp

#### 1. Crear Cuenta en Twilio

1. Ve a https://www.twilio.com/
2. Regístrate (gratis para pruebas)
3. Ve a **Console** → **Messaging** → **Try it Out** → **Send a WhatsApp message**

#### 2. Configurar WhatsApp Sandbox (Modo Prueba)

1. En Twilio, ve a **WhatsApp Sandbox**
2. Verás un número como `+1 415 523 8886`
3. Desde tu WhatsApp, envía el código que te dan (ej: `join abc-xyz`)
4. ¡Ya estás conectado al sandbox!

#### 3. Obtener Credenciales

En Twilio Console:
- **Account SID**: Algo como `ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx`
- **Auth Token**: Tu token secreto
- **WhatsApp Number**: `whatsapp:+14155238886` (sandbox) o tu número verificado

#### 4. Configurar .env

```env
# WhatsApp (Twilio)
TWILIO_ACCOUNT_SID=ACxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
TWILIO_AUTH_TOKEN=tu_auth_token_aqui
TWILIO_WHATSAPP_NUMBER=whatsapp:+14155238886
WHATSAPP_AUTHORIZED_NUMBERS=+5491123456789,+5491198765432
```

Los números autorizados deben incluir código de país (ej: `+549` para Argentina).

#### 5. Instalar Dependencias

```bash
pip install flask twilio
```

#### 6. Exponer Servidor Públicamente

Para pruebas locales, usa **ngrok**:

```bash
# Instalar ngrok
# Mac: brew install ngrok
# O descarga de: https://ngrok.com/

# Ejecutar ngrok
ngrok http 5000
```

Ngrok te dará una URL pública como: `https://abc123.ngrok.io`

#### 7. Configurar Webhook en Twilio

1. Ve a Twilio Console → WhatsApp Sandbox Settings
2. En **"When a message comes in"**:
3. Pon tu URL: `https://abc123.ngrok.io/webhook`
4. Método: **POST**
5. Guarda

#### 8. Iniciar Bot WhatsApp

```bash
python whatsapp_bot.py
```

#### 9. Probar en WhatsApp

1. Abre WhatsApp
2. Envía mensaje al número del sandbox
3. ¡El bot responderá!

**Ejemplos:**
- "Hola"
- "Crea un post sobre retiros"
- "Estado"
- "Muestra calendario"

---

## 🎯 ¿Cuál Elegir?

### 📱 Usa **Telegram** si:
- ✅ Quieres configuración rápida (5 minutos)
- ✅ Es para uso personal o de equipo pequeño
- ✅ No tienes servidor público
- ✅ Quieres que sea **gratis**
- ✅ Prefieres comandos y botones

### 💚 Usa **WhatsApp** si:
- ✅ Tus clientes ya te contactan por WhatsApp
- ✅ Necesitas apariencia más profesional
- ✅ Tienes servidor o hosting
- ✅ Estás dispuesto a pagar (después del trial)
- ✅ Es para producción/negocio real

---

## 🔄 Mantener el Bot Corriendo 24/7

### Para Telegram (Local):

**Opción 1: Screen/Tmux (Linux/Mac)**
```bash
screen -S telegram_bot
python telegram_bot.py
# Presiona Ctrl+A, luego D para detach
# Para reconectar: screen -r telegram_bot
```

**Opción 2: Systemd (Linux - Recomendado)**
```bash
# Crear servicio
sudo nano /etc/systemd/system/sacred-telegram.service
```

Contenido:
```ini
[Unit]
Description=Sacred Rebirth Telegram Bot
After=network.target

[Service]
Type=simple
User=tu_usuario
WorkingDirectory=/ruta/a/sacred-rebirth-ai-agent
Environment="PATH=/usr/bin:/usr/local/bin"
ExecStart=/usr/bin/python3 telegram_bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Habilitar:
```bash
sudo systemctl enable sacred-telegram
sudo systemctl start sacred-telegram
sudo systemctl status sacred-telegram
```

### Para WhatsApp (Servidor):

**Opción 1: Heroku (Gratis)**
```bash
# Instalar Heroku CLI
# Crear Procfile:
echo "web: python whatsapp_bot.py" > Procfile

# Deploy
heroku create sacred-rebirth-whatsapp
git push heroku main

# Configurar variables
heroku config:set TWILIO_ACCOUNT_SID=...
heroku config:set TWILIO_AUTH_TOKEN=...
```

**Opción 2: Railway/Render**
1. Conecta tu repo de GitHub
2. Configura variables de entorno
3. Deploy automático

---

## 🔐 Seguridad

### Telegram:
- Solo usuarios autorizados (IDs en `TELEGRAM_AUTHORIZED_USERS`)
- Token del bot es secreto (no compartir)
- Puedes revocar token en @BotFather si se filtra

### WhatsApp:
- Solo números autorizados (`WHATSAPP_AUTHORIZED_NUMBERS`)
- Credenciales Twilio en `.env` (no subir a Git)
- Usa HTTPS siempre para webhooks
- En producción, migra de Sandbox a número verificado

---

## 📊 Comparación Rápida

| Característica | Telegram | WhatsApp |
|----------------|----------|----------|
| **Costo** | Gratis | Gratis (trial), luego de pago |
| **Configuración** | 5 minutos | 30+ minutos |
| **Servidor** | No necesario | Requerido |
| **Comandos** | ✅ Soportados | ⚠️ Básicos |
| **Multimedia** | ✅ Imágenes, docs | ✅ Imágenes, docs |
| **Popularidad** | Media | Alta (en LATAM) |
| **Uso empresarial** | Bueno | Excelente |

---

## 🐛 Solución de Problemas

### Telegram

**Error: "Invalid token"**
- Verifica que copiaste bien el token de @BotFather
- No debe tener espacios al inicio/final

**Bot no responde**
- Verifica que el script esté corriendo
- Revisa que tu user ID esté en `TELEGRAM_AUTHORIZED_USERS`

### WhatsApp

**Webhook no recibe mensajes**
- Verifica URL en Twilio Console
- Asegúrate que ngrok esté corriendo
- Revisa que la URL termine en `/webhook`

**Error 401 Unauthorized**
- Verifica `TWILIO_ACCOUNT_SID` y `TWILIO_AUTH_TOKEN`
- No confundas con API Key (son diferentes)

---

## 🎨 Personalización

Puedes editar los archivos `telegram_bot.py` o `whatsapp_bot.py` para:
- Cambiar mensajes de bienvenida
- Agregar más comandos
- Personalizar respuestas
- Agregar botones interactivos (Telegram)
- Enviar imágenes automáticamente

---

## 📞 Soporte

¿Problemas configurando los bots?
- Email: rebirthsecred@gmail.com
- Revisa logs en terminal
- Consulta documentación oficial:
  - Telegram: https://core.telegram.org/bots
  - Twilio: https://www.twilio.com/docs/whatsapp

---

¡Disfruta tu agente de marketing en el celular! 📱✨
