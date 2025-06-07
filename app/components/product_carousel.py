import reflex as rx
from app.models.models import Product as ProductModel
from app.components.product_card import product_card
from app.states.theme_state import ThemeState


def product_carousel(
    category: str, products: list[ProductModel]
) -> rx.Component:
    scroll_area_id = (
        f"carousel-{category.lower().replace(' ', '-')}"
    )
    return rx.el.div(
        rx.el.h3(
            category,
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-2xl sm:text-3xl font-bold text-sky-800 mb-4 px-4 md:px-6",
                "text-2xl sm:text-3xl font-bold text-sky-300 mb-4 px-4 md:px-6",
            ),
        ),
        rx.el.div(
            rx.el.button(
                rx.icon(
                    tag="chevron_left", class_name="h-6 w-6"
                ),
                on_click=rx.call_script(
                    f"document.getElementById('{scroll_area_id}').scrollBy({{ left: -350, behavior: 'smooth' }})"
                ),
                class_name="absolute left-2 top-1/2 -translate-y-1/2 z-20 bg-white/80 dark:bg-gray-800/80 p-2 rounded-full shadow-md hover:bg-white dark:hover:bg-gray-700 transition-opacity opacity-0 group-hover:opacity-100",
            ),
            rx.el.div(
                rx.el.div(
                    rx.foreach(
                        products,
                        lambda product: rx.el.div(
                            product_card(
                                product, is_sponsored=False
                            ),
                            class_name="w-72 flex-shrink-0",
                        ),
                    ),
                    class_name="flex space-x-6 px-4",
                ),
                id=scroll_area_id,
                class_name="flex overflow-x-auto carousel-scroll-area pb-4",
                style={"scroll-snap-type": "x mandatory"},
            ),
            rx.el.button(
                rx.icon(
                    tag="chevron_right",
                    class_name="h-6 w-6",
                ),
                on_click=rx.call_script(
                    f"document.getElementById('{scroll_area_id}').scrollBy({{ left: 350, behavior: 'smooth' }})"
                ),
                class_name="absolute right-2 top-1/2 -translate-y-1/2 z-20 bg-white/80 dark:bg-gray-800/80 p-2 rounded-full shadow-md hover:bg-white dark:hover:bg-gray-700 transition-opacity opacity-0 group-hover:opacity-100",
            ),
            class_name="relative group",
        ),
        class_name="mb-12",
    )