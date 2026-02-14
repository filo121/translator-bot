FROM eclipse-temurin:17-jdk

# Install Python + utilities
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Download LibreTranslate JAR
RUN mkdir -p /libretranslate
RUN curl -L -o /libretranslate/libretranslate.jar https://github.com/LibreTranslate/LibreTranslate/releases/download/4.11.0/libretranslate.jar

# Copy bot
COPY bot/ /bot
WORKDIR /bot

# Expose ports
EXPOSE 8080
EXPOSE 5000

# Start LibreTranslate and bot
CMD ["sh", "-c", "java -jar /libretranslate/libretranslate.jar & python bot.py"]



