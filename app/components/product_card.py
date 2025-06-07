import reflex as rx
from app.models.models import Product as ProductModel
from app.states.product_state import ProductState
from app.states.cart_state import CartState
from app.states.theme_state import ThemeState


def product_card(
    product: ProductModel, is_sponsored: bool = False
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.img(
                src=product.image_url,
                alt=product.name,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "w-full h-48 object-cover rounded-t-lg product-card-image-light",
                    "w-full h-48 object-cover rounded-t-lg",
                ),
                on_click=lambda: ProductState.select_product(
                    product
                ),
                cursor="pointer",
            ),
            rx.cond(
                is_sponsored,
                rx.el.span(
                    "Patrocinado",
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "absolute top-2 right-2 bg-yellow-400 text-yellow-800 text-xs font-semibold px-2 py-1 rounded-full shadow",
                        "absolute top-2 right-2 bg-yellow-500 text-yellow-900 text-xs font-semibold px-2 py-1 rounded-full shadow",
                    ),
                ),
                rx.el.div(),
            ),
            class_name="relative",
        ),
        rx.el.div(
            rx.el.h3(
                product.name,
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-xl font-semibold text-sky-700 mb-1 truncate",
                    "text-xl font-semibold text-sky-400 mb-1 truncate",
                ),
            ),
            rx.el.p(
                f"COP {product.price:,.0f}",
                class_name="text-lg text-green-600 dark:text-green-400 font-bold mb-2",
            ),
            rx.el.div(
                rx.el.button(
                    "Añadir al Carrito",
                    on_click=lambda: CartState.add_item(
                        {
                            "product_id": product.id,
                            "name": product.name,
                            "price": product.price,
                            "quantity": 1,
                            "image_url": product.image_url,
                            "stock": product.stock,
                        },
                        1,
                    ),
                    class_name=rx.cond(
                        ThemeState.current_theme == "light",
                        "w-full mt-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50 button-light-interactive",
                        "w-full mt-2 bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md transition-all duration-200 transform hover:scale-105 focus:outline-none focus:ring-2 focus:ring-green-400 focus:ring-opacity-50",
                    ),
                    disabled=product.stock == 0,
                ),
                class_name="mt-auto",
            ),
            rx.cond(
                product.stock == 0,
                rx.el.p(
                    "Agotado",
                    class_name="text-center text-red-500 dark:text-red-500 text-sm mt-2",
                ),
                rx.el.div(),
            ),
            class_name="p-4 flex flex-col flex-grow",
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "group bg-white rounded-lg overflow-hidden flex flex-col h-full animate-float product-card-light",
            "group bg-gray-800 rounded-lg shadow-xl overflow-hidden transform hover:shadow-sky-500/40 transition-all duration-300 hover:-translate-y-1.5 flex flex-col h-full animate-float",
        ),
    )