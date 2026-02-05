# 🏭 Facilita Factory Dashboard

Dashboard interativo em tempo real para acompanhar tasks e agentes.

## 🚀 Acesso Rápido

**URL do Dashboard:** https://gist.github.com/tsrrodrigues/f5cfd1d8d567e68f55e5693710fcc549

Clique em "View raw" ou acesse diretamente:
https://gist.githubusercontent.com/tsrrodrigues/f5cfd1d8d567e68f55e5693710fcc549/raw/index.html

## 📊 Funcionalidades

### Visão Geral
- **Total de tasks** no sistema
- **Tasks ativas** (não concluídas)
- **Tasks concluídas hoje**
- **Agentes ativos** no momento

### Tab "Tasks"
- **Cards visuais** com status, prioridade e assignee
- **Clique no card** para ver detalhes completos:
  - Timestamps (criado/atualizado)
  - Notas da task
  - Arquivos (spec, testes)
- **Cores por prioridade:**
  - 🔴 Critical (vermelho)
  - 🟠 High (laranja)
  - 🟡 Medium (amarelo)
  - ⚪ Low (cinza)

### Tab "Agentes"
- **Status de cada agente** (ativo/ocioso)
- **Task atual** que está trabalhando
- **Cards visuais** com avatar e status

## 🔄 Atualizar Dashboard

### Opção 1: Manual Local
```bash
cd /home/ubuntu/facilita-factory/dashboard
./update.sh
```

Depois abra no navegador:
```
file:///home/ubuntu/facilita-factory/dashboard/index.html
```

### Opção 2: Manual com Upload (Recomendado)
```bash
cd /home/ubuntu/facilita-factory/dashboard
./update.sh --upload
```

Isso gera o HTML e faz upload para o GitHub Gist, mantendo a URL pública sempre atualizada.

### Opção 3: Automático (Cron) ⭐
Configure atualização automática a cada 5 minutos:
```bash
cd /home/ubuntu/facilita-factory/dashboard
./setup-cron.sh
```

**Benefícios:**
- Dashboard sempre atualizado automaticamente
- Não precisa rodar comandos manualmente
- URL pública sempre com dados mais recentes

**Para desabilitar:**
```bash
crontab -e
# Delete a linha com "auto-update.sh"
```

## 📝 Como Funciona

1. **Script Python** (`generate.py`) lê os JSONs do `/shared/`:
   - `/shared/tasks/task-*.json` — todas as tasks
   - `/shared/status.json` — status de agentes

2. **Gera HTML** com interface moderna e interativa

3. **Salva localmente** em `index.html`

4. **(Opcional) Upload para Gist** — mantém versão pública atualizada

## 🎨 Interface

- **Design moderno** com gradiente roxo
- **Responsivo** (funciona em mobile)
- **Interativo** (clique para expandir detalhes)
- **Botão de refresh** no canto inferior direito

## ⚡ Comandos Rápidos

**Gerar dashboard:**
```bash
python3 /home/ubuntu/facilita-factory/dashboard/generate.py
```

**Atualizar e abrir no navegador:**
```bash
cd /home/ubuntu/facilita-factory/dashboard && ./update.sh && xdg-open index.html
```

**Atualizar e publicar:**
```bash
cd /home/ubuntu/facilita-factory/dashboard && ./update.sh --upload
```

## 📱 Acesso via Telegram

O dashboard pode ser enviado via Telegram usando o Markdown Viewer, mas a melhor opção é usar a URL pública do Gist (sempre atualizada com `./update.sh --upload`).

---

**Última atualização:** 2026-02-05
