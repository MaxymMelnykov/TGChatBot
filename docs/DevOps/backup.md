# 🛡️ Інструкція з резервного копіювання Telegram-бота

## Стратегія резервного копіювання
- Повні: раз на тиждень
- Інкрементальні: щодня
- Диференціальні: раз на 3 дні

## Що включає резервна копія
- Код, конфігурації, база даних, логи

## Типи резервних копій
| Тип         | Опис                                     | Частота       |
|-------------|------------------------------------------|----------------|
| Повна       | Усе                                      | Раз на тиждень |
| Інкрементальна | Зміни після останньої копії            | Щодня          |
| Диференціальна | Зміни з моменту останньої повної       | Раз на 3 дні   |

## Скрипт резервного копіювання

Файл: `backup.sh`

```bash
#!/bin/bash

TIMESTAMP=$(date +%F)
BACKUP_DIR="/home/ubuntu/backups/$TIMESTAMP"
PROJECT_DIR="/home/ubuntu/tg-container-bot"

mkdir -p "$BACKUP_DIR"

rsync -av --exclude '__pycache__' "$PROJECT_DIR" "$BACKUP_DIR/code/"
cp "$PROJECT_DIR/.env" "$BACKUP_DIR/"
cp "$PROJECT_DIR/db.sqlite3" "$BACKUP_DIR/"
cp /var/log/tg-bot.log "$BACKUP_DIR/"

tar -czf "/home/ubuntu/backups/backup-$TIMESTAMP.tar.gz" -C "$BACKUP_DIR" .
rm -r "$BACKUP_DIR"
```

## Перевірка цілісності

```bash
tar -tzf backup-YYYY-MM-DD.tar.gz >/dev/null && echo "✅ OK" || echo "❌ Помилка"
```

## Відновлення з резервної копії

```bash
tar -xzf backup-YYYY-MM-DD.tar.gz -C /tmp/
cp -r /tmp/code/* /home/ubuntu/tg-container-bot/
cp /tmp/.env /home/ubuntu/tg-container-bot/
cp /tmp/db.sqlite3 /home/ubuntu/tg-container-bot/
systemctl restart tg-bot
```
