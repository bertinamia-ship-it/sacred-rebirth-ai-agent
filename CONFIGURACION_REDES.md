# 🔗 Guía de Configuración - Redes Sociales y APIs

Esta guía te ayudará a conectar tu bot de Telegram con todas tus cuentas para automatizar:
- 📱 Publicaciones en Instagram y Facebook
- 📧 Campañas de email
- 📞 Captura de leads y agendamiento de llamadas

---

## 📱 PASO 1: Conectar Instagram y Facebook (Meta Business)

Para que el bot pueda publicar automáticamente en tus redes sociales.

### 1.1. Requisitos Previos
- ✅ Tener una **Página de Facebook** (no perfil personal)
- ✅ Tener una **Cuenta de Instagram Business** vinculada a esa página
- ✅ Ser administrador de ambas cuentas

### 1.2. Crear App de Facebook

1. **Ve a:** https://developers.facebook.com/
2. **Click en:** "Mis Apps" (esquina superior derecha)
3. **Click en:** "Crear App"
4. **Selecciona:** "Empresa" como tipo de app
5. **Completa:**
   - Nombre de la app: `Sacred Rebirth Marketing Bot`
   - Email de contacto: `rebirthsecred@gmail.com`
6. **Click:** "Crear App"

### 1.3. Configurar Permisos

En tu nueva app:

1. **Panel izquierdo → Click en:** "Agregar producto"
2. **Busca y agrega:** 
   - ✅ "Instagram Graph API"
   - ✅ "Facebook Login"
   - ✅ "Marketing API"

### 1.4. Obtener Access Token

1. **Panel izquierdo → Click:** "Herramientas" → "Explorador de la API Graph"
2. **Selecciona tu app** en el menú desplegable
3. **Click en:** "Generar token de acceso"
4. **Selecciona los permisos:**
   - ✅ `pages_manage_posts`
   - ✅ `pages_read_engagement`
   - ✅ `instagram_basic`
   - ✅ `instagram_content_publish`
   - ✅ `business_management`
5. **Click:** "Generar token de acceso"
6. **COPIA EL TOKEN** (algo como: `EAABsb...`)

### 1.5. Obtener IDs de Instagram y Facebook

**Para Instagram:**
1. Ve a: https://developers.facebook.com/tools/explorer/
2. En "Obtener token" selecciona tu página
3. En la barra de búsqueda escribe: `me/accounts`
4. Click "Enviar"
5. Busca tu página y copia el `id`
6. Ahora escribe: `{PAGE_ID}?fields=instagram_business_account`
7. Copia el `instagram_business_account id`

**Para Facebook:**
1. Ve a tu página de Facebook
2. Click en "Acerca de"
3. Desplázate hacia abajo, verás "ID de la página"
4. O usa el Graph API Explorer con: `me/accounts`

---

## 📧 PASO 2: Configurar Email (SendGrid)

Para enviar campañas de email y capturar leads.

### 2.1. Crear Cuenta en SendGrid

1. **Ve a:** https://sendgrid.com/
2. **Click en:** "Start for Free" (100 emails/día gratis)
3. **Completa el registro** con tu email: `rebirthsecred@gmail.com`
4. **Verifica tu email**

### 2.2. Obtener API Key

1. **Login en SendGrid**
2. **Panel izquierdo → Settings → API Keys**
3. **Click:** "Create API Key"
4. **Nombre:** `Sacred Rebirth Marketing Bot`
5. **Permisos:** Selecciona "Full Access"
6. **Click:** "Create & View"
7. **COPIA LA API KEY** (empieza con `SG.`)
   ⚠️ Solo se muestra una vez, guárdala bien!

### 2.3. Verificar Dominio de Envío

1. **Settings → Sender Authentication**
2. **Click:** "Verify a Single Sender"
3. **Completa con tu información:**
   - From Name: `Sacred Rebirth`
   - From Email: `rebirthsecred@gmail.com`
   - Reply To: `rebirthsecred@gmail.com`
4. **Verifica el email de confirmación**

---

## 📞 PASO 3: Configurar Captura de Leads (Opcional - Calendly)

Para que los clientes puedan agendar llamadas automáticamente.

### 3.1. Crear Cuenta en Calendly

1. **Ve a:** https://calendly.com/
2. **Regístrate gratis**
3. **Configura tu disponibilidad** para llamadas

### 3.2. Crear Enlace de Agendamiento

1. **En Calendly → Event Types**
2. **Click:** "Create New Event Type"
3. **Completa:**
   - Nombre: "Consulta - Sacred Rebirth"
   - Duración: 30 minutos
   - Ubicación: Llamada de teléfono o Zoom
4. **Copia el enlace** (algo como: `calendly.com/tu-usuario/consulta`)

---

## 🔧 PASO 4: Configurar el Bot

Una vez que tengas todos los datos, pégalos aquí en este formato:

```
META_ACCESS_TOKEN: [tu token de Facebook]
INSTAGRAM_ID: [tu ID de Instagram Business]
FACEBOOK_PAGE_ID: [tu ID de página de Facebook]
SENDGRID_API_KEY: [tu key de SendGrid]
CALENDLY_LINK: [tu enlace de Calendly] (opcional)
```

Y yo configuraré todo automáticamente.

---

## ✅ CHECKLIST RÁPIDO

Antes de empezar, asegúrate de tener:

- [ ] Página de Facebook creada
- [ ] Instagram Business vinculado a esa página
- [ ] App de Facebook Developers creada
- [ ] Cuenta de SendGrid creada y verificada
- [ ] (Opcional) Cuenta de Calendly para agendamiento

---

## 🆘 ¿Necesitas Ayuda?

### Opción 1: Configuración Asistida Completa
Si prefieres que te guíe paso a paso con capturas de pantalla, dime y te creo una guía visual detallada.

### Opción 2: Configuración Básica (Solo Email)
Si solo quieres empezar con emails (más fácil), puedo configurar primero SendGrid y después agregamos Instagram/Facebook.

### Opción 3: Simulación/Testing
Puedo configurar el bot en modo "simulación" para que veas cómo funciona sin necesitar las APIs reales todavía.

---

## 💡 Recomendación

**Empieza con lo más fácil:**
1. ✅ SendGrid (5 minutos) - Para emails
2. ✅ Calendly (5 minutos) - Para agendamiento de llamadas  
3. ⏳ Meta APIs (30 minutos) - Para Instagram/Facebook

De esta forma puedes empezar a usar el bot YA para emails y leads, y después agregas las redes sociales.

¿Qué prefieres hacer primero?
