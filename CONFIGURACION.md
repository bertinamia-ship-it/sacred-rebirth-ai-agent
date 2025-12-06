# 🚀 GUÍA DE CONFIGURACIÓN PASO A PASO

## ✅ CHECKLIST DE CONFIGURACIÓN

Sigue estos pasos en orden de prioridad:

---

## 📋 PASO 1: Configurar OpenAI API Key (OBLIGATORIO - 5 minutos)

**🎯 PRIORIDAD: MÁXIMA - Sin esto NO funciona nada**

### ¿Qué hace?
Permite que el agente genere contenido usando IA (GPT-4)

### ¿Cómo conseguirla?

1. **Ve a:** https://platform.openai.com/api-keys

2. **Inicia sesión** (o crea cuenta si no tienes)

3. **Click en:** "Create new secret key"

4. **Copia** la key (empieza con `sk-...`)
   ⚠️ IMPORTANTE: Guárdala en un lugar seguro, solo se muestra una vez

5. **Configura en el proyecto:**
```bash
# En la terminal
cd /workspaces/sacred-rebirth-ai-agent
cp .env.example .env
nano .env
```

6. **Edita la línea:**
```
OPENAI_API_KEY=sk-TU-KEY-REAL-AQUI
```

7. **Guarda:** Ctrl+O, Enter, Ctrl+X

8. **Verifica:**
```bash
cat .env | grep OPENAI_API_KEY
```

### 💰 Costo
- **Cuenta nueva:** $5 de crédito gratis
- **Uso real:** ~$0.01-0.05 por post generado
- **Recomendado:** Cargar $10-20 para empezar

### ✅ Con esto YA PUEDES:
- ✅ Generar posts de Instagram
- ✅ Generar posts de Facebook
- ✅ Crear emails
- ✅ Planificar estrategias
- ✅ **Usar el modo CHAT** 💬

---

## 📋 PASO 2: Probar el Sistema (AHORA MISMO - 2 minutos)

Una vez configurado OpenAI:

```bash
# Modo CHAT (recomendado)
python chat.py

# Luego prueba escribiendo:
# "crea un post de instagram sobre ayahuasca"
# "genera contenido para facebook sobre el retiro"
```

O prueba el modo interactivo:
```bash
python main.py
# Selecciona opción 2 (Crear Contenido)
```

---

## 📋 PASO 3: Configurar Meta/Facebook (OPCIONAL - 30 minutos)

**🎯 PRIORIDAD: MEDIA - Solo si quieres publicar automáticamente**

### ¿Qué hace?
Permite publicar automáticamente en Instagram y Facebook

### ¿Cómo conseguirlo?

1. **Ve a:** https://developers.facebook.com/

2. **Crea una App:**
   - Tipo: "Business"
   - Nombre: "Sacred Rebirth Marketing"

3. **Agrega productos:**
   - Instagram Basic Display API
   - Facebook Login

4. **Obtén Access Token:**
   - Tools → Graph API Explorer
   - Permisos: `instagram_basic`, `instagram_content_publish`, `pages_read_engagement`, `pages_manage_posts`
   - Generate Access Token

5. **Obtén IDs:**
   - Instagram Business Account ID:
     ```
     GET /me/accounts
     Luego: GET /{page-id}?fields=instagram_business_account
     ```
   - Facebook Page ID: Está en la configuración de tu página

6. **Agrega a .env:**
```bash
META_ACCESS_TOKEN=tu-token-aqui
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu-id-de-instagram
FACEBOOK_PAGE_ID=tu-id-de-facebook
```

### ✅ Con esto ADEMÁS PUEDES:
- ✅ Publicar automáticamente en Instagram
- ✅ Publicar automáticamente en Facebook
- ✅ Programar publicaciones

### 💡 Alternativa:
**Puedes usar el agente para GENERAR el contenido** y copiarlo manualmente a tus redes. ¡Sigue siendo súper útil!

---

## 📋 PASO 4: Configurar SendGrid Email (OPCIONAL - 20 minutos)

**🎯 PRIORIDAD: BAJA - Solo si quieres enviar emails automáticos**

### ¿Qué hace?
Permite enviar campañas de email a tus leads

### ¿Cómo conseguirlo?

1. **Ve a:** https://sendgrid.com/

2. **Crea cuenta gratis:**
   - Plan Free: 100 emails/día gratis

3. **Verifica dominio/email:**
   - Settings → Sender Authentication
   - Single Sender Verification
   - Usa: rebirthsecred@gmail.com

4. **Crea API Key:**
   - Settings → API Keys
   - Create API Key
   - Full Access

5. **Agrega a .env:**
```bash
SENDGRID_API_KEY=SG.tu-key-aqui
EMAIL_FROM=rebirthsecred@gmail.com
```

### ✅ Con esto ADEMÁS PUEDES:
- ✅ Enviar campañas de email automáticas
- ✅ Nutrir leads automáticamente
- ✅ Seguimiento personalizado

### 💡 Alternativa:
El agente genera el contenido del email y tú lo copias a tu plataforma de email actual.

---

## 🎯 RESUMEN DE PRIORIDADES

### ⚡ HACER AHORA (5 min):
1. ✅ Configurar OPENAI_API_KEY
2. ✅ Probar con `python chat.py`

### 📅 HACER HOY (30 min):
3. ⚙️ Configurar Meta/Facebook (si quieres publicar auto)

### 📅 HACER ESTA SEMANA (20 min):
4. 📧 Configurar SendGrid (si quieres emails auto)

---

## 💬 MODO CHAT - TU ASISTENTE PERSONAL

Una vez configurado OpenAI, usa el modo chat:

```bash
python chat.py
```

**Ejemplos de lo que puedes decir:**

```
💬 Tú: "crea un post de instagram sobre los beneficios de la ayahuasca"
🤖 Agente: [genera el post completo]

💬 Tú: "necesito contenido para facebook sobre el retiro de enero"
🤖 Agente: [genera post promocional]

💬 Tú: "hazme una campaña completa"
🤖 Agente: [crea estrategia, contenido IG/FB, emails, todo]

💬 Tú: "muéstrame los leads"
🤖 Agente: [muestra base de datos de leads]

💬 Tú: "envía un email educativo"
🤖 Agente: [crea y envía email sobre preparación]
```

---

## 🆘 SOPORTE

Si algo no funciona:

1. **Verifica .env existe:**
   ```bash
   ls -la .env
   ```

2. **Verifica API key correcta:**
   ```bash
   cat .env | grep OPENAI_API_KEY
   ```

3. **Prueba conexión:**
   ```bash
   python -c "from openai import OpenAI; client = OpenAI(); print('✅ OpenAI conectado')"
   ```

4. **Revisa logs de error** y comparte si necesitas ayuda

---

## 🎉 ¡LISTO!

Con solo OPENAI_API_KEY configurado ya tienes:
- ✅ Generación de contenido IA
- ✅ Modo chat interactivo
- ✅ Planificación estratégica
- ✅ Gestión de leads
- ✅ Todo funcional al 90%

¡El agente está listo para trabajar! 🚀
