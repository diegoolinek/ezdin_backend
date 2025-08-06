import shutil
import os
import sys

def switch_to_local():
    """Alterna para banco local (PostgreSQL via Docker)"""
    if os.path.exists('.env.local'):
        shutil.copy('.env.local', '.env')
        print("✅ Configuração alterada para banco LOCAL")
        print("🐳 Certifique-se de que o Docker está rodando: docker-compose up -d")
    else:
        print("❌ Arquivo .env.local não encontrado")

def switch_to_render():
    """Alterna para banco do Render (compartilhado)"""
    if os.path.exists('.env.render'):
        shutil.copy('.env.render', '.env')
        print("✅ Configuração alterada para banco do RENDER")
        print("🌐 Agora você está usando o banco compartilhado da equipe")
    else:
        print("❌ Arquivo .env.render não encontrado")

def show_current():
    """Mostra a configuração atual"""
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            content = f.read()
            if 'localhost' in content:
                print("📍 Configuração atual: BANCO LOCAL")
            elif 'render.com' in content:
                print("📍 Configuração atual: BANCO RENDER")
            else:
                print("📍 Configuração atual: DESCONHECIDA")
    else:
        print("❌ Arquivo .env não encontrado")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python switch_db.py local   - Usar banco local (Docker)")
        print("  python switch_db.py render  - Usar banco Render (compartilhado)")
        print("  python switch_db.py status  - Ver configuração atual")
        sys.exit(1)
    
    command = sys.argv[1].lower()
    
    if command == "local":
        switch_to_local()
    elif command == "render":
        switch_to_render()
    elif command == "status":
        show_current()
    else:
        print("❌ Comando inválido. Use 'local', 'render' ou 'status'")
