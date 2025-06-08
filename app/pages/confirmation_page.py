import reflex as rx
from app.components.navbar import navbar
from app.states.invoice_state import InvoiceState
from app.states.theme_state import ThemeState
from app.models.models import CartItem
from typing import Union


def confirmation_item_summary_row(
    item_dict: dict[str, Union[str, int, float]],
) -> rx.Component:
    name = item_dict["name"]
    quantity = item_dict["quantity"].to(int)
    price = item_dict["price"].to(float)
    item_total = price * quantity
    return rx.el.div(
        rx.el.div(
            rx.el.p(
                name,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "font-medium text-sky-700 text-sm",
                    "font-medium text-sky-300 text-sm",
                ),
            ),
            rx.el.p(
                f"Cantidad: {quantity} x COP {price:,.0f}",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-xs text-sky-600",
                    "text-xs text-gray-400",
                ),
            ),
            class_name="flex-grow",
        ),
        rx.el.p(
            f"COP {item_total:,.0f}",
            class_name="font-semibold text-green-600 dark:text-green-400 text-sm",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "flex items-center justify-between py-2 px-3 bg-sky-50 rounded-md mb-2",
            "flex items-center justify-between py-2 px-3 bg-gray-700/50 rounded-md mb-2",
        ),
    )


def fpdf_missing_banner() -> rx.Component:
    return rx.cond(
        ~InvoiceState.is_fpdf_available,
        rx.el.div(
            rx.el.p(
                "ADVERTENCIA: La descarga de PDF no está disponible porque falta la librería 'fpdf'.",
                class_name="text-sm font-medium",
            ),
            rx.el.p(
                "Por favor, instálela en su entorno (ej: ",
                rx.el.code(
                    "pip install fpdf",
                    class_name="text-xs bg-red-200 p-0.5 rounded",
                ),
                ") y reinicie la aplicación.",
                class_name="text-xs mt-1",
            ),
            class_name="bg-red-100 border-t-4 border-red-500 text-red-700 p-4 fixed bottom-0 left-0 right-0 z-[1000] text-center shadow-lg",
        ),
        rx.fragment(),
    )


def confirmation_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.h1(
                "¡Compra Confirmada!",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-3xl sm:text-4xl font-bold text-green-600 mb-6 text-center title-bounce",
                    "text-3xl sm:text-4xl font-bold text-green-400 mb-6 text-center title-bounce",
                ),
            ),
            rx.el.p(
                "Gracias por tu pedido. Hemos recibido tu información y tu factura se está generando.",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-center text-sky-700 mb-8 text-base sm:text-lg",
                    "text-center text-gray-300 mb-8 text-base sm:text-lg",
                ),
            ),
            rx.el.div(
                rx.el.h2(
                    "Resumen de tu Pedido",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-xl sm:text-2xl font-semibold text-sky-700 mb-4",
                        "text-xl sm:text-2xl font-semibold text-sky-400 mb-4",
                    ),
                ),
                rx.cond(
                    InvoiceState.display_items.length() > 0,
                    rx.el.div(
                        rx.foreach(
                            InvoiceState.display_items,
                            confirmation_item_summary_row,
                        ),
                        class_name="mb-4 max-h-60 overflow-y-auto p-1 rounded-lg border border-sky-200 dark:border-gray-700 custom-scrollbar",
                    ),
                    rx.el.p(
                        rx.cond(
                            InvoiceState.is_generating_invoice,
                            "Generando detalles del pedido...",
                            "No hay artículos en este pedido o ocurrió un error.",
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600",
                            "text-gray-400",
                        ),
                    ),
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.p(
                            "Número de Factura:",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-700",
                                "text-gray-300",
                            ),
                        ),
                        rx.el.p(
                            rx.cond(
                                InvoiceState.order_details.invoice_number
                                != "",
                                InvoiceState.order_details.invoice_number,
                                "Generando...",
                            ),
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "font-semibold text-sky-800",
                                "font-semibold text-sky-300",
                            ),
                        ),
                        class_name="flex justify-between text-sm mb-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "CUFE:",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-700 text-xs break-all",
                                "text-gray-300 text-xs break-all",
                            ),
                        ),
                        rx.el.p(
                            rx.cond(
                                InvoiceState.order_details.cufe
                                != "",
                                InvoiceState.order_details.cufe,
                                "Generando...",
                            ),
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "font-mono text-sky-800 text-xs break-all",
                                "font-mono text-sky-300 text-xs break-all",
                            ),
                        ),
                        class_name="flex justify-between text-xs mb-1 items-start",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Subtotal:",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-700 text-sm",
                                "text-gray-300 text-sm",
                            ),
                        ),
                        rx.el.p(
                            f"COP {InvoiceState.order_details.subtotal:,.0f}",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "font-medium text-sky-800 text-sm",
                                "font-medium text-sky-300 text-sm",
                            ),
                        ),
                        class_name="flex justify-between text-sm mb-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            f"IVA ({InvoiceState.IVA_RATE * 100:.0f}%):",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-700 text-sm",
                                "text-gray-300 text-sm",
                            ),
                        ),
                        rx.el.p(
                            f"COP {InvoiceState.order_details.vat:,.0f}",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "font-medium text-sky-800 text-sm",
                                "font-medium text-sky-300 text-sm",
                            ),
                        ),
                        class_name="flex justify-between text-sm mb-1",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Total Pagado:",
                            class_name=rx.cond(
                                ThemeState.current_theme
                                == "light",
                                "text-sky-700 text-base sm:text-lg font-bold",
                                "text-gray-300 text-base sm:text-lg font-bold",
                            ),
                        ),
                        rx.el.p(
                            f"COP {InvoiceState.order_details.total_price:,.0f}",
                            class_name="font-bold text-lg sm:text-xl text-green-600 dark:text-green-400",
                        ),
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "flex justify-between items-center pt-2 border-t border-sky-200 mt-2",
                            "flex justify-between items-center pt-2 border-t border-gray-700 mt-2",
                        ),
                    ),
                    class_name="mt-4",
                ),
                rx.el.div(
                    rx.el.p(
                        "Enviado a:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sm text-sky-700 mt-4 font-semibold",
                            "text-sm text-gray-300 mt-4 font-semibold",
                        ),
                    ),
                    rx.el.p(
                        InvoiceState.order_details.customer_name,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600 text-sm",
                            "text-gray-400 text-sm",
                        ),
                    ),
                    rx.el.p(
                        InvoiceState.order_details.customer_address,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600 text-sm",
                            "text-gray-400 text-sm",
                        ),
                    ),
                    rx.el.p(
                        f"Documento: {InvoiceState.order_details.customer_document_id}",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600 text-sm",
                            "text-gray-400 text-sm",
                        ),
                    ),
                    rx.el.p(
                        InvoiceState.order_details.customer_email,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-600 text-sm",
                            "text-gray-400 text-sm",
                        ),
                    ),
                ),
                rx.el.button(
                    rx.cond(
                        InvoiceState.is_generating_invoice,
                        rx.el.span(
                            rx.el.div(
                                class_name="animate-spin rounded-full h-4 w-4 border-t-2 border-b-2 border-white mr-2"
                            ),
                            "Generando Factura...",
                            class_name="flex items-center justify-center",
                        ),
                        "Descargar Factura (PDF)",
                    ),
                    on_click=InvoiceState.download_invoice,
                    disabled=(
                        InvoiceState.invoice_pdf_path
                        == None
                    )
                    | InvoiceState.is_generating_invoice
                    | ~InvoiceState.is_fpdf_available,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full mt-8 bg-sky-500 hover:bg-sky-600 text-white font-bold py-3 px-4 rounded-lg transition-all focus:outline-none focus:ring-2 focus:ring-sky-400 button-light-interactive disabled:opacity-50",
                        "w-full mt-8 bg-sky-600 hover:bg-sky-700 text-white font-bold py-3 px-4 rounded-lg transition-colors focus:outline-none focus:ring-2 focus:ring-sky-500 disabled:opacity-50",
                    ),
                ),
                rx.el.button(
                    "🐞 Debug Info",
                    on_click=InvoiceState.debug_download_info,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full mt-3 bg-yellow-400 hover:bg-yellow-500 text-black font-semibold py-2 px-4 rounded-lg button-light-interactive",
                        "w-full mt-3 bg-yellow-500 hover:bg-yellow-600 text-black font-semibold py-2 px-4 rounded-lg",
                    ),
                ),
                rx.el.a(
                    "Volver a la Tienda",
                    href="/products",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "block w-full mt-3 text-center bg-gray-200 hover:bg-gray-300 text-sky-700 font-semibold py-3 px-4 rounded-lg transition-all",
                        "block w-full mt-3 text-center bg-gray-600 hover:bg-gray-500 text-white font-semibold py-3 px-4 rounded-lg transition-colors",
                    ),
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "bg-white p-6 sm:p-8 rounded-xl shadow-xl shadow-sky-200/50 w-full max-w-lg",
                    "bg-gray-800 p-6 sm:p-8 rounded-xl shadow-xl w-full max-w-lg",
                ),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "min-h-screen flex flex-col items-center justify-center py-10 px-4 pt-24 bg-white",
                "min-h-screen flex flex-col items-center justify-center py-10 px-4 pt-24 bg-slate-900",
            ),
        ),
        fpdf_missing_banner(),
        class_name=ThemeState.current_theme,
        on_mount=rx.cond(
            InvoiceState.has_raw_order_data,
            InvoiceState.generate_invoice_details,
            rx.noop(),
        ),
    )