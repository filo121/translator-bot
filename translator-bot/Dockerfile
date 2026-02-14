FROM python:3.13-slim

RUN apt-get update && apt-get install -y \
    curl \
    unzip \
    openjdk-17-jdk \
    && rm -rf /var/lib/apt/lists/*

COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN curl -LO https://github.com/LibreTranslate/LibreTranslate/releases/download/4.12.0/libretranslate-4.12.0.zip \
    && unzip libretranslate-4.12.0.zip -d /libretranslate \
    && rm libretranslate-4.12.0.zip

COPY bot/ ./bot
WORKDIR /bot

EXPOSE 8080
EXPOSE 5000

CMD ["sh", "-c", "java -jar /libretranslate/libretranslate.jar & python bot.py"]
