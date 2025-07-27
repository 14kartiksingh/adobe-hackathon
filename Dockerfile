FROM --platform=linux/amd64 python:3.9-slim

WORKDIR /app

COPY app/ ./app
COPY input/ ./input
COPY output/ ./output
COPY persona_config.json ./persona_config.json

RUN pip install --no-cache-dir PyMuPDF scikit-learn

CMD ["python", "app/persona_engine.py"]
