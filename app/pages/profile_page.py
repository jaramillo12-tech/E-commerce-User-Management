import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def change_user_details_form() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Cambiar Nombre de Usuario o Contraseña",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-xl sm:text-2xl font-bold text-sky-700 mb-6 text-center",
                "text-xl sm:text-2xl font-bold text-sky-300 mb-6 text-center",
            ),
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    "Contraseña Actual:",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="change_current_password",
                    type="password",
                    default_value=AuthState.change_current_password,
                    placeholder="Ingresa tu contraseña actual",
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
                    "Nuevo Nombre de Usuario (opcional):",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="change_new_username",
                    default_value=AuthState.change_new_username,
                    placeholder="Ingresa nuevo nombre de usuario",
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
                    "Nueva Contraseña (opcional):",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="change_new_password",
                    type="password",
                    default_value=AuthState.change_new_password,
                    placeholder="Ingresa nueva contraseña",
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
                    "Confirmar Nueva Contraseña:",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.el.input(
                    name="change_confirm_new_password",
                    type="password",
                    default_value=AuthState.change_confirm_new_password,
                    placeholder="Confirma nueva contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                        "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                    ),
                ),
                class_name="mb-6",
            ),
            rx.cond(
                AuthState.change_user_details_message != "",
                rx.el.p(
                    AuthState.change_user_details_message,
                    class_name=rx.cond(
                        AuthState.change_user_details_message.contains(
                            "exitosamente"
                        ),
                        "text-green-500 dark:text-green-400 text-sm mb-4 text-center",
                        "text-red-500 dark:text-red-400 text-sm mb-4 text-center",
                    ),
                ),
                rx.el.div(),
            ),
            rx.el.button(
                "Guardar Cambios",
                type="submit",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                    "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                ),
            ),
            on_submit=AuthState.handle_change_user_details,
            reset_on_submit=False,
            class_name="w-full max-w-md",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "bg-white p-6 sm:p-8 rounded-xl shadow-xl shadow-sky-200/50",
            "bg-gray-800 p-6 sm:p-8 rounded-xl shadow-2xl",
        ),
    )


def profile_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Mi Perfil",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-8 text-center title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-8 text-center title-bounce",
                ),
            ),
            rx.el.p(
                f"Nombre de Usuario: {AuthState.username}",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-lg text-sky-700 mb-2",
                    "text-lg text-gray-300 mb-2",
                ),
            ),
            rx.el.p(
                f"Correo Electrónico: {AuthState.email}",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-lg text-sky-700 mb-6",
                    "text-lg text-gray-300 mb-6",
                ),
            ),
            change_user_details_form(),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "flex flex-col items-center justify-start min-h-screen pt-24 px-4 bg-white",
                "flex flex-col items-center justify-start min-h-screen pt-24 px-4 bg-slate-900",
            ),
        ),
        on_mount=[
            AuthState.check_general_login_session,
            AuthState.check_login_status,
        ],
        class_name=ThemeState.current_theme,
    )