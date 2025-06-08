import reflex as rx
from typing import Optional
from app.models.models import Purchase, PurchaseItem
from sqlmodel import Session, select
from sqlalchemy.orm import selectinload
from app.database import engine
import datetime
import os


class AdminPurchaseHistoryState(rx.State):
    purchases: list[Purchase] = []

    @rx.event(background=True)
    async def load_purchase_history(self):
        with Session(engine) as session:
            statement = (
                select(Purchase)
                .options(selectinload(Purchase.items))
                .order_by(Purchase.created_at.desc())
            )
            results = session.exec(statement).all()
            async with self:
                self.purchases = results
        yield

    @rx.event
    def view_invoice_pdf(self, invoice_url: str):
        if invoice_url and invoice_url != "N/A":
            return rx.redirect(invoice_url, external=True)
        return rx.toast(
            "La factura para esta compra no está disponible.",
            duration=3000,
        )

    @rx.var
    def formatted_purchase_groups(self) -> list[dict]:
        groups = []
        for pg in self.purchases:
            groups.append(
                {
                    "id": pg.id,
                    "date": pg.created_at.strftime(
                        "%Y-%m-%d %H:%M:%S"
                    ),
                    "customer": pg.customer_name,
                    "email": pg.customer_email,
                    "total": f"{pg.total_price:,.0f} COP",
                    "item_count": sum(
                        (item.quantity for item in pg.items)
                    ),
                    "invoice_available": pg.invoice_pdf_path
                    and pg.invoice_pdf_path != "N/A",
                    "invoice_url": pg.invoice_pdf_path,
                }
            )
        return groups