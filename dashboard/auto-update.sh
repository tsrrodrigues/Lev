#!/bin/bash
# Auto-update dashboard (para uso com cron)
# Exemplo de cron (a cada 5 minutos):
# */5 * * * * /home/ubuntu/Lev/dashboard/auto-update.sh

cd /home/ubuntu/Lev/dashboard

# Gera dashboard
python3 generate.py > /dev/null 2>&1

# Commit e push
cd /home/ubuntu/Lev
git add dashboard/index.html > /dev/null 2>&1
git commit -m "update: dashboard data $(date '+%Y-%m-%d %H:%M:%S')" > /dev/null 2>&1
git push > /dev/null 2>&1

# Log
echo "[$(date '+%Y-%m-%d %H:%M:%S')] Dashboard atualizado e deployed" >> /home/ubuntu/Lev/dashboard/auto-update.log
