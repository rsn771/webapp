# 💳 Telegram Payment Mini App с PayMaster

Полноценное миниприложение для Telegram с интеграцией платежной системы PayMaster для покупки виртуальных звезд.

## 🚀 Возможности

- ✅ Красивый адаптивный интерфейс
- ✅ Интеграция с Telegram Web App API
- ✅ Платежи через PayMaster (тестовый режим)
- ✅ Выбор количества звезд (10, 25, 50, 100)
- ✅ Обработка платежей и webhook'ов
- ✅ Современный дизайн с анимациями

## 📋 Требования

- Python 3.8+
- FastAPI
- PayMaster тестовый аккаунт
- Telegram Bot Token

## 🛠 Установка

1. **Клонируйте репозиторий:**
```bash
git clone <your-repo>
cd backend
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте переменные окружения:**
Создайте файл `.env` в корне проекта:
```env
PAYMASTER_TOKEN=1744374395:TEST:1a8282597a855bf711c0
PAYMASTER_URL=https://sandbox.paymaster.ru/api/v2/invoices
TELEGRAM_BOT_TOKEN=8302025614:AAGiJVFrJwun-DJneCbqetbtJX4VM2O8B7Q
```

## 🚀 Запуск

### Локальная разработка:
```bash
python run.py
```

### Продакшн:
```bash
uvicorn main:app --host 0.0.0.0 --port 8000
```

Приложение будет доступно по адресу: `http://localhost:8000`

## 📱 Настройка Telegram Bot

1. **Создайте бота через @BotFather**
2. **Получите токен бота**
3. **Настройте миниприложение:**
   - Отправьте `/newapp` @BotFather
   - Выберите вашего бота
   - Укажите название и описание
   - Укажите URL вашего приложения (например: `https://your-domain.com`)
   - Загрузите иконку приложения

## 🔧 Структура проекта

```
backend/
├── main.py              # Основной FastAPI сервер
├── config.py            # Конфигурация
├── requirements.txt     # Зависимости Python
├── run.py              # Скрипт запуска
├── static/             # Статические файлы
│   ├── index.html      # Главная страница
│   ├── styles.css      # Стили
│   └── app.js          # JavaScript логика
└── README.md           # Документация
```

## 🔌 API Endpoints

### Основные эндпоинты:

- `GET /` - Главная страница миниприложения
- `GET /health` - Проверка здоровья сервиса
- `POST /create_invoice` - Создание платежного счета
- `POST /payment_webhook` - Webhook для уведомлений PayMaster
- `GET /payment_status/{invoice_id}` - Статус платежа

### Пример создания платежа:

```bash
curl -X POST "http://localhost:8000/create_invoice" \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123456, "stars": 25}'
```

## 💳 Настройка PayMaster

1. **Зарегистрируйтесь на [PayMaster](https://paymaster.ru)**
2. **Получите тестовый токен**
3. **Настройте webhook URL** (если нужно):
   - URL: `https://your-domain.com/payment_webhook`
   - Метод: POST

## 🎨 Кастомизация

### Изменение цен:
Отредактируйте файл `static/index.html`:
```html
<div class="star-option" data-stars="10">
    <div class="star-price">10 ₽</div>
</div>
```

### Изменение цветов:
Отредактируйте файл `static/styles.css`:
```css
:root {
    --primary-color: #0088cc;
    --secondary-color: #f8f9fa;
}
```

### Добавление новых опций:
1. Добавьте HTML в `static/index.html`
2. Обновите JavaScript в `static/app.js`
3. При необходимости обновите CSS

## 🔒 Безопасность

- ✅ Валидация входных данных
- ✅ Обработка ошибок
- ✅ CORS настройки
- ✅ Таймауты для API запросов
- ✅ Логирование платежей

## 🐛 Отладка

### Проверка логов:
```bash
tail -f logs/app.log
```

### Тестирование API:
```bash
# Проверка здоровья
curl http://localhost:8000/health

# Создание тестового платежа
curl -X POST http://localhost:8000/create_invoice \
     -H "Content-Type: application/json" \
     -d '{"user_id": 123, "stars": 10}'
```

## 📦 Деплой

### Heroku:
```bash
heroku create your-app-name
git push heroku main
```

### Docker:
```bash
docker build -t telegram-payment-app .
docker run -p 8000:8000 telegram-payment-app
```

### VPS:
```bash
# Установите nginx
sudo apt install nginx

# Настройте reverse proxy
sudo nano /etc/nginx/sites-available/telegram-app

# Активируйте сайт
sudo ln -s /etc/nginx/sites-available/telegram-app /etc/nginx/sites-enabled/
sudo systemctl restart nginx
```

## 🤝 Поддержка

Если у вас возникли вопросы или проблемы:

1. Проверьте логи сервера
2. Убедитесь, что все переменные окружения настроены
3. Проверьте доступность PayMaster API
4. Убедитесь, что URL миниприложения доступен извне

## 📄 Лицензия

MIT License

---

**Удачной разработки! 🚀**
