#!/bin/bash
# 💾 Respaldo automático de knowledge_base.txt

DATE=$(date +%Y%m%d_%H%M%S)
BACKUP_DIR="/workspaces/sacred-rebirth-ai-agent/backups"

# Crear respaldo
cp /workspaces/sacred-rebirth-ai-agent/knowledge_base.txt "$BACKUP_DIR/knowledge_base_$DATE.txt"

# Mantener solo últimos 30 respaldos
ls -t "$BACKUP_DIR"/knowledge_base_*.txt | tail -n +31 | xargs rm -f 2>/dev/null

echo "[$(date)] ✅ Respaldo creado: knowledge_base_$DATE.txt"
