import reflex as rx
from app.models.models import Product as ProductModel
from app.states.product_state import ProductState
from app.states.cart_state import CartState
from app.states.theme_state import ThemeState


def lite_product_card(
    product: ProductModel, is_sponsored: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    product.name,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-lg font-semibold text-sky-700 mb-1",
                        "text-lg font-semibold text-sky-300 mb-1",
                    ),
                ),
                rx.el.p(
                    f"COP {product.price:,.0f}",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-md text-green-600 font-bold mb-2",
                        "text-md text-green-400 font-bold mb-2",
                    ),
                ),
                class_name="flex-grow",
            ),
            rx.cond(
                is_sponsored,
                rx.el.span(
                    "Sponsor",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "absolute top-1 right-1 bg-yellow-300 text-yellow-700 text-xs font-medium px-1.5 py-0.5 rounded",
                        "absolute top-1 right-1 bg-yellow-600 text-yellow-100 text-xs font-medium px-1.5 py-0.5 rounded",
                    ),
                ),
                rx.el.div(),
            ),
            class_name="relative flex-grow",
        ),
        rx.el.div(
            rx.el.button(
                "Ver Detalles",
                on_click=lambda: ProductState.select_product(
                    product
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-3 rounded-md text-sm button-light-interactive",
                    "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-3 rounded-md text-sm",
                ),
                disabled=product.stock == 0,
            ),
            rx.el.button(
                "Añadir al Carrito",
                on_click=lambda: CartState.add_item(
                    {
                        "product_id": product.id,
                        "name": product.name,
                        "price": product.price,
                        "quantity": 1,
                        "image_url": product.image_url,
                        "stock": product.stock,
                    },
                    1,
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full mt-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-3 rounded-md text-sm button-light-interactive",
                    "w-full mt-2 bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-3 rounded-md text-sm",
                ),
                disabled=product.stock == 0,
            ),
            rx.cond(
                product.stock == 0,
                rx.el.p(
                    "Agotado",
                    class_name="text-center text-red-500 text-xs mt-1",
                ),
                rx.el.div(),
            ),
            class_name="mt-auto",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "relative bg-white p-3 rounded-lg shadow border border-sky-200 flex flex-col h-full",
            "relative bg-gray-800 p-3 rounded-lg shadow border border-gray-700 flex flex-col h-full",
        ),
    )