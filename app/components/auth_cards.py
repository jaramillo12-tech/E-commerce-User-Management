import reflex as rx
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def sign_in_card() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Iniciar Sesión",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-2xl sm:text-3xl font-bold text-sky-700 mb-6 text-center title-bounce",
                "text-2xl sm:text-3xl font-bold text-sky-300 mb-6 text-center title-bounce",
            ),
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Usuario",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="username",
                    default_value=AuthState.username,
                    placeholder="Ingresa tu usuario",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    type="password",
                    name="password",
                    default_value=AuthState.password,
                    placeholder="Ingresa tu contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-2",
            ),
            rx.el.div(
                rx.el.a(
                    "¿Olvidaste tu contraseña?",
                    href="/forgot-password",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-xs text-sky-600 hover:text-sky-700 hover:underline",
                        "text-xs text-sky-400 hover:underline",
                    ),
                ),
                class_name="text-right mb-4",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.p(
                    AuthState.error_message,
                    class_name="text-red-500 dark:text-red-400 text-sm mb-4 text-center",
                ),
                rx.el.div(),
            ),
            rx.el.button(
                "Iniciar Sesión",
                type="submit",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                    "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                ),
            ),
            on_submit=AuthState.login,
            class_name="w-full max-w-sm",
            reset_on_submit=False,
        ),
        rx.el.p(
            "¿No tienes una cuenta? ",
            rx.el.a(
                "Regístrate",
                href="/sign_up",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-sky-600 hover:text-sky-700 hover:underline",
                    "text-sky-400 hover:underline",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-center mt-6 text-sky-700 text-sm sm:text-base",
                "text-center mt-6 text-gray-400 text-sm sm:text-base",
            ),
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "bg-white p-6 sm:p-8 rounded-xl shadow-xl shadow-sky-200/50 w-full max-w-md",
            "bg-gray-800 p-6 sm:p-8 rounded-xl shadow-2xl w-full max-w-md",
        ),
    )


def sign_up_card() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Regístrate",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-2xl sm:text-3xl font-bold text-sky-700 mb-6 text-center title-bounce",
                "text-2xl sm:text-3xl font-bold text-sky-300 mb-6 text-center title-bounce",
            ),
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Usuario",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="username",
                    default_value=AuthState.username,
                    placeholder="Elige un nombre de usuario",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Correo Electrónico",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    type="email",
                    name="email",
                    default_value=AuthState.email,
                    placeholder="Ingresa tu correo electrónico",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    type="password",
                    name="password",
                    default_value=AuthState.password,
                    placeholder="Crea una contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.error_message != "",
                rx.el.p(
                    AuthState.error_message,
                    class_name="text-red-500 dark:text-red-400 text-sm mb-4 text-center",
                ),
                rx.el.div(),
            ),
            rx.el.button(
                "Regístrate",
                type="submit",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                    "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                ),
            ),
            on_submit=AuthState.signup,
            class_name="w-full max-w-sm",
            reset_on_submit=False,
        ),
        rx.el.p(
            "¿Ya tienes una cuenta? ",
            rx.el.a(
                "Iniciar Sesión",
                href="/sign_in",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-sky-600 hover:text-sky-700 hover:underline",
                    "text-sky-400 hover:underline",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-center mt-6 text-sky-700 text-sm sm:text-base",
                "text-center mt-6 text-gray-400 text-sm sm:text-base",
            ),
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "bg-white p-6 sm:p-8 rounded-xl shadow-xl shadow-sky-200/50 w-full max-w-md",
            "bg-gray-800 p-6 sm:p-8 rounded-xl shadow-2xl w-full max-w-md",
        ),
    )