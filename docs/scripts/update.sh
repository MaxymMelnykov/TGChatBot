#!/bin/bash

echo "Updating bot..."

# Backup DB or important files here
cp data/database.db backups/db_backup_$(date +%F_%T).db

# Pull latest changes
git pull origin main

# Migrate database if needed
# python migrate.py

# Restart bot
sudo systemctl restart tg-bot

echo "Update complete."
