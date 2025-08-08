import requests
import os
import json
import shutil
from urllib.parse import urlparse
import time

def clean_directory(directory_path):
    """Remove todo o conteúdo de um diretório"""
    if os.path.exists(directory_path):
        print(f"🗑️  Limpando pasta: {directory_path}")
        for item in os.listdir(directory_path):
            item_path = os.path.join(directory_path, item)
            if os.path.isfile(item_path):
                os.remove(item_path)
                print(f"   - Removido arquivo: {item}")
            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)
                print(f"   - Removido diretório: {item}")
    else:
        print(f"📁 Criando pasta: {directory_path}")
        os.makedirs(directory_path, exist_ok=True)

def download_file(url, local_path):
    """Faz o download de um arquivo e salva no caminho especificado"""
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        with open(local_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"✅ Download concluído: {os.path.basename(local_path)}")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar {url}: {str(e)}")
        return False

def get_file_extension(url):
    """Extrai a extensão do arquivo da URL"""
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1]

def is_audio_file(url):
    """Verifica se a URL é um arquivo de áudio"""
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
    extension = get_file_extension(url).lower()
    return extension in audio_extensions

def is_video_file(url):
    """Verifica se a URL é um arquivo de vídeo"""
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
    extension = get_file_extension(url).lower()
    return extension in video_extensions

def is_image_file(url):
    """Verifica se a URL é um arquivo de imagem"""
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']
    extension = get_file_extension(url).lower()
    return extension in image_extensions

def get_filename_from_url(url):
    """Extrai o nome do arquivo da URL"""
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)

def main():
    # Carrega as URLs do arquivo JSON
    try:
        with open('urls.json', 'r', encoding='utf-8') as f:
            urls = json.load(f)
    except FileNotFoundError:
        print("❌ Arquivo urls.json não encontrado!")
        return
    except json.JSONDecodeError:
        print("❌ Erro ao decodificar o arquivo JSON!")
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
    
    for i, url in enumerate(urls, 1):
        print(f"\n[{i}/{len(urls)}] Processando: {url}")
        
        # Determina o tipo de arquivo e o caminho de destino
        if is_audio_file(url):
            filename = get_filename_from_url(url)
            local_path = os.path.join('audios', filename)
            audio_count += 1
            file_type = "áudio"
        elif is_video_file(url):
            filename = get_filename_from_url(url)
            local_path = os.path.join('videos', filename)
            video_count += 1
            file_type = "vídeo"
        elif is_image_file(url):
            filename = get_filename_from_url(url)
            local_path = os.path.join('images', filename)
            image_count += 1
            file_type = "imagem"
        else:
            print(f"⚠️  Tipo de arquivo não reconhecido: {url}")
            error_count += 1
            continue
        
        # Faz o download
        if download_file(url, local_path):
            print(f"📁 Salvo em: {local_path}")
        else:
            error_count += 1
        
        # Pausa pequena para não sobrecarregar o servidor
        time.sleep(0.5)
    
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DOWNLOAD:")
    print(f"✅ Áudios baixados: {audio_count}")
    print(f"✅ Vídeos baixados: {video_count}")
    print(f"✅ Imagens baixadas: {image_count}")
    print(f"❌ Erros: {error_count}")
    print(f"📁 Total processado: {len(urls)}")
    
    # Lista os arquivos baixados
    print("\n📂 ARQUIVOS BAIXADOS:")
    
    audio_dir = 'audios'
    video_dir = 'videos'
    image_dir = 'images'
    
    if os.path.exists(audio_dir):
        audio_files = os.listdir(audio_dir)
        if audio_files:
            print(f"\n🎵 Áudios ({len(audio_files)}):")
            for file in sorted(audio_files):
                print(f"   - {file}")
    
    if os.path.exists(video_dir):
        video_files = os.listdir(video_dir)
        if video_files:
            print(f"\n🎬 Vídeos ({len(video_files)}):")
            for file in sorted(video_files):
                print(f"   - {file}")
    
    if os.path.exists(image_dir):
        image_files = os.listdir(image_dir)
        if image_files:
            print(f"\n🖼️  Imagens ({len(image_files)}):")
            for file in sorted(image_files):
                print(f"   - {file}")

if __name__ == "__main__":
    main() 