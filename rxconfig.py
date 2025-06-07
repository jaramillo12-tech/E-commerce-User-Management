import reflex as rx
import os
from dotenv import load_dotenv

load_dotenv()
config = rx.Config(
    app_name="app",
    db_url=os.getenv(
        "DATABASE_URL", "sqlite:///./techstore.db"
    ),
    backend_port=os.getenv("BACKEND_PORT", 8000),
    frontend_port=os.getenv("FRONTEND_PORT", 3000),
)