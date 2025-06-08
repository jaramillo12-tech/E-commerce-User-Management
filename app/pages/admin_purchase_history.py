import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.theme_state import ThemeState
from app.states.admin_purchase_history_state import (
    AdminPurchaseHistoryState,
)


def purchase_group_row(pg_formatted: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            pg_formatted["date"],
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
        ),
        rx.el.td(
            pg_formatted["customer"],
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
        ),
        rx.el.td(
            pg_formatted["email"],
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
        ),
        rx.el.td(
            pg_formatted["item_count"],
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm text-center",
        ),
        rx.el.td(
            pg_formatted["total"],
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm font-semibold text-right",
        ),
        rx.el.td(
            rx.cond(
                pg_formatted["invoice_available"],
                rx.el.button(
                    "Ver Factura",
                    on_click=lambda: AdminPurchaseHistoryState.view_invoice_pdf(
                        pg_formatted["invoice_url"]
                    ),
                    class_name="bg-sky-500 hover:bg-sky-600 text-white px-3 py-1 rounded text-xs",
                ),
                rx.el.span(
                    "No Disponible",
                    class_name="text-xs text-gray-500",
                ),
            ),
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-center",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "hover:bg-sky-50/50",
            "hover:bg-gray-700/50",
        ),
    )


def admin_purchase_history_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Historial de Compras de Clientes",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-10 text-center title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-10 text-center title-bounce",
                ),
            ),
            rx.cond(
                AdminPurchaseHistoryState.formatted_purchase_groups.length()
                > 0,
                rx.el.div(
                    rx.el.table(
                        rx.el.thead(
                            rx.el.tr(
                                rx.el.th(
                                    "Fecha",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Cliente",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Email",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Artículos",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-center text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Total Compra",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-right text-sm font-semibold",
                                ),
                                rx.el.th(
                                    "Factura",
                                    class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-center text-sm font-semibold",
                                ),
                            )
                        ),
                        rx.el.tbody(
                            rx.foreach(
                                AdminPurchaseHistoryState.formatted_purchase_groups,
                                purchase_group_row,
                            )
                        ),
                        class_name="min-w-full",
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "overflow-x-auto shadow-lg rounded-lg bg-white p-4",
                        "overflow-x-auto shadow-lg rounded-lg bg-gray-800 p-4",
                    ),
                ),
                rx.el.p(
                    "No hay historial de compras para mostrar.",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-center text-sky-600 text-lg py-10",
                        "text-center text-gray-500 text-lg py-10",
                    ),
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "container mx-auto py-10 px-4 min-h-screen pt-24 bg-white",
                "container mx-auto py-10 px-4 min-h-screen pt-24 bg-slate-900",
            ),
        ),
        on_mount=[
            AuthState.check_admin_session,
            AdminPurchaseHistoryState.load_purchase_history,
        ],
        class_name=ThemeState.current_theme,
    )