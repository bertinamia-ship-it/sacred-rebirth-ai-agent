#!/bin/bash
# 🔄 Script simple para reiniciar el bot

echo "🛑 Deteniendo bot..."
pkill -9 -f telegram_bot.py
sleep 2

echo "🚀 Iniciando bot..."
nohup python /workspaces/sacred-rebirth-ai-agent/telegram_bot.py > telegram_bot.log 2>&1 &
sleep 3

if pgrep -f "telegram_bot.py" > /dev/null; then
    echo "✅ Bot reiniciado correctamente"
    echo "📊 Ver logs: tail -f telegram_bot.log"
else
    echo "❌ Error al reiniciar bot"
    echo "🔍 Ver errores: cat telegram_bot.log"
    exit 1
fi
