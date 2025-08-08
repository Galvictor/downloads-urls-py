# 📥 Script de Download de Assets

Este script faz o download automático de todas as URLs encontradas nos arquivos JSON e organiza os arquivos nas pastas corretas.

## 📁 Estrutura de Pastas

Os arquivos serão organizados da seguinte forma:

```
scripts/
├── audios/             # Áudios baixados (.mp3, .wav, .aac, etc.)
├── videos/             # Vídeos baixados (.mp4, .avi, .mov, etc.)
├── images/             # Imagens baixadas (.png, .jpg, etc.)
├── downloads_YYYY-MM-DD_HH-MM-SS.zip  # Arquivo ZIP opcional
├── download_assets.py  # Script principal
├── utils.py            # Módulo de funções auxiliares
├── run_download.py     # Script de execução automática
├── requirements.txt    # Dependências
├── urls.json          # Lista de URLs para download
└── README.md          # Documentação
```

## 🏗️ Arquitetura Modular

O projeto foi organizado em módulos para melhor manutenção:

### 📄 `download_assets.py` - Script Principal

-   **Função**: Orquestra todo o processo de download
-   **Responsabilidades**:
    -   Carrega URLs do arquivo JSON
    -   Coordena o processo de download
    -   Gerencia contadores e estatísticas
    -   Chama funções do módulo utils
    -   **Pergunta sobre criação de ZIP**
    -   **Cria arquivo compactado se solicitado**

### 🔧 `utils.py` - Módulo de Utilitários

-   **Função**: Contém todas as funções auxiliares
-   **Categorias de funções**:
    -   **Manipulação de arquivos**: `get_file_size_mb()`, `clean_directory()`
    -   **Download**: `download_file()` com barra de progresso
    -   **Detecção de tipos**: `is_audio_file()`, `is_video_file()`, `is_image_file()`
    -   **Formatação**: `format_file_size()`, `get_filename_from_url()`
    -   **Relatórios**: `print_download_summary()`, `print_file_listing()`
    -   **Compactação**: `ask_user_for_zip()`, `create_zip_from_downloads()`

## 🚀 Como Usar

### Opção 1: Execução Automática (Recomendado)

```bash
python run_download.py
```

Este comando irá:

1. Instalar automaticamente as dependências
2. Limpar e preparar as pastas de destino
3. Executar o download de todos os arquivos com barra de progresso
4. Mostrar um relatório detalhado com tamanhos
5. **Perguntar se deseja criar um arquivo ZIP**
6. **Criar ZIP e limpar pastas se solicitado**

### Opção 2: Execução Manual

```bash
# 1. Instalar dependências
pip install -r requirements.txt

# 2. Executar o download
python download_assets.py
```

## 📋 Pré-requisitos

-   Python 3.6 ou superior
-   Conexão com a internet
-   Arquivo `urls.json` no diretório atual

## 🔧 Funcionalidades

-   ✅ Download automático de áudios, vídeos e imagens
-   ✅ Organização automática por tipo de arquivo
-   ✅ **Limpeza automática das pastas antes do download**
-   ✅ Criação automática das pastas se não existirem
-   ✅ **Barra de progresso em tempo real (0% a 100%)**
-   ✅ **Monitoramento de tamanho dos arquivos em tempo real**
-   ✅ **Cálculo do espaço total ocupado**
-   ✅ **Arquitetura modular** para fácil manutenção
-   ✅ **Criação opcional de arquivo ZIP** com limpeza automática
-   ✅ Relatório detalhado do progresso
-   ✅ Tratamento de erros
-   ✅ Pausa entre downloads para não sobrecarregar o servidor

## 📊 Tipos de Arquivo Suportados

### Áudios

-   `.mp3`, `.wav`, `.ogg`, `.m4a`, `.aac`

### Vídeos

-   `.mp4`, `.avi`, `.mov`, `.wmv`, `.flv`, `.webm`, `.mkv`

### Imagens

-   `.png`, `.jpg`, `.jpeg`, `.gif`, `.bmp`, `.webp`, `.svg`

## 📈 Relatório Detalhado

O script fornece um relatório completo incluindo:

-   Número de arquivos baixados por tipo
-   **Tamanho total de cada categoria (MB/GB)**
-   **Tamanho individual de cada arquivo**
-   **Espaço total ocupado por todas as pastas**
-   Lista detalhada de arquivos com seus tamanhos
-   Contagem de erros

## ⏳ Barra de Progresso

### Durante o Download

O script mostra uma barra de progresso detalhada para cada arquivo:

```
📥 video.mp4: 100%|██████████| 15.2M/15.2M [00:05<00:00, 3.2MB/s]
```

A barra inclui:

-   **Nome do arquivo** sendo baixado
-   **Percentual** de conclusão (0% a 100%)
-   **Barra visual** de progresso
-   **Bytes baixados/Total** de bytes
-   **Tempo decorrido** e **tempo restante**
-   **Velocidade** de download (MB/s)

### Informações Exibidas

-   📥 Nome do arquivo
-   ██████████ Barra de progresso visual
-   15.2M/15.2M Bytes baixados/Total
-   [00:05<00:00] Tempo decorrido < Tempo restante
-   3.2MB/s Velocidade de download

## 💾 Monitoramento de Tamanho

### Durante o Download

-   Mostra o tamanho de cada arquivo após o download
-   Exemplo: `✅ Download concluído: video.mp4 (15.23 MB)`

### No Relatório Final

-   **Tamanho por categoria:**

    -   Áudios: X arquivos (Y MB/GB)
    -   Vídeos: X arquivos (Y MB/GB)
    -   Imagens: X arquivos (Y MB/GB)

-   **Tamanho total:**

    -   Espaço total ocupado: Z MB/GB

-   **Lista detalhada:**
    -   Cada arquivo com seu tamanho individual

## 📦 Funcionalidade de ZIP

### Após o Download

O script pergunta se você deseja criar um arquivo ZIP:

```
🤔 Deseja criar um arquivo ZIP com todos os downloads? (s/n):
```

### Se Você Responder "Sim" (s/y):

1. **Cria um arquivo ZIP** com timestamp: `downloads_2024-01-15_14-30-25.zip`
2. **Organiza os arquivos** mantendo a estrutura de pastas:
    - `audios/` - Todos os arquivos de áudio
    - `videos/` - Todos os arquivos de vídeo
    - `images/` - Todos os arquivos de imagem
3. **Mostra o progresso** da compressão
4. **Limpa as pastas originais** após criar o ZIP
5. **Exibe o tamanho** do arquivo ZIP criado

### Se Você Responder "Não" (n):

-   Mantém as pastas originais com os arquivos
-   Não cria arquivo ZIP
-   Processo finaliza normalmente

### Exemplo de Saída:

```
🤔 Deseja criar um arquivo ZIP com todos os downloads? (s/n): s

📦 Criando arquivo ZIP...
📁 Adicionando audios/ (5 arquivos)
📁 Adicionando videos/ (19 arquivos)
📁 Adicionando images/ (3 arquivos)
✅ ZIP criado com sucesso: downloads_2024-01-15_14-30-25.zip (171.57 MB)
🗑️  Limpando pastas originais...
✅ Processo concluído! Arquivos compactados e pastas limpas.

🎉 Processo finalizado! Arquivo ZIP criado: downloads_2024-01-15_14-30-25.zip
```

## 🔧 Funções Principais (utils.py)

### Manipulação de Arquivos

-   `get_file_size_mb()` - Calcula tamanho de arquivo em MB
-   `get_directory_size_mb()` - Calcula tamanho total de diretório
-   `clean_directory()` - Limpa ou cria diretórios

### Download

-   `download_file()` - Download com barra de progresso
-   `format_file_size()` - Formata tamanhos para exibição

### Detecção de Tipos

-   `is_audio_file()` - Verifica se é arquivo de áudio
-   `is_video_file()` - Verifica se é arquivo de vídeo
-   `is_image_file()` - Verifica se é arquivo de imagem
-   `determine_file_type_and_path()` - Determina tipo e caminho

### Relatórios

-   `print_download_summary()` - Imprime resumo do download
-   `print_file_listing()` - Lista arquivos com tamanhos

### Compactação

-   `ask_user_for_zip()` - Pergunta se quer criar ZIP
-   `create_zip_from_downloads()` - Cria ZIP e limpa pastas

## ⚠️ Observações

-   **ATENÇÃO**: O script limpa completamente as pastas `audios`, `videos` e `images` antes de cada execução
-   O script faz uma pausa de 0.5 segundos entre downloads para não sobrecarregar o servidor
-   Erros de download são registrados mas não interrompem o processo
-   As pastas `audios`, `videos` e `images` serão criadas automaticamente se não existirem
-   **Tamanhos são calculados automaticamente** e mostrados em MB ou GB conforme apropriado
-   **A barra de progresso funciona apenas quando o servidor fornece o tamanho total do arquivo**
-   **Código modular** facilita manutenção e extensão
-   **Se criar ZIP, as pastas originais serão limpas** após a compressão

## 🧹 Limpeza Automática

Antes de iniciar o download, o script:

1. **Verifica se as pastas existem:**

    - Se não existirem, cria as pastas `audios`, `videos` e `images`
    - Se existirem, remove todo o conteúdo dentro delas

2. **Remove arquivos e subpastas:**
    - Deleta todos os arquivos dentro das pastas
    - Remove subpastas e seu conteúdo
    - Mostra um log detalhado do que foi removido

## 🐛 Solução de Problemas

### Erro de Conexão

Se houver problemas de conexão, o script continuará com os próximos arquivos.

### Arquivo urls.json não encontrado

Certifique-se de que o arquivo `urls.json` está no mesmo diretório do script.

### Erro de Permissão

Certifique-se de ter permissões de escrita no diretório atual.

### Arquivos perdidos

⚠️ **IMPORTANTE**: O script limpa as pastas antes do download. Se você tiver arquivos importantes nas pastas `audios`, `videos` ou `images`, faça backup antes de executar o script.

### Problemas com tamanho de arquivo

Se houver problemas ao calcular o tamanho dos arquivos, o script continuará funcionando normalmente, apenas não mostrará as informações de tamanho.

### Barra de progresso não aparece

Se a barra de progresso não aparecer, pode ser porque:

-   O servidor não fornece o tamanho total do arquivo
-   Problemas de conectividade
-   O script continuará funcionando normalmente, apenas sem a barra visual

### Problemas com módulos

Se houver erro de importação do `utils.py`:

-   Verifique se o arquivo `utils.py` está no mesmo diretório
-   Certifique-se de que todas as dependências estão instaladas

### Problemas com ZIP

Se houver erro ao criar o arquivo ZIP:

-   Verifique se há espaço suficiente no disco
-   Certifique-se de que não há outros processos usando os arquivos
-   As pastas originais serão mantidas em caso de erro

## 📝 Logs

O script mostra logs detalhados durante a execução:

-   🗑️ Limpando pasta
-   📁 Criando pasta
-   📥 Barra de progresso do download
-   ✅ Download concluído (com tamanho)
-   ❌ Erro ao baixar
-   ⚠️ Tipo de arquivo não reconhecido
-   💾 Espaço total ocupado
-   🤔 Pergunta sobre ZIP
-   📦 Criando arquivo ZIP
-   🗑️ Limpando pastas originais
