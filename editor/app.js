// Estado global
let currentGistId = null;
let currentFilename = null;

// Inicializar editor
const easyMDE = new EasyMDE({
    element: document.getElementById('editor'),
    spellChecker: false,
    autosave: { enabled: false },
    toolbar: [
        'bold', 'italic', 'heading', '|',
        'quote', 'unordered-list', 'ordered-list', '|',
        'link', 'image', '|',
        'preview', 'side-by-side', 'fullscreen', '|',
        'guide'
    ],
    placeholder: 'Cole ou digite seu markdown aqui...',
    renderingConfig: {
        codeSyntaxHighlighting: true
    }
});

// Preview em tempo real
easyMDE.codemirror.on('change', () => {
    const markdown = easyMDE.value();
    const html = marked.parse(markdown);
    document.getElementById('preview').innerHTML = html;
});

// Carregar do Gist
async function loadFromGist() {
    const gistId = prompt('Cole o ID ou URL do Gist:');
    if (!gistId) return;
    
    // Extrair ID da URL se necessário
    const id = gistId.includes('gist.github.com') 
        ? gistId.split('/').pop() 
        : gistId;
    
    showStatus('Carregando...', 'loading');
    
    try {
        const response = await fetch(`https://api.github.com/gists/${id}`);
        if (!response.ok) throw new Error('Gist não encontrado');
        
        const gist = await response.json();
        const files = Object.values(gist.files);
        
        if (files.length === 0) throw new Error('Gist vazio');
        
        // Pegar primeiro arquivo .md
        const mdFile = files.find(f => f.filename.endsWith('.md')) || files[0];
        
        currentGistId = id;
        currentFilename = mdFile.filename;
        
        easyMDE.value(mdFile.content);
        document.getElementById('filename').textContent = mdFile.filename;
        
        showStatus('✅ Carregado: ' + mdFile.filename, 'success');
    } catch (error) {
        showStatus('❌ Erro: ' + error.message, 'error');
    }
}

// Salvar no Gist (criar nova versão)
async function saveToGist() {
    if (!currentGistId) {
        alert('❌ Carregue um Gist primeiro usando "Carregar do Gist"');
        return;
    }
    
    const content = easyMDE.value();
    if (!content.trim()) {
        alert('❌ Conteúdo vazio');
        return;
    }
    
    const description = prompt('Descrição da alteração (opcional):', 'Atualizado via Lev Editor');
    
    showStatus('Salvando...', 'loading');
    
    try {
        // Criar novo Gist (fork do original)
        const newGist = {
            description: `${description} [Fork de ${currentGistId}]`,
            public: true,
            files: {
                [currentFilename]: {
                    content: content
                }
            }
        };
        
        const response = await fetch('https://api.github.com/gists', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Accept': 'application/vnd.github.v3+json'
            },
            body: JSON.stringify(newGist)
        });
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.message || 'Erro ao salvar');
        }
        
        const savedGist = await response.json();
        
        // Atualizar estado
        currentGistId = savedGist.id;
        
        showStatus(`✅ Salvo! Nova versão: ${savedGist.id}`, 'success');
        
        // Copiar URL para clipboard
        const url = savedGist.html_url;
        navigator.clipboard.writeText(url).then(() => {
            setTimeout(() => {
                showStatus(`📋 URL copiada: ${url}`, 'success');
            }, 2000);
        });
        
    } catch (error) {
        showStatus('❌ Erro ao salvar: ' + error.message, 'error');
    }
}

// Mostrar notificação de status
function showStatus(message, type = 'info') {
    const statusEl = document.getElementById('status');
    statusEl.textContent = message;
    statusEl.style.display = 'block';
    
    if (type === 'error') {
        statusEl.style.background = '#da3633';
    } else if (type === 'success') {
        statusEl.style.background = '#238636';
    } else {
        statusEl.style.background = '#1f6feb';
    }
    
    setTimeout(() => {
        statusEl.style.display = 'none';
    }, 4000);
}

// Detectar Gist na URL (query param ?gist=ID)
window.addEventListener('DOMContentLoaded', () => {
    const urlParams = new URLSearchParams(window.location.search);
    const gistParam = urlParams.get('gist');
    
    if (gistParam) {
        // Auto-load do gist
        setTimeout(() => {
            loadFromGistAuto(gistParam);
        }, 500);
    }
});

async function loadFromGistAuto(id) {
    currentGistId = id;
    showStatus('Carregando automaticamente...', 'loading');
    
    try {
        const response = await fetch(`https://api.github.com/gists/${id}`);
        if (!response.ok) throw new Error('Gist não encontrado');
        
        const gist = await response.json();
        const files = Object.values(gist.files);
        const mdFile = files.find(f => f.filename.endsWith('.md')) || files[0];
        
        currentFilename = mdFile.filename;
        easyMDE.value(mdFile.content);
        document.getElementById('filename').textContent = mdFile.filename;
        
        showStatus('✅ Carregado: ' + mdFile.filename, 'success');
    } catch (error) {
        showStatus('❌ Erro: ' + error.message, 'error');
    }
}

// Atalhos de teclado
document.addEventListener('keydown', (e) => {
    // Ctrl/Cmd + S para salvar
    if ((e.ctrlKey || e.metaKey) && e.key === 's') {
        e.preventDefault();
        saveToGist();
    }
});
