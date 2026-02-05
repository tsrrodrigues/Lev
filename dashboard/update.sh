#!/bin/bash
# Atualiza o dashboard da Facilita Factory

cd /home/ubuntu/facilita-factory/dashboard

echo "🏭 Atualizando dashboard..."
python3 generate.py

if [ "$1" == "--upload" ]; then
    echo "📤 Fazendo upload para GitHub Gist..."
    GIST_ID="f5cfd1d8d567e68f55e5693710fcc549"
    gh gist edit $GIST_ID index.html
    echo "✅ Dashboard atualizado: https://gist.github.com/tsrrodrigues/$GIST_ID"
else
    echo ""
    echo "✅ Dashboard gerado localmente"
    echo "   Arquivo: /home/ubuntu/facilita-factory/dashboard/index.html"
    echo ""
    echo "Para fazer upload para o Gist, use:"
    echo "   ./update.sh --upload"
fi
