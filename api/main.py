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

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"],
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_DIR = os.path.join(BASE_DIR, "static")

app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

class InvoiceRequest(BaseModel):
	user_id: int
	stars: int

class PaymentNotification(BaseModel):
	invoice_id: str
	status: str
	amount: float
	currency: str


def _find_url_in_obj(obj):
	"""Best-effort search for first http(s) URL in dict/list/str."""
	try:
		if obj is None:
			return None
		if isinstance(obj, str):
			return obj if obj.startswith("http://") or obj.startswith("https://") else None
		if isinstance(obj, list):
			for item in obj:
				url = _find_url_in_obj(item)
				if url:
					return url
			return None
		if isinstance(obj, dict):
			# check common keys first
			for key in [
				"paymentUrl", "confirmationUrl", "redirectUrl", "payUrl", "url", "link", "href"
			]:
				if key in obj:
					url = _find_url_in_obj(obj.get(key))
					if url:
						return url
			# check links arrays or nested objects
			for k, v in obj.items():
				url = _find_url_in_obj(v)
				if url:
					return url
			return None
		return None
	except Exception:
		return None

@app.get("/", response_class=HTMLResponse)
async def read_root():
	return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/health")
async def health_check():
	return {"status": "healthy", "timestamp": time.time()}

@app.post("/create_invoice")
async def create_invoice(req: InvoiceRequest):
	try:
		if not Config.PAYMASTER_TOKEN or Config.PAYMASTER_TOKEN.strip() == "":
			return {"success": False, "error": "PAYMASTER_TOKEN is not configured on server"}
		payload = {
			"externalId": f"tg_{req.user_id}_{int(time.time())}",
			"amount": {"value": str(req.stars), "currency": "RUB"},
			"description": f"Покупка {req.stars} звёзд для пользователя TG:{req.user_id}",
			"successUrl": "https://t.me/payment_stars_bot",
			"failUrl": "https://t.me/payment_stars_bot",
			"expirationDateTime": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 3600))
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
			status_ok = response.status_code in (200, 201)
			resp_text = response.text
			if not status_ok:
				return {
					"success": False,
					"error": f"PayMaster API error",
					"status": response.status_code,
					"body": resp_text
				}
			try:
				data = response.json()
			except Exception:
				return {"success": False, "error": "Invalid JSON from PayMaster", "body": resp_text}
			payment_url = _find_url_in_obj(data)
			if not payment_url:
				return {"success": False, "error": "Payment URL not received", "data": data}
			return {
				"success": True,
				"paymentUrl": payment_url,
				"invoice_id": data.get("id") or data.get("invoiceId"),
				"amount": req.stars,
				"currency": "RUB"
			}
	except httpx.RequestError as e:
		return {"success": False, "error": f"Network error: {e}"}
	except Exception as e:
		return {"success": False, "error": str(e)}

@app.post("/payment_webhook")
async def payment_webhook(request: Request):
	try:
		body = await request.body()
		data = json.loads(body)
		print(f"Payment webhook received: {data}")
		return {"status": "ok"}
	except Exception as e:
		print(f"Webhook error: {e}")
		return {"status": "error", "message": str(e)}

@app.get("/payment_status/{invoice_id}")
async def get_payment_status(invoice_id: str):
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
			if response.status_code in (200, 201):
				data = response.json()
				return {
					"success": True,
					"status": data.get("status"),
					"amount": data.get("amount"),
					"paid_at": data.get("paidAt")
				}
			else:
				return {"success": False, "error": f"Status check failed", "status": response.status_code, "body": response.text}
	except Exception as e:
		return {"success": False, "error": str(e)}

if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)