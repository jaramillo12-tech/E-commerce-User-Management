import reflex as rx
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import datetime


class Complaint(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    name: str
    email: str
    subject: str
    message: str
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    status: str = Field(default="new")
    reply_message: Optional[str] = Field(default=None)
    replied_at: Optional[datetime.datetime] = Field(
        default=None
    )


class Review(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    product_id: int = Field(foreign_key="product.id")
    reviewer_name: str
    rating: int
    comment: Optional[str] = Field(default=None)
    image_url: Optional[str] = Field(default=None)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    product: Optional["Product"] = Relationship(
        back_populates="reviews"
    )


class Product(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    name: str = Field(index=True)
    description: str
    price: float
    image_url: str = Field(default="/placeholder.svg")
    category: str = Field(index=True)
    stock: int = Field(default=0)
    reviews: list["Review"] = Relationship(
        back_populates="product"
    )


class User(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    username: str = Field(unique=True, index=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_admin: bool = Field(default=False)
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    purchases: list["Purchase"] = Relationship(
        back_populates="user"
    )


class PurchaseItem(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    purchase_id: int = Field(foreign_key="purchase.id")
    product_id: int
    name: str
    quantity: int
    price_at_sale: float
    purchase: Optional["Purchase"] = Relationship(
        back_populates="items"
    )


class Purchase(SQLModel, table=True):
    id: Optional[int] = Field(
        default=None, primary_key=True
    )
    user_id: Optional[int] = Field(
        default=None, foreign_key="user.id"
    )
    customer_name: str
    customer_email: str
    customer_address: str
    customer_document_id: str
    total_price: float
    invoice_number: str
    invoice_pdf_path: str
    created_at: datetime.datetime = Field(
        default_factory=datetime.datetime.utcnow
    )
    items: list["PurchaseItem"] = Relationship(
        back_populates="purchase", cascade_delete=True
    )
    user: Optional["User"] = Relationship(
        back_populates="purchases"
    )


class CartItem(rx.Base):
    product_id: int
    name: str
    price: float
    quantity: int
    image_url: str
    stock: int


class DisplayReview(rx.Base):
    id: int
    product_id: int
    reviewer_name: str
    rating: int
    comment: str | None
    image_url: str | None
    created_at_formatted: str