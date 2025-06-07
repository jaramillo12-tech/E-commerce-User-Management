import reflex as rx
from sqlmodel import Session
from app.database import engine
from app.models.models import Review, Product
import os
import datetime


class FeedbackState(rx.State):
    reviewer_name: str = ""
    current_rating: int = 0
    comment_text: str = ""
    selected_product_id_for_review: int | None = None
    uploaded_image_relative_path: str | None = None
    review_submitted_trigger: bool = False

    @rx.event
    def set_selected_product_for_review(
        self, product_id: int | None
    ):
        self.selected_product_id_for_review = product_id
        self.reviewer_name = ""
        self.current_rating = 0
        self.comment_text = ""
        self.uploaded_image_relative_path = None
        self.review_submitted_trigger = False

    @rx.event
    def set_star_rating(self, rating: int):
        self.current_rating = rating

    @rx.event(background=True)
    async def handle_upload(
        self, files: list[rx.UploadFile]
    ):
        if not files:
            return
        upload_dir = "assets/review_images"
        os.makedirs(upload_dir, exist_ok=True)
        file_data: rx.UploadFile = files[0]
        try:
            content = await file_data.read()
            original_filename = file_data.filename
        except AttributeError:
            yield rx.toast(
                "Error: Invalid file object received by handler.",
                duration=3000,
            )
            return
        timestamp = datetime.datetime.now().strftime(
            "%Y%m%d%H%M%S%f"
        )
        safe_filename = f"{timestamp}_{original_filename.replace(' ', '_')}"
        file_path = os.path.join(upload_dir, safe_filename)
        with open(file_path, "wb") as f:
            f.write(content)
        _uploaded_image_relative_path = (
            f"/review_images/{safe_filename}"
        )
        async with self:
            self.uploaded_image_relative_path = (
                _uploaded_image_relative_path
            )
        yield rx.toast(
            f"Imagen '{original_filename}' subida."
        )

    @rx.event
    def submit_review(self, form_data: dict):
        self.reviewer_name = form_data.get(
            "reviewer_name", ""
        )
        self.comment_text = form_data.get(
            "comment_text", ""
        )
        if not self.selected_product_id_for_review:
            yield rx.toast(
                "Error: No hay producto seleccionado para reseñar.",
                duration=3000,
            )
            return
        if not self.reviewer_name:
            yield rx.toast(
                "Por favor, ingresa tu nombre.",
                duration=3000,
            )
            return
        if self.current_rating == 0:
            yield rx.toast(
                "Por favor, selecciona una calificación de estrellas.",
                duration=3000,
            )
            return
        new_review = Review(
            product_id=self.selected_product_id_for_review,
            reviewer_name=self.reviewer_name,
            rating=self.current_rating,
            comment=(
                self.comment_text
                if self.comment_text
                else None
            ),
            image_url=self.uploaded_image_relative_path,
        )
        try:
            with Session(engine) as session:
                session.add(new_review)
                session.commit()
                session.refresh(new_review)
            yield rx.toast(
                "¡Reseña enviada exitosamente!",
                duration=3000,
            )
            self.reviewer_name = ""
            self.current_rating = 0
            self.comment_text = ""
            self.uploaded_image_relative_path = None
            self.review_submitted_trigger = (
                not self.review_submitted_trigger
            )
            from app.states.product_state import (
                ProductState,
            )

            if (
                self.selected_product_id_for_review
                is not None
            ):
                yield ProductState.load_reviews_for_selected_product(
                    self.selected_product_id_for_review
                )
        except Exception as e:
            print(f"Error saving review: {e}")
            yield rx.toast(
                f"Error al enviar la reseña: {str(e)}",
                duration=4000,
            )

    @rx.event
    def set_comment_text(self, text: str):
        self.comment_text = text