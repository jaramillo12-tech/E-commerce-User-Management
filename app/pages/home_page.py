import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def home_page_content() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AuthState.is_logged_in,
            rx.el.div(
                rx.el.h1(
                    f"Bienvenido de nuevo, {AuthState.username}!",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-3xl md:text-4xl lg:text-5xl font-bold text-sky-700 mb-6 text-center animate-float-fade-in",
                        "text-3xl md:text-4xl lg:text-5xl font-bold text-sky-300 mb-6 text-center animate-float-fade-in",
                    ),
                ),
                rx.el.p(
                    "Has iniciado sesión en TechStore.",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-lg md:text-xl text-sky-600 mb-8 text-center animate-float-fade-in delay-1",
                        "text-lg md:text-xl text-gray-400 mb-8 text-center animate-float-fade-in delay-1",
                    ),
                ),
                rx.el.button(
                    "Cerrar Sesión",
                    on_click=AuthState.logout,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "bg-red-500 hover:bg-red-600 text-white font-semibold py-2 px-6 rounded-lg transition-all button-light-interactive animate-float-fade-in delay-2",
                        "bg-red-600 hover:bg-red-700 text-white font-semibold py-2 px-6 rounded-lg transition-colors animate-float-fade-in delay-2",
                    ),
                ),
                class_name="flex flex-col items-center justify-center py-20",
            ),
            rx.el.div(
                rx.el.h1(
                    "Bienvenido a TechStore",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-4xl sm:text-5xl md:text-6xl font-bold text-sky-700 mb-6 text-center animate-float-fade-in",
                        "text-4xl sm:text-5xl md:text-6xl font-bold text-sky-300 mb-6 text-center animate-float-fade-in",
                    ),
                ),
                rx.el.p(
                    "Tu destino para la última tecnología y gadgets. Explora nuestra amplia selección de productos de alta calidad.",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-md sm:text-lg md:text-xl text-sky-600 mb-10 text-center max-w-xl md:max-w-2xl mx-auto animate-float-fade-in delay-1",
                        "text-md sm:text-lg md:text-xl text-gray-400 mb-10 text-center max-w-xl md:max-w-2xl mx-auto animate-float-fade-in delay-1",
                    ),
                ),
                rx.el.div(
                    rx.el.a(
                        "Explorar Productos",
                        href="/products",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-6 md:px-8 rounded-lg text-base md:text-lg transition-all transform hover:scale-105 button-light-interactive animate-float-fade-in delay-2",
                            "bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-6 md:px-8 rounded-lg text-base md:text-lg transition-colors transform hover:scale-105 animate-float-fade-in delay-2",
                        ),
                    ),
                    rx.el.a(
                        "Iniciar Sesión",
                        href="/sign_in",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 md:px-8 rounded-lg text-base md:text-lg transition-all transform hover:scale-105 button-light-interactive animate-float-fade-in delay-3",
                            "bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 md:px-8 rounded-lg text-base md:text-lg transition-colors transform hover:scale-105 animate-float-fade-in delay-3",
                        ),
                    ),
                    class_name="flex flex-col sm:flex-row justify-center items-center space-y-4 sm:space-y-0 sm:space-x-4",
                ),
                class_name="py-16 md:py-24 text-center",
            ),
        ),
        class_name="container mx-auto px-4",
    )


def home_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.main(
            home_page_content(),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "min-h-screen text-sky-800 pt-16 sm:pt-20 bg-gradient-to-br from-sky-100 via-sky-50 to-white flex items-center justify-center",
                "min-h-screen text-white pt-16 sm:pt-20 bg-gradient-to-br from-slate-900 via-gray-800 to-gray-900 flex items-center justify-center",
            ),
        ),
        class_name=ThemeState.current_theme,
        on_mount=AuthState.check_login_status,
    )