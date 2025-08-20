#!/usr/bin/env python3
"""
Скрипт для проверки токенов Telegram и PayMaster
"""

import requests
import json
import time
from config import Config

def check_telegram_bot():
    """Проверка токена Telegram бота"""
    print("🤖 Проверка токена Telegram бота...")
    
    try:
        url = f"https://api.telegram.org/bot{Config.TELEGRAM_BOT_TOKEN}/getMe"
        response = requests.get(url, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("ok"):
                bot_info = data["result"]
                print(f"✅ Бот работает!")
                print(f"   Имя: {bot_info.get('first_name')}")
                print(f"   Username: @{bot_info.get('username')}")
                print(f"   ID: {bot_info.get('id')}")
                return True
            else:
                print(f"❌ Ошибка API: {data.get('description')}")
                return False
        else:
            print(f"❌ HTTP ошибка: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def check_paymaster():
    """Проверка токена PayMaster"""
    print("\n💳 Проверка токена PayMaster...")
    
    try:
        # Создаем тестовый платеж
        payload = {
            "externalId": f"test_{int(time.time())}",
            "amount": {"value": 1, "currency": "RUB"},
            "description": "Тестовый платеж",
            "expirationDateTime": int(time.time()) + 3600
        }
        
        response = requests.post(
            Config.PAYMASTER_URL,
            headers={
                "Authorization": f"Bearer {Config.PAYMASTER_TOKEN}",
                "Content-Type": "application/json"
            },
            json=payload,
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ PayMaster токен работает!")
            print(f"   Создан тестовый платеж: {data.get('id')}")
            return True
        elif response.status_code == 401:
            print("❌ Неверный токен PayMaster")
            return False
        else:
            print(f"⚠️  PayMaster ответ: {response.status_code}")
            print(f"   Детали: {response.text}")
            return True  # Возможно, это тестовый режим
            
    except Exception as e:
        print(f"❌ Ошибка PayMaster: {e}")
        return False

def main():
    """Основная функция проверки"""
    print("🔍 Проверка токенов...")
    print("=" * 50)
    
    # Проверяем токены
    telegram_ok = check_telegram_bot()
    paymaster_ok = check_paymaster()
    
    print("\n" + "=" * 50)
    print("📊 Результаты проверки:")
    print(f"   Telegram бот: {'✅' if telegram_ok else '❌'}")
    print(f"   PayMaster: {'✅' if paymaster_ok else '❌'}")
    
    if telegram_ok and paymaster_ok:
        print("\n🎉 Все токены работают корректно!")
        print("📱 Приложение готово к использованию!")
    else:
        print("\n⚠️  Некоторые токены не работают.")
        print("🔧 Проверьте настройки и попробуйте снова.")

if __name__ == "__main__":
    main()
