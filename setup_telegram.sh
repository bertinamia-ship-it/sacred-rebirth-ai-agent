#!/bin/bash
# Script de configuración rápida para bot de Telegram

echo "🤖 Configuración Rápida - Bot de Telegram"
echo "========================================"
echo ""

# Verificar si ya existe TELEGRAM_BOT_TOKEN
if grep -q "^TELEGRAM_BOT_TOKEN=.*[^_here]" .env 2>/dev/null; then
    echo "✅ Ya tienes un TELEGRAM_BOT_TOKEN configurado"
    echo ""
else
    echo "📱 Paso 1: Crear el bot en Telegram"
    echo "------------------------------------"
    echo "1. Abre Telegram y busca: @BotFather"
    echo "2. Envíale: /newbot"
    echo "3. Sigue las instrucciones"
    echo "4. Copia el TOKEN que te da"
    echo ""
    read -p "Pega tu TOKEN de Telegram: " TELEGRAM_TOKEN
    
    if [ -z "$TELEGRAM_TOKEN" ]; then
        echo "❌ No ingresaste un token. Saliendo..."
        exit 1
    fi
    
    # Agregar al .env
    if [ -f .env ]; then
        # Reemplazar si existe
        sed -i.bak "s|^TELEGRAM_BOT_TOKEN=.*|TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN|" .env
        echo "✅ Token agregado a .env"
    else
        echo "TELEGRAM_BOT_TOKEN=$TELEGRAM_TOKEN" >> .env
        echo "✅ Archivo .env creado con el token"
    fi
fi

echo ""
echo "📱 Paso 2: Obtener tu User ID"
echo "------------------------------------"
echo "1. Busca en Telegram: @userinfobot"
echo "2. Envíale cualquier mensaje"
echo "3. Te dirá tu ID (número)"
echo ""
read -p "Ingresa tu User ID: " USER_ID

if [ -z "$USER_ID" ]; then
    echo "⚠️ No ingresaste User ID. Continuando sin restricciones..."
else
    # Agregar al .env
    if grep -q "^TELEGRAM_AUTHORIZED_USERS=" .env 2>/dev/null; then
        sed -i.bak "s|^TELEGRAM_AUTHORIZED_USERS=.*|TELEGRAM_AUTHORIZED_USERS=$USER_ID|" .env
    else
        echo "TELEGRAM_AUTHORIZED_USERS=$USER_ID" >> .env
    fi
    echo "✅ User ID agregado a .env"
fi

echo ""
echo "📦 Paso 3: Instalar dependencias"
echo "------------------------------------"
pip install python-telegram-bot --quiet
echo "✅ Dependencias instaladas"

echo ""
echo "🚀 Paso 4: Iniciar el bot"
echo "------------------------------------"
echo ""
echo "Ejecuta: python telegram_bot.py"
echo ""
echo "Luego busca tu bot en Telegram y envíale: /start"
echo ""
echo "✅ ¡Configuración completa!"
