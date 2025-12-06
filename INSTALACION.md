# 🚀 Guía de Instalación - Sacred Rebirth AI Agent

## Requisitos Previos

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Cuenta de OpenAI con API key
- (Opcional) Cuentas en Meta, SendGrid para funcionalidad completa

## Paso 1: Verificar Python

```bash
python --version
# Debe mostrar Python 3.11 o superior
```

Si no tienes Python instalado:
- **Mac**: `brew install python@3.11`
- **Ubuntu/Debian**: `sudo apt install python3.11`
- **Windows**: Descargar de [python.org](https://python.org)

## Paso 2: Clonar o Descargar el Proyecto

```bash
# Si tienes el proyecto en Git
git clone <tu-repo-url>
cd sacred-rebirth-ai-agent

# O simplemente navega a la carpeta del proyecto
cd /ruta/a/sacred-rebirth-ai-agent
```

## Paso 3: Instalar Dependencias

```bash
pip install -r requirements.txt
```

**Nota**: Si tienes problemas con permisos, usa:
```bash
pip install --user -r requirements.txt
```

O crea un entorno virtual (recomendado):
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Paso 4: Configurar Variables de Entorno

### 4.1. Copiar archivo de ejemplo
```bash
cp .env.example .env
```

### 4.2. Obtener OpenAI API Key

1. Ve a https://platform.openai.com/api-keys
2. Inicia sesión o crea una cuenta
3. Click en "Create new secret key"
4. Copia la key (empieza con `sk-...`)

### 4.3. Editar archivo .env

```bash
nano .env
# O usa cualquier editor: code .env, vim .env, etc.
```

**Configuración mínima:**
```env
OPENAI_API_KEY=sk-tu-api-key-real-aqui
OPENAI_MODEL=gpt-4-turbo-preview
```

### 4.4. (Opcional) Configurar APIs adicionales

**Para publicar en Instagram/Facebook:**
1. Ve a https://developers.facebook.com/
2. Crea una App de Facebook
3. Obtén tu Access Token
4. Agrega a `.env`:
```env
META_ACCESS_TOKEN=tu-token-aqui
INSTAGRAM_BUSINESS_ACCOUNT_ID=tu-ig-id
FACEBOOK_PAGE_ID=tu-fb-page-id
```

**Para enviar emails con SendGrid:**
1. Ve a https://sendgrid.com/
2. Crea cuenta y obtén API Key
3. Agrega a `.env`:
```env
SENDGRID_API_KEY=SG.tu-sendgrid-key
EMAIL_FROM=rebirthsecred@gmail.com
```

## Paso 5: Verificar Instalación

```bash
python main.py --help
```

Deberías ver el menú de ayuda del programa.

## Paso 6: Probar con Ejemplos

```bash
# Ejecutar ejemplos interactivos
python ejemplos.py
```

O prueba generar un post rápido:
```bash
python main.py --mode social --platform instagram --topic "Ayahuasca"
```

## ✅ Instalación Completa!

Si llegaste hasta aquí sin errores, ¡estás listo para usar el agente!

### Próximos Pasos

1. Lee **GUIA_USO.md** para conocer todas las funcionalidades
2. Ejecuta `python main.py` para el menú interactivo
3. Prueba los ejemplos en `python ejemplos.py`
4. Configura automatización diaria (ver sección de Cron en GUIA_USO.md)

## 🐛 Solución de Problemas Comunes

### Error: "No module named 'crewai'"
```bash
pip install crewai crewai-tools
```

### Error: "ModuleNotFoundError: No module named 'openai'"
```bash
pip install openai
```

### Error: "OPENAI_API_KEY not set"
Asegúrate de:
1. Tener el archivo `.env` en la raíz del proyecto
2. Que contenga `OPENAI_API_KEY=sk-...`
3. Reiniciar el terminal después de editar `.env`

### Error al instalar dependencias
```bash
# Actualizar pip primero
pip install --upgrade pip

# Luego instalar requisitos
pip install -r requirements.txt
```

### Problemas con Python 3.11
Si no puedes instalar Python 3.11, el proyecto también funciona con Python 3.9+:
```bash
python3.9 -m pip install -r requirements.txt
python3.9 main.py
```

## 📞 Soporte

Si tienes problemas con la instalación:
1. Revisa esta guía completamente
2. Consulta GUIA_USO.md
3. Contacta: rebirthsecred@gmail.com

---

¡Bienvenido al futuro del marketing automatizado con IA! 🚀
