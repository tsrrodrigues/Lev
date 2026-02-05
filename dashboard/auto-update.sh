#!/bin/bash
# Auto-update dashboard (para uso com cron)
# Exemplo de cron (a cada 5 minutos):
# */5 * * * * /home/ubuntu/facilita-factory/dashboard/auto-update.sh

cd /home/ubuntu/facilita-factory/dashboard

# Gera dashboard
python3 generate.py > /dev/null 2>&1

# Faz upload para o Gist
GIST_ID="f5cfd1d8d567e68f55e5693710fcc549"
gh gist edit $GIST_ID index.html > /dev/null 2>&1

# Log (opcional)
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Dashboard atualizado" >> /home/ubuntu/facilita-factory/dashboard/auto-update.log
