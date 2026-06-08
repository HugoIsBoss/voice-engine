# Voice Engine

Motor experimental para gerar voice-over a partir de texto, usando o VibeVoice-Realtime como base.

Este projecto foi pensado como uma camada simples por cima do VibeVoice: escreves texto, escolhes uma voz, e o script gera um ficheiro de áudio.

> Estado actual: prova de conceito. Primeiro objectivo: correr localmente ou em Colab. Depois podemos evoluir para API, interface web e workflows mais completos.

## Objectivo

- Gerar voice-over a partir de texto.
- Testar vozes disponíveis no VibeVoice-Realtime.
- Criar um fluxo simples para scripts de marketing, vídeos e narrações.
- Guardar outputs áudio numa pasta local.

## Estrutura

```text
voice-engine/
├── README.md
├── .gitignore
├── .env.example
├── requirements.txt
├── input/
│   └── sample.txt
├── output/
│   └── .gitkeep
├── scripts/
│   ├── generate_voice.py
│   └── setup_vibevoice.sh
└── docker/
    └── Dockerfile
```

## Instalação local

Este projecto assume uma máquina com Python 3.11+ e, idealmente, uma GPU NVIDIA para correr o VibeVoice de forma decente.

### 1. Clonar este repo

```bash
git clone https://github.com/HugoIsBoss/voice-engine.git
cd voice-engine
```

### 2. Criar ambiente Python

```bash
python -m venv .venv
source .venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

Em Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Instalar o VibeVoice

```bash
bash scripts/setup_vibevoice.sh
```

Isto vai clonar o repositório oficial da Microsoft para `third_party/VibeVoice` e instalar o extra `streamingtts`.

## Gerar um voice-over

A partir de um ficheiro:

```bash
python scripts/generate_voice.py \
  --file input/sample.txt \
  --voice Carter \
  --output output/sample.wav
```

Ou directamente com texto:

```bash
python scripts/generate_voice.py \
  --text "Olá. Isto é um teste de voice-over gerado por IA." \
  --voice Carter \
  --output output/test.wav
```

## Modelo usado

Por defeito, o projecto usa:

```text
microsoft/VibeVoice-Realtime-0.5B
```

Podes mudar com:

```bash
python scripts/generate_voice.py \
  --file input/sample.txt \
  --model microsoft/VibeVoice-Realtime-0.5B \
  --voice Carter
```

## Notas importantes

- O VibeVoice-Realtime é experimental.
- A qualidade em português deve ser testada caso a caso.
- Não uses este projecto para clonar vozes reais sem autorização explícita.
- Para uso comercial, valida licenças, qualidade, privacidade e compliance antes de avançar.

## Próximos passos

- Adicionar API com FastAPI.
- Criar interface web simples.
- Adicionar fila de jobs para textos longos.
- Exportar WAV/MP3.
- Criar presets de vozes.
- Criar templates de narração para vídeos.
