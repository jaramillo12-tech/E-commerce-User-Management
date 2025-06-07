import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.admin_product_state import AdminProductState
from app.models.models import Product as ProductModel
from app.states.theme_state import ThemeState


def product_form_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.el.h2(
                rx.cond(
                    AdminProductState.is_editing,
                    "Editar Producto",
                    "Añadir Nuevo Producto",
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-2xl font-bold text-sky-700 mb-6",
                    "text-2xl font-bold text-sky-300 mb-6",
                ),
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Nombre:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.input(
                        name="product_name",
                        default_value=AdminProductState.form_name,
                        placeholder="Nombre del producto",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Descripción:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.textarea(
                        name="product_description",
                        default_value=AdminProductState.form_description,
                        on_change=AdminProductState.set_form_description,
                        placeholder="Descripción",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Precio (COP):",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.input(
                        name="product_price",
                        type="number",
                        default_value=AdminProductState.form_price.to_string(),
                        placeholder="0",
                        step="100",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "URL de Imagen:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.input(
                        name="product_image_url",
                        default_value=AdminProductState.form_image_url,
                        placeholder="/placeholder.svg",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Categoría:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.input(
                        name="product_category",
                        default_value=AdminProductState.form_category,
                        placeholder="Categoría",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.label(
                        "Stock:",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-sky-700",
                            "text-gray-300",
                        ),
                    ),
                    rx.el.input(
                        name="product_stock",
                        type="number",
                        default_value=AdminProductState.form_stock.to_string(),
                        placeholder="0",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "w-full p-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                            "w-full p-2 border border-gray-600 rounded bg-gray-700 text-white",
                        ),
                    ),
                    class_name="mb-3",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.cond(
                            AdminProductState.is_editing,
                            "Guardar Cambios",
                            "Añadir Producto",
                        ),
                        type="submit",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600 button-light-interactive",
                            "px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700",
                        ),
                    ),
                    rx.el.button(
                        "Cancelar",
                        type="button",
                        on_click=AdminProductState.close_product_modal,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "ml-2 px-4 py-2 bg-red-500 text-white rounded hover:bg-red-600 button-light-interactive",
                            "ml-2 px-4 py-2 bg-red-600 text-white rounded hover:bg-red-700",
                        ),
                    ),
                    class_name="mt-6 flex justify-end",
                ),
                on_submit=AdminProductState.handle_product_submit,
                reset_on_submit=False,
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "bg-white p-8 rounded-lg shadow-xl w-full max-w-lg text-sky-800",
                "bg-gray-800 p-8 rounded-lg shadow-xl w-full max-w-lg text-white",
            ),
        ),
        open=AdminProductState.show_product_modal,
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "fixed inset-0 bg-sky-700 bg-opacity-30 backdrop-blur-sm open:flex items-center justify-center p-4 z-[100]",
            "fixed inset-0 bg-black bg-opacity-50 dark:bg-opacity-80 backdrop-blur-sm open:flex items-center justify-center p-4 z-[100]",
        ),
    )


def admin_product_row(
    product: ProductModel,
) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            product.id,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            product.name,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            f"COP {product.price:,.0f}",
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            product.stock,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            product.category,
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        rx.el.td(
            rx.el.button(
                "Editar",
                on_click=lambda: AdminProductState.open_edit_product_modal(
                    product
                ),
                class_name="bg-blue-500 hover:bg-blue-600 text-white px-3 py-1 rounded text-sm mr-2",
            ),
            rx.el.button(
                "Eliminar",
                on_click=lambda: AdminProductState.delete_product(
                    product.id
                ),
                class_name="bg-red-500 hover:bg-red-600 text-white px-3 py-1 rounded text-sm",
            ),
            class_name="py-2 px-4 border-b border-gray-200 dark:border-gray-700",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "hover:bg-sky-50",
            "hover:bg-gray-700",
        ),
    )


def admin_manage_products_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        product_form_modal(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Gestionar Productos",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "text-3xl font-bold text-sky-800 mb-6 title-bounce",
                        "text-3xl font-bold text-white mb-6 title-bounce",
                    ),
                ),
                rx.el.button(
                    "Añadir Nuevo Producto",
                    on_click=AdminProductState.open_add_product_modal,
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-lg mb-6 button-light-interactive",
                        "bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-lg mb-6",
                    ),
                ),
                class_name="flex justify-between items-center mb-6",
            ),
            rx.el.div(
                rx.el.table(
                    rx.el.thead(
                        rx.el.tr(
                            rx.el.th(
                                "ID",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                            rx.el.th(
                                "Nombre",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                            rx.el.th(
                                "Precio",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                            rx.el.th(
                                "Stock",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                            rx.el.th(
                                "Categoría",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                            rx.el.th(
                                "Acciones",
                                class_name="py-2 px-4 border-b-2 border-gray-300 dark:border-gray-600 text-left",
                            ),
                        )
                    ),
                    rx.el.tbody(
                        rx.foreach(
                            AdminProductState.products_for_admin,
                            admin_product_row,
                        )
                    ),
                    class_name="min-w-full",
                ),
                class_name="overflow-x-auto shadow-md rounded-lg",
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "container mx-auto py-10 px-4 pt-24 bg-white text-sky-800",
                "container mx-auto py-10 px-4 pt-24 bg-slate-900 text-white",
            ),
        ),
        on_mount=[
            AuthState.check_admin_session,
            AdminProductState.load_products_for_admin,
        ],
        class_name=ThemeState.current_theme,
    )