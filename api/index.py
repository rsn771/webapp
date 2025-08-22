from main import app as fastapi_app

# Vercel Python runtime will look for a top-level ASGI "app"
app = fastapi_app