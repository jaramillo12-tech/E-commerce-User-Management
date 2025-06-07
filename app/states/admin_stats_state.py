import reflex as rx
from app.models.models import CartItem
import time


class SalesRecord(rx.Base):
    product_id: int
    name: str
    quantity_sold: int
    price_at_sale: float
    timestamp: float


class AdminStatsState(rx.State):
    sales_records: list[SalesRecord] = []

    @rx.event
    def record_sale_from_cart_item(
        self, cart_item: CartItem
    ):
        record = SalesRecord(
            product_id=cart_item.product_id,
            name=cart_item.name,
            quantity_sold=cart_item.quantity,
            price_at_sale=cart_item.price,
            timestamp=time.time(),
        )
        self.sales_records.append(record)

    @rx.var
    def product_purchase_summary(self) -> list[dict]:
        summary: dict[int, dict] = {}
        for record in self.sales_records:
            pid = record.product_id
            if pid not in summary:
                summary[pid] = {
                    "name": record.name,
                    "total_sold": 0,
                    "total_revenue": 0.0,
                }
            summary[pid][
                "total_sold"
            ] += record.quantity_sold
            summary[pid]["total_revenue"] += (
                record.quantity_sold * record.price_at_sale
            )
        summary_list = [
            {
                "product_id": pid,
                "name": data["name"],
                "total_sold": data["total_sold"],
                "total_revenue": round(
                    data["total_revenue"], 2
                ),
            }
            for pid, data in summary.items()
        ]
        summary_list.sort(
            key=lambda x: x["total_sold"], reverse=True
        )
        return summary_list

    @rx.var
    def chart_data(self) -> list[dict[str, str | int]]:
        return [
            {
                "name": item["name"],
                "Vendidos": item["total_sold"],
            }
            for item in self.product_purchase_summary
        ]