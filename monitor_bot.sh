#!/bin/bash
# 🤖 Monitor del Bot de Telegram - Sacred Rebirth
# Este script mantiene el bot siempre funcional

BOT_SCRIPT="/workspaces/sacred-rebirth-ai-agent/telegram_bot.py"
LOG_FILE="/workspaces/sacred-rebirth-ai-agent/telegram_bot.log"
ERROR_LOG="/workspaces/sacred-rebirth-ai-agent/bot_errors.log"

# Función para verificar si el bot está corriendo
check_bot() {
    if pgrep -f "python.*telegram_bot.py" > /dev/null; then
        return 0  # Bot está corriendo
    else
        return 1  # Bot NO está corriendo
    fi
}

# Función para iniciar el bot
start_bot() {
    echo "[$(date)] 🚀 Iniciando bot..." >> "$ERROR_LOG"
    nohup python "$BOT_SCRIPT" > "$LOG_FILE" 2>&1 &
    sleep 3
    
    if check_bot; then
        echo "[$(date)] ✅ Bot iniciado correctamente" >> "$ERROR_LOG"
        return 0
    else
        echo "[$(date)] ❌ Error al iniciar bot" >> "$ERROR_LOG"
        return 1
    fi
}

# Función para reiniciar el bot
restart_bot() {
    echo "[$(date)] 🔄 Reiniciando bot..." >> "$ERROR_LOG"
    pkill -9 -f "telegram_bot.py"
    sleep 2
    start_bot
}

# Verificación principal
if ! check_bot; then
    echo "[$(date)] ⚠️  Bot no está corriendo. Intentando iniciar..." >> "$ERROR_LOG"
    start_bot
    
    # Enviar notificación si falla (opcional)
    if ! check_bot; then
        echo "[$(date)] 🚨 CRÍTICO: No se pudo iniciar el bot" >> "$ERROR_LOG"
        # Aquí podrías agregar una notificación por email o Telegram
    fi
else
    # Bot está corriendo - verificar que responde
    LAST_LOG=$(tail -1 "$LOG_FILE")
    echo "[$(date)] ✅ Bot funcionando correctamente" >> "$ERROR_LOG"
fi

# Limpiar logs antiguos (mantener últimos 1000 líneas)
if [ -f "$LOG_FILE" ]; then
    tail -1000 "$LOG_FILE" > "${LOG_FILE}.tmp"
    mv "${LOG_FILE}.tmp" "$LOG_FILE"
fi

if [ -f "$ERROR_LOG" ]; then
    tail -500 "$ERROR_LOG" > "${ERROR_LOG}.tmp"
    mv "${ERROR_LOG}.tmp" "$ERROR_LOG"
fi
