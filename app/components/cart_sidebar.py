import reflex as rx
from app.states.cart_state import CartState
from app.components.cart_item_row import cart_item_row
from app.states.theme_state import ThemeState


def cart_sidebar() -> rx.Component:
    return rx.cond(
        CartState.is_cart_open,
        rx.el.div(
            rx.el.div(
                rx.el.h3(
                    "Tu Carrito",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-xl sm:text-2xl font-semibold text-sky-700",
                        "text-xl sm:text-2xl font-semibold text-sky-300",
                    ),
                ),
                rx.el.button(
                    "Cerrar",
                    on_click=CartState.toggle_cart,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-sky-600 hover:text-sky-800 p-1 rounded-md hover:bg-sky-100 transition-colors",
                        "text-gray-400 hover:text-white p-1 rounded-md hover:bg-gray-700 transition-colors",
                    ),
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "flex justify-between items-center p-4 border-b border-sky-200 sticky top-0 bg-white z-10",
                    "flex justify-between items-center p-4 border-b border-gray-700 sticky top-0 bg-gray-800 z-10",
                ),
            ),
            rx.el.div(
                rx.cond(
                    CartState.items.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            CartState.items, cart_item_row
                        )
                    ),
                    rx.el.p(
                        "Tu carrito está vacío. ¡Añade algo de tecnología genial!",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "p-6 text-center text-sky-600 text-sm sm:text-base",
                            "p-6 text-center text-gray-500 text-sm sm:text-base",
                        ),
                    ),
                ),
                class_name="overflow-y-auto flex-grow p-2 custom-scrollbar",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.p(
                        "Artículos Totales:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700 text-sm sm:text-base",
                            "text-gray-400 text-sm sm:text-base",
                        ),
                    ),
                    rx.el.p(
                        CartState.total_items.to_string(),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "font-semibold text-sky-800 text-sm sm:text-base",
                            "font-semibold text-sky-300 text-sm sm:text-base",
                        ),
                    ),
                    class_name="flex justify-between mb-1",
                ),
                rx.el.div(
                    rx.el.p(
                        "Precio Total:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700 text-base sm:text-lg",
                            "text-gray-400 text-base sm:text-lg",
                        ),
                    ),
                    rx.el.p(
                        f"$ {CartState.total_price:.2f}",
                        class_name="font-bold text-xl sm:text-2xl text-green-600 dark:text-green-400",
                    ),
                    class_name="flex justify-between items-center mb-4",
                ),
                rx.el.button(
                    "Finalizar Compra",
                    on_click=[
                        CartState.toggle_cart,
                        lambda: rx.redirect("/checkout"),
                    ],
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 sm:py-3 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-green-400 text-sm sm:text-base button-light-interactive",
                        "w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 sm:py-3 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-green-400 text-sm sm:text-base",
                    ),
                    disabled=CartState.items.length() == 0,
                ),
                rx.el.button(
                    "Vaciar Carrito",
                    on_click=CartState.clear_cart,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full mt-2 bg-red-500 hover:bg-red-600 text-white font-semibold py-2 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-red-400 text-sm sm:text-base button-light-interactive",
                        "w-full mt-2 bg-red-600 hover:bg-red-700 text-white font-semibold py-2 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-red-500 text-sm sm:text-base",
                    ),
                    disabled=CartState.items.length() == 0,
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "p-4 border-t border-sky-200 sticky bottom-0 bg-white z-10",
                    "p-4 border-t border-gray-700 sticky bottom-0 bg-gray-800 z-10",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "fixed top-0 right-0 h-full w-full sm:w-96 md:w-[450px] bg-white text-sky-800 shadow-2xl shadow-sky-300/70 flex flex-col transform transition-transform duration-300 ease-in-out z-[90]",
                "fixed top-0 right-0 h-full w-full sm:w-96 md:w-[450px] bg-gray-800 text-white shadow-2xl flex flex-col transform transition-transform duration-300 ease-in-out z-[90]",
            ),
            style={
                "transform": rx.cond(
                    CartState.is_cart_open,
                    "translateX(0%)",
                    "translateX(100%)",
                )
            },
        ),
        rx.el.div(),
    )