import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def request_step_component() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.label(
                "Método de Recuperación:",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "block text-sm font-medium text-sky-700 mb-1",
                    "block text-sm font-medium text-gray-300 mb-1",
                ),
            ),
            rx.el.div(
                rx.el.label(
                    rx.el.input(
                        type="radio",
                        name="recovery_method_selector_radio",
                        checked=AuthState.recovery_method
                        == "email",
                        on_change=lambda: AuthState.set_recovery_method(
                            "email"
                        ),
                        class_name="mr-2",
                    ),
                    "Correo Electrónico",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-sky-700 cursor-pointer",
                        "text-gray-300 cursor-pointer",
                    ),
                ),
                rx.el.label(
                    rx.el.input(
                        type="radio",
                        name="recovery_method_selector_radio",
                        checked=AuthState.recovery_method
                        == "phone",
                        on_change=lambda: AuthState.set_recovery_method(
                            "phone"
                        ),
                        class_name="mr-2 ml-4",
                    ),
                    "Número de Celular (SMS)",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-sky-700 cursor-pointer",
                        "text-gray-300 cursor-pointer",
                    ),
                ),
                class_name="flex items-center",
            ),
            class_name="mb-4",
        ),
        rx.el.form(
            rx.el.div(
                rx.el.label(
                    rx.cond(
                        AuthState.recovery_method
                        == "email",
                        "Correo Electrónico:",
                        "Número de Celular:",
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block text-sm font-medium text-sky-700 mb-1",
                        "block text-sm font-medium text-gray-300 mb-1",
                    ),
                ),
                rx.cond(
                    AuthState.recovery_method == "email",
                    rx.el.input(
                        name="recovery_input_field",
                        type="email",
                        default_value=AuthState.recovery_target,
                        placeholder="tu@email.com",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                            "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                        ),
                    ),
                    rx.el.input(
                        name="recovery_input_field",
                        type="tel",
                        default_value=AuthState.recovery_target,
                        placeholder="+1234567890 (incluye código de país)",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                            "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                        ),
                    ),
                ),
                class_name="mb-4",
            ),
            rx.el.button(
                "Enviar Código de Verificación",
                type="submit",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                    "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                ),
            ),
            on_submit=AuthState.request_password_reset,
            reset_on_submit=False,
        ),
    )


def forgot_password_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h2(
                    "Recuperar Contraseña",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-2xl sm:text-3xl font-bold text-sky-700 mb-6 text-center title-bounce",
                        "text-2xl sm:text-3xl font-bold text-sky-300 mb-6 text-center title-bounce",
                    ),
                ),
                rx.el.div(
                    rx.match(
                        AuthState.recovery_step,
                        (
                            "request",
                            request_step_component(),
                        ),
                        (
                            "verify",
                            rx.el.form(
                                rx.el.p(
                                    f"Se ha enviado un código de verificación a {AuthState.recovery_target}.",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "text-sky-700 mb-4 text-center",
                                        "text-gray-300 mb-4 text-center",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Código de Verificación:",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "block text-sm font-medium text-sky-700 mb-1",
                                            "block text-sm font-medium text-gray-300 mb-1",
                                        ),
                                    ),
                                    rx.el.input(
                                        name="reset_code_input_field",
                                        default_value=AuthState.reset_code_input,
                                        placeholder="Ingresa el código",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                            "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                        ),
                                    ),
                                    class_name="mb-4",
                                ),
                                rx.el.button(
                                    "Verificar Código",
                                    type="submit",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                                        "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                                    ),
                                ),
                                rx.el.button(
                                    "Volver / Cambiar Método",
                                    on_click=AuthState.go_to_request_step,
                                    type="button",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full mt-2 bg-gray-200 hover:bg-gray-300 text-sky-700 font-semibold py-3 px-4 rounded-lg transition-all",
                                        "w-full mt-2 bg-gray-600 hover:bg-gray-500 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                                    ),
                                ),
                                on_submit=AuthState.verify_reset_code,
                                reset_on_submit=False,
                            ),
                        ),
                        (
                            "reset",
                            rx.el.form(
                                rx.el.p(
                                    "Código verificado. Ahora puedes restablecer tu contraseña.",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "text-green-600 mb-4 text-center",
                                        "text-green-400 mb-4 text-center",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.label(
                                        "Nueva Contraseña:",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "block text-sm font-medium text-sky-700 mb-1",
                                            "block text-sm font-medium text-gray-300 mb-1",
                                        ),
                                    ),
                                    rx.el.input(
                                        name="new_password_field",
                                        type="password",
                                        default_value=AuthState.new_password_recovery,
                                        placeholder="Ingresa tu nueva contraseña",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
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
                                            ThemeState.current_theme
                                            == "light",
                                            "block text-sm font-medium text-sky-700 mb-1",
                                            "block text-sm font-medium text-gray-300 mb-1",
                                        ),
                                    ),
                                    rx.el.input(
                                        name="confirm_new_password_field",
                                        type="password",
                                        default_value=AuthState.confirm_new_password_recovery,
                                        placeholder="Confirma tu nueva contraseña",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "w-full p-3 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                                            "w-full p-3 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                                        ),
                                    ),
                                    class_name="mb-6",
                                ),
                                rx.el.button(
                                    "Restablecer Contraseña",
                                    type="submit",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-4 rounded-lg transition-all button-light-interactive",
                                        "w-full bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                                    ),
                                ),
                                on_submit=AuthState.process_password_reset,
                                reset_on_submit=True,
                            ),
                        ),
                        rx.el.p(
                            "Estado desconocido de recuperación."
                        ),
                    ),
                    class_name="w-full max-w-sm",
                ),
                rx.cond(
                    AuthState.recovery_message != "",
                    rx.el.p(
                        AuthState.recovery_message,
                        class_name=rx.cond(
                            AuthState.recovery_message.contains(
                                "exitosamente"
                            )
                            | AuthState.recovery_message.contains(
                                "verificado"
                            ),
                            "text-green-500 dark:text-green-400 text-sm mt-4 text-center",
                            "text-red-500 dark:text-red-400 text-sm mt-4 text-center",
                        ),
                    ),
                    rx.el.div(),
                ),
                rx.el.div(
                    rx.el.a(
                        "Volver a Iniciar Sesión",
                        href="/sign_in",
                        on_click=AuthState.go_to_request_step,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600 hover:text-sky-700 hover:underline",
                            "text-sky-400 hover:underline",
                        ),
                    ),
                    class_name="text-center mt-6 text-sm",
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "bg-white p-6 sm:p-8 rounded-xl shadow-xl shadow-sky-200/50 w-full max-w-md",
                    "bg-gray-800 p-6 sm:p-8 rounded-xl shadow-2xl w-full max-w-md",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "flex flex-col items-center justify-center min-h-screen p-4 pt-20 bg-white",
                "flex flex-col items-center justify-center min-h-screen p-4 pt-20 bg-slate-900",
            ),
        ),
        on_mount=AuthState.go_to_request_step,
        class_name=ThemeState.current_theme,
    )