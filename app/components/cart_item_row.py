import reflex as rx
from app.models.models import CartItem
from app.states.cart_state import CartState
from app.states.theme_state import ThemeState


def cart_item_row(item: CartItem) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=item.image_url,
            alt=item.name,
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "w-16 h-16 object-cover rounded mr-4 border border-sky-200",
                "w-16 h-16 object-cover rounded mr-4 border border-gray-700",
            ),
        ),
        rx.el.div(
            rx.el.h4(
                item.name,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "font-semibold text-sky-700",
                    "font-semibold text-sky-300",
                ),
            ),
            rx.el.p(
                f"${item.price:.2f} x {item.quantity}",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-sm text-sky-600",
                    "text-sm text-gray-400",
                ),
            ),
            class_name="flex-grow",
        ),
        rx.el.div(
            rx.el.button(
                "-",
                on_click=lambda: CartState.update_item_quantity(
                    item.product_id, -1
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "px-2 py-1 bg-sky-100 hover:bg-sky-200 rounded-l text-sm text-sky-700 focus:outline-none focus:ring-1 focus:ring-sky-400",
                    "px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded-l text-sm text-white focus:outline-none focus:ring-1 focus:ring-sky-500",
                ),
            ),
            rx.el.span(
                item.quantity,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "px-3 py-1 bg-white text-sm text-sky-800 border-y border-sky-200",
                    "px-3 py-1 bg-gray-800 text-sm text-white border-y border-gray-700",
                ),
            ),
            rx.el.button(
                "+",
                on_click=lambda: CartState.update_item_quantity(
                    item.product_id, 1
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "px-2 py-1 bg-sky-100 hover:bg-sky-200 rounded-r text-sm text-sky-700 focus:outline-none focus:ring-1 focus:ring-sky-400",
                    "px-2 py-1 bg-gray-700 hover:bg-gray-600 rounded-r text-sm text-white focus:outline-none focus:ring-1 focus:ring-sky-500",
                ),
            ),
            class_name="flex items-center mx-2",
        ),
        rx.el.p(
            f"${item.price * item.quantity:.2f}",
            class_name="font-semibold text-green-600 dark:text-green-400 w-20 text-right",
        ),
        rx.el.button(
            "X",
            on_click=lambda: CartState.remove_item(
                item.product_id
            ),
            class_name="ml-4 text-red-600 dark:text-red-500 hover:text-red-500 dark:hover:text-red-400 font-bold focus:outline-none",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "flex items-center justify-between p-3 border-b border-sky-200 hover:bg-sky-50/50 transition-colors",
            "flex items-center justify-between p-3 border-b border-gray-700 hover:bg-gray-700/30 transition-colors",
        ),
    )