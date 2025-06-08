import reflex as rx
import asyncio
from app.models.models import (
    CartItem,
    Purchase,
    PurchaseItem,
    User,
)
from sqlmodel import Session, select
from app.database import engine


class CheckoutState(rx.State):
    full_name: str = ""
    address: str = ""
    email: str = ""
    document_id: str = ""
    card_number: str = ""
    card_expiry: str = ""
    card_cvc: str = ""
    error_message: str = ""
    is_processing: bool = False

    @rx.event
    async def process_payment(self, form_data: dict):
        self.full_name = form_data.get("full_name", "")
        self.address = form_data.get("address", "")
        self.email = form_data.get("email", "")
        self.document_id = form_data.get("document_id", "")
        self.card_number = form_data.get("card_number", "")
        self.card_expiry = form_data.get("card_expiry", "")
        self.card_cvc = form_data.get("card_cvc", "")
        if not all(
            [
                self.full_name,
                self.address,
                self.email,
                self.document_id,
                self.card_number,
                self.card_expiry,
                self.card_cvc,
            ]
        ):
            self.error_message = "Todos los campos son obligatorios, incluyendo el documento de identidad."
            yield rx.toast(
                self.error_message, duration=3000
            )
            return
        self.is_processing = True
        self.error_message = ""
        yield
        await asyncio.sleep(2)
        from app.states.cart_state import CartState

        cart_s = await self.get_state(CartState)
        if not cart_s.items:
            self.is_processing = False
            self.error_message = "Tu carrito está vacío. No se puede procesar el pago."
            yield rx.toast(
                self.error_message, duration=3000
            )
            return
        if "1234" in self.card_number:
            self.is_processing = False
            items_for_invoice = [
                item.dict() for item in cart_s.items
            ]
            order_details_for_invoice = {
                "customer_name": self.full_name,
                "customer_address": self.address,
                "customer_email": self.email,
                "customer_document_id": self.document_id,
                "items": items_for_invoice,
                "total_price": cart_s.total_price,
            }
            from app.states.invoice_state import (
                InvoiceState,
            )

            invoice_s = await self.get_state(InvoiceState)
            yield InvoiceState.set_raw_order_data(
                order_details_for_invoice
            )
            await asyncio.sleep(2)
            invoice_s = await self.get_state(InvoiceState)
            with Session(engine) as session:
                from app.states.auth_state import AuthState

                auth_s = await self.get_state(AuthState)
                user_id = None
                if auth_s.is_logged_in:
                    user = session.exec(
                        select(User).where(
                            User.username == auth_s.username
                        )
                    ).first()
                    if user:
                        user_id = user.id
                new_purchase = Purchase(
                    user_id=user_id,
                    customer_name=self.full_name,
                    customer_email=self.email,
                    customer_address=self.address,
                    customer_document_id=self.document_id,
                    total_price=cart_s.total_price,
                    invoice_number=invoice_s.order_details.invoice_number,
                    invoice_pdf_path=invoice_s.invoice_pdf_path
                    or "N/A",
                )
                session.add(new_purchase)
                session.commit()
                session.refresh(new_purchase)
                for item in cart_s.items:
                    purchase_item = PurchaseItem(
                        purchase_id=new_purchase.id,
                        product_id=item.product_id,
                        name=item.name,
                        quantity=item.quantity,
                        price_at_sale=item.price,
                    )
                    session.add(purchase_item)
                session.commit()
            yield rx.toast(
                "¡Pago Exitoso! Gracias por tu pedido.",
                duration=5000,
            )
            self.full_name = ""
            self.address = ""
            self.email = ""
            self.document_id = ""
            self.card_number = ""
            self.card_expiry = ""
            self.card_cvc = ""
            yield rx.redirect("/confirmation")
            yield CartState.clear_cart_after_checkout
        else:
            self.is_processing = False
            self.error_message = "Pago fallido. Por favor, revisa los detalles de tu tarjeta."
            yield rx.toast(
                self.error_message, duration=4000
            )