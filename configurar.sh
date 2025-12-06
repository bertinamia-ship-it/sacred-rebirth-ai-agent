#!/bin/bash
# 🔧 Script de Configuración Automática - Sacred Rebirth AI Agent

echo "╔═══════════════════════════════════════════════════════════╗"
echo "║                                                           ║"
echo "║       🔧 CONFIGURACIÓN - Sacred Rebirth AI Agent         ║"
echo "║                                                           ║"
echo "╚═══════════════════════════════════════════════════════════╝"
echo ""

# Colores
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Verificar si .env ya existe
if [ -f .env ]; then
    echo -e "${YELLOW}⚠️  El archivo .env ya existe${NC}"
    read -p "¿Quieres reconfigurarlo? (s/n): " respuesta
    if [[ ! $respuesta =~ ^[Ss]$ ]]; then
        echo "Saliendo sin cambios"
        exit 0
    fi
    echo "Creando backup..."
    cp .env .env.backup
    echo -e "${GREEN}✅ Backup guardado en .env.backup${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  PASO 1: Configuración de OpenAI (OBLIGATORIO)"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Para obtener tu API Key:"
echo "1. Ve a: ${BLUE}https://platform.openai.com/api-keys${NC}"
echo "2. Inicia sesión o crea cuenta"
echo "3. Click en 'Create new secret key'"
echo "4. Copia la key (empieza con sk-...)"
echo ""

read -p "Ingresa tu OpenAI API Key: " openai_key

if [[ $openai_key != sk-* ]]; then
    echo -e "${RED}❌ Error: La API key debe empezar con 'sk-'${NC}"
    echo "Ejemplo: sk-proj-abc123..."
    exit 1
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  PASO 2: Configuración de Meta/Facebook (OPCIONAL)"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Esto permite publicar automáticamente en Instagram/Facebook"
echo ""
read -p "¿Quieres configurar Meta API ahora? (s/n): " config_meta

meta_token=""
ig_id=""
fb_id=""

if [[ $config_meta =~ ^[Ss]$ ]]; then
    echo ""
    echo "Para obtener estas credenciales:"
    echo "1. Ve a: ${BLUE}https://developers.facebook.com/${NC}"
    echo "2. Crea una app tipo 'Business'"
    echo "3. Genera Access Token con permisos de Instagram/Facebook"
    echo ""
    
    read -p "Meta Access Token: " meta_token
    read -p "Instagram Business Account ID: " ig_id
    read -p "Facebook Page ID: " fb_id
else
    echo -e "${YELLOW}⏭️  Saltando configuración de Meta (puedes hacerlo después)${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  PASO 3: Configuración de SendGrid Email (OPCIONAL)"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "Esto permite enviar emails automáticamente"
echo ""
read -p "¿Quieres configurar SendGrid ahora? (s/n): " config_sendgrid

sendgrid_key=""
email_from="rebirthsecred@gmail.com"

if [[ $config_sendgrid =~ ^[Ss]$ ]]; then
    echo ""
    echo "Para obtener API Key:"
    echo "1. Ve a: ${BLUE}https://sendgrid.com/${NC}"
    echo "2. Crea cuenta (plan Free: 100 emails/día)"
    echo "3. Settings → API Keys → Create API Key"
    echo ""
    
    read -p "SendGrid API Key: " sendgrid_key
    read -p "Email From (default: rebirthsecred@gmail.com): " input_email
    if [ ! -z "$input_email" ]; then
        email_from=$input_email
    fi
else
    echo -e "${YELLOW}⏭️  Saltando configuración de SendGrid (puedes hacerlo después)${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Creando archivo .env..."
echo "═══════════════════════════════════════════════════════════"

# Crear archivo .env
cat > .env << EOF
# API Keys
OPENAI_API_KEY=$openai_key
OPENAI_MODEL=gpt-4-turbo-preview

# Meta/Facebook/Instagram
META_ACCESS_TOKEN=${meta_token:-your_meta_access_token_here}
INSTAGRAM_BUSINESS_ACCOUNT_ID=${ig_id:-your_instagram_account_id}
FACEBOOK_PAGE_ID=${fb_id:-your_facebook_page_id}

# Email Configuration
SENDGRID_API_KEY=${sendgrid_key:-your_sendgrid_api_key_here}
EMAIL_FROM=$email_from
EMAIL_FROM_NAME=Sacred Rebirth

# Business Information
BUSINESS_NAME=Sacred Rebirth
BUSINESS_WEBSITE=https://sacred-rebirth.com
BUSINESS_PHONE=+52 722 512 3413
BUSINESS_LOCATION=Valle de Bravo, Mexico
INSTAGRAM_HANDLE=@sacredrebirthvalle
FACEBOOK_HANDLE=sacredbirthretreats

# Content Settings
POSTS_PER_DAY=2
CONTENT_LANGUAGE=es
TIMEZONE=America/Mexico_City

# Email Campaign Settings
EMAIL_CAMPAIGN_FREQUENCY=weekly
MAX_EMAILS_PER_DAY=50
EOF

echo -e "${GREEN}✅ Archivo .env creado exitosamente${NC}"

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  Verificando configuración..."
echo "═══════════════════════════════════════════════════════════"
echo ""

echo -e "${GREEN}✅ OpenAI API Key: Configurada${NC}"

if [ ! -z "$meta_token" ]; then
    echo -e "${GREEN}✅ Meta API: Configurada${NC}"
else
    echo -e "${YELLOW}⚠️  Meta API: No configurada (publicación manual)${NC}"
fi

if [ ! -z "$sendgrid_key" ]; then
    echo -e "${GREEN}✅ SendGrid: Configurado${NC}"
else
    echo -e "${YELLOW}⚠️  SendGrid: No configurado (emails manuales)${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  🎉 ¡CONFIGURACIÓN COMPLETADA!"
echo "═══════════════════════════════════════════════════════════"
echo ""

echo "Funcionalidades disponibles:"
echo ""
if [ ! -z "$openai_key" ]; then
    echo -e "${GREEN}✅ Generación de contenido con IA${NC}"
    echo -e "${GREEN}✅ Modo chat interactivo${NC}"
    echo -e "${GREEN}✅ Planificación estratégica${NC}"
    echo -e "${GREEN}✅ Gestión de leads${NC}"
fi

if [ ! -z "$meta_token" ]; then
    echo -e "${GREEN}✅ Publicación automática en Instagram/Facebook${NC}"
else
    echo -e "${YELLOW}⏭️  Publicación automática (requiere Meta API)${NC}"
fi

if [ ! -z "$sendgrid_key" ]; then
    echo -e "${GREEN}✅ Envío automático de emails${NC}"
else
    echo -e "${YELLOW}⏭️  Envío automático de emails (requiere SendGrid)${NC}"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "  📖 PRÓXIMOS PASOS"
echo "═══════════════════════════════════════════════════════════"
echo ""
echo "1️⃣  Probar el modo CHAT:"
echo "   ${BLUE}python chat.py${NC}"
echo ""
echo "2️⃣  O modo interactivo tradicional:"
echo "   ${BLUE}python main.py${NC}"
echo ""
echo "3️⃣  Generar tu primer post:"
echo "   ${BLUE}python main.py --mode social --platform instagram --topic \"Ayahuasca\"${NC}"
echo ""
echo "4️⃣  Ver documentación completa:"
echo "   ${BLUE}cat CONFIGURACION.md${NC}"
echo ""

if [ -z "$meta_token" ]; then
    echo "💡 TIP: Para configurar Meta API después, ejecuta:"
    echo "   ${BLUE}nano .env${NC}"
    echo ""
fi

if [ -z "$sendgrid_key" ]; then
    echo "💡 TIP: Para configurar SendGrid después, ejecuta:"
    echo "   ${BLUE}nano .env${NC}"
    echo ""
fi

echo "═══════════════════════════════════════════════════════════"
echo "¡Listo para automatizar tu marketing con IA! 🚀✨"
echo "═══════════════════════════════════════════════════════════"
