import reflex as rx
from app.components.navbar import navbar
from app.components.product_list import (
    product_carousels_display,
)
from app.components.selected_product_view import (
    selected_product_modal,
)
from app.components.cart_sidebar import cart_sidebar
from app.states.product_state import ProductState
from app.states.theme_state import ThemeState
from app.components.chat_ai_widget import chat_ai_widget


def products_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            product_carousels_display(),
            selected_product_modal(),
            cart_sidebar(),
            chat_ai_widget(),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "min-h-screen text-sky-800 pt-16 sm:pt-20 bg-white",
                "min-h-screen text-white pt-16 sm:pt-20 bg-slate-900",
            ),
        ),
        on_mount=ProductState.load_products,
        class_name=ThemeState.current_theme,
    )