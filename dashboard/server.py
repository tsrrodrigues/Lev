#!/usr/bin/env python3
"""
Servidor HTTP simples para o Dashboard da Facilita Factory
"""

import http.server
import socketserver
import os
import socket

PORT = 8080
DIRECTORY = "/home/ubuntu/facilita-factory"

class CustomHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        # Adiciona headers CORS
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()

def get_ip():
    """Obtém o IP local da máquina"""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "localhost"

def main():
    # Bind em 0.0.0.0 para aceitar conexões externas
    with socketserver.TCPServer(("0.0.0.0", PORT), CustomHandler) as httpd:
        ip = get_ip()
        print(f"✅ Dashboard rodando!")
        print(f"")
        print(f"   🌐 Acesso local:  http://localhost:{PORT}/dashboard/monitor.html")
        print(f"   🌐 Acesso remoto: http://{ip}:{PORT}/dashboard/monitor.html")
        print(f"")
        print(f"📂 Servindo arquivos de: {DIRECTORY}")
        print(f"")
        print(f"⚠️  Certifique-se que a porta {PORT} está aberta no firewall")
        print(f"   Pressione Ctrl+C para parar")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n👋 Servidor encerrado")

if __name__ == "__main__":
    main()
