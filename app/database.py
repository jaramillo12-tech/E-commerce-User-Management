import reflex as rx
from sqlmodel import create_engine, SQLModel
from rxconfig import config as app_config
from app.models.models import Product, User, Review

DATABASE_URL = app_config.db_url
if not DATABASE_URL:
    DATABASE_URL = "sqlite:///./techstore.db"
engine = create_engine(DATABASE_URL, echo=False)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)