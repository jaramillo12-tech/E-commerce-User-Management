import reflex as rx
from app.states.cart_state import CartState
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def navbar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.a(
                "TechStore",
                href="/",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-2xl font-bold text-sky-700 hover:text-sky-600 transition-colors",
                    "text-2xl font-bold text-sky-400 hover:text-sky-300 transition-colors",
                ),
            ),
            rx.el.div(
                rx.el.a(
                    "Productos",
                    href="/products",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                        "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                    ),
                ),
                rx.el.a(
                    "Contacto",
                    href="/contact",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                        "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                    ),
                ),
                rx.cond(
                    AuthState.is_admin_user,
                    rx.el.a(
                        "Admin",
                        href="/admin",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "px-3 py-2 text-red-600 font-semibold hover:text-red-800 hover:bg-red-100 rounded-md transition-colors",
                            "px-3 py-2 text-red-400 font-semibold hover:text-red-200 transition-colors",
                        ),
                    ),
                    rx.el.div(),
                ),
                rx.cond(
                    AuthState.is_logged_in,
                    rx.fragment(
                        rx.el.a(
                            "Mi Perfil",
                            href="/profile",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                                "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                            ),
                        ),
                        rx.el.button(
                            "Cerrar Sesión",
                            on_click=AuthState.logout,
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                                "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                            ),
                        ),
                    ),
                    rx.fragment(
                        rx.el.a(
                            "Iniciar Sesión",
                            href="/sign_in",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                                "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                            ),
                        ),
                        rx.el.a(
                            "Registrarse",
                            href="/sign_up",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "px-3 py-2 text-sky-700 hover:text-sky-900 hover:bg-sky-100 rounded-md transition-colors",
                                "px-3 py-2 text-gray-300 hover:text-white transition-colors",
                            ),
                        ),
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        ThemeState.current_theme == "light",
                        rx.icon(
                            tag="moon",
                            class_name="h-5 w-5 text-sky-700",
                        ),
                        rx.icon(
                            tag="sun",
                            class_name="h-5 w-5 text-yellow-400",
                        ),
                    ),
                    on_click=ThemeState.toggle_theme,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "ml-0 sm:ml-4 p-2 rounded-full text-sky-700 hover:bg-sky-100 transition-colors",
                        "ml-0 sm:ml-4 p-2 rounded-full text-white hover:bg-gray-700 transition-colors",
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        ThemeState.is_lite_mode,
                        rx.icon(
                            tag="zap_off",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "h-5 w-5 text-sky-700",
                                "h-5 w-5 text-yellow-400",
                            ),
                        ),
                        rx.icon(
                            tag="zap",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "h-5 w-5 text-sky-700",
                                "h-5 w-5 text-yellow-400",
                            ),
                        ),
                    ),
                    on_click=ThemeState.toggle_lite_mode,
                    title=rx.cond(
                        ThemeState.is_lite_mode,
                        "Desactivar Modo Lite",
                        "Activar Modo Lite",
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "ml-0 sm:ml-2 p-2 rounded-full text-sky-700 hover:bg-sky-100 transition-colors",
                        "ml-0 sm:ml-2 p-2 rounded-full text-white hover:bg-gray-700 transition-colors",
                    ),
                ),
                rx.el.button(
                    rx.el.div(
                        rx.icon(
                            tag="shopping_cart",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "h-6 w-6 text-sky-700",
                                "h-6 w-6 text-white",
                            ),
                        ),
                        rx.el.span(
                            CartState.total_items.to_string(),
                            class_name="absolute -top-2 -right-2 bg-red-500 text-white text-xs rounded-full h-5 w-5 flex items-center justify-center",
                        ),
                        class_name="relative",
                    ),
                    on_click=CartState.toggle_cart,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "ml-0 sm:ml-2 p-2 rounded-full text-sky-700 hover:bg-sky-100 transition-colors",
                        "ml-0 sm:ml-2 p-2 rounded-full text-white hover:bg-gray-700 transition-colors",
                    ),
                ),
                class_name="flex flex-col items-center mt-4 space-y-2 sm:flex-row sm:space-y-0 sm:space-x-1 md:space-x-2 sm:mt-0",
            ),
            class_name="container mx-auto flex flex-col sm:flex-row items-center justify-between py-4 px-6",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "bg-white text-sky-800 shadow-lg shadow-sky-200/50 sticky top-0 z-50",
            "bg-gray-900 text-white shadow-lg sticky top-0 z-50",
        ),
    )