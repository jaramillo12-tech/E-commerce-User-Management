import reflex as rx
from sqlmodel import Session, select, delete
from app.database import engine
from app.models.models import Product as ProductModel
from typing import Optional


class AdminProductState(rx.State):
    products_for_admin: list[ProductModel] = []
    show_product_modal: bool = False
    is_editing: bool = False
    editing_product_id: Optional[int] = None
    form_name: str = ""
    form_description: str = ""
    form_price: float = 0.0
    form_image_url: str = ""
    form_category: str = ""
    form_stock: int = 0

    @rx.event(background=True)
    async def load_products_for_admin(self):
        async with self:
            with Session(engine) as session:
                self.products_for_admin = session.exec(
                    select(ProductModel).order_by(
                        ProductModel.id
                    )
                ).all()
        yield

    def _clear_form(self):
        self.form_name = ""
        self.form_description = ""
        self.form_price = 0.0
        self.form_image_url = ""
        self.form_category = ""
        self.form_stock = 0
        self.is_editing = False
        self.editing_product_id = None

    @rx.event
    def open_add_product_modal(self):
        self._clear_form()
        self.show_product_modal = True

    @rx.event
    def open_edit_product_modal(
        self, product: ProductModel
    ):
        self.is_editing = True
        self.editing_product_id = product.id
        self.form_name = product.name
        self.form_description = product.description
        self.form_price = product.price
        self.form_image_url = product.image_url
        self.form_category = product.category
        self.form_stock = product.stock
        self.show_product_modal = True

    @rx.event
    def close_product_modal(self):
        self.show_product_modal = False
        self._clear_form()

    @rx.event(background=True)
    async def handle_product_submit(self, form_data: dict):
        toast_message = ""
        async with self:
            self.form_name = form_data.get(
                "product_name", ""
            )
            self.form_description = form_data.get(
                "product_description", ""
            )
            self.form_image_url = form_data.get(
                "product_image_url", ""
            )
            self.form_category = form_data.get(
                "product_category", ""
            )
            try:
                self.form_price = float(
                    form_data.get("product_price", "0")
                )
            except (ValueError, TypeError):
                self.form_price = 0.0
            try:
                self.form_stock = int(
                    form_data.get("product_stock", "0")
                )
            except (ValueError, TypeError):
                self.form_stock = 0
            if not self.form_name:
                yield rx.toast(
                    "El nombre del producto es obligatorio.",
                    duration=3000,
                )
                return
            if not self.form_category:
                yield rx.toast(
                    "La categoría del producto es obligatoria.",
                    duration=3000,
                )
                return
        with Session(engine) as session:
            if (
                self.is_editing
                and self.editing_product_id is not None
            ):
                db_product = session.get(
                    ProductModel, self.editing_product_id
                )
                if db_product:
                    db_product.name = self.form_name
                    db_product.description = (
                        self.form_description
                    )
                    db_product.price = self.form_price
                    db_product.image_url = (
                        self.form_image_url
                        or "/placeholder.svg"
                    )
                    db_product.category = self.form_category
                    db_product.stock = self.form_stock
                    session.add(db_product)
                    session.commit()
                    toast_message = (
                        "Producto actualizado exitosamente."
                    )
            else:
                new_product = ProductModel(
                    name=self.form_name,
                    description=self.form_description,
                    price=self.form_price,
                    image_url=self.form_image_url
                    or "/placeholder.svg",
                    category=self.form_category,
                    stock=self.form_stock,
                )
                session.add(new_product)
                session.commit()
                toast_message = (
                    "Producto añadido exitosamente."
                )
        async with self:
            self.show_product_modal = False
            self._clear_form()
        if toast_message:
            yield rx.toast(toast_message, duration=2000)
        yield AdminProductState.load_products_for_admin
        from app.states.product_state import ProductState

        yield ProductState.load_products

    @rx.event(background=True)
    async def delete_product(self, product_id: int):
        toast_message = ""
        product_deleted_successfully = False
        with Session(engine) as session:
            product_to_delete = session.get(
                ProductModel, product_id
            )
            if product_to_delete:
                session.delete(product_to_delete)
                session.commit()
                toast_message = "Producto eliminado."
                product_deleted_successfully = True
            else:
                toast_message = (
                    "Error: Producto no encontrado."
                )
        async with self:
            pass
        if toast_message:
            yield rx.toast(toast_message, duration=2000)
        if product_deleted_successfully:
            yield AdminProductState.load_products_for_admin
            from app.states.product_state import (
                ProductState,
            )

            yield ProductState.load_products

    @rx.event
    def set_form_description(self, value: str):
        self.form_description = value

    @rx.event
    def set_form_price(self, value: str):
        try:
            self.form_price = float(value)
        except (ValueError, TypeError):
            self.form_price = 0.0

    @rx.event
    def set_form_stock(self, value: str):
        try:
            self.form_stock = int(value)
        except (ValueError, TypeError):
            self.form_stock = 0