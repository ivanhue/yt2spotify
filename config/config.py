# src/config.py
from dotenv import load_dotenv
import os
from pathlib import Path

# Cargar el .env automáticamente al importar este módulo
load_dotenv(dotenv_path=Path(__file__).resolve().parents[1] / ".env")

# Variables centralizadas
YOUTUBE_CLIENT_ID = os.getenv("YOUTUBE_CLIENT_ID")
YOUTUBE_CLIENT_SECRET = os.getenv("YOUTUBE_CLIENT_SECRET")

SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_CLIENT_SECRET = os.getenv("SPOTIFY_CLIENT_SECRET")
SPOTIPY_REDIRECT_URI = os.getenv("SPOTIPY_REDIRECT_URI")
