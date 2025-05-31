FROM python:3.12-slim


RUN apt update && \
    apt install -y curl bash dos2unix zip unzip mc && \
    apt install -y iputils-ping dnsutils && \
    apt clean && \
    rm -rf /var/lib/apt/lists/*


WORKDIR /app
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY TelegramBot ./TelegramBot

CMD ["python", "TelegramBot/flowerdelivery_bot.py"]
