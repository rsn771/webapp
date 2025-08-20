#!/usr/bin/env python3
"""
Скрипт для запуска Telegram Payment Mini App
"""

import uvicorn
from main import app

if __name__ == "__main__":
    print("🚀 Запуск Telegram Payment Mini App...")
    print("📱 Приложение будет доступно по адресу: http://localhost:8000")
    print("🔗 Для Telegram миниприложения используйте: https://your-domain.com")
    print("💳 PayMaster тестовый режим активен")
    print("-" * 50)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
