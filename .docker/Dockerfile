FROM python:3.10-slim

RUN apt-get update && apt-get install -y netcat-openbsd

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Copiar start.sh
COPY .docker/resources/start.sh /start.sh
RUN chmod +x /start.sh

EXPOSE 8000

CMD ["bash", "/start.sh"]
