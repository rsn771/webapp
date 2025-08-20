# 📱 Настройка Telegram Mini App

## Шаг 1: Создание бота

1. **Откройте Telegram и найдите @BotFather**
2. **Отправьте команду `/newbot`**
3. **Следуйте инструкциям:**
   - Введите имя бота (например: "Payment Stars Bot")
   - Введите username бота (например: "payment_stars_bot")
4. **Сохраните токен бота** - он понадобится позже

## Шаг 2: Создание миниприложения

1. **Отправьте @BotFather команду `/newapp`**
2. **Выберите вашего бота из списка**
3. **Заполните информацию о миниприложении:**
   - **Название:** "Payment Stars"
   - **Описание:** "Покупка виртуальных звезд через PayMaster"
   - **URL:** `https://your-domain.com` (замените на ваш домен)
   - **Загрузите иконку** (512x512px, PNG/JPG)

## Шаг 3: Настройка веб-сервера

### Локальная разработка:
```bash
# Запустите сервер
python3 run.py

# Приложение будет доступно на http://localhost:8000
```

### Продакшн деплой:

#### Вариант 1: Heroku
```bash
# Установите Heroku CLI
# Создайте приложение
heroku create your-app-name

# Добавьте переменные окружения
heroku config:set PAYMASTER_TOKEN="1744374395:TEST:1a8282597a855bf711c0"
heroku config:set TELEGRAM_BOT_TOKEN="your_bot_token"

# Деплой
git push heroku main
```

#### Вариант 2: VPS с nginx
```bash
# Установите nginx
sudo apt update
sudo apt install nginx

# Создайте конфигурацию
sudo nano /etc/nginx/sites-available/telegram-app

# Добавьте конфигурацию:
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Активируйте сайт
sudo ln -s /etc/nginx/sites-available/telegram-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx

# Настройте SSL (обязательно для Telegram)
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

## Шаг 4: Настройка PayMaster

1. **Зарегистрируйтесь на [PayMaster](https://paymaster.ru)**
2. **Получите тестовый токен** (уже есть в коде)
3. **Настройте webhook** (опционально):
   - URL: `https://your-domain.com/payment_webhook`
   - Метод: POST

## Шаг 5: Тестирование

1. **Откройте вашего бота в Telegram**
2. **Нажмите на кнопку меню или отправьте команду**
3. **Выберите миниприложение**
4. **Протестируйте покупку звезд**

## 🔧 Полезные команды

### Проверка статуса сервера:
```bash
curl http://localhost:8000/health
```

### Тестирование создания платежа:
```bash
curl -X POST "http://localhost:8000/create_invoice" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123456, "stars": 25}'
```

### Просмотр логов:
```bash
# Если используете systemd
sudo journalctl -u your-app-service -f

# Если запускаете напрямую
python3 run.py
```

## 🐛 Решение проблем

### Проблема: "App not found"
- Убедитесь, что URL в настройках бота правильный
- Проверьте, что сервер доступен извне
- Убедитесь, что используется HTTPS

### Проблема: "Payment failed"
- Проверьте токен PayMaster
- Убедитесь, что тестовый режим активен
- Проверьте логи сервера

### Проблема: "CORS error"
- Проверьте настройки CORS в main.py
- Убедитесь, что домен добавлен в allow_origins

## 📞 Поддержка

Если у вас возникли проблемы:

1. Проверьте логи сервера
2. Убедитесь, что все переменные окружения настроены
3. Проверьте доступность вашего домена
4. Убедитесь, что используется HTTPS (обязательно для Telegram)

---

**Удачной разработки! 🚀**
