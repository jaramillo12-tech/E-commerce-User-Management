import reflex as rx
import asyncio
from app.models.models import CartItem


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
            items_for_invoice = []
            for item_model in cart_s.items:
                items_for_invoice.append(
                    {
                        "product_id": item_model.product_id,
                        "name": item_model.name,
                        "quantity": item_model.quantity,
                        "price": item_model.price,
                        "image_url": item_model.image_url,
                        "stock": item_model.stock,
                    }
                )
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
            yield rx.toast(
                "¡Pago Exitoso! Gracias por tu pedido.",
                duration=5000,
            )
            from app.states.admin_stats_state import (
                AdminStatsState,
            )

            for item_model in cart_s.items:
                yield AdminStatsState.record_sale_from_cart_item(
                    item_model
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