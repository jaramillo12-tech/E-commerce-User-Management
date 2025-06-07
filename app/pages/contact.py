import reflex as rx
from app.components.navbar import navbar
from app.states.contact_state import ContactState
from app.states.theme_state import ThemeState


def contact_form() -> rx.Component:
    return rx.el.form(
        rx.el.div(
            rx.el.label(
                "Tu Nombre:",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "block text-sm font-medium text-sky-700 mb-1",
                    "block text-sm font-medium text-gray-300 mb-1",
                ),
            ),
            rx.el.input(
                name="name",
                default_value=ContactState.name,
                placeholder="Ingresa tu nombre",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full p-2 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                    "w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Tu Correo Electrónico:",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "block text-sm font-medium text-sky-700 mb-1",
                    "block text-sm font-medium text-gray-300 mb-1",
                ),
            ),
            rx.el.input(
                type="email",
                name="email",
                default_value=ContactState.email,
                placeholder="Ingresa tu correo electrónico",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full p-2 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                    "w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Asunto:",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "block text-sm font-medium text-sky-700 mb-1",
                    "block text-sm font-medium text-gray-300 mb-1",
                ),
            ),
            rx.el.input(
                name="subject",
                default_value=ContactState.subject,
                placeholder="Asunto de tu mensaje",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full p-2 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                    "w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                ),
            ),
            class_name="mb-4",
        ),
        rx.el.div(
            rx.el.label(
                "Mensaje (Quejas/Comentarios):",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "block text-sm font-medium text-sky-700 mb-1",
                    "block text-sm font-medium text-gray-300 mb-1",
                ),
            ),
            rx.el.textarea(
                name="message",
                default_value=ContactState.message,
                on_change=ContactState.set_message,
                placeholder="Tu mensaje o queja...",
                rows=5,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full p-2 bg-sky-50 border border-sky-300 rounded-md text-sky-800 focus:ring-sky-400 focus:border-sky-400 placeholder-sky-400",
                    "w-full p-2 bg-gray-700 border border-gray-600 rounded-md text-white focus:ring-sky-500 focus:border-sky-500 placeholder-gray-400",
                ),
            ),
            class_name="mb-6",
        ),
        rx.el.button(
            "Enviar Mensaje",
            type="submit",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "w-full bg-sky-500 hover:bg-sky-600 text-white font-semibold py-2 px-4 rounded-lg transition-all button-light-interactive",
                "w-full bg-sky-600 hover:bg-sky-700 text-white font-semibold py-2 px-4 rounded-lg transition-colors",
            ),
        ),
        on_submit=ContactState.handle_submit,
        reset_on_submit=True,
        class_name="w-full max-w-lg",
    )


def contact_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Contáctanos",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-6 sm:mb-8 title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-6 sm:mb-8 title-bounce",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Información del Desarrollador",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-xl sm:text-2xl font-semibold text-sky-700 mb-3",
                        "text-xl sm:text-2xl font-semibold text-sky-400 mb-3",
                    ),
                ),
                rx.el.p(
                    "Nombre: Jhonier Pulgarin Jaramillo",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-sky-700 mb-1 text-sm sm:text-base",
                        "text-gray-300 mb-1 text-sm sm:text-base",
                    ),
                ),
                rx.el.p(
                    "Rol: Desarrollador Principal - TechStore",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-sky-700 mb-6 text-sm sm:text-base",
                        "text-gray-300 mb-6 text-sm sm:text-base",
                    ),
                ),
                rx.el.h2(
                    "Enviar una Queja o Comentario",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-xl sm:text-2xl font-semibold text-sky-700 mb-4",
                        "text-xl sm:text-2xl font-semibold text-sky-400 mb-4",
                    ),
                ),
                contact_form(),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "bg-white p-6 sm:p-8 rounded-lg shadow-xl shadow-sky-200/50 w-full max-w-2xl",
                    "bg-gray-800 p-6 sm:p-8 rounded-lg shadow-xl w-full max-w-2xl",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "container mx-auto flex flex-col items-center py-10 px-4 min-h-screen pt-24 bg-white",
                "container mx-auto flex flex-col items-center py-10 px-4 min-h-screen pt-24 bg-slate-900",
            ),
        ),
        class_name=ThemeState.current_theme,
    )