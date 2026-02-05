#!/bin/bash
# Deploy dashboard to GitHub Pages

cd /home/ubuntu/Lev/dashboard

echo "🏭 Atualizando dashboard..."
python3 generate.py

echo ""
echo "📤 Fazendo commit e push..."
cd /home/ubuntu/Lev
git add dashboard/index.html
git commit -m "update: dashboard data $(date '+%Y-%m-%d %H:%M:%S')"
git push

echo ""
echo "✅ Deploy concluído!"
echo "   O GitHub Actions fará deploy automático em 1-2 minutos"
echo "   URL: https://tsrrodrigues.github.io/Lev/"
