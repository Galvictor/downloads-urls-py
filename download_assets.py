"""
Script principal para download de assets.
Este script carrega URLs de um arquivo JSON e faz o download
organizando os arquivos por tipo (áudio, vídeo, imagem).
"""

import json
import time
from utils import (
    clean_directory,
    download_file,
    determine_file_type_and_path,
    print_download_summary,
    print_file_listing
)


def load_urls_from_json(filename='urls.json'):
    """
    Carrega as URLs do arquivo JSON.
    
    Args:
        filename (str): Nome do arquivo JSON com as URLs
        
    Returns:
        list: Lista de URLs para download
        
    Raises:
        FileNotFoundError: Se o arquivo não for encontrado
        json.JSONDecodeError: Se o JSON for inválido
    """
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            urls = json.load(f)
        return urls
    except FileNotFoundError:
        print(f"❌ Arquivo {filename} não encontrado!")
        raise
    except json.JSONDecodeError:
        print(f"❌ Erro ao decodificar o arquivo {filename}!")
        raise


def main():
    """
    Função principal que executa todo o processo de download.
    
    Este script:
    1. Carrega as URLs do arquivo JSON
    2. Limpa e prepara as pastas de destino
    3. Processa cada URL e faz o download
    4. Mostra um relatório detalhado
    """
    # Carrega as URLs do arquivo JSON
    try:
        urls = load_urls_from_json()
    except (FileNotFoundError, json.JSONDecodeError):
        return
    
    print(f"📥 Iniciando download de {len(urls)} arquivos...")
    print("=" * 50)
    
    # Limpa e cria as pastas de destino
    print("\n🧹 Preparando pastas de destino...")
    clean_directory('audios')
    clean_directory('videos')
    clean_directory('images')
    print("✅ Pastas preparadas!\n")
    
    # Contadores
    audio_count = 0
    video_count = 0
    image_count = 0
    error_count = 0
    
    # Contadores de tamanho
    audio_size_total = 0
    video_size_total = 0
    image_size_total = 0
    
    print("🚀 Iniciando downloads...\n")
    
    # Processa cada URL
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processando: {url}")
        
        # Determina o tipo de arquivo e caminho de destino
        local_path, file_type, counter_type = determine_file_type_and_path(url)
        
        if local_path is None:
            print(f"⚠️  Tipo de arquivo não reconhecido: {url}")
            error_count += 1
            continue
        
        # Incrementa o contador apropriado
        if counter_type == "audio_count":
            audio_count += 1
        elif counter_type == "video_count":
            video_count += 1
        elif counter_type == "image_count":
            image_count += 1
        
        # Faz o download
        success, file_size = download_file(url, local_path)
        if success:
            print(f"📁 Salvo em: {local_path}")
            
            # Adiciona o tamanho ao total correspondente
            if counter_type == "audio_count":
                audio_size_total += file_size
            elif counter_type == "video_count":
                video_size_total += file_size
            elif counter_type == "image_count":
                image_size_total += file_size
        else:
            error_count += 1
        
        # Pausa pequena para não sobrecarregar o servidor
        time.sleep(0.5)
    
    # Mostra o resumo do download
    print_download_summary(
        audio_count, video_count, image_count, error_count,
        audio_size_total, video_size_total, image_size_total, len(urls)
    )
    
    # Lista os arquivos baixados
    print_file_listing()


if __name__ == "__main__":
    main() 