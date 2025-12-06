# 💾 Guía Rápida de Respaldo y Seguridad

## 🎯 ¿Por qué necesitas respaldos?

Tu `knowledge_base.txt` contiene **TODA** la información que le enseñaste al bot:
- Información de tu negocio
- Preferencias de contenido
- Datos de retiros
- Estrategias de marketing

Si se borra, **pierdes todo** y tienes que empezar de cero.

---

## 1️⃣ Respaldo Automático Local (YA CONFIGURADO ✅)

### Qué hace:
- Script `backup_knowledge.sh` crea respaldos automáticos
- Guarda en carpeta `backups/`
- Mantiene últimos 30 respaldos
- Puedes configurar cron para que corra cada día

### Cómo usar:

**Manual:**
```bash
./backup_knowledge.sh
```

**Automático (cada día a las 3 AM):**
```bash
crontab -e
# Agregar esta línea:
0 3 * * * /workspaces/sacred-rebirth-ai-agent/backup_knowledge.sh
```

### Ver respaldos:
```bash
ls -lh backups/
```

### Restaurar respaldo:
```bash
# Ver respaldos disponibles
ls backups/

# Restaurar uno específico
cp backups/knowledge_base_20251206_193001.txt knowledge_base.txt

# Reiniciar bot
./restart_bot.sh
```

---

## 2️⃣ Respaldo en Google Drive (RECOMENDADO 🌟)

### Por qué:
- Respaldos locales se pierden si se daña el servidor
- Google Drive es gratuito (15 GB)
- Acceso desde cualquier lugar
- Protección contra pérdida de datos

### Opción A: Manual (Más Fácil)

1. **Descargar archivo:**
   - Click derecho en `knowledge_base.txt` en VS Code
   - "Download"
   - Guardar en tu computadora

2. **Subir a Google Drive:**
   - Ve a https://drive.google.com
   - Crear carpeta "Sacred Rebirth Bot Backup"
   - Arrastrar `knowledge_base.txt`
   - Listo! ✅

3. **Repetir cada semana** (o cuando agregues mucha info nueva)

### Opción B: Automático con Google Drive API

Necesitas configurar API de Google Drive (más avanzado):

```bash
# Instalar librería
pip install pydrive2

# Crear script de respaldo automático
# (requiere configuración de OAuth - ver documentación de Google)
```

**Más fácil:** Usa opción manual o Dropbox (ver abajo)

---

## 3️⃣ Respaldo en Dropbox (ALTERNATIVA FÁCIL)

### Opción A: Dropbox Desktop
1. Instalar Dropbox en tu computadora
2. Crear carpeta sincronizada
3. Copiar `knowledge_base.txt` ahí
4. Se sincroniza automáticamente a la nube

### Opción B: Dropbox CLI (Servidor)
```bash
# Instalar Dropbox Uploader
cd ~
git clone https://github.com/andreafabrizi/Dropbox-Uploader.git
cd Dropbox-Uploader
./dropbox_uploader.sh

# Configurar y subir
./dropbox_uploader.sh upload /workspaces/sacred-rebirth-ai-agent/knowledge_base.txt /
```

---

## 4️⃣ Respaldo en GitHub (TÉCNICO)

### Ventajas:
- Control de versiones completo
- Historial de todos los cambios
- Gratuito e ilimitado
- Profesional

### Configuración:

**IMPORTANTE:** Antes de subir, protege tus API keys:

```bash
# 1. Verificar que .env está en .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo "backups/" >> .gitignore

# 2. Hacer commit de knowledge_base.txt
git add knowledge_base.txt
git commit -m "Backup: knowledge base actualizada $(date +%Y-%m-%d)"

# 3. Subir a GitHub
git push origin main
```

### Restaurar desde GitHub:
```bash
# Descargar última versión
git pull origin main

# Ver historial de cambios
git log knowledge_base.txt

# Restaurar versión anterior
git checkout <commit-hash> knowledge_base.txt
```

---

## 5️⃣ Seguridad de API Keys

### ⚠️ NUNCA SUBAS ESTO A INTERNET:
- `.env` (contiene tus API keys)
- `telegram_bot.log` (puede tener info sensible)
- Archivos con credenciales

### Protección:

**.gitignore ya configurado ✅**
```
.env
*.log
backups/
__pycache__/
*.pyc
```

### Respaldo seguro de .env:

**Opción 1: USB o disco duro externo**
```bash
# Copiar a USB
cp .env /media/usb/sacred-rebirth-backup.env
```

**Opción 2: Gestor de contraseñas** (Recomendado)
- 1Password
- LastPass
- Bitwarden (gratis)

Guarda ahí:
- OPENAI_API_KEY
- TELEGRAM_BOT_TOKEN
- Cualquier otra credencial

**Opción 3: Encriptado local**
```bash
# Encriptar .env
gpg -c .env  # Genera .env.gpg
# Pedirá contraseña

# Guardar .env.gpg en Google Drive
# Borrar .env sin encriptar de lugares públicos

# Desencriptar cuando necesites
gpg .env.gpg  # Genera .env de nuevo
```

---

## 6️⃣ Rotar API Keys (Cada 3 meses)

### Por qué:
- Seguridad
- Si alguien obtuvo tu key, ya no funciona
- Buena práctica

### Cómo rotar OpenAI API Key:

1. **Crear nueva key:**
   - Ve a https://platform.openai.com/api-keys
   - Click "Create new secret key"
   - Copia la nueva key

2. **Actualizar .env:**
   ```bash
   nano .env
   # Reemplazar OPENAI_API_KEY con la nueva
   ```

3. **Revocar key vieja:**
   - En el dashboard de OpenAI
   - Click en "Revoke" en la key antigua

4. **Reiniciar bot:**
   ```bash
   ./restart_bot.sh
   ```

5. **Verificar:**
   - Envía mensaje al bot
   - Debería responder normalmente

---

## 7️⃣ Monitorear Uso y Costos

### Dashboard de OpenAI:
👉 https://platform.openai.com/usage

**Qué ver:**
- Cuánto has gastado este mes
- Cuántos requests has hecho
- Qué modelo usa más

### Configurar alertas:
1. Ve a https://platform.openai.com/settings/organization/billing
2. Click "Set up payment method"
3. Configurar "Usage limit" (ej: $50/mes)
4. OpenAI te avisará si te acercas al límite

### Ver costos en tiempo real:
```bash
# Ver últimos logs del bot
tail -50 telegram_bot.log | grep "Usando modelo"

# Contar cuántos de cada tipo
grep "gpt-4o-mini" telegram_bot.log | wc -l
grep "gpt-4o" telegram_bot.log | wc -l
grep "gpt-4-turbo" telegram_bot.log | wc -l
```

---

## ✅ Checklist de Respaldo (Semanal)

- [ ] Crear respaldo manual: `./backup_knowledge.sh`
- [ ] Subir `knowledge_base.txt` a Google Drive
- [ ] Verificar que .env está respaldado en lugar seguro
- [ ] Revisar uso de OpenAI (dashboard)
- [ ] Verificar que bot está corriendo: `./monitor_bot.sh`
- [ ] Probar bot en Telegram (enviar mensaje de prueba)

---

## 🚨 Plan de Emergencia

### Si pierdes knowledge_base.txt:
1. Buscar en carpeta `backups/`
2. Restaurar el más reciente:
   ```bash
   cp backups/knowledge_base_*.txt knowledge_base.txt
   ```
3. Si no hay backups locales, descargar de Google Drive
4. Reiniciar bot: `./restart_bot.sh`

### Si pierdes .env:
1. Recuperar de gestor de contraseñas
2. Crear nuevo .env con tus keys guardadas
3. Reiniciar bot

### Si pierdes TODO:
1. Clonar repositorio de GitHub (si hiciste backup ahí)
2. Restaurar knowledge_base.txt de Google Drive
3. Recrear .env con API keys guardadas
4. Ejecutar `./SETUP_COMPLETO.sh`

---

## 📞 Soporte

Si algo falla:
1. Revisar `backups/` para archivos locales
2. Buscar en Google Drive
3. Consultar logs: `cat telegram_bot.log`
4. Ver errores: `cat bot_errors.log`

---

**Recuerda:** 15 minutos de respaldos semanales pueden salvarte horas (o días) de trabajo perdido. 🛡️
