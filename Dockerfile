# Use lightweight Python image
FROM python:3.14-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY bot.py requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot
CMD ["python", "bot.py"]
