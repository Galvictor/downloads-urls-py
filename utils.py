"""
Módulo de utilitários para o script de download de assets.
Contém todas as funções auxiliares para manipulação de arquivos, 
cálculo de tamanhos e organização de downloads.
"""

import os
import shutil
from urllib.parse import urlparse
from tqdm import tqdm
import requests


def get_file_size_mb(file_path):
    """
    Calcula o tamanho de um arquivo em megabytes.
    
    Args:
        file_path (str): Caminho completo do arquivo
        
    Returns:
        float: Tamanho do arquivo em MB, ou 0 se houver erro
        
    Exemplo:
        >>> get_file_size_mb('video.mp4')
        15.23
    """
    try:
        size_bytes = os.path.getsize(file_path)
        size_mb = size_bytes / (1024 * 1024)
        return size_mb
    except (OSError, FileNotFoundError):
        return 0


def get_directory_size_mb(directory_path):
    """
    Calcula o tamanho total de um diretório e seus subdiretórios em MB.
    
    Args:
        directory_path (str): Caminho do diretório
        
    Returns:
        float: Tamanho total em MB, ou 0 se houver erro
        
    Exemplo:
        >>> get_directory_size_mb('videos/')
        156.78
    """
    total_size = 0
    try:
        for dirpath, dirnames, filenames in os.walk(directory_path):
            for filename in filenames:
                file_path = os.path.join(dirpath, filename)
                total_size += os.path.getsize(file_path)
        return total_size / (1024 * 1024)
    except (OSError, FileNotFoundError):
        return 0


def format_file_size(size_mb):
    """
    Formata o tamanho de arquivo para exibição em MB ou GB.
    
    Args:
        size_mb (float): Tamanho em megabytes
        
    Returns:
        str: Tamanho formatado (ex: "15.23 MB" ou "1.5 GB")
        
    Exemplo:
        >>> format_file_size(1536.0)
        '1.50 GB'
        >>> format_file_size(15.23)
        '15.23 MB'
    """
    if size_mb >= 1024:
        return f"{size_mb/1024:.2f} GB"
    else:
        return f"{size_mb:.2f} MB"


def clean_directory(directory_path):
    """
    Remove todo o conteúdo de um diretório ou cria o diretório se não existir.
    
    Esta função:
    1. Verifica se o diretório existe
    2. Se existir, remove todos os arquivos e subpastas
    3. Se não existir, cria o diretório
    4. Mostra logs detalhados do processo
    
    Args:
        directory_path (str): Caminho do diretório a ser limpo/criado
        
    Exemplo:
        >>> clean_directory('videos/')
        🗑️  Limpando pasta: videos/
           - Removido arquivo: video1.mp4
           - Removido arquivo: video2.mp4
    """
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
    """
    Faz o download de um arquivo com barra de progresso em tempo real.
    
    Esta função:
    1. Faz uma requisição HTTP para a URL
    2. Cria o diretório de destino se necessário
    3. Mostra uma barra de progresso durante o download
    4. Salva o arquivo no caminho especificado
    5. Retorna o status e tamanho do arquivo
    
    Args:
        url (str): URL do arquivo a ser baixado
        local_path (str): Caminho local onde salvar o arquivo
        
    Returns:
        tuple: (bool, float) - (sucesso, tamanho_em_mb)
        
    Exemplo:
        >>> download_file('https://exemplo.com/video.mp4', 'videos/video.mp4')
        📥 video.mp4: 100%|██████████| 15.2M/15.2M [00:05<00:00, 3.2MB/s]
        ✅ Download concluído: video.mp4 (15.23 MB)
        (True, 15.23)
    """
    try:
        # Faz a requisição HTTP com streaming
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        # Cria o diretório se não existir
        os.makedirs(os.path.dirname(local_path), exist_ok=True)
        
        # Obtém o tamanho total do arquivo do header HTTP
        total_size = int(response.headers.get('content-length', 0))
        
        # Nome do arquivo para exibição na barra de progresso
        filename = os.path.basename(local_path)
        
        # Faz o download com barra de progresso
        with open(local_path, 'wb') as f:
            with tqdm(
                total=total_size,
                unit='B',
                unit_scale=True,
                unit_divisor=1024,
                desc=f"📥 {filename}",
                bar_format='{l_bar}{bar}| {n_fmt}/{total_fmt} [{elapsed}<{remaining}, {rate_fmt}]'
            ) as pbar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
                        pbar.update(len(chunk))
        
        # Calcula o tamanho do arquivo baixado
        file_size_mb = get_file_size_mb(local_path)
        file_size_str = format_file_size(file_size_mb)
        
        print(f"✅ Download concluído: {filename} ({file_size_str})")
        return True, file_size_mb
        
    except Exception as e:
        print(f"❌ Erro ao baixar {url}: {str(e)}")
        return False, 0


def get_file_extension(url):
    """
    Extrai a extensão do arquivo de uma URL.
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        str: Extensão do arquivo com ponto (ex: ".mp4", ".jpg")
        
    Exemplo:
        >>> get_file_extension('https://exemplo.com/video.mp4')
        '.mp4'
        >>> get_file_extension('https://exemplo.com/imagem.jpg')
        '.jpg'
    """
    parsed_url = urlparse(url)
    path = parsed_url.path
    return os.path.splitext(path)[1]


def is_audio_file(url):
    """
    Verifica se a URL aponta para um arquivo de áudio.
    
    Suporta os formatos: .mp3, .wav, .ogg, .m4a, .aac
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        bool: True se for arquivo de áudio, False caso contrário
        
    Exemplo:
        >>> is_audio_file('https://exemplo.com/musica.mp3')
        True
        >>> is_audio_file('https://exemplo.com/video.mp4')
        False
    """
    audio_extensions = ['.mp3', '.wav', '.ogg', '.m4a', '.aac']
    extension = get_file_extension(url).lower()
    return extension in audio_extensions


def is_video_file(url):
    """
    Verifica se a URL aponta para um arquivo de vídeo.
    
    Suporta os formatos: .mp4, .avi, .mov, .wmv, .flv, .webm, .mkv
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        bool: True se for arquivo de vídeo, False caso contrário
        
    Exemplo:
        >>> is_video_file('https://exemplo.com/video.mp4')
        True
        >>> is_video_file('https://exemplo.com/musica.mp3')
        False
    """
    video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv']
    extension = get_file_extension(url).lower()
    return extension in video_extensions


def is_image_file(url):
    """
    Verifica se a URL aponta para um arquivo de imagem.
    
    Suporta os formatos: .png, .jpg, .jpeg, .gif, .bmp, .webp, .svg
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        bool: True se for arquivo de imagem, False caso contrário
        
    Exemplo:
        >>> is_image_file('https://exemplo.com/foto.jpg')
        True
        >>> is_image_file('https://exemplo.com/video.mp4')
        False
    """
    image_extensions = ['.png', '.jpg', '.jpeg', '.gif', '.bmp', '.webp', '.svg']
    extension = get_file_extension(url).lower()
    return extension in image_extensions


def get_filename_from_url(url):
    """
    Extrai o nome do arquivo de uma URL.
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        str: Nome do arquivo com extensão
        
    Exemplo:
        >>> get_filename_from_url('https://exemplo.com/pasta/video.mp4')
        'video.mp4'
        >>> get_filename_from_url('https://exemplo.com/imagem.jpg?param=123')
        'imagem.jpg'
    """
    parsed_url = urlparse(url)
    return os.path.basename(parsed_url.path)


def determine_file_type_and_path(url):
    """
    Determina o tipo de arquivo e retorna o caminho de destino apropriado.
    
    Esta função analisa a URL e decide:
    1. Se é áudio, vídeo ou imagem
    2. Qual pasta de destino usar
    3. Qual contador incrementar
    
    Args:
        url (str): URL do arquivo
        
    Returns:
        tuple: (caminho_destino, tipo_arquivo, contador_a_incrementar)
               ou (None, None, None) se tipo não reconhecido
        
    Exemplo:
        >>> determine_file_type_and_path('https://exemplo.com/video.mp4')
        ('videos/video.mp4', 'vídeo', 'video_count')
        >>> determine_file_type_and_path('https://exemplo.com/musica.mp3')
        ('audios/musica.mp3', 'áudio', 'audio_count')
    """
    if is_audio_file(url):
        filename = get_filename_from_url(url)
        local_path = os.path.join('audios', filename)
        return local_path, "áudio", "audio_count"
    elif is_video_file(url):
        filename = get_filename_from_url(url)
        local_path = os.path.join('videos', filename)
        return local_path, "vídeo", "video_count"
    elif is_image_file(url):
        filename = get_filename_from_url(url)
        local_path = os.path.join('images', filename)
        return local_path, "imagem", "image_count"
    else:
        return None, None, None


def print_download_summary(audio_count, video_count, image_count, error_count, 
                          audio_size_total, video_size_total, image_size_total, total_urls):
    """
    Imprime um resumo detalhado do processo de download.
    
    Args:
        audio_count (int): Número de áudios baixados
        video_count (int): Número de vídeos baixados
        image_count (int): Número de imagens baixadas
        error_count (int): Número de erros
        audio_size_total (float): Tamanho total dos áudios em MB
        video_size_total (float): Tamanho total dos vídeos em MB
        image_size_total (float): Tamanho total das imagens em MB
        total_urls (int): Total de URLs processadas
        
    Exemplo:
        >>> print_download_summary(5, 19, 3, 0, 12.45, 156.78, 2.34, 27)
        📊 RESUMO DO DOWNLOAD:
        ✅ Áudios baixados: 5 (12.45 MB)
        ✅ Vídeos baixados: 19 (156.78 MB)
        ✅ Imagens baixadas: 3 (2.34 MB)
        ❌ Erros: 0
        📁 Total processado: 27
        💾 ESPAÇO TOTAL OCUPADO: 171.57 MB
    """
    print("\n" + "=" * 50)
    print("📊 RESUMO DO DOWNLOAD:")
    print(f"✅ Áudios baixados: {audio_count} ({format_file_size(audio_size_total)})")
    print(f"✅ Vídeos baixados: {video_count} ({format_file_size(video_size_total)})")
    print(f"✅ Imagens baixadas: {image_count} ({format_file_size(image_size_total)})")
    print(f"❌ Erros: {error_count}")
    print(f"📁 Total processado: {total_urls}")
    
    # Calcula o tamanho total
    total_size = audio_size_total + video_size_total + image_size_total
    print(f"\n💾 ESPAÇO TOTAL OCUPADO: {format_file_size(total_size)}")


def print_file_listing():
    """
    Imprime uma lista detalhada de todos os arquivos baixados com seus tamanhos.
    
    Esta função:
    1. Verifica cada pasta (audios, videos, images)
    2. Lista todos os arquivos com seus tamanhos
    3. Organiza por categoria
    
    Exemplo:
        >>> print_file_listing()
        📂 ARQUIVOS BAIXADOS:
        
        🎵 Áudios (5):
           - audio1.mp3 (2.34 MB)
           - audio2.wav (3.12 MB)
        
        🎬 Vídeos (19):
           - video1.mp4 (8.45 MB)
           - video2.mp4 (12.67 MB)
        
        🖼️  Imagens (3):
           - imagem1.jpg (0.78 MB)
           - imagem2.png (1.23 MB)
    """
    print("\n📂 ARQUIVOS BAIXADOS:")
    
    audio_dir = 'audios'
    video_dir = 'videos'
    image_dir = 'images'
    
    # Lista arquivos de áudio
    if os.path.exists(audio_dir):
        audio_files = os.listdir(audio_dir)
        if audio_files:
            print(f"\n🎵 Áudios ({len(audio_files)}):")
            for file in sorted(audio_files):
                file_path = os.path.join(audio_dir, file)
                file_size = get_file_size_mb(file_path)
                print(f"   - {file} ({format_file_size(file_size)})")
    
    # Lista arquivos de vídeo
    if os.path.exists(video_dir):
        video_files = os.listdir(video_dir)
        if video_files:
            print(f"\n🎬 Vídeos ({len(video_files)}):")
            for file in sorted(video_files):
                file_path = os.path.join(video_dir, file)
                file_size = get_file_size_mb(file_path)
                print(f"   - {file} ({format_file_size(file_size)})")
    
    # Lista arquivos de imagem
    if os.path.exists(image_dir):
        image_files = os.listdir(image_dir)
        if image_files:
            print(f"\n🖼️  Imagens ({len(image_files)}):")
            for file in sorted(image_files):
                file_path = os.path.join(image_dir, file)
                file_size = get_file_size_mb(file_path)
                print(f"   - {file} ({format_file_size(file_size)})")
