#!/usr/bin/env python3
"""
Script para instalar dependências e executar o download dos assets
"""

import subprocess
import sys
import os

def install_requirements():
    """Instala as dependências necessárias"""
    print("📦 Instalando dependências...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependências instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao instalar dependências!")
        return False

def run_download():
    """Executa o script de download"""
    print("🚀 Executando script de download...")
    try:
        subprocess.check_call([sys.executable, "download_assets.py"])
        return True
    except subprocess.CalledProcessError:
        print("❌ Erro ao executar o script de download!")
        return False

def main():
    print("🎯 INICIANDO DOWNLOAD DE ASSETS")
    print("=" * 50)
    
    # Verifica se o arquivo urls.json existe
    if not os.path.exists('urls.json'):
        print("❌ Arquivo urls.json não encontrado!")
        print("Certifique-se de que o arquivo urls.json está no diretório atual.")
        return
    
    # Instala dependências
    if not install_requirements():
        return
    
    print("\n" + "=" * 50)
    
    # Executa o download
    if run_download():
        print("\n🎉 Processo concluído com sucesso!")
    else:
        print("\n💥 Processo falhou!")

if __name__ == "__main__":
    main() 