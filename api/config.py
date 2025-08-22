import os
from dotenv import load_dotenv

load_dotenv()

class Config:
	PAYMASTER_TOKEN = os.getenv("PAYMASTER_TOKEN", "1744374395:TEST:1a8282597a855bf711c0")
	PAYMASTER_URL = os.getenv("PAYMASTER_URL", "https://sandbox.paymaster.ru/api/v2/invoices")
	TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "8302025614:AAGiJVFrJwun-DJneCbqetbtJX4VM2O8B7Q")