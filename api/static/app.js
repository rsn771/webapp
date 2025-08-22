let tg = window.Telegram.WebApp;
tg.ready();
tg.expand();

tg.setHeaderColor('#0088cc');
tg.setBackgroundColor('#ffffff');

let selectedStars = 0;
let selectedPrice = 0;

const starOptions = document.querySelectorAll('.star-option');
const selectedInfo = document.getElementById('selectedInfo');
const selectedCount = document.getElementById('selectedCount');
const selectedPriceElement = document.getElementById('selectedPrice');
const payButton = document.getElementById('payButton');
const status = document.getElementById('status');

starOptions.forEach(option => {
	option.addEventListener('click', () => {
		starOptions.forEach(opt => opt.classList.remove('selected'));
		option.classList.add('selected');
		selectedStars = parseInt(option.dataset.stars);
		selectedPrice = selectedStars;
		selectedInfo.style.display = 'block';
		selectedCount.textContent = selectedStars;
		selectedPriceElement.textContent = selectedPrice;
		payButton.disabled = false;
		status.textContent = '';
		status.className = 'status';
	});
});

payButton.addEventListener('click', async () => {
	if (selectedStars === 0) {
		showStatus('Выберите количество звезд', 'error');
		return;
	}
	try {
		showStatus('Создание платежа...', 'loading');
		payButton.disabled = true;
		const user = tg.initDataUnsafe?.user;
		const userId = user?.id || Math.floor(Math.random() * 1000000);
		const response = await fetch('/create_invoice', {
			method: 'POST',
			headers: { 'Content-Type': 'application/json' },
			body: JSON.stringify({ user_id: userId, stars: selectedStars })
		});
		if (!response.ok) throw new Error('Ошибка создания платежа');
		const data = await response.json();
		if (data.paymentUrl) {
			showStatus('Перенаправление на страницу оплаты...', 'success');
			if (tg.openLink) { tg.openLink(data.paymentUrl); } else { window.open(data.paymentUrl, '_blank'); }
		} else {
			throw new Error('Не получена ссылка для оплаты');
		}
	} catch (error) {
		console.error('Ошибка:', error);
		showStatus('Ошибка создания платежа: ' + error.message, 'error');
		payButton.disabled = false;
	}
});

function showStatus(message, type) {
	status.textContent = message;
	status.className = `status ${type}`;
}

tg.onEvent('viewportChanged', () => {});

tg.BackButton.onClick(() => { tg.close(); });

document.addEventListener('DOMContentLoaded', () => {
	if (tg.initDataUnsafe?.user) {
		const user = tg.initDataUnsafe.user;
		console.log('Пользователь Telegram:', user);
	}
	showStatus('Выберите количество звезд для покупки', '');
});