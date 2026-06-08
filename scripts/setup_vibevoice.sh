#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
THIRD_PARTY_DIR="$ROOT_DIR/third_party"
VIBEVOICE_DIR="$THIRD_PARTY_DIR/VibeVoice"

mkdir -p "$THIRD_PARTY_DIR"

if [ ! -d "$VIBEVOICE_DIR" ]; then
  echo "A clonar VibeVoice..."
  git clone https://github.com/microsoft/VibeVoice.git "$VIBEVOICE_DIR"
else
  echo "VibeVoice já existe em $VIBEVOICE_DIR"
fi

echo "A instalar VibeVoice com suporte streamingtts..."
pip install -e "$VIBEVOICE_DIR[streamingtts]"

echo "Instalação concluída."
