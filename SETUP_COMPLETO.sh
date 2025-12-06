#!/bin/bash
# 🚀 SETUP COMPLETO - Sacred Rebirth AI Bot
# Este script configura TODO automáticamente

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🚀 CONFIGURACIÓN COMPLETA DEL BOT                        ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""

# 1. Verificar permisos de scripts
echo "1️⃣  Configurando permisos de scripts..."
chmod +x /workspaces/sacred-rebirth-ai-agent/restart_bot.sh
chmod +x /workspaces/sacred-rebirth-ai-agent/monitor_bot.sh
chmod +x /workspaces/sacred-rebirth-ai-agent/backup_knowledge.sh
echo "   ✅ Permisos configurados"
echo ""

# 2. Crear directorio de respaldos
echo "2️⃣  Creando sistema de respaldos..."
mkdir -p /workspaces/sacred-rebirth-ai-agent/backups
./backup_knowledge.sh
echo "   ✅ Sistema de respaldos activo"
echo ""

# 3. Reiniciar bot con nueva configuración
echo "3️⃣  Reiniciando bot con sistema híbrido IA..."
./restart_bot.sh
echo ""

# 4. Configurar monitoreo automático (cron)
echo "4️⃣  Configurando monitoreo automático..."
echo "   ℹ️  Para activar monitoreo cada 5 minutos, ejecuta:"
echo "   "
echo "   crontab -e"
echo "   "
echo "   Luego agrega esta línea:"
echo "   */5 * * * * /workspaces/sacred-rebirth-ai-agent/monitor_bot.sh"
echo ""

# 5. Verificar estado
echo "5️⃣  Verificando estado del bot..."
sleep 3

if pgrep -f "telegram_bot.py" > /dev/null; then
    BOT_PID=$(pgrep -f "telegram_bot.py")
    echo "   ✅ Bot corriendo (PID: $BOT_PID)"
else
    echo "   ❌ Bot no está corriendo"
    echo "   Intenta: ./restart_bot.sh"
fi
echo ""

# Resumen
echo "╔════════════════════════════════════════════════════════════╗"
echo "║   ✅ CONFIGURACIÓN COMPLETA                                ║"
echo "╚════════════════════════════════════════════════════════════╝"
echo ""
echo "🎯 SISTEMA HÍBRIDO ACTIVADO:"
echo "   • Tareas básicas → gpt-4o-mini (rápido y barato)"
echo "   • Tareas profesionales → gpt-4o (calidad premium)"
echo "   • Tareas ultra → gpt-4-turbo (máxima calidad)"
echo ""
echo "📊 NUEVO COMANDO DISPONIBLE:"
echo "   /models - Ver modelos de IA y cómo activarlos"
echo ""
echo "🔧 SCRIPTS DISPONIBLES:"
echo "   ./restart_bot.sh     - Reiniciar bot"
echo "   ./monitor_bot.sh     - Verificar estado"
echo "   ./backup_knowledge.sh - Crear respaldo"
echo ""
echo "📝 PRÓXIMOS PASOS:"
echo ""
echo "1. PAGAR OPENAI API:"
echo "   👉 https://platform.openai.com/settings/organization/billing/overview"
echo "   • Agregar $20-50 USD (dura 3-6 meses)"
echo ""
echo "2. PROBAR BOT EN TELEGRAM:"
echo "   • Abre @Marketing9502_bot"
echo "   • Escribe: 'crea un anuncio PROFESIONAL sobre ayahuasca'"
echo "   • Verás: '🤖 Usando modelo: gpt-4o (✨ PROFESIONAL)' en los logs"
echo ""
echo "3. CONFIGURAR SERVIDOR 24/7 (Opcional):"
echo "   • Opción A: Replit.com (GRATIS, 10 min setup)"
echo "   • Opción B: Railway.app ($5/mes, profesional)"
echo "   • Instrucciones en MANTENIMIENTO.md"
echo ""
echo "4. ACTIVAR MONITOREO AUTOMÁTICO:"
echo "   crontab -e"
echo "   # Agregar: */5 * * * * $PWD/monitor_bot.sh"
echo ""
echo "5. LEER DOCUMENTACIÓN:"
echo "   • MANTENIMIENTO.md - Guía completa"
echo "   • BOTS_GUIA.md - Configuración avanzada"
echo ""
echo "═══════════════════════════════════════════════════════════"
echo "¡Tu bot ahora es INTELIGENTE y se auto-gestiona! 🚀"
echo "═══════════════════════════════════════════════════════════"
