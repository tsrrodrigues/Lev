#!/bin/bash
# Configura atualização automática do dashboard a cada 5 minutos

CRON_LINE="*/5 * * * * /home/ubuntu/Lev/dashboard/auto-update.sh"

# Verifica se a linha já existe no crontab
if crontab -l 2>/dev/null | grep -q "auto-update.sh"; then
    echo "⚠️  Cron já configurado!"
    echo "Para remover, use: crontab -e"
else
    # Adiciona ao crontab
    (crontab -l 2>/dev/null; echo "$CRON_LINE") | crontab -
    echo "✅ Cron configurado!"
    echo "   Dashboard será atualizado automaticamente a cada 5 minutos"
    echo ""
    echo "Para verificar: crontab -l"
    echo "Para remover: crontab -e (e deletar a linha)"
fi
