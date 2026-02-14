FROM eclipse-temurin:17-jdk

# Install tools
RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-venv \
    python3-pip \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Create Python virtual environment
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Install Python dependencies
COPY bot/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Clone LibreTranslate
RUN git clone https://github.com/LibreTranslate/LibreTranslate.git /libretranslate-source

# Build LibreTranslate
WORKDIR /libretranslate-source
RUN ./build.sh

# Copy bot
COPY bot/ /bot
WORKDIR /bot

# Expose ports
EXPOSE 8080
EXPOSE 5000

# Start LibreTranslate and bot
CMD ["sh", "-c", "java -jar /libretranslate-source/libretranslate.jar & python bot.py"]



