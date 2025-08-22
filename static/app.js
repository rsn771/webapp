// Инициализация Telegram Web App
let tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

// Настройка темы
tg.setHeaderColor('#0088cc');
tg.setBackgroundColor('#ffffff');

// Состояние приложения
let selectedStars = 0;
let selectedPrice = 0;

// Элементы DOM
const starOptions = document.querySelectorAll('.star-option');
const selectedInfo = document.getElementById('selectedInfo');
const selectedCount = document.getElementById('selectedCount');
const selectedPriceElement = document.getElementById('selectedPrice');
const payButton = document.getElementById('payButton');
const status = document.getElementById('status');

// Обработчики выбора звезд
starOptions.forEach(option => {
    option.addEventListener('click', () => {
        // Убираем выделение со всех опций
        starOptions.forEach(opt => opt.classList.remove('selected'));
        
        // Выделяем выбранную опцию
        option.classList.add('selected');
        
        // Обновляем состояние
        selectedStars = parseInt(option.dataset.stars);
        selectedPrice = selectedStars;
        
        // Показываем информацию о выборе
        selectedInfo.style.display = 'block';
        selectedCount.textContent = selectedStars;
        selectedPriceElement.textContent = selectedPrice;
        
        // Активируем кнопку оплаты
        payButton.disabled = false;
        
        // Скрываем статус
        status.textContent = '';
        status.className = 'status';
    });
});

// Обработчик кнопки оплаты
payButton.addEventListener('click', async () => {
    if (selectedStars === 0) {
        showStatus('Выберите количество звезд', 'error');
        return;
    }
    
    try {
        // Показываем статус загрузки
        showStatus('Создание платежа...', 'loading');
        payButton.disabled = true;
        
        // Получаем данные пользователя из Telegram
        const user = tg.initDataUnsafe?.user;
        const userId = user?.id || Math.floor(Math.random() * 1000000);
        
        // Создаем платеж через API
        const response = await fetch('/create_invoice', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                user_id: userId,
                stars: selectedStars
            })
        });
        
        if (!response.ok) {
            throw new Error('Ошибка создания платежа');
        }
        
        const data = await response.json();
        
        if (data.paymentUrl) {
            showStatus('Перенаправление на страницу оплаты...', 'success');
            
            // Открываем страницу оплаты
            tg.openTelegramLink(data.paymentUrl);
            
            // Альтернативно можно открыть в новом окне
            // window.open(data.paymentUrl, '_blank');
        } else {
            throw new Error('Не получена ссылка для оплаты');
        }
        
    } catch (error) {
        console.error('Ошибка:', error);
        showStatus('Ошибка создания платежа: ' + error.message, 'error');
        payButton.disabled = false;
    }
});

// Функция для отображения статуса
function showStatus(message, type) {
    status.textContent = message;
    status.className = `status ${type}`;
}

// Обработка успешной оплаты (если PayMaster поддерживает webhook)
function handlePaymentSuccess(paymentData) {
    showStatus('Оплата прошла успешно!', 'success');
    
    // Можно отправить уведомление в Telegram
    if (tg.sendData) {
        tg.sendData(JSON.stringify({
            type: 'payment_success',
            stars: selectedStars,
            amount: selectedPrice
        }));
    }
}

// Обработка ошибки оплаты
function handlePaymentError(error) {
    showStatus('Ошибка оплаты: ' + error, 'error');
    payButton.disabled = false;
}

// Обработка закрытия приложения
tg.onEvent('viewportChanged', () => {
    // Адаптация под изменение размера окна
});

// Обработка нажатия кнопки "Назад"
tg.BackButton.onClick(() => {
    tg.close();
});

// Показываем кнопку "Назад" если нужно
// tg.BackButton.show();

// Инициализация при загрузке
document.addEventListener('DOMContentLoaded', () => {
    // Проверяем, что приложение загружено в Telegram
    if (tg.initDataUnsafe?.user) {
        const user = tg.initDataUnsafe.user;
        console.log('Пользователь Telegram:', user);
        
        // Можно персонализировать интерфейс
        // document.querySelector('.header h1').textContent = `Привет, ${user.first_name}!`;
    }
    
    showStatus('Выберите количество звезд для покупки', '');
});