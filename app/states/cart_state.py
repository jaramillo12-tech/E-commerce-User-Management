import reflex as rx
from app.models.models import (
    CartItem,
    Product as ProductModel,
)
from sqlmodel import Session, select
from app.database import engine


class CartState(rx.State):
    items: list[CartItem] = []
    is_cart_open: bool = False

    @rx.event
    def add_item(
        self, product_data: dict, quantity: int = 1
    ):
        product_id_any = product_data.get("product_id")
        if product_id_any is None:
            yield rx.toast(
                "Error: ID de producto no válido.",
                duration=3000,
            )
            return
        try:
            product_id = int(product_id_any)
        except (ValueError, TypeError):
            yield rx.toast(
                f"Error: ID de producto '{product_id_any}' no es un entero válido.",
                duration=3000,
            )
            return
        stock = product_data.get("stock", 0)
        if not isinstance(stock, int):
            try:
                stock = int(stock)
            except (ValueError, TypeError):
                yield rx.toast(
                    f"Error: Stock de producto '{product_data.get('name', 'Desconocido')}' no es válido.",
                    duration=3000,
                )
                return
        found_item = None
        for item_model in self.items:
            item = CartItem(**item_model.dict())
            if item.product_id == product_id:
                found_item = item
                break
        if found_item:
            if found_item.quantity + quantity <= stock:
                found_item.quantity += quantity
                for i, orig_item_model in enumerate(
                    self.items
                ):
                    if (
                        orig_item_model.product_id
                        == product_id
                    ):
                        self.items[i] = found_item
                        break
            else:
                found_item.quantity = stock
                for i, orig_item_model in enumerate(
                    self.items
                ):
                    if (
                        orig_item_model.product_id
                        == product_id
                    ):
                        self.items[i] = found_item
                        break
                yield rx.toast(
                    f"No puedes añadir más de {stock} unidades de {found_item.name} (stock disponible).",
                    duration=3000,
                )
        elif quantity <= stock:
            new_item = CartItem(
                product_id=product_id,
                name=str(product_data.get("name", "N/A")),
                price=float(product_data.get("price", 0.0)),
                quantity=quantity,
                image_url=str(
                    product_data.get(
                        "image_url", "/placeholder.svg"
                    )
                ),
                stock=stock,
            )
            self.items.append(new_item)
        else:
            yield rx.toast(
                f"No puedes añadir {quantity} unidades de {product_data.get('name', 'N/A')} (stock disponible: {stock}).",
                duration=3000,
            )
        if not self.is_cart_open:
            self.is_cart_open = True
        yield rx.toast(
            f"{quantity} x {product_data.get('name', 'Producto')} añadido al carrito.",
            duration=2000,
        )

    @rx.event
    def remove_item(self, product_id: int):
        self.items = [
            item
            for item in self.items
            if item.product_id != product_id
        ]
        if not self.items:
            self.is_cart_open = False

    @rx.event
    def update_item_quantity(
        self, product_id: int, change: int
    ):
        item_to_update_model = None
        idx_to_update = -1
        for i, item_model in enumerate(self.items):
            if item_model.product_id == product_id:
                item_to_update_model = item_model
                idx_to_update = i
                break
        if item_to_update_model and idx_to_update != -1:
            item_to_update = CartItem(
                **item_to_update_model.dict()
            )
            new_quantity = item_to_update.quantity + change
            if new_quantity <= 0:
                self.items.pop(idx_to_update)
                if not self.items:
                    self.is_cart_open = False
            elif new_quantity <= item_to_update.stock:
                item_to_update.quantity = new_quantity
                self.items[idx_to_update] = item_to_update
            else:
                item_to_update.quantity = (
                    item_to_update.stock
                )
                self.items[idx_to_update] = item_to_update
                yield rx.toast(
                    f"No puedes añadir más de {item_to_update.stock} unidades de {item_to_update.name} (stock disponible).",
                    duration=3000,
                )

    @rx.event
    def clear_cart(self):
        self.items = []
        self.is_cart_open = False
        yield rx.toast("Carrito vaciado.", duration=2000)

    @rx.event
    def clear_cart_after_checkout(self):
        self.items = []
        self.is_cart_open = False

    @rx.event
    def toggle_cart(self):
        self.is_cart_open = not self.is_cart_open

    @rx.var
    def total_items(self) -> int:
        return sum((item.quantity for item in self.items))

    @rx.var
    def total_price(self) -> float:
        return sum(
            (
                item.price * item.quantity
                for item in self.items
            )
        )

    @rx.event(background=True)
    async def check_stock_and_update_cart(self):
        toast_messages_to_yield: list[str] = []
        _updated_items_temp: list[CartItem] = []
        _stock_issues_temp = False
        _is_cart_open_local: bool = False
        _current_items_local: list[CartItem] = []
        async with self:
            _is_cart_open_local = self.is_cart_open
            _current_items_local = [
                CartItem(**item.dict())
                for item in self.items
            ]
        with Session(engine) as session:
            for item_in_cart in _current_items_local:
                db_product = session.get(
                    ProductModel, item_in_cart.product_id
                )
                if db_product:
                    if db_product.stock == 0:
                        toast_messages_to_yield.append(
                            f"Producto {item_in_cart.name} agotado y eliminado del carrito."
                        )
                        _stock_issues_temp = True
                        continue
                    elif (
                        item_in_cart.quantity
                        > db_product.stock
                    ):
                        toast_messages_to_yield.append(
                            f"Stock de {item_in_cart.name} actualizado a {db_product.stock} en el carrito."
                        )
                        item_in_cart.quantity = (
                            db_product.stock
                        )
                        item_in_cart.stock = (
                            db_product.stock
                        )
                        _stock_issues_temp = True
                    else:
                        item_in_cart.stock = (
                            db_product.stock
                        )
                    _updated_items_temp.append(item_in_cart)
                else:
                    toast_messages_to_yield.append(
                        f"Producto {item_in_cart.name} no encontrado y eliminado del carrito."
                    )
                    _stock_issues_temp = True
            if (
                not _updated_items_temp
                and _stock_issues_temp
            ):
                _is_cart_open_local = False
        async with self:
            self.items = [
                CartItem(**item.dict())
                for item in _updated_items_temp
            ]
            self.is_cart_open = _is_cart_open_local
        for msg in toast_messages_to_yield:
            yield rx.toast(msg, duration=3000)
        if not toast_messages_to_yield and (
            not _stock_issues_temp
        ):
            yield