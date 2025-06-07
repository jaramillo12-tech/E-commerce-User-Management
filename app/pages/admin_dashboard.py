import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState


def admin_dashboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Panel de Administración",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-8 title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-8 title-bounce",
                ),
            ),
            rx.el.div(
                rx.el.a(
                    "Gestionar Productos",
                    href="/admin/manage-products",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block w-full max-w-xs text-center bg-sky-500 hover:bg-sky-600 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-all transform hover:scale-105 button-light-interactive mb-4",
                        "block w-full max-w-xs text-center bg-sky-600 hover:bg-sky-700 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-colors transform hover:scale-105 mb-4",
                    ),
                ),
                rx.el.a(
                    "Ver Estadísticas de Productos",
                    href="/admin/statistics",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block w-full max-w-xs text-center bg-green-500 hover:bg-green-600 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-all transform hover:scale-105 button-light-interactive mb-4",
                        "block w-full max-w-xs text-center bg-green-600 hover:bg-green-700 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-colors transform hover:scale-105 mb-4",
                    ),
                ),
                rx.el.a(
                    "Historial de Compras",
                    href="/admin/purchase-history",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block w-full max-w-xs text-center bg-purple-500 hover:bg-purple-600 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-all transform hover:scale-105 button-light-interactive mb-4",
                        "block w-full max-w-xs text-center bg-purple-600 hover:bg-purple-700 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-colors transform hover:scale-105",
                    ),
                ),
                rx.el.a(
                    "Buzón de Quejas",
                    href="/admin/mailbox",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block w-full max-w-xs text-center bg-orange-500 hover:bg-orange-600 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-all transform hover:scale-105 button-light-interactive",
                        "block w-full max-w-xs text-center bg-orange-600 hover:bg-orange-700 text-white font-semibold py-3 px-6 rounded-lg text-lg transition-colors transform hover:scale-105",
                    ),
                ),
                class_name="flex flex-col items-center space-y-4",
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "container mx-auto flex flex-col items-center justify-center min-h-screen pt-24 px-4 bg-white",
                "container mx-auto flex flex-col items-center justify-center min-h-screen pt-24 px-4 bg-slate-900",
            ),
        ),
        on_mount=AuthState.check_admin_session,
        class_name=ThemeState.current_theme,
    )