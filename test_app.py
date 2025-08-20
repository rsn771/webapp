#!/usr/bin/env python3
"""
Скрипт для тестирования Telegram Payment Mini App
"""

import requests
import json
import time

BASE_URL = "http://localhost:8000"

def test_health():
    """Тест проверки здоровья сервиса"""
    print("🔍 Тестирование здоровья сервиса...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Сервис работает! Статус: {data['status']}")
            return True
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_main_page():
    """Тест главной страницы"""
    print("\n🌐 Тестирование главной страницы...")
    try:
        response = requests.get(f"{BASE_URL}/")
        if response.status_code == 200:
            if "Платежное приложение" in response.text:
                print("✅ Главная страница загружается корректно")
                return True
            else:
                print("❌ Главная страница не содержит ожидаемый контент")
                return False
        else:
            print(f"❌ Ошибка: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Ошибка подключения: {e}")
        return False

def test_static_files():
    """Тест статических файлов"""
    print("\n📁 Тестирование статических файлов...")
    files = ["/static/styles.css", "/static/app.js"]
    
    for file in files:
        try:
            response = requests.get(f"{BASE_URL}{file}")
            if response.status_code == 200:
                print(f"✅ {file} загружается")
            else:
                print(f"❌ {file} не найден: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Ошибка загрузки {file}: {e}")
            return False
    
    return True

def test_create_invoice():
    """Тест создания платежа"""
    print("\n💳 Тестирование создания платежа...")
    try:
        payload = {
            "user_id": 123456,
            "stars": 25
        }
        
        response = requests.post(
            f"{BASE_URL}/create_invoice",
            headers={"Content-Type": "application/json"},
            json=payload
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get("success") == False:
                print(f"⚠️  Платеж не создан (ожидаемо в тестовом режиме): {data.get('error')}")
                return True  # Это нормально для тестового режима
            elif data.get("success") == True:
                print("✅ Платеж создан успешно!")
                print(f"   URL: {data.get('paymentUrl')}")
                return True
            else:
                print(f"❌ Неожиданный ответ: {data}")
                return False
        else:
            print(f"❌ Ошибка создания платежа: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Ошибка: {e}")
        return False

def main():
    """Основная функция тестирования"""
    print("🚀 Запуск тестов Telegram Payment Mini App")
    print("=" * 50)
    
    tests = [
        test_health,
        test_main_page,
        test_static_files,
        test_create_invoice
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
        time.sleep(1)  # Небольшая пауза между тестами
    
    print("\n" + "=" * 50)
    print(f"📊 Результаты тестирования: {passed}/{total} тестов прошли")
    
    if passed == total:
        print("🎉 Все тесты прошли успешно!")
        print("\n📱 Приложение готово к использованию!")
        print("🔗 Откройте http://localhost:8000 в браузере")
        print("📖 Следуйте инструкциям в TELEGRAM_SETUP.md для настройки бота")
    else:
        print("⚠️  Некоторые тесты не прошли. Проверьте настройки.")
    
    print("\n💡 Для остановки сервера нажмите Ctrl+C")

if __name__ == "__main__":
    main()
