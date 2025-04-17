#!/bin/bash

echo "Deploying the Telegram Bot..."

# Pull latest code
git pull origin main

# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Restart service
sudo systemctl restart tg-bot

echo "Deployment complete."
