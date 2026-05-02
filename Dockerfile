FROM python:3.10

WORKDIR /andi

COPY . /andi

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        git \
        ffmpeg \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

RUN pip install -r requirements.txt

CMD ["python3", "-m", "bot"]
