import reflex as rx
from app.components.navbar import navbar
from app.states.cart_state import CartState
from app.states.checkout_state import CheckoutState
from app.states.theme_state import ThemeState
from app.models.models import CartItem


def checkout_item_summary_row(
    item: CartItem,
) -> rx.Component:
    return rx.el.div(
        rx.el.img(
            src=item.image_url,
            alt=item.name,
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "w-10 h-10 sm:w-12 sm:h-12 object-cover rounded mr-3 border border-sky-200",
                "w-10 h-10 sm:w-12 sm:h-12 object-cover rounded mr-3 border border-gray-600",
            ),
        ),
        rx.el.div(
            rx.el.p(
                item.name,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "font-medium text-sky-700 text-xs sm:text-sm",
                    "font-medium text-sky-300 text-xs sm:text-sm",
                ),
            ),
            rx.el.p(
                f"Cant: {item.quantity}",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-xs text-sky-600",
                    "text-xs text-gray-400",
                ),
            ),
            class_name="flex-grow",
        ),
        rx.el.p(
            f"COP {item.price * item.quantity:,.0f}",
            class_name="font-semibold text-green-600 dark:text-green-400 text-xs sm:text-sm",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "flex items-center justify-between py-2 px-2 sm:px-3 bg-sky-50 rounded-md mb-2",
            "flex items-center justify-between py-2 px-2 sm:px-3 bg-gray-700/50 rounded-md mb-2",
        ),
    )


def checkout_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Finalizar Compra",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-8 sm:mb-10 text-center title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-8 sm:mb-10 text-center title-bounce",
                ),
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Resumen del Pedido",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-xl sm:text-2xl font-semibold text-sky-700 mb-4",
                            "text-xl sm:text-2xl font-semibold text-sky-400 mb-4",
                        ),
                    ),
                    rx.cond(
                        CartState.items.length() > 0,
                        rx.el.div(
                            rx.foreach(
                                CartState.items,
                                checkout_item_summary_row,
                            ),
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "mb-6 max-h-60 overflow-y-auto p-1 rounded-lg border border-sky-200 custom-scrollbar",
                                "mb-6 max-h-60 overflow-y-auto p-1 rounded-lg border border-gray-700 custom-scrollbar",
                            ),
                        ),
                        rx.el.p(
                            "Tu carrito está vacío. Por favor, añade artículos para continuar.",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-600 text-center py-4 text-sm sm:text-base",
                                "text-gray-500 text-center py-4 text-sm sm:text-base",
                            ),
                        ),
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.p(
                                "Artículos Totales:",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-sky-700 text-xs sm:text-sm",
                                    "text-gray-300 text-xs sm:text-sm",
                                ),
                            ),
                            rx.el.p(
                                CartState.total_items.to_string(),
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "font-semibold text-sky-800 text-xs sm:text-sm",
                                    "font-semibold text-sky-300 text-xs sm:text-sm",
                                ),
                            ),
                            class_name="flex justify-between text-sm mb-1",
                        ),
                        rx.el.div(
                            rx.el.p(
                                "Precio Total:",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-sky-700 text-base sm:text-lg",
                                    "text-gray-300 text-base sm:text-lg",
                                ),
                            ),
                            rx.el.p(
                                f"COP {CartState.total_price:,.0f}",
                                class_name="font-bold text-lg sm:text-xl text-green-600 dark:text-green-400",
                            ),
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "flex justify-between items-center mb-4 pt-2 border-t border-sky-200",
                                "flex justify-between items-center mb-4 pt-2 border-t border-gray-700",
                            ),
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "bg-sky-50 p-3 sm:p-4 rounded-lg",
                            "bg-gray-800 p-3 sm:p-4 rounded-lg",
                        ),
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full lg:w-1/3 bg-white p-4 sm:p-6 rounded-xl shadow-xl shadow-sky-200/50 mb-8 lg:mb-0",
                        "w-full lg:w-1/3 bg-gray-800 p-4 sm:p-6 rounded-xl shadow-xl mb-8 lg:mb-0",
                    ),
                ),
                rx.el.div(
                    rx.el.h2(
                        "Envío y Pago",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-xl sm:text-2xl font-semibold text-sky-700 mb-6",
                            "text-xl sm:text-2xl font-semibold text-sky-400 mb-6",
                        ),
                    ),
                    rx.el.form(
                        rx.el.div(
                            rx.el.label(
                                "Nombre Completo",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "block text-sm font-medium text-sky-700 mb-1",
                                    "block text-sm font-medium text-gray-300 mb-1",
                                ),
                            ),
                            rx.el.input(
                                name="full_name",
                                default_value=CheckoutState.full_name,
                                placeholder="Ingresa tu nombre completo",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                    "w-full p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                ),
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Dirección de Envío",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "block text-sm font-medium text-sky-700 mb-1",
                                    "block text-sm font-medium text-gray-300 mb-1",
                                ),
                            ),
                            rx.el.input(
                                name="address",
                                default_value=CheckoutState.address,
                                placeholder="Ingresa tu dirección de envío",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                    "w-full p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                ),
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Correo Electrónico",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "block text-sm font-medium text-sky-700 mb-1",
                                    "block text-sm font-medium text-gray-300 mb-1",
                                ),
                            ),
                            rx.el.input(
                                name="email",
                                type="email",
                                default_value=CheckoutState.email,
                                placeholder="Ingresa tu correo electrónico",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                    "w-full p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                ),
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Documento de Identidad (NIT/CC)",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "block text-sm font-medium text-sky-700 mb-1",
                                    "block text-sm font-medium text-gray-300 mb-1",
                                ),
                            ),
                            rx.el.input(
                                name="document_id",
                                default_value=CheckoutState.document_id,
                                placeholder="Ej: 1234567890 o 900123456-7",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                    "w-full p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                ),
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Información de Tarjeta",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "block text-sm font-medium text-sky-700 mb-1",
                                    "block text-sm font-medium text-gray-300 mb-1",
                                ),
                            ),
                            rx.el.input(
                                name="card_number",
                                default_value=CheckoutState.card_number,
                                placeholder="Número de Tarjeta (ej., **** **** **** ****)",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400 mb-2",
                                    "w-full p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400 mb-2",
                                ),
                            ),
                            rx.el.div(
                                rx.el.input(
                                    name="card_expiry",
                                    default_value=CheckoutState.card_expiry,
                                    placeholder="MM/AA",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-1/2 p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                        "w-1/2 p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                    ),
                                ),
                                rx.el.input(
                                    name="card_cvc",
                                    default_value=CheckoutState.card_cvc,
                                    placeholder="CVC",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-1/2 p-2 sm:p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                        "w-1/2 p-2 sm:p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                    ),
                                ),
                                class_name="flex space-x-2",
                            ),
                            class_name="mb-6",
                        ),
                        rx.cond(
                            CheckoutState.error_message
                            != "",
                            rx.el.p(
                                CheckoutState.error_message,
                                class_name="text-red-500 dark:text-red-400 text-sm mb-4 text-center",
                            ),
                            rx.el.div(),
                        ),
                        rx.el.button(
                            "Realizar Pedido",
                            type="submit",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 sm:py-3 px-4 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-green-400 button-light-interactive",
                                "w-full bg-green-500 hover:bg-green-600 text-white font-bold py-2 sm:py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-green-400",
                            ),
                            disabled=(
                                CartState.items.length()
                                == 0
                            )
                            | CheckoutState.is_processing,
                        ),
                        on_submit=CheckoutState.process_payment,
                        reset_on_submit=False,
                        class_name="w-full",
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full lg:w-2/3 bg-white p-4 sm:p-6 rounded-xl shadow-xl shadow-sky-200/50 lg:ml-8",
                        "w-full lg:w-2/3 bg-gray-800 p-4 sm:p-6 rounded-xl shadow-xl lg:ml-8",
                    ),
                ),
                class_name="container mx-auto flex flex-col lg:flex-row items-start justify-center gap-8 px-4",
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "min-h-screen text-sky-800 py-10 px-0 sm:px-4 pt-24 bg-white",
                "min-h-screen text-white py-10 px-0 sm:px-4 pt-24 bg-slate-900",
            ),
        ),
        class_name=ThemeState.current_theme,
    )