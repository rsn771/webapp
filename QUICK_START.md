# 🚀 Быстрый старт

## Установка и запуск

1. **Установите зависимости:**
```bash
python3 -m pip install -r requirements.txt
```

2. **Запустите сервер:**
```bash
python3 run.py
```

3. **Откройте в браузере:**
```
http://localhost:8000
```

4. **Запустите тесты:**
```bash
python3 test_app.py
```

## 📱 Настройка Telegram

1. Создайте бота через @BotFather (`/newbot`)
2. Создайте миниприложение (`/newapp`)
3. Укажите URL вашего сервера
4. Протестируйте в Telegram

## 💳 PayMaster

- Токен уже настроен для тестового режима
- Для продакшна замените на реальный токен
- Настройте webhook при необходимости

## 📁 Структура проекта

```
backend/
├── main.py              # FastAPI сервер
├── config.py            # Конфигурация
├── run.py              # Запуск сервера
├── test_app.py         # Тесты
├── static/             # Веб-интерфейс
│   ├── index.html      # Главная страница
│   ├── styles.css      # Стили
│   └── app.js          # JavaScript
└── README.md           # Полная документация
```

## 🔧 Полезные команды

```bash
# Запуск сервера
python3 run.py

# Тестирование
python3 test_app.py

# Проверка здоровья
curl http://localhost:8000/health

# Создание платежа
curl -X POST "http://localhost:8000/create_invoice" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "stars": 25}'
```

---

**Готово! 🎉**
