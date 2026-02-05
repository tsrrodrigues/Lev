# 📋 Lev - Facilita Factory Tools

Repositório de ferramentas e dashboards do Lev (PM) para a Facilita Factory.

## 🏭 Projetos

### Dashboard
Dashboard interativo em tempo real para acompanhar tasks e agentes da Factory.

**Localização:** `/dashboard/`
**Ver:** [Dashboard README](./dashboard/README.md)

## 🚀 Setup do GitHub Pages

Para acessar o dashboard via web, habilite GitHub Pages:

1. Acesse: https://github.com/tsrrodrigues/Lev/settings/pages
2. Em "Build and deployment":
   - Source: **GitHub Actions**
3. Salve e aguarde o deploy (1-2 minutos)

**URL após deploy:** https://tsrrodrigues.github.io/Lev/

O GitHub Actions já está configurado (`.github/workflows/deploy-pages.yml`) e fará deploy automático a cada push na branch `main`.

## 🔄 Atualizar Dashboard

```bash
cd ~/Lev/dashboard
python3 generate.py
git add index.html
git commit -m "update: dashboard data"
git push
```

O GitHub Actions fará deploy automático.

## 📦 Estrutura

```
Lev/
├── .github/
│   └── workflows/
│       └── deploy-pages.yml    # GitHub Actions config
├── dashboard/                   # Dashboard project
│   ├── generate.py             # Dashboard generator
│   ├── index.html              # Generated dashboard
│   ├── update.sh               # Update script
│   └── README.md               # Dashboard docs
└── README.md                   # This file
```

## 🛠️ Ferramentas Futuras

Este repositório pode conter outros projetos/ferramentas desenvolvidos pelo Lev:
- Analytics dashboards
- Automation scripts
- Monitoring tools
- etc.

---

**Mantido por:** Lev (PM) - Facilita Factory
**Última atualização:** 2026-02-05
