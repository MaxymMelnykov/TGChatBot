#!/bin/bash

echo "🚀 Запуск у PRODUCTION-середовищі..."

# Лог-файл
LOG_FILE="/var/log/tg-bot.log"

# Активуємо virtualenv
source /home/ubuntu/tg-container-bot/venv/bin/activate

# Запускаємо бота у фоновому режимі + логування
nohup python3 /home/ubuntu/tg-container-bot/main.py >> $LOG_FILE 2>&1 &
