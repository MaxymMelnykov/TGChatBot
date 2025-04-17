# 📦 Production Deployment Guide for Telegram Bot

Цей документ призначений для DevOps/Release-інженерів. Він описує процес розгортання Telegram-бота у виробничому середовищі.

---
## 1. Вимоги до апаратного забезпечення
| Компонент         | Мінімальні вимоги                                    |
|-------------------|------------------------------------------------------|
| Архітектура        | x86_64 (або ARM64 для VPS)                           |
| CPU               | 1 vCPU                                               |
| RAM               | 512 MB (1 GB рекомендується)                         |
| Диск              | 512 MB (SSD рекомендовано)                           |
| ОС                | Ubuntu 20.04+, Debian 11+, або сумісна Linux-система |

---

## 2. Необхідне програмне забезпечення
- Python 3.10+
- pip (Python package manager)
- Git
- systemd (для автозапуску як сервіс)
- (опціонально) Docker (альтернатива systemd)

---

## 3. Налаштування мережі

- Вихід в інтернет, якщо використовується Long Polling
- Дозвіл на підключення до `api.telegram.org`

---
### 4.1 Створення файлу сервісу /etc/systemd/system/tg-bot.service
```text
[Unit]
Description=Telegram Bot Service
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/ubuntu/локальна-директорія(в нашому випадку tg-container-bot)
ExecStart=/home/ubuntu/tg-container-bot/venv/bin/python3 main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

### 4.1 Створення користувача бота:
```bash
sudo adduser tg_bot
sudo su - tg_bot
```
### 4.2 Клонування репозиторію:
```bash
git clone https://github.com/your_username/tg-container-bot.git
cd tg-container-bot
```

### 4.3 Налаштування Python:
```bash
sudo apt update
sudo apt install python3.10 python3.10-venv git -y
```
```bash
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```
### 4.4 Створення .env з токеном:
```bash
echo "BOT_TOKEN=your_token_here" > .env
```
## 6. Розгортання коду
## Docker

```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY .. .
RUN pip install -r requirements.txt
CMD ["python", "main.py"]
```
```bash
docker build -t tg-bot .
docker run -d --name telegram-bot --env BOT_TOKEN=your_token_here tg-bot
```

## 7. Перевірка працездатності
В Telegram:
- Відкрити бота
- Ввести /start
- Перевірити, чи з'являється стартове повідомлення
