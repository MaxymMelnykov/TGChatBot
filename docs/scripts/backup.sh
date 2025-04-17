#!/bin/bash

TIMESTAMP=$(date +%F)
BACKUP_DIR="/home/ubuntu/backups/$TIMESTAMP"
PROJECT_DIR="/home/ubuntu/tg-container-bot"

mkdir -p "$BACKUP_DIR"

# 1. Копія коду
rsync -av --exclude '__pycache__' "$PROJECT_DIR" "$BACKUP_DIR/code/"

# 2. Копія конфігів
cp "$PROJECT_DIR/.env" "$BACKUP_DIR/"

# 3. База даних
cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/"  # або `pg_dump` для PostgreSQL

# 4. Копія логів
cp /var/log/tg-bot.log "$BACKUP_DIR/"

# 5. Архівування
tar -czf "/home/ubuntu/backups/backup-$TIMESTAMP.tar.gz" -C "$BACKUP_DIR" .
rm -r "$BACKUP_DIR"
