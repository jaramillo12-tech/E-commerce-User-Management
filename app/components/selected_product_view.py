import reflex as rx
from app.models.models import (
    Product as ProductModel,
    DisplayReview,
)
from app.states.product_state import ProductState
from app.states.cart_state import CartState
from app.states.theme_state import ThemeState
from app.states.feedback_state import FeedbackState
from reflex.app import UploadFile


def star_display(
    rating: int, max_stars: int = 5
) -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(1, max_stars + 1),
            lambda i: rx.icon(
                tag="star",
                color=rx.cond(
                    i <= rating,
                    "gold",
                    rx.cond(
                        ThemeState.current_theme == "light",
                        "gray.300",
                        "gray.600",
                    ),
                ),
                fill=rx.cond(
                    i <= rating,
                    "gold",
                    rx.cond(
                        ThemeState.current_theme == "light",
                        "gray.300",
                        "gray.600",
                    ),
                ),
                size=16,
            ),
        ),
        class_name="flex items-center",
    )


def star_rating_input() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            rx.Var.range(1, 6),
            lambda i: rx.el.button(
                rx.icon(
                    "star",
                    size=24,
                    color=rx.cond(
                        i <= FeedbackState.current_rating,
                        "gold",
                        rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "gray.400",
                            "gray.500",
                        ),
                    ),
                    fill=rx.cond(
                        i <= FeedbackState.current_rating,
                        "gold",
                        rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "gray.400",
                            "gray.500",
                        ),
                    ),
                ),
                on_click=lambda: FeedbackState.set_star_rating(
                    i
                ),
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "p-1 bg-transparent border-none text-sky-700 hover:text-sky-600",
                    "p-1 bg-transparent border-none text-gray-300 hover:text-white",
                ),
            ),
        ),
        class_name="flex items-center my-2",
    )


def review_display_component(
    review: DisplayReview,
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.strong(
                f"{review.reviewer_name}: ",
                class_name=rx.cond(
                    ThemeState.current_theme == "light",
                    "text-sky-700",
                    "text-sky-300",
                ),
            ),
            star_display(review.rating),
            class_name="flex items-center mb-1",
        ),
        rx.el.p(
            rx.cond(
                review.comment,
                review.comment,
                "Sin comentario.",
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-sm text-sky-600 mb-1",
                "text-sm text-gray-400 mb-1",
            ),
        ),
        rx.cond(
            review.image_url,
            rx.el.img(
                src=review.image_url,
                alt="Review image",
                class_name="max-w-xs max-h-48 object-contain rounded-md my-2 border border-gray-300 dark:border-gray-600",
            ),
            rx.el.div(),
        ),
        rx.el.p(
            f"Fecha: {review.created_at_formatted}",
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "text-xs text-gray-500",
                "text-xs text-gray-500",
            ),
        ),
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "p-3 mb-3 border border-sky-100 rounded-lg bg-sky-50/50",
            "p-3 mb-3 border border-gray-700 rounded-lg bg-gray-700/30",
        ),
    )


def selected_product_modal() -> rx.Component:
    return rx.el.dialog(
        rx.el.div(
            rx.cond(
                ProductState.selected_product,
                rx.fragment(
                    rx.el.div(
                        rx.el.div(
                            rx.el.img(
                                src=ProductState.selected_product.image_url,
                                alt=ProductState.selected_product.name,
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "w-full h-auto max-h-[30vh] sm:max-h-[40vh] object-contain rounded-lg mb-4 border border-sky-200 p-2 bg-white",
                                    "w-full h-auto max-h-[30vh] sm:max-h-[40vh] object-contain rounded-lg mb-4 border border-gray-700 p-2 bg-gray-700",
                                ),
                            ),
                            rx.el.h2(
                                ProductState.selected_product.name,
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-2xl sm:text-3xl font-bold text-sky-700 mb-2",
                                    "text-2xl sm:text-3xl font-bold text-sky-300 mb-2",
                                ),
                            ),
                            rx.el.p(
                                f"COP {ProductState.selected_product.price:,.0f}",
                                class_name="text-xl sm:text-2xl text-green-600 dark:text-green-400 font-bold mb-3",
                            ),
                            rx.el.p(
                                ProductState.selected_product.description,
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-sm text-sky-600 mb-4 h-20 overflow-y-auto custom-scrollbar",
                                    "text-sm text-gray-400 mb-4 h-20 overflow-y-auto custom-scrollbar",
                                ),
                            ),
                            rx.el.div(
                                rx.el.p(
                                    f"Stock: {ProductState.selected_product.stock}",
                                    class_name=rx.cond(
                                        ProductState.selected_product.stock
                                        > 0,
                                        rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "text-green-600",
                                            "text-green-400",
                                        ),
                                        rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "text-red-600",
                                            "text-red-500",
                                        ),
                                    ),
                                ),
                                class_name="mb-4",
                            ),
                            rx.el.div(
                                rx.el.input(
                                    type="number",
                                    default_value=ProductState.selected_product_quantity.to_string(),
                                    on_change=ProductState.set_selected_product_quantity,
                                    min=1,
                                    max=ProductState.selected_product.stock,
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-20 p-2 border border-sky-300 rounded-md mr-2 text-center bg-sky-50 text-sky-800",
                                        "w-20 p-2 border border-gray-600 rounded-md mr-2 text-center bg-gray-700 text-white",
                                    ),
                                    disabled=ProductState.selected_product.stock
                                    == 0,
                                ),
                                rx.el.button(
                                    "Añadir al Carrito",
                                    on_click=ProductState.add_selected_to_cart,
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "flex-grow bg-green-500 hover:bg-green-600 text-white font-semibold py-2 px-4 rounded-md transition-all button-light-interactive",
                                        "flex-grow bg-green-600 hover:bg-green-700 text-white font-semibold py-2 px-4 rounded-md transition-colors",
                                    ),
                                    disabled=ProductState.selected_product.stock
                                    == 0,
                                ),
                                class_name="flex items-center mb-4",
                            ),
                            class_name="w-full md:w-1/2 pr-0 md:pr-4 mb-6 md:mb-0",
                        ),
                        rx.el.div(
                            rx.el.h3(
                                "Reseñas",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-xl font-semibold text-sky-700 mb-3",
                                    "text-xl font-semibold text-sky-300 mb-3",
                                ),
                            ),
                            rx.el.div(
                                rx.cond(
                                    ProductState.selected_product_reviews.length()
                                    > 0,
                                    rx.foreach(
                                        ProductState.selected_product_reviews,
                                        review_display_component,
                                    ),
                                    rx.el.p(
                                        "Aún no hay reseñas para este producto. ¡Sé el primero!",
                                        class_name=rx.cond(
                                            ThemeState.current_theme
                                            == "light",
                                            "text-sky-600",
                                            "text-gray-400",
                                        ),
                                    ),
                                ),
                                class_name="max-h-[40vh] overflow-y-auto mb-4 pr-2 custom-scrollbar",
                            ),
                            rx.el.h3(
                                "Deja tu Reseña",
                                class_name=rx.cond(
                                    ThemeState.current_theme
                                    == "light",
                                    "text-lg font-semibold text-sky-700 mb-2",
                                    "text-lg font-semibold text-sky-300 mb-2",
                                ),
                            ),
                            rx.el.form(
                                rx.el.input(
                                    name="reviewer_name",
                                    placeholder="Tu Nombre",
                                    default_value=FeedbackState.reviewer_name,
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full p-2 mb-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                                        "w-full p-2 mb-2 border border-gray-600 rounded bg-gray-700 text-white",
                                    ),
                                ),
                                star_rating_input(),
                                rx.el.textarea(
                                    name="comment_text",
                                    placeholder="Tu comentario...",
                                    default_value=FeedbackState.comment_text,
                                    on_change=FeedbackState.set_comment_text,
                                    rows=3,
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full p-2 mb-2 border border-sky-300 rounded bg-sky-50 text-sky-800",
                                        "w-full p-2 mb-2 border border-gray-600 rounded bg-gray-700 text-white",
                                    ),
                                ),
                                rx.upload(
                                    rx.el.div(
                                        rx.el.button(
                                            "Seleccionar Imagen (Opcional)",
                                            type="button",
                                            class_name=rx.cond(
                                                ThemeState.current_theme
                                                == "light",
                                                "text-xs text-sky-600 hover:text-sky-700",
                                                "text-xs text-gray-400 hover:text-gray-300",
                                            ),
                                        ),
                                        rx.cond(
                                            FeedbackState.uploaded_image_relative_path,
                                            rx.el.p(
                                                f"Imagen: {FeedbackState.uploaded_image_relative_path.split('/')[-1]}",
                                                class_name="text-xs text-green-500 ml-2",
                                            ),
                                            rx.el.div(),
                                        ),
                                        class_name="flex items-center",
                                    ),
                                    id="review_image_upload",
                                    border=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "1px dashed #cbd5e1",
                                        "1px dashed #4a5568",
                                    ),
                                    padding="0.5em",
                                    on_drop=FeedbackState.handle_upload(
                                        rx.upload_files(
                                            upload_id="review_image_upload"
                                        )
                                    ),
                                    class_name="mb-3 w-full cursor-pointer hover:bg-sky-50/50 dark:hover:bg-gray-700/30 rounded",
                                ),
                                rx.el.button(
                                    "Enviar Reseña",
                                    type="submit",
                                    class_name=rx.cond(
                                        ThemeState.current_theme
                                        == "light",
                                        "w-full bg-sky-500 hover:bg-sky-600 text-white py-2 rounded button-light-interactive",
                                        "w-full bg-sky-600 hover:bg-sky-700 text-white py-2 rounded",
                                    ),
                                ),
                                on_submit=FeedbackState.submit_review,
                                reset_on_submit=False,
                            ),
                            class_name="w-full md:w-1/2 pl-0 md:pl-4",
                        ),
                        class_name="flex flex-col md:flex-row",
                    ),
                    rx.el.button(
                        "Cerrar",
                        on_click=ProductState.close_selected_product_modal,
                        class_name=rx.cond(
                            ThemeState.current_theme
                            == "light",
                            "absolute top-3 right-3 bg-red-500 hover:bg-red-600 text-white font-semibold py-1 px-3 rounded-md text-sm button-light-interactive",
                            "absolute top-3 right-3 bg-red-600 hover:bg-red-700 text-white font-semibold py-1 px-3 rounded-md text-sm",
                        ),
                    ),
                ),
                rx.el.p("Cargando producto..."),
            ),
            class_name=rx.cond(
                ThemeState.current_theme == "light",
                "relative bg-white p-4 sm:p-6 rounded-xl shadow-2xl shadow-sky-300/70 w-full max-w-xl md:max-w-3xl lg:max-w-4xl max-h-[90vh] flex flex-col",
                "relative bg-gray-800 p-4 sm:p-6 rounded-xl shadow-2xl w-full max-w-xl md:max-w-3xl lg:max-w-4xl max-h-[90vh] flex flex-col",
            ),
            style={"overflowY": "auto"},
        ),
        open=ProductState.show_selected_product_modal,
        class_name=rx.cond(
            ThemeState.current_theme == "light",
            "fixed inset-0 bg-sky-700 bg-opacity-30 backdrop-blur-sm open:flex items-center justify-center p-2 sm:p-4 z-[100]",
            "fixed inset-0 bg-black bg-opacity-50 dark:bg-opacity-80 backdrop-blur-sm open:flex items-center justify-center p-2 sm:p-4 z-[100]",
        ),
    )