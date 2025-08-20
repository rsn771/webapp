from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from pydantic import BaseModel
import httpx
import os
import time
import json
from config import Config

app = FastAPI(title="Telegram Payment Mini App", version="1.0.0")

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключение статических файлов
app.mount("/static", StaticFiles(directory="static"), name="static")

# Модели данных
class InvoiceRequest(BaseModel):
    user_id: int
    stars: int

class PaymentNotification(BaseModel):
    invoice_id: str
    status: str
    amount: float
    currency: str

# Основные эндпоинты
@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Главная страница миниприложения"""
    return FileResponse("static/index.html")

@app.get("/health")
async def health_check():
    """Проверка здоровья сервиса"""
    return {"status": "healthy", "timestamp": time.time()}

@app.post("/create_invoice")
async def create_invoice(req: InvoiceRequest):
    """Создание платежного счета через PayMaster"""
    try:
        payload = {
            "externalId": f"tg_{req.user_id}_{int(time.time())}",
            "amount": {"value": req.stars, "currency": "RUB"},
            "description": f"Покупка {req.stars} звёзд для пользователя TG:{req.user_id}",
            "successUrl": "https://t.me/payment_stars_bot",  # URL вашего бота
            "failUrl": "https://t.me/payment_stars_bot",     # URL вашего бота
            "expirationDateTime": int(time.time()) + 3600,  # Счет действителен 1 час
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                Config.PAYMASTER_URL,
                headers={
                    "Authorization": f"Bearer {Config.PAYMASTER_TOKEN}",
                    "Content-Type": "application/json"
                },
                json=payload,
                timeout=30.0
            )
            
            if response.status_code != 200:
                raise Exception(f"PayMaster API error: {response.status_code}")
            
            data = response.json()
            
            if "paymentUrl" not in data:
                raise Exception("Payment URL not received from PayMaster")
            
            return {
                "success": True,
                "paymentUrl": data["paymentUrl"],
                "invoice_id": data.get("id"),
                "amount": req.stars,
                "currency": "RUB"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

@app.post("/payment_webhook")
async def payment_webhook(request: Request):
    """Webhook для получения уведомлений от PayMaster"""
    try:
        body = await request.body()
        data = json.loads(body)
        
        # Логируем уведомление
        print(f"Payment webhook received: {data}")
        
        # Здесь можно добавить логику обработки платежа
        # Например, обновить статус в базе данных, отправить уведомление пользователю
        
        return {"status": "ok"}
        
    except Exception as e:
        print(f"Webhook error: {e}")
        return {"status": "error", "message": str(e)}

@app.get("/payment_status/{invoice_id}")
async def get_payment_status(invoice_id: str):
    """Получение статуса платежа"""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{Config.PAYMASTER_URL}/{invoice_id}",
                headers={
                    "Authorization": f"Bearer {Config.PAYMASTER_TOKEN}",
                    "Content-Type": "application/json"
                },
                timeout=30.0
            )
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "success": True,
                    "status": data.get("status"),
                    "amount": data.get("amount"),
                    "paid_at": data.get("paidAt")
                }
            else:
                return {
                    "success": False,
                    "error": f"Status check failed: {response.status_code}"
                }
                
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# Запуск сервера
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)