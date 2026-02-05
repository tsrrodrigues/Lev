#!/usr/bin/env python3
"""
Facilita Factory Dashboard Generator
Gera dashboard HTML interativo com status de tasks e agentes
"""

import json
import os
from datetime import datetime
from pathlib import Path

FACTORY_ROOT = Path("/home/ubuntu/facilita-factory")
SHARED = FACTORY_ROOT / "shared"
DASHBOARD = Path("/home/ubuntu/Lev/dashboard")

def load_json(path):
    """Carrega JSON ou retorna {} se não existir"""
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

def load_tasks():
    """Carrega todas as tasks do diretório shared/tasks/"""
    tasks = []
    tasks_dir = SHARED / "tasks"
    if tasks_dir.exists():
        for file in tasks_dir.glob("task-*.json"):
            task = load_json(file)
            if task:
                tasks.append(task)
    return sorted(tasks, key=lambda x: x.get('createdAt', ''), reverse=True)

def load_status():
    """Carrega status.json"""
    return load_json(SHARED / "status.json")

def format_datetime(iso_str):
    """Formata ISO datetime para exibição"""
    if not iso_str:
        return "N/A"
    try:
        dt = datetime.fromisoformat(iso_str.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return iso_str

def get_status_emoji(status):
    """Retorna emoji para cada status"""
    emojis = {
        'backlog': '📋',
        'spec': '📝',
        'in-progress': '💻',
        'review': '🔍',
        'done': '✅',
        'blocked': '🚨'
    }
    return emojis.get(status, '❓')

def get_priority_color(priority):
    """Retorna cor CSS para cada prioridade"""
    colors = {
        'critical': '#e74c3c',
        'high': '#e67e22',
        'medium': '#f39c12',
        'low': '#95a5a6'
    }
    return colors.get(priority, '#95a5a6')

def generate_html(tasks, status):
    """Gera HTML do dashboard"""
    
    # Estatísticas
    total_tasks = len(tasks)
    active_tasks = len([t for t in tasks if t.get('status') not in ['done']])
    done_today = status.get('tasks', {}).get('done_today', 0)
    
    # Agentes
    agents = status.get('agents', {})
    active_agents = len([a for a in agents.values() if a.get('status') == 'active'])
    
    # HTML
    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Facilita Factory Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
            color: #2d3748;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .header {{
            background: white;
            border-radius: 12px;
            padding: 30px;
            margin-bottom: 20px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.1);
        }}
        
        .header h1 {{
            font-size: 32px;
            color: #667eea;
            margin-bottom: 10px;
        }}
        
        .header .subtitle {{
            color: #718096;
            font-size: 14px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        
        .stat-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: transform 0.2s;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
        }}
        
        .stat-card .label {{
            font-size: 12px;
            text-transform: uppercase;
            color: #a0aec0;
            font-weight: 600;
            margin-bottom: 5px;
        }}
        
        .stat-card .value {{
            font-size: 32px;
            font-weight: bold;
            color: #667eea;
        }}
        
        .tabs {{
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }}
        
        .tab {{
            background: white;
            border: none;
            padding: 12px 24px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 14px;
            font-weight: 600;
            color: #718096;
            transition: all 0.2s;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }}
        
        .tab.active {{
            background: #667eea;
            color: white;
        }}
        
        .tab-content {{
            display: none;
        }}
        
        .tab-content.active {{
            display: block;
        }}
        
        .task-grid {{
            display: grid;
            gap: 15px;
        }}
        
        .task-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            transition: all 0.2s;
            cursor: pointer;
            border-left: 4px solid #667eea;
        }}
        
        .task-card:hover {{
            box-shadow: 0 8px 25px rgba(0,0,0,0.15);
            transform: translateY(-2px);
        }}
        
        .task-card.critical {{ border-left-color: #e74c3c; }}
        .task-card.high {{ border-left-color: #e67e22; }}
        .task-card.medium {{ border-left-color: #f39c12; }}
        .task-card.low {{ border-left-color: #95a5a6; }}
        
        .task-header {{
            display: flex;
            justify-content: space-between;
            align-items: start;
            margin-bottom: 15px;
        }}
        
        .task-title {{
            font-size: 18px;
            font-weight: bold;
            color: #2d3748;
            flex: 1;
        }}
        
        .task-badges {{
            display: flex;
            gap: 8px;
            flex-wrap: wrap;
        }}
        
        .badge {{
            padding: 4px 12px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: 600;
            white-space: nowrap;
        }}
        
        .badge.status {{
            background: #edf2f7;
            color: #4a5568;
        }}
        
        .badge.priority {{
            color: white;
        }}
        
        .task-meta {{
            font-size: 13px;
            color: #718096;
            margin-bottom: 10px;
        }}
        
        .task-description {{
            color: #4a5568;
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 15px;
        }}
        
        .task-footer {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .assignee {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 13px;
            color: #4a5568;
        }}
        
        .assignee-avatar {{
            width: 28px;
            height: 28px;
            border-radius: 50%;
            background: #667eea;
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 12px;
        }}
        
        .task-details {{
            display: none;
            margin-top: 15px;
            padding-top: 15px;
            border-top: 1px solid #e2e8f0;
        }}
        
        .task-details.expanded {{
            display: block;
        }}
        
        .detail-section {{
            margin-bottom: 15px;
        }}
        
        .detail-section h4 {{
            font-size: 13px;
            text-transform: uppercase;
            color: #a0aec0;
            margin-bottom: 8px;
        }}
        
        .detail-section ul {{
            list-style: none;
            padding-left: 0;
        }}
        
        .detail-section li {{
            padding: 6px 0;
            color: #4a5568;
            font-size: 14px;
        }}
        
        .detail-section li:before {{
            content: "•";
            color: #667eea;
            font-weight: bold;
            margin-right: 8px;
        }}
        
        .agents-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 15px;
        }}
        
        .agent-card {{
            background: white;
            border-radius: 12px;
            padding: 20px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }}
        
        .agent-card.active {{
            border-left: 4px solid #48bb78;
        }}
        
        .agent-card.idle {{
            border-left: 4px solid #cbd5e0;
        }}
        
        .agent-header {{
            display: flex;
            align-items: center;
            gap: 12px;
            margin-bottom: 12px;
        }}
        
        .agent-avatar {{
            width: 40px;
            height: 40px;
            border-radius: 50%;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: bold;
            font-size: 16px;
        }}
        
        .agent-name {{
            font-size: 18px;
            font-weight: bold;
            color: #2d3748;
        }}
        
        .agent-status {{
            font-size: 13px;
            color: #718096;
        }}
        
        .agent-task {{
            background: #f7fafc;
            padding: 12px;
            border-radius: 8px;
            font-size: 13px;
            color: #4a5568;
        }}
        
        .refresh-btn {{
            position: fixed;
            bottom: 30px;
            right: 30px;
            background: #667eea;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 50px;
            font-weight: bold;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(102, 126, 234, 0.4);
            transition: all 0.2s;
        }}
        
        .refresh-btn:hover {{
            background: #5a67d8;
            transform: scale(1.05);
        }}
        
        .empty-state {{
            text-align: center;
            padding: 60px 20px;
            color: #a0aec0;
        }}
        
        .empty-state h3 {{
            font-size: 24px;
            margin-bottom: 10px;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🏭 Facilita Factory</h1>
            <p class="subtitle">Dashboard de Acompanhamento • Atualizado em {datetime.now().strftime('%d/%m/%Y às %H:%M:%S')}</p>
        </div>
        
        <div class="stats">
            <div class="stat-card">
                <div class="label">Total de Tasks</div>
                <div class="value">{total_tasks}</div>
            </div>
            <div class="stat-card">
                <div class="label">Tasks Ativas</div>
                <div class="value">{active_tasks}</div>
            </div>
            <div class="stat-card">
                <div class="label">Concluídas Hoje</div>
                <div class="value">{done_today}</div>
            </div>
            <div class="stat-card">
                <div class="label">Agentes Ativos</div>
                <div class="value">{active_agents}/{len(agents)}</div>
            </div>
        </div>
        
        <div class="tabs">
            <button class="tab active" onclick="showTab('tasks')">📋 Tasks</button>
            <button class="tab" onclick="showTab('agents')">👥 Agentes</button>
        </div>
        
        <div id="tasks-tab" class="tab-content active">
            <div class="task-grid">
"""
    
    # Tasks
    if tasks:
        for task in tasks:
            task_id = task.get('id', 'N/A')
            title = task.get('title', 'Sem título')
            description = task.get('description', '')
            status = task.get('status', 'backlog')
            priority = task.get('priority', 'medium')
            assigned = task.get('assignedTo', None)
            created = format_datetime(task.get('createdAt'))
            updated = format_datetime(task.get('updatedAt'))
            notes = task.get('notes', [])
            
            assigned_display = assigned.upper() if assigned else 'Não atribuído'
            assigned_initial = assigned[0].upper() if assigned else '?'
            
            status_emoji = get_status_emoji(status)
            priority_color = get_priority_color(priority)
            
            html += f"""
                <div class="task-card {priority}" onclick="toggleDetails('{task_id}')">
                    <div class="task-header">
                        <div class="task-title">{status_emoji} {title}</div>
                        <div class="task-badges">
                            <span class="badge status">{status.upper()}</span>
                            <span class="badge priority" style="background: {priority_color}">{priority.upper()}</span>
                        </div>
                    </div>
                    
                    <div class="task-meta">
                        <strong>ID:</strong> {task_id} • <strong>Projeto:</strong> {task.get('project', 'N/A')}
                    </div>
                    
                    <div class="task-description">{description[:200]}{'...' if len(description) > 200 else ''}</div>
                    
                    <div class="task-footer">
                        <div class="assignee">
                            <div class="assignee-avatar">{assigned_initial}</div>
                            {assigned_display}
                        </div>
                        <div style="font-size: 12px; color: #a0aec0;">
                            Atualizado: {updated}
                        </div>
                    </div>
                    
                    <div class="task-details" id="details-{task_id}">
                        <div class="detail-section">
                            <h4>⏱️ Timestamps</h4>
                            <ul>
                                <li><strong>Criado:</strong> {created}</li>
                                <li><strong>Atualizado:</strong> {updated}</li>
                            </ul>
                        </div>
"""
            
            if notes:
                html += """
                        <div class="detail-section">
                            <h4>📝 Notas</h4>
                            <ul>
"""
                for note in notes:
                    html += f"                                <li>{note}</li>\n"
                html += """
                            </ul>
                        </div>
"""
            
            spec_file = task.get('specFile')
            test_file = task.get('testScenariosFile')
            if spec_file or test_file:
                html += """
                        <div class="detail-section">
                            <h4>📂 Arquivos</h4>
                            <ul>
"""
                if spec_file:
                    html += f"                                <li><strong>Spec:</strong> <code>/home/ubuntu/facilita-factory/shared/{spec_file}</code></li>\n"
                if test_file:
                    html += f"                                <li><strong>Testes:</strong> <code>/home/ubuntu/facilita-factory/shared/{test_file}</code></li>\n"
                html += """
                            </ul>
                        </div>
"""
            
            html += """
                    </div>
                </div>
"""
    else:
        html += """
                <div class="empty-state">
                    <h3>📭 Nenhuma task encontrada</h3>
                    <p>As tasks aparecerão aqui quando forem criadas.</p>
                </div>
"""
    
    html += """
            </div>
        </div>
        
        <div id="agents-tab" class="tab-content">
            <div class="agents-grid">
"""
    
    # Agentes
    agent_names = {
        'pm': 'Lev (PM)',
        'spec': 'Spec',
        'dev-1': 'Dev-1',
        'dev-2': 'Dev-2',
        'support': 'Support',
        'qa': 'QA',
        'docs': 'Docs'
    }
    
    for agent_id, agent_data in agents.items():
        name = agent_names.get(agent_id, agent_id.upper())
        status = agent_data.get('status', 'idle')
        current_task = agent_data.get('currentTask')
        
        status_class = 'active' if status == 'active' else 'idle'
        status_text = '🟢 Ativo' if status == 'active' else '⚪ Ocioso'
        
        html += f"""
                <div class="agent-card {status_class}">
                    <div class="agent-header">
                        <div class="agent-avatar">{agent_id[0].upper()}</div>
                        <div>
                            <div class="agent-name">{name}</div>
                            <div class="agent-status">{status_text}</div>
                        </div>
                    </div>
"""
        
        if current_task:
            task_obj = next((t for t in tasks if t.get('id') == current_task), None)
            task_title = task_obj.get('title', current_task) if task_obj else current_task
            html += f"""
                    <div class="agent-task">
                        <strong>Trabalhando em:</strong><br>{task_title}
                    </div>
"""
        else:
            html += """
                    <div class="agent-task" style="color: #a0aec0;">
                        Aguardando atribuição
                    </div>
"""
        
        html += """
                </div>
"""
    
    html += """
            </div>
        </div>
    </div>
    
    <button class="refresh-btn" onclick="window.location.reload()">🔄 Atualizar</button>
    
    <script>
        function showTab(tabName) {
            // Hide all tabs
            document.querySelectorAll('.tab-content').forEach(content => {
                content.classList.remove('active');
            });
            document.querySelectorAll('.tab').forEach(tab => {
                tab.classList.remove('active');
            });
            
            // Show selected tab
            document.getElementById(tabName + '-tab').classList.add('active');
            event.target.classList.add('active');
        }
        
        function toggleDetails(taskId) {
            const details = document.getElementById('details-' + taskId);
            if (details.classList.contains('expanded')) {
                details.classList.remove('expanded');
            } else {
                // Close all other details
                document.querySelectorAll('.task-details').forEach(d => {
                    d.classList.remove('expanded');
                });
                details.classList.add('expanded');
            }
        }
    </script>
</body>
</html>
"""
    
    return html

def main():
    """Função principal"""
    print("🏭 Gerando dashboard...")
    
    # Carregar dados
    tasks = load_tasks()
    status = load_status()
    
    print(f"   Tasks encontradas: {len(tasks)}")
    print(f"   Agentes: {len(status.get('agents', {}))}")
    
    # Gerar HTML
    html = generate_html(tasks, status)
    
    # Salvar
    output_file = DASHBOARD / "index.html"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"✅ Dashboard gerado: {output_file}")
    print(f"   Abra no navegador: file://{output_file}")

if __name__ == '__main__':
    main()
