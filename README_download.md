# 📥 Script de Download de Assets

Este script faz o download automático de todas as URLs encontradas nos arquivos JSON e organiza os arquivos nas pastas corretas.

## 📁 Estrutura de Pastas

Os arquivos serão organizados da seguinte forma:

```
scripts/
├── audios/             # Áudios baixados (.mp3, .wav, .aac, etc.)
├── videos/             # Vídeos baixados (.mp4, .avi, .mov, etc.)
├── images/             # Imagens baixadas (.png, .jpg, etc.)
├── download_assets.py
├── run_download.py
├── requirements.txt
├── urls.json
└── README_download.md
```

## 🚀 Como Usar

### Opção 1: Execução Automática (Recomendado)

```bash
python run_download.py
```

Este comando irá:

1. Instalar automaticamente as dependências
2. Limpar e preparar as pastas de destino
3. Executar o download de todos os arquivos
4. Mostrar um relatório detalhado

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

## 📈 Relatório

O script fornece um relatório detalhado incluindo:

-   Número de áudios baixados
-   Número de vídeos baixados
-   Número de imagens baixadas
-   Lista de arquivos baixados
-   Contagem de erros

## ⚠️ Observações

-   **ATENÇÃO**: O script limpa completamente as pastas `audios`, `videos` e `images` antes de cada execução
-   O script faz uma pausa de 0.5 segundos entre downloads para não sobrecarregar o servidor
-   Erros de download são registrados mas não interrompem o processo
-   As pastas `audios`, `videos` e `images` serão criadas automaticamente se não existirem

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

## 📝 Logs

O script mostra logs detalhados durante a execução:

-   🗑️ Limpando pasta
-   📁 Criando pasta
-   ✅ Download concluído
-   ❌ Erro ao baixar
-   ⚠️ Tipo de arquivo não reconhecido
