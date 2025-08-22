import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from main import app as app

# Vercel Python runtime will look for a top-level ASGI "app"