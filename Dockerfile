FROM eclipse-temurin:17-jdk

# Install Python + utilities
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy Python dependencies and install in venv
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Install LibreTranslate
RUN curl -LO https://github.com/LibreTranslate/LibreTranslate/releases/download/4.12.0/libretranslate-4.12.0.zip \
    && unzip libretranslate-4.12.0.zip -d /libretranslate \
    && rm libretranslate-4.12.0.zip

# Copy bot code
COPY bot/ ./bot
WORKDIR /bot

# Expose ports
EXPOSE 8080
EXPOSE 5000

# Start LibreTranslate and bot
CMD ["sh", "-c", "java -jar /libretranslate/libretranslate.jar & python bot.py"]

