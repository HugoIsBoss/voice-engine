#!/usr/bin/env python3
"""Gerador simples de voice-over usando VibeVoice-Realtime.

Este script é uma camada fina por cima do demo oficial do VibeVoice.
Ele cria um ficheiro temporário com o texto e chama o script oficial
`realtime_model_inference_from_file.py`.
"""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path


ROOT_DIR = Path(__file__).resolve().parents[1]
DEFAULT_MODEL = "microsoft/VibeVoice-Realtime-0.5B"
DEFAULT_VIBEVOICE_DIR = ROOT_DIR / "third_party" / "VibeVoice"
DEFAULT_OUTPUT = ROOT_DIR / "output" / "voice.wav"


def read_text(args: argparse.Namespace) -> str:
    if args.text:
        return args.text.strip()

    if args.file:
        input_path = Path(args.file)
        if not input_path.exists():
            raise FileNotFoundError(f"Ficheiro não encontrado: {input_path}")
        return input_path.read_text(encoding="utf-8").strip()

    raise ValueError("Tens de passar --text ou --file.")


def build_command(
    vibevoice_dir: Path,
    model: str,
    text_file: Path,
    speaker: str,
    output: Path,
) -> list[str]:
    demo_script = vibevoice_dir / "demo" / "realtime_model_inference_from_file.py"

    if not demo_script.exists():
        raise FileNotFoundError(
            "Não encontrei o script oficial do VibeVoice. "
            "Corre primeiro: bash scripts/setup_vibevoice.sh"
        )

    command = [
        sys.executable,
        str(demo_script),
        "--model_path",
        model,
        "--txt_path",
        str(text_file),
        "--speaker_name",
        speaker,
    ]

    # O demo oficial pode mudar de argumentos entre versões.
    # Se a tua versão suportar --output_path, activamos aqui.
    # Caso contrário, o áudio será gerado no local definido pelo próprio demo.
    if output:
        command.extend(["--output_path", str(output)])

    return command


def main() -> int:
    parser = argparse.ArgumentParser(description="Gerar voice-over com VibeVoice-Realtime.")
    parser.add_argument("--text", help="Texto a converter em voz.")
    parser.add_argument("--file", help="Ficheiro .txt com o texto a converter.")
    parser.add_argument("--voice", default="Carter", help="Nome da voz/speaker. Default: Carter.")
    parser.add_argument("--model", default=os.getenv("VOICE_MODEL", DEFAULT_MODEL), help="Modelo Hugging Face a usar.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Caminho do ficheiro áudio de saída.")
    parser.add_argument(
        "--vibevoice-dir",
        default=str(DEFAULT_VIBEVOICE_DIR),
        help="Pasta onde está clonado o VibeVoice.",
    )

    args = parser.parse_args()

    try:
        text = read_text(args)
        if not text:
            raise ValueError("O texto está vazio.")

        output_path = Path(args.output).resolve()
        output_path.parent.mkdir(parents=True, exist_ok=True)

        vibevoice_dir = Path(args.vibevoice_dir).resolve()

        with tempfile.NamedTemporaryFile("w", suffix=".txt", encoding="utf-8", delete=False) as tmp:
            tmp.write(text)
            tmp_path = Path(tmp.name)

        try:
            command = build_command(
                vibevoice_dir=vibevoice_dir,
                model=args.model,
                text_file=tmp_path,
                speaker=args.voice,
                output=output_path,
            )

            print("A gerar voz...")
            print("Comando:", " ".join(command))
            subprocess.run(command, check=True)
            print(f"Concluído. Output esperado: {output_path}")
            return 0
        finally:
            tmp_path.unlink(missing_ok=True)

    except subprocess.CalledProcessError as exc:
        print(f"Erro ao correr o VibeVoice: {exc}", file=sys.stderr)
        return exc.returncode or 1
    except Exception as exc:
        print(f"Erro: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
