FROM nvcr.io/nvidia/pytorch:24.07-py3

WORKDIR /workspace/voice-engine

COPY requirements.txt ./requirements.txt
RUN pip install --upgrade pip && pip install -r requirements.txt

COPY . .

RUN bash scripts/setup_vibevoice.sh

CMD ["python", "scripts/generate_voice.py", "--file", "input/sample.txt", "--voice", "Carter", "--output", "output/sample.wav"]
