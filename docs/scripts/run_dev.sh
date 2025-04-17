#!/bin/bash

echo "🔧 Запускаю Telegram-бота в DEV-режимі..."

# Активуємо virtualenv
source venv/bin/activate

# Запускаємо головний файл
python3 main.py
