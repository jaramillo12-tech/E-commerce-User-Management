import reflex as rx
from app.states.product_state import ProductState
from app.states.theme_state import ThemeState
from app.components.product_carousel import product_carousel


def category_filter_buttons() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Filtrar por Categoría:",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-lg sm:text-xl font-semibold text-sky-700 mb-3",
                "text-lg sm:text-xl font-semibold text-sky-300 mb-3",
            ),
        ),
        rx.el.div(
            rx.foreach(
                ProductState.categories,
                lambda category: rx.el.button(
                    category,
                    on_click=lambda: ProductState.set_selected_category(
                        category
                    ),
                    class_name=rx.cond(
                        ProductState.selected_category
                        == category,
                        rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "bg-sky-500 text-white font-semibold py-2 px-3 sm:px-4 rounded-md mr-2 mb-2 text-xs sm:text-sm transition-all transform hover:scale-105 shadow-md",
                            "bg-sky-600 text-white font-semibold py-2 px-3 sm:px-4 rounded-md mr-2 mb-2 text-xs sm:text-sm transition-all transform hover:scale-105 shadow-md",
                        ),
                        rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "bg-sky-100 text-sky-700 hover:bg-sky-200 font-semibold py-2 px-3 sm:px-4 rounded-md mr-2 mb-2 text-xs sm:text-sm transition-all transform hover:scale-105",
                            "bg-gray-700 text-gray-200 hover:bg-gray-600 font-semibold py-2 px-3 sm:px-4 rounded-md mr-2 mb-2 text-xs sm:text-sm transition-all transform hover:scale-105",
                        ),
                    ),
                ),
            ),
            class_name="flex flex-wrap justify-center mb-6 sm:mb-8",
        ),
        class_name="mb-6 sm:mb-8 px-4",
    )


def product_carousels_display() -> rx.Component:
    return rx.el.div(
        rx.el.h2(
            "Nuestros Productos",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-3xl sm:text-4xl font-bold text-center text-sky-800 mt-8 mb-4 sm:mt-10 sm:mb-6 tracking-wide title-bounce",
                "text-3xl sm:text-4xl font-bold text-center text-sky-300 mt-8 mb-4 sm:mt-10 sm:mb-6 tracking-wide title-bounce",
            ),
        ),
        category_filter_buttons(),
        rx.el.input(
            default_value=ProductState.search_query,
            placeholder="Buscar productos por nombre...",
            on_change=ProductState.set_search_query.debounce(
                300
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "w-full max-w-md sm:max-w-xl mx-auto p-3 mb-8 bg-sky-50 border border-sky-300 rounded-lg text-sky-800 placeholder-sky-500 focus:ring-2 focus:ring-sky-400 focus:border-sky-400 shadow-md transition-shadow focus:shadow-sky-400/50",
                "w-full max-w-md sm:max-w-xl mx-auto p-3 mb-8 bg-gray-700 border border-gray-600 rounded-lg text-white placeholder-gray-400 focus:ring-2 focus:ring-sky-500 focus:border-sky-500 shadow-lg transition-shadow focus:shadow-sky-500/50",
            ),
        ),
        rx.cond(
            ProductState.products_by_category_keys.length()
            > 0,
            rx.el.div(
                rx.foreach(
                    ProductState.products_by_category_keys,
                    lambda category: product_carousel(
                        category,
                        ProductState.products_by_category[
                            category
                        ],
                    ),
                )
            ),
            rx.el.div(
                rx.cond(
                    (ProductState.search_query != "")
                    | (
                        ProductState.selected_category
                        != "All"
                    ),
                    rx.el.p(
                        "No hay productos que coincidan con los filtros actuales.",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-lg sm:text-xl text-sky-700",
                            "text-lg sm:text-xl text-gray-500",
                        ),
                    ),
                    rx.el.p(
                        "No hay productos disponibles en este momento. ¡Vuelve más tarde!",
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "text-lg sm:text-xl text-sky-700",
                            "text-lg sm:text-xl text-gray-500",
                        ),
                    ),
                ),
                class_name="text-center py-12",
            ),
        ),
        class_name="container mx-auto px-0 pb-10",
    )