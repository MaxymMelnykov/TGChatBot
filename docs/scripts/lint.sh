#!/bin/bash
# lint.sh — запуск перевірок як єдиного етапу

echo "🔍 Запускаємо перевірки з pre-commit..."
pre-commit run --all-files

echo ""
echo "✅ Перевірка завершена."
