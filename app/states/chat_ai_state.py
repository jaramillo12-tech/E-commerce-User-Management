import reflex as rx
import asyncio
from app.states.product_state import ProductState


class ChatAIState(rx.State):
    is_chat_open: bool = False
    is_processing: bool = False
    messages: list[dict[str, str]] = []

    @rx.event
    def toggle_chat(self):
        self.is_chat_open = not self.is_chat_open
        if self.is_chat_open and (not self.messages):
            self.messages = [
                {
                    "role": "assistant",
                    "content": "¡Hola! Soy tu asistente de compras. ¿Cómo puedo ayudarte a encontrar el producto perfecto?",
                }
            ]

    @rx.event(background=True)
    async def handle_submit(self, form_data: dict):
        question = form_data.get("question", "").strip()
        if not question:
            return
        async with self:
            self.messages.append(
                {"role": "user", "content": question}
            )
            self.is_processing = True
            yield
        await asyncio.sleep(1)
        product_s = await self.get_state(ProductState)
        products = product_s.products
        product_info = ""
        if products:
            product_info = ". ".join(
                [
                    f"{p.name}: {p.description[:100]}..."
                    for p in products[:5]
                ]
            )
        response_text = "No estoy seguro de cómo responder a eso. ¿Puedes preguntar sobre nuestros productos?"
        if any(
            (
                keyword in question.lower()
                for keyword in ["laptop", "portátil"]
            )
        ):
            response_text = "Tenemos varias laptops potentes. La Laptop Pro X1 es excelente para profesionales. ¿Quieres saber más sobre ella?"
        elif any(
            (
                keyword in question.lower()
                for keyword in [
                    "celular",
                    "teléfono",
                    "smartphone",
                ]
            )
        ):
            response_text = "El Smartphone Galaxy S25 Ultra es nuestro modelo más nuevo con una cámara increíble. ¿Te gustaría ver sus especificaciones?"
        elif "precio" in question.lower():
            response_text = "Para ver los precios, por favor explora nuestra sección de productos. ¿Qué categoría te interesa?"
        async with self:
            self.messages.append(
                {
                    "role": "assistant",
                    "content": response_text,
                }
            )
            self.is_processing = False
            yield