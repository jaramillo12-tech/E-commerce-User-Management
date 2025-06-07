import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.admin_stats_state import AdminStatsState
from app.states.theme_state import ThemeState


def admin_statistics_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "Estadísticas de Productos",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-sky-800 mb-10 text-center title-bounce",
                    "text-3xl sm:text-4xl font-bold text-white mb-10 text-center title-bounce",
                ),
            ),
            rx.cond(
                AdminStatsState.product_purchase_summary.length()
                > 0,
                rx.el.div(
                    rx.el.h2(
                        "Productos Más Comprados",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-2xl font-semibold text-sky-700 mb-6 text-center",
                            "text-2xl font-semibold text-sky-300 mb-6 text-center",
                        ),
                    ),
                    rx.el.div(
                        rx.recharts.bar_chart(
                            rx.recharts.cartesian_grid(
                                stroke_dasharray="3 3",
                                stroke=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "#e0f2fe",
                                    "#374151",
                                ),
                            ),
                            rx.recharts.graphing_tooltip(
                                wrapper_style={
                                    "zIndex": 1000
                                },
                                content_style=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    {
                                        "backgroundColor": "white",
                                        "border": "1px solid #e0f2fe",
                                        "borderRadius": "0.375rem",
                                        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                                        "color": "#374151",
                                    },
                                    {
                                        "backgroundColor": "#1f2937",
                                        "border": "1px solid #4b5563",
                                        "borderRadius": "0.375rem",
                                        "boxShadow": "0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06)",
                                        "color": "#e5e7eb",
                                    },
                                ),
                                cursor={
                                    "fill": rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "rgba(14, 165, 233, 0.1)",
                                        "rgba(56, 189, 248, 0.1)",
                                    )
                                },
                            ),
                            rx.recharts.x_axis(
                                data_key="name",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-xs fill-sky-700",
                                    "text-xs fill-gray-300",
                                ),
                                interval=0,
                                angle=-30,
                                text_anchor="end",
                                height=70,
                            ),
                            rx.recharts.y_axis(
                                allow_decimals=False,
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-xs fill-sky-700",
                                    "text-xs fill-gray-300",
                                ),
                            ),
                            rx.recharts.legend(
                                wrapper_style={
                                    "paddingTop": "10px"
                                }
                            ),
                            rx.recharts.bar(
                                data_key="Vendidos",
                                fill=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "#0ea5e9",
                                    "#38bdf8",
                                ),
                                radius=[6, 6, 0, 0],
                                active_bar={
                                    "fill": rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "#0284c7",
                                        "#0ea5e9",
                                    )
                                },
                            ),
                            data=AdminStatsState.chart_data,
                            height=450,
                            margin={
                                "top": 20,
                                "right": 30,
                                "left": 0,
                                "bottom": 30,
                            },
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "p-4 sm:p-6 bg-white rounded-xl shadow-xl shadow-sky-200/50",
                            "p-4 sm:p-6 bg-gray-800 rounded-xl shadow-xl",
                        ),
                    ),
                    rx.el.h3(
                        "Resumen Detallado",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-xl font-semibold text-sky-700 mt-10 mb-4 text-center",
                            "text-xl font-semibold text-sky-300 mt-10 mb-4 text-center",
                        ),
                    ),
                    rx.el.div(
                        rx.el.table(
                            rx.el.thead(
                                rx.el.tr(
                                    rx.el.th(
                                        "Producto",
                                        class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                    ),
                                    rx.el.th(
                                        "Total Vendido",
                                        class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                    ),
                                    rx.el.th(
                                        "Ingresos Totales (COP)",
                                        class_name="py-3 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left text-sm font-semibold",
                                    ),
                                )
                            ),
                            rx.el.tbody(
                                rx.foreach(
                                    AdminStatsState.product_purchase_summary,
                                    lambda item: rx.el.tr(
                                        rx.el.td(
                                            item["name"],
                                            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
                                        ),
                                        rx.el.td(
                                            item[
                                                "total_sold"
                                            ],
                                            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm",
                                        ),
                                        rx.el.td(
                                            f"{item['total_revenue']:,.0f}",
                                            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700 text-sm font-medium",
                                        ),
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "hover:bg-sky-50/50",
                                            "hover:bg-gray-700/50",
                                        ),
                                    ),
                                )
                            ),
                            class_name="min-w-full",
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "overflow-x-auto shadow-lg rounded-lg mt-4 bg-white p-4",
                            "overflow-x-auto shadow-lg rounded-lg mt-4 bg-gray-800 p-4",
                        ),
                    ),
                    class_name="w-full max-w-4xl mx-auto",
                ),
                rx.el.p(
                    "No hay datos de ventas para mostrar estadísticas.",
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
        on_mount=AuthState.check_admin_session,
        class_name=ThemeState.current_theme,
    )